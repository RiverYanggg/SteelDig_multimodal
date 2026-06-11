from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from verify.common import (
    EvidenceBlock,
    SchemaSpec,
    SharedLLMClient,
    build_evidence_blocks,
    ensure_schema,
    flatten_section_records,
    load_schema_spec,
    normalize_identifier,
    read_json,
    validation_report,
    write_json,
)


CORRECTNESS_SCORE = {
    "yes": 1.0,
    "partial": 0.6,
    "unknown": 0.3,
    "no": 0.0,
}

SCORING_FORMULA = {
    "correctness_mapping": CORRECTNESS_SCORE,
    "field_score": "correctness_score * evidence_confidence * 100",
    "sample_score": "sum(field_score * field_weight) / sum(field_weight)",
    "paper_score": "sum(sample_score * sample_weight) / sum(sample_weight)",
    "sample_weight": "sum(field_weight for fields in this sample group)",
    "gate_rule": "if structure gate fails, paper_score = 0",
    "field_weight_rules": {
        "structures/properties/performance": 1.5,
        "samples/processing_steps/interfaces": 1.3,
        "papers/unmapped_findings": 0.7,
        "default": 1.0,
    },
}


@dataclass(frozen=True)
class VerifyEvalResult:
    paper_id: str
    report_path: Path
    paper_score: float
    field_count: int
    target_kind: str
    gate_ok: bool


def run_verify_eval_for_paper(
    paper_dir: str | Path,
    *,
    field_rules: dict[str, Any],
    llm_client: SharedLLMClient | None = None,
    force: bool = False,
    max_evidence_chars: int = 80_000,
    schema_spec: SchemaSpec | None = None,
) -> VerifyEvalResult:
    schema = schema_spec or load_schema_spec()
    paper_path = Path(paper_dir).expanduser().resolve()
    paper_id = paper_path.name
    out_dir = paper_path / "verify_eval"
    report_path = out_dir / "quality_report.json"
    if report_path.exists() and not force:
        report = read_json(report_path)
        if not (llm_client and int(report.get("llm_error_count", 0)) > 0):
            return VerifyEvalResult(
                paper_id=paper_id,
                report_path=report_path,
                paper_score=float(report.get("paper_score", 0.0)),
                field_count=int(report.get("field_count", 0)),
                target_kind=str(report.get("target_kind", "")),
                gate_ok=bool(report.get("gate", {}).get("ok", False)),
            )

    target_path, target_kind = _resolve_target(paper_path)
    return _run_verify_eval_target(
        paper_path=paper_path,
        paper_id=paper_id,
        target_path=target_path,
        target_kind=target_kind,
        out_dir=out_dir,
        report_path=report_path,
        field_rules=field_rules,
        llm_client=llm_client,
        schema=schema,
    )


def run_verify_compare_for_paper(
    paper_dir: str | Path,
    *,
    field_rules: dict[str, Any],
    llm_client: SharedLLMClient | None = None,
    force: bool = False,
    max_evidence_chars: int = 80_000,
    schema_spec: SchemaSpec | None = None,
) -> VerifyEvalResult:
    schema = schema_spec or load_schema_spec()
    paper_path = Path(paper_dir).expanduser().resolve()
    paper_id = paper_path.name
    compare_dir = paper_path / "verify_compare"
    compare_report_path = compare_dir / "compare_report.json"
    if compare_report_path.exists() and not force:
        report = read_json(compare_report_path)
        after = report.get("after", {})
        if not (llm_client and int(report.get("llm_error_count", 0)) > 0):
            return VerifyEvalResult(
                paper_id=paper_id,
                report_path=compare_report_path,
                paper_score=float(after.get("paper_score", 0.0)),
                field_count=int(after.get("field_count", 0)),
                target_kind="verify_compare",
                gate_ok=bool(after.get("gate_ok", False)),
            )

    final_path = paper_path / "final" / "text_extraction.json"
    fixed_path = paper_path / "verify" / "text_extraction_fixed.json"
    if not final_path.is_file():
        raise FileNotFoundError(f"missing final text_extraction.json: {final_path}")
    if not fixed_path.is_file():
        raise FileNotFoundError(f"missing verify fixed text_extraction_fixed.json: {fixed_path}")

    before_result = _run_verify_eval_target(
        paper_path=paper_path,
        paper_id=paper_id,
        target_path=final_path,
        target_kind="final_original",
        out_dir=compare_dir / "before_final",
        report_path=compare_dir / "before_final" / "quality_report.json",
        field_rules=field_rules,
        llm_client=llm_client,
        schema=schema,
    )
    after_result = _run_verify_eval_target(
        paper_path=paper_path,
        paper_id=paper_id,
        target_path=fixed_path,
        target_kind="verify_fixed",
        out_dir=compare_dir / "after_verify",
        report_path=compare_dir / "after_verify" / "quality_report.json",
        field_rules=field_rules,
        llm_client=llm_client,
        schema=schema,
    )
    before_report = read_json(before_result.report_path)
    after_report = read_json(after_result.report_path)
    compare_report = {
        "paper_id": paper_id,
        "score_formula": SCORING_FORMULA,
        "before": _compact_report_summary(before_report),
        "after": _compact_report_summary(after_report),
        "delta": {
            "paper_score": after_result.paper_score - before_result.paper_score,
            "field_count": after_result.field_count - before_result.field_count,
            "target": "after_verify - before_final",
        },
        "paths": {
            "before_report": str(before_result.report_path),
            "after_report": str(after_result.report_path),
        },
        "llm_error_count": int(before_report.get("llm_error_count", 0)) + int(after_report.get("llm_error_count", 0)),
    }
    write_json(compare_report, compare_report_path)
    _write_compare_markdown(compare_report, compare_dir / "compare_report.md")
    return VerifyEvalResult(
        paper_id=paper_id,
        report_path=compare_report_path,
        paper_score=after_result.paper_score,
        field_count=after_result.field_count,
        target_kind="verify_compare",
        gate_ok=before_result.gate_ok and after_result.gate_ok and compare_report["llm_error_count"] == 0,
    )


def _run_verify_eval_target(
    *,
    paper_path: Path,
    paper_id: str,
    target_path: Path,
    target_kind: str,
    out_dir: Path,
    report_path: Path,
    field_rules: dict[str, Any],
    llm_client: SharedLLMClient | None,
    schema: SchemaSpec,
) -> VerifyEvalResult:
    data = ensure_schema(read_json(target_path), schema)
    gate = validation_report(data, schema)
    out_dir.mkdir(parents=True, exist_ok=True)
    write_json(gate, out_dir / "gate_report.json")

    evidence_blocks = _load_or_build_evidence(paper_path)
    write_json([block.to_dict() for block in evidence_blocks], out_dir / "evidence_blocks.json")

    facts = extract_field_facts(data, field_rules, schema_spec=schema)
    write_json(facts, out_dir / "field_facts.json")

    if not gate["ok"]:
        report = _zero_report(paper_id, target_path, target_kind, gate, len(facts), reason="structure gate failed")
        write_json(report, report_path)
        _write_markdown_report(report, out_dir / "quality_report.md")
        return VerifyEvalResult(paper_id, report_path, 0.0, len(facts), target_kind, False)

    samples = _sample_index(data)
    sample_reports = []
    raw_outputs = []
    llm_error_count = 0
    facts_by_sample = _group_facts_by_sample(facts)
    for sample_id, sample_facts in facts_by_sample.items():
        sample_context = _sample_bundle_for_eval(data, sample_id, samples)
        evidence_payload = [block.to_dict() for block in evidence_blocks]
        judge_input = {
            "instruction": VERIFY_EVAL_INSTRUCTION,
            "paper_id": paper_id,
            "sample_id": sample_id,
            "sample_context": sample_context,
            "fields": sample_facts,
            "evidence_blocks": evidence_payload,
        }
        write_json(judge_input, out_dir / "sample_inputs" / f"{_safe_id(sample_id)}.json")
        if llm_client and evidence_blocks:
            try:
                response = llm_client.complete_json(
                    system="You are a strict evidence-based field quality judge.",
                    prompt=json.dumps(judge_input, ensure_ascii=False, indent=2),
                )
            except Exception as exc:
                llm_error_count += 1
                response = {
                    "paper_id": paper_id,
                    "sample_id": sample_id,
                    "error": str(exc),
                    "results": [
                        {
                            "field_id": fact["field_id"],
                            "is_correct": "unknown",
                            "evidence_confidence": 0.0,
                            "evidence_refs": [],
                            "reason": "LLM judge failed.",
                        }
                        for fact in sample_facts
                    ],
                }
        else:
            response = {
                "paper_id": paper_id,
                "sample_id": sample_id,
                "results": [
                    {
                        "field_id": fact["field_id"],
                        "is_correct": "unknown",
                        "evidence_confidence": 0.0,
                        "evidence_refs": [],
                        "reason": "LLM disabled or evidence missing.",
                    }
                    for fact in sample_facts
                ],
            }
        raw_outputs.append(response)
        write_json(response, out_dir / "sample_raw_outputs" / f"{_safe_id(sample_id)}.json")
        sample_report = score_sample(sample_id, sample_facts, response, evidence_blocks)
        write_json(sample_report, out_dir / "sample_outputs" / f"{_safe_id(sample_id)}.json")
        sample_reports.append(sample_report)

    paper_score = _weighted_average(
        [(item["sample_score"], item["sample_weight"]) for item in sample_reports]
    )
    report = {
        "paper_id": paper_id,
        "target_kind": target_kind,
        "target_path": str(target_path),
        "paper_score": paper_score,
        "score_formula": SCORING_FORMULA,
        "field_count": len(facts),
        "sample_count": len(sample_reports),
        "gate": gate,
        "llm_used": llm_client is not None,
        "llm_error_count": llm_error_count,
        "sample_reports": sample_reports,
        "summary": _quality_summary(sample_reports),
    }
    write_json(sample_reports, out_dir / "sample_eval_report.json")
    write_json(report, report_path)
    _write_markdown_report(report, out_dir / "quality_report.md")
    return VerifyEvalResult(paper_id, report_path, paper_score, len(facts), target_kind, True)


def extract_field_facts(data: dict[str, Any], field_rules: dict[str, Any], schema_spec: SchemaSpec | None = None) -> list[dict[str, Any]]:
    facts: list[dict[str, Any]] = []
    schema = schema_spec or load_schema_spec()
    payload = ensure_schema(data, schema)
    identity_map = _identity_canonical_map(payload)
    for section in schema.sections:
        flat = flatten_section_records(section, payload[section], identity_map, field_rules, schema_spec=schema)
        for key, value in sorted(flat.items()):
            sample_id = _sample_id_for_flat_key(key, payload)
            facts.append(
                {
                    "field_id": f"F{len(facts) + 1:05d}",
                    "sample_id": sample_id,
                    "section": section,
                    "path": key,
                    "value": value,
                    "field_weight": _field_weight(section, key),
                    "candidate_evidence_refs": [],
                }
            )
    return facts


def score_sample(
    sample_id: str,
    facts: list[dict[str, Any]],
    response: dict[str, Any],
    evidence_blocks: list[EvidenceBlock],
) -> dict[str, Any]:
    evidence_ids = {block.block_id for block in evidence_blocks}
    result_by_id = {}
    for item in response.get("results", []):
        if isinstance(item, dict) and item.get("field_id"):
            result_by_id[str(item["field_id"])] = item

    field_reports = []
    for fact in facts:
        result = result_by_id.get(fact["field_id"], {})
        label = str(result.get("is_correct", "unknown")).lower()
        if label not in CORRECTNESS_SCORE:
            label = "unknown"
        try:
            evidence_confidence = float(result.get("evidence_confidence", 0.0))
        except (TypeError, ValueError):
            evidence_confidence = 0.0
        evidence_confidence = max(0.0, min(1.0, evidence_confidence))
        refs = result.get("evidence_refs", [])
        refs = [str(ref) for ref in refs if str(ref) in evidence_ids] if isinstance(refs, list) else []
        field_score = CORRECTNESS_SCORE[label] * evidence_confidence * 100.0
        field_reports.append(
            {
                **fact,
                "is_correct": label,
                "evidence_confidence": evidence_confidence,
                "evidence_refs": refs,
                "reason": result.get("reason", ""),
                "field_score": field_score,
            }
        )
    sample_score = _weighted_average(
        [(item["field_score"], float(item.get("field_weight", 1.0))) for item in field_reports]
    )
    sample_weight = sum(float(item.get("field_weight", 1.0)) for item in field_reports) or 1.0
    return {
        "sample_id": sample_id,
        "sample_score": sample_score,
        "sample_weight": sample_weight,
        "field_count": len(field_reports),
        "correct_yes_count": sum(1 for item in field_reports if item["is_correct"] == "yes"),
        "unknown_count": sum(1 for item in field_reports if item["is_correct"] == "unknown"),
        "no_count": sum(1 for item in field_reports if item["is_correct"] == "no"),
        "fields": field_reports,
    }


def _resolve_target(paper_path: Path) -> tuple[Path, str]:
    fixed = paper_path / "verify" / "text_extraction_fixed.json"
    if fixed.is_file():
        return fixed, "verify_fixed"
    normalized = paper_path / "normalized" / "text_extraction_units.json"
    if normalized.is_file():
        return normalized, "normalized_units"
    final = paper_path / "final" / "text_extraction.json"
    if final.is_file():
        return final, "final_original"
    raise FileNotFoundError(f"no verify fixed, normalized, or final text_extraction.json under {paper_path}")


def _load_or_build_evidence(paper_path: Path) -> list[EvidenceBlock]:
    verify_blocks = paper_path / "verify" / "evidence_blocks.json"
    if verify_blocks.is_file():
        payload = read_json(verify_blocks)
        if isinstance(payload, list):
            return [EvidenceBlock(**item) for item in payload if isinstance(item, dict)]
    cleaned = paper_path / "preprocess" / "cleaned_input.md"
    if not cleaned.is_file():
        return []
    return build_evidence_blocks(cleaned.read_text(encoding="utf-8"))


def _zero_report(paper_id: str, target_path: Path, target_kind: str, gate: dict[str, Any], field_count: int, *, reason: str) -> dict[str, Any]:
    return {
        "paper_id": paper_id,
        "target_kind": target_kind,
        "target_path": str(target_path),
        "paper_score": 0.0,
        "score_formula": SCORING_FORMULA,
        "field_count": field_count,
        "sample_count": 0,
        "gate": gate,
        "summary": {"reason": reason},
        "sample_reports": [],
    }


def _sample_index(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(record.get("sample_id")): record for record in data.get("samples", []) if isinstance(record, dict) and record.get("sample_id")}


def _group_facts_by_sample(facts: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for fact in facts:
        grouped.setdefault(str(fact.get("sample_id") or "paper_level"), []).append(fact)
    return grouped


def _sample_bundle_for_eval(data: dict[str, Any], sample_id: str, samples: dict[str, dict[str, Any]]) -> dict[str, Any]:
    sample = samples.get(sample_id, {"sample_id": sample_id})
    return {
        "sample_id": sample_id,
        "sample": sample,
        "alloy": _find_by_id(data.get("alloys", []), "alloy_id", sample.get("alloy_id")),
        "process": _find_by_id(data.get("processes", []), "process_id", sample.get("process_id")),
    }


def _find_by_id(records: list[Any], key: str, value: Any) -> dict[str, Any] | None:
    for record in records:
        if isinstance(record, dict) and value and str(record.get(key)) == str(value):
            return record
    return None


def _identity_canonical_map(data: dict[str, Any]) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for section, id_key in (("papers", "paper_id"), ("alloys", "alloy_id"), ("processes", "process_id"), ("samples", "sample_id")):
        for record in data.get(section, []):
            if isinstance(record, dict) and record.get(id_key):
                mapping[normalize_identifier(record[id_key])] = str(record[id_key])
    return mapping


def _sample_id_for_flat_key(key: str, data: dict[str, Any]) -> str:
    parts = key.split(".")
    if len(parts) > 1 and parts[1]:
        anchor = parts[1]
        sample_ids = {str(record.get("sample_id")) for record in data.get("samples", []) if isinstance(record, dict)}
        if anchor in sample_ids:
            return anchor
    return "paper_level"


def _field_weight(section: str, key: str) -> float:
    if section in {"structures", "properties", "performance"}:
        return 1.5
    if section in {"samples", "processing_steps", "interfaces"}:
        return 1.3
    if section in {"papers", "unmapped_findings"}:
        return 0.7
    return 1.0


def _weighted_average(items: list[tuple[float, float]]) -> float:
    total_weight = sum(weight for _, weight in items)
    if total_weight <= 0:
        return 0.0
    return sum(value * weight for value, weight in items) / total_weight


def _quality_summary(sample_reports: list[dict[str, Any]]) -> dict[str, Any]:
    fields = [field for sample in sample_reports for field in sample.get("fields", [])]
    return {
        "avg_sample_score": _weighted_average([(item["sample_score"], item["sample_weight"]) for item in sample_reports]),
        "field_count": len(fields),
        "yes_count": sum(1 for item in fields if item.get("is_correct") == "yes"),
        "partial_count": sum(1 for item in fields if item.get("is_correct") == "partial"),
        "unknown_count": sum(1 for item in fields if item.get("is_correct") == "unknown"),
        "no_count": sum(1 for item in fields if item.get("is_correct") == "no"),
    }


def _write_markdown_report(report: dict[str, Any], path: Path) -> None:
    lines = [
        f"# Verify Eval Report: {report['paper_id']}",
        "",
        f"- target_kind: {report.get('target_kind')}",
        f"- paper_score: {report.get('paper_score', 0):.2f}",
        f"- field_count: {report.get('field_count', 0)}",
        f"- gate_ok: {report.get('gate', {}).get('ok', False)}",
        "",
        "## Scoring Formula",
        "",
        "- yes=1.0, partial=0.6, unknown=0.3, no=0.0",
        "- field_score = correctness_score * evidence_confidence * 100",
        "- sample_score = sum(field_score * field_weight) / sum(field_weight)",
        "- paper_score = sum(sample_score * sample_weight) / sum(sample_weight)",
        "- if structure gate fails, paper_score = 0",
        "",
        "## Samples",
    ]
    for sample in report.get("sample_reports", []):
        lines.append(f"- {sample['sample_id']}: {sample['sample_score']:.2f} ({sample['field_count']} fields)")
    lines.extend(["", "## Field-Level Trace"])
    for sample in report.get("sample_reports", []):
        lines.append("")
        lines.append(f"### {sample['sample_id']}")
        for field in sample.get("fields", [])[:80]:
            refs = ",".join(field.get("evidence_refs", []))
            lines.append(
                f"- {field['field_id']} `{field['path']}`: score={field['field_score']:.2f}, "
                f"judge={field['is_correct']}, conf={field['evidence_confidence']:.2f}, refs={refs or '-'}"
            )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _compact_report_summary(report: dict[str, Any]) -> dict[str, Any]:
    return {
        "target_kind": report.get("target_kind"),
        "target_path": report.get("target_path"),
        "paper_score": report.get("paper_score", 0.0),
        "field_count": report.get("field_count", 0),
        "sample_count": report.get("sample_count", 0),
        "gate_ok": report.get("gate", {}).get("ok", False),
        "llm_error_count": report.get("llm_error_count", 0),
        "summary": report.get("summary", {}),
    }


def _write_compare_markdown(report: dict[str, Any], path: Path) -> None:
    before = report["before"]
    after = report["after"]
    delta = report["delta"]
    lines = [
        f"# Verify Compare Report: {report['paper_id']}",
        "",
        "## Scores",
        "",
        "| target | score | fields | gate |",
        "|---|---:|---:|---|",
        f"| before final | {before['paper_score']:.2f} | {before['field_count']} | {before['gate_ok']} |",
        f"| after verify | {after['paper_score']:.2f} | {after['field_count']} | {after['gate_ok']} |",
        f"| delta | {delta['paper_score']:+.2f} | {delta['field_count']:+d} | - |",
        "",
        f"- llm_error_count: {report.get('llm_error_count', 0)}",
        "",
        "## Formula",
        "",
        "- yes=1.0, partial=0.6, unknown=0.3, no=0.0",
        "- field_score = correctness_score * evidence_confidence * 100",
        "- sample_score = sum(field_score * field_weight) / sum(field_weight)",
        "- paper_score = sum(sample_score * sample_weight) / sum(sample_weight)",
        "",
        "## Detail Reports",
        "",
        f"- before: {report['paths']['before_report']}",
        f"- after: {report['paths']['after_report']}",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _safe_id(value: Any) -> str:
    return normalize_identifier(value) or "unknown"


VERIFY_EVAL_INSTRUCTION = """你正在执行材料论文结构化抽取结果的证据质量评估。

你不是抽取器，也不是修复器。你不能修改 JSON，不能补充 prompt 中未列出的字段，不能凭外部知识判断。你只能根据 evidence_blocks 判断 fields 中每个字段值是否被论文证据支持。

判断标准：
- yes：字段值被证据明确支持，或与证据表达等价。
- partial：字段大体正确，但有细节缺失、范围不完整或表达略有偏差。
- unknown：给定证据不足以判断，或证据没有直接覆盖该字段。
- no：字段值与证据矛盾，或明显归属到错误 sample。

evidence_confidence：
- 0.9-1.0：证据直接、明确、字段值基本逐项可核验。
- 0.6-0.8：证据支持主要含义，但不是完全逐字对应。
- 0.3-0.5：证据较弱，只能间接支持。
- 0.0-0.2：几乎没有证据或证据冲突。

输出要求：
只输出 JSON，不要 Markdown，不要解释性前后缀。格式固定为：
{
  "paper_id": "...",
  "sample_id": "...",
  "results": [
    {
      "field_id": "F00001",
      "is_correct": "yes" 或 "partial" 或 "unknown" 或 "no",
      "evidence_confidence": 0.0,
      "evidence_refs": ["b0001"],
      "reason": "简短中文理由"
    }
  ]
}

必须为输入 fields 中的每个 field_id 输出一条 result。evidence_refs 只能引用输入 evidence_blocks 中存在的 block_id。
"""
