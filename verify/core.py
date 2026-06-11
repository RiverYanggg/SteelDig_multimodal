from __future__ import annotations

import copy
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from verify.common import (
    EvidenceBlock,
    SchemaSpec,
    SharedLLMClient,
    build_evidence_blocks,
    compact_evidence_for_terms,
    ensure_schema,
    load_schema_spec,
    read_json,
    sample_terms,
    normalize_identifier,
    validation_report,
    write_json,
)


PATCH_OPS = {"replace_field", "move_record_to_sample", "drop_record", "append_record"}
DEFAULT_APPEND_ENABLED = False


@dataclass(frozen=True)
class VerifyResult:
    paper_id: str
    fixed_path: Path
    report_path: Path
    accepted_patch_count: int
    rejected_patch_count: int
    before_error_count: int
    after_error_count: int


def run_verify_for_paper(
    paper_dir: str | Path,
    *,
    llm_client: SharedLLMClient | None = None,
    force: bool = False,
    append_enabled: bool = DEFAULT_APPEND_ENABLED,
    max_evidence_chars: int = 80_000,
    schema_spec: SchemaSpec | None = None,
) -> VerifyResult:
    schema = schema_spec or load_schema_spec()
    paper_path = Path(paper_dir).expanduser().resolve()
    paper_id = paper_path.name
    final_path = _resolve_input_path(paper_path)
    cleaned_path = paper_path / "preprocess" / "cleaned_input.md"
    verify_dir = paper_path / "verify"
    fixed_path = verify_dir / "text_extraction_fixed.json"
    report_path = verify_dir / "verify_report.json"
    if fixed_path.exists() and report_path.exists() and not force:
        report = read_json(report_path)
        summary = report.get("summary", {})
        return VerifyResult(
            paper_id=paper_id,
            fixed_path=fixed_path,
            report_path=report_path,
            accepted_patch_count=int(summary.get("accepted_patch_count", 0)),
            rejected_patch_count=int(summary.get("rejected_patch_count", 0)),
            before_error_count=int(summary.get("before_error_count", 0)),
            after_error_count=int(summary.get("after_error_count", 0)),
        )
    if not final_path.is_file():
        raise FileNotFoundError(f"missing normalized or final text_extraction.json under {paper_path}")

    original = ensure_schema(read_json(final_path), schema)
    before_report = validation_report(original, schema)
    markdown = cleaned_path.read_text(encoding="utf-8") if cleaned_path.is_file() else ""
    evidence_blocks = build_evidence_blocks(markdown) if markdown else []

    verify_dir.mkdir(parents=True, exist_ok=True)
    write_json(before_report, verify_dir / "deterministic_report.json")
    write_json([block.to_dict() for block in evidence_blocks], verify_dir / "evidence_blocks.json")

    sample_bundles = build_sample_bundles(original, evidence_blocks, before_report, max_evidence_chars=max_evidence_chars, schema_spec=schema)
    for bundle in sample_bundles:
        write_json(bundle, verify_dir / "sample_bundles" / f"{_safe_id(bundle['sample_id'])}.json")

    working = copy.deepcopy(original)
    accepted_patches: list[dict[str, Any]] = []
    rejected_patches: list[dict[str, Any]] = []
    raw_outputs: list[dict[str, Any]] = []

    if llm_client and evidence_blocks:
        for bundle in sample_bundles:
            prompt_payload = {
                "instruction": VERIFY_INSTRUCTION,
                "paper_id": paper_id,
                "sample_bundle": bundle,
                "allowed_patch_ops": sorted(PATCH_OPS),
                "append_record_enabled": append_enabled,
            }
            write_json(prompt_payload, verify_dir / "sample_inputs" / f"{_safe_id(bundle['sample_id'])}.json")
            try:
                response = llm_client.complete_json(
                    system="You are a conservative evidence-based JSON verification engine.",
                    prompt=json.dumps(prompt_payload, ensure_ascii=False, indent=2),
                )
            except Exception as exc:
                rejected_patches.append(
                    {
                        "sample_id": bundle["sample_id"],
                        "op": "llm_call",
                        "accepted": False,
                        "reason": str(exc),
                    }
                )
                continue
            raw_outputs.append({"sample_id": bundle["sample_id"], "response": response})
            write_json(response, verify_dir / "sample_raw_outputs" / f"{_safe_id(bundle['sample_id'])}.json")
            proposal_path = verify_dir / "patches" / f"{_safe_id(bundle['sample_id'])}.patch.json"
            write_json(response, proposal_path)
            for patch in _patches_from_response(response, bundle["sample_id"]):
                patch_result = validate_and_apply_patch(
                    working,
                    patch,
                    evidence_blocks=evidence_blocks,
                    append_enabled=append_enabled,
                    before_error_count=validation_report(working, schema)["error_count"],
                    schema_spec=schema,
                )
                if patch_result["accepted"]:
                    accepted_patches.append(patch_result)
                else:
                    rejected_patches.append(patch_result)
    elif llm_client and not evidence_blocks:
        rejected_patches.append(
            {
                "op": "llm_verify",
                "accepted": False,
                "reason": "cleaned_input.md missing or empty; evidence-based verify skipped",
            }
        )

    after_report = validation_report(working, schema)
    if after_report["error_count"] > before_report["error_count"]:
        working = original
        after_report = before_report
        rejected_patches.append(
            {
                "op": "global_recheck",
                "accepted": False,
                "reason": "global recheck worsened structural errors; all patches rolled back",
            }
        )
        accepted_patches = []

    write_json(working, fixed_path)
    write_json(after_report, verify_dir / "deterministic_report_after.json")
    report = {
        "paper_id": paper_id,
        "target_path": str(final_path),
        "fixed_path": str(fixed_path),
        "target_kind": "normalized_units" if "normalized" in final_path.parts else "final_original",
        "llm_used": llm_client is not None,
        "append_record_enabled": append_enabled,
        "summary": {
            "sample_count": len(sample_bundles),
            "accepted_patch_count": len(accepted_patches),
            "rejected_patch_count": len(rejected_patches),
            "before_issue_count": before_report["issue_count"],
            "after_issue_count": after_report["issue_count"],
            "before_error_count": before_report["error_count"],
            "after_error_count": after_report["error_count"],
        },
        "before_validation": before_report,
        "after_validation": after_report,
        "accepted_patches": accepted_patches,
        "rejected_patches": rejected_patches,
    }
    write_json(report, report_path)
    return VerifyResult(
        paper_id=paper_id,
        fixed_path=fixed_path,
        report_path=report_path,
        accepted_patch_count=len(accepted_patches),
        rejected_patch_count=len(rejected_patches),
        before_error_count=before_report["error_count"],
        after_error_count=after_report["error_count"],
    )


def _resolve_input_path(paper_path: Path) -> Path:
    normalized = paper_path / "normalized" / "text_extraction_units.json"
    if normalized.is_file():
        return normalized
    return paper_path / "final" / "text_extraction.json"


def build_sample_bundles(
    data: dict[str, Any],
    evidence_blocks: list[EvidenceBlock],
    deterministic_report: dict[str, Any],
    *,
    max_evidence_chars: int,
    schema_spec: SchemaSpec | None = None,
) -> list[dict[str, Any]]:
    schema = schema_spec or load_schema_spec()
    payload = ensure_schema(data, schema)
    alloys = _index_by_id(payload["alloys"], "alloy_id")
    processes = _index_by_id(payload["processes"], "process_id")
    issues = deterministic_report.get("issues", [])
    bundles = []
    for sample in payload["samples"]:
        if not isinstance(sample, dict) or not sample.get("sample_id"):
            continue
        sample_id = str(sample["sample_id"])
        bundle = {
            "sample_id": sample_id,
            "sample": sample,
            "alloy": alloys.get(str(sample.get("alloy_id")), None),
            "process": processes.get(str(sample.get("process_id")), None),
            "processing_steps": _records_for_sample(payload["processing_steps"], sample_id),
            "structures": _records_for_sample(payload["structures"], sample_id),
            "interfaces": _records_for_sample(payload["interfaces"], sample_id),
            "properties": _records_for_sample(payload["properties"], sample_id),
            "performance": _records_for_sample(payload["performance"], sample_id),
            "known_issues": _issues_for_sample(issues, sample_id),
        }
        bundle["evidence_blocks"] = compact_evidence_for_terms(
            evidence_blocks,
            sample_terms(bundle),
            max_total_chars=max_evidence_chars,
        )
        bundles.append(bundle)
    return bundles


def validate_and_apply_patch(
    data: dict[str, Any],
    patch: dict[str, Any],
    *,
    evidence_blocks: list[EvidenceBlock],
    append_enabled: bool,
    before_error_count: int,
    schema_spec: SchemaSpec | None = None,
) -> dict[str, Any]:
    result = dict(patch)
    result["accepted"] = False
    reason = _validate_patch_shape(patch, evidence_blocks=evidence_blocks, append_enabled=append_enabled)
    if reason:
        result["reason"] = reason
        return result

    trial = copy.deepcopy(data)
    try:
        _apply_patch(trial, patch)
    except Exception as exc:
        result["reason"] = str(exc)
        return result
    after = validation_report(trial, schema_spec)
    if after["error_count"] > before_error_count:
        result["reason"] = "patch worsens structural validation"
        result["after_error_count"] = after["error_count"]
        return result

    data.clear()
    data.update(trial)
    result["accepted"] = True
    result["reason"] = patch.get("reason", "accepted")
    result["after_error_count"] = after["error_count"]
    return result


def _validate_patch_shape(
    patch: dict[str, Any],
    *,
    evidence_blocks: list[EvidenceBlock],
    append_enabled: bool,
) -> str | None:
    op = patch.get("op")
    if op not in PATCH_OPS:
        return f"unsupported patch op: {op}"
    if op == "append_record" and not append_enabled:
        return "append_record is disabled"
    confidence = str(patch.get("confidence", "high")).lower()
    if confidence == "low":
        return "low confidence patch rejected"
    evidence_ids = {block.block_id for block in evidence_blocks}
    refs = patch.get("evidence_refs", [])
    if not isinstance(refs, list):
        return "evidence_refs must be a list"
    if evidence_blocks and not refs:
        return "patch must cite at least one evidence block"
    missing_refs = [ref for ref in refs if ref not in evidence_ids]
    if missing_refs:
        return f"unknown evidence_refs: {missing_refs}"
    if op == "replace_field" and ("path" not in patch or "value" not in patch):
        return "replace_field requires path and value"
    if op == "move_record_to_sample" and ("record_path" not in patch or "to_sample_id" not in patch):
        return "move_record_to_sample requires record_path and to_sample_id"
    if op == "drop_record" and "record_path" not in patch:
        return "drop_record requires record_path"
    if op == "append_record" and ("section" not in patch or "record" not in patch):
        return "append_record requires section and record"
    return None


def _apply_patch(data: dict[str, Any], patch: dict[str, Any]) -> None:
    op = patch["op"]
    if op == "replace_field":
        record, field_path = _resolve_record_and_field(data, str(patch["path"]))
        _set_nested_value(record, field_path, patch["value"])
        return
    if op == "move_record_to_sample":
        sample_ids = {str(record.get("sample_id")) for record in data["samples"] if isinstance(record, dict)}
        to_sample_id = str(patch["to_sample_id"])
        if to_sample_id not in sample_ids:
            raise ValueError(f"to_sample_id does not exist: {to_sample_id}")
        record = _resolve_record(data, str(patch["record_path"]))
        if not isinstance(record, dict) or "sample_id" not in record:
            raise ValueError("record has no sample_id field")
        record["sample_id"] = to_sample_id
        return
    if op == "drop_record":
        section, index = _resolve_record_index(data, str(patch["record_path"]))
        if section in {"papers", "alloys", "processes", "samples"}:
            raise ValueError(f"drop_record is not allowed for core section: {section}")
        del data[section][index]
        return
    if op == "append_record":
        section = str(patch["section"])
        if section not in data or not isinstance(data[section], list):
            raise ValueError(f"invalid append section: {section}")
        record = patch["record"]
        if not isinstance(record, dict):
            raise ValueError("append record must be an object")
        data[section].append(record)
        return
    raise ValueError(f"unsupported patch op: {op}")


def _resolve_record_and_field(data: dict[str, Any], path: str) -> tuple[dict[str, Any], str]:
    head, _, field_path = path.partition(".")
    if not field_path:
        raise ValueError(f"replace path must include a field: {path}")
    record = _resolve_record(data, head)
    if not isinstance(record, dict):
        raise ValueError("replace target record must be an object")
    return record, field_path


def _resolve_record(data: dict[str, Any], path: str) -> Any:
    section, index = _resolve_record_index(data, path)
    return data[section][index]


def _resolve_record_index(data: dict[str, Any], path: str) -> tuple[str, int]:
    if "[" not in path or not path.endswith("]"):
        raise ValueError(f"invalid record path: {path}")
    section, selector = path.split("[", 1)
    selector = selector[:-1]
    if section not in data:
        raise ValueError(f"unknown section: {section}")
    if selector.isdigit():
        index = int(selector)
        if index >= len(data[section]):
            raise ValueError(f"index out of range: {path}")
        return section, index
    if "=" not in selector:
        raise ValueError(f"selector must be index or key=value: {path}")
    key, value = selector.split("=", 1)
    matches = [
        index
        for index, record in enumerate(data[section])
        if isinstance(record, dict) and str(record.get(key)) == value
    ]
    if len(matches) != 1:
        raise ValueError(f"selector must match exactly one record: {path}")
    return section, matches[0]


def _set_nested_value(record: dict[str, Any], field_path: str, value: Any) -> None:
    parts = field_path.split(".")
    cursor: Any = record
    for part in parts[:-1]:
        if not isinstance(cursor, dict) or part not in cursor:
            raise ValueError(f"field path does not exist: {field_path}")
        cursor = cursor[part]
    if not isinstance(cursor, dict) or parts[-1] not in cursor:
        raise ValueError(f"field path does not exist: {field_path}")
    cursor[parts[-1]] = value


def _patches_from_response(response: dict[str, Any], sample_id: str) -> list[dict[str, Any]]:
    patches = response.get("patch_ops", [])
    if not isinstance(patches, list):
        return []
    normalized = []
    for patch in patches:
        if isinstance(patch, dict):
            item = dict(patch)
            item.setdefault("sample_id", sample_id)
            normalized.append(item)
    return normalized


def _index_by_id(records: list[Any], key: str) -> dict[str, dict[str, Any]]:
    return {str(record[key]): record for record in records if isinstance(record, dict) and record.get(key)}


def _records_for_sample(records: list[Any], sample_id: str) -> list[Any]:
    return [record for record in records if isinstance(record, dict) and str(record.get("sample_id")) == sample_id]


def _issues_for_sample(issues: list[dict[str, Any]], sample_id: str) -> list[dict[str, Any]]:
    normalized = normalize_identifier(sample_id)
    return [issue for issue in issues if normalized in normalize_identifier(json.dumps(issue, ensure_ascii=False))]


def _safe_id(value: Any) -> str:
    return normalize_identifier(value) or "unknown"


VERIFY_INSTRUCTION = """你正在执行材料论文结构化抽取结果的保守校验与修复建议。

你的角色不是重新抽取器，而是“证据驱动的审查员”。你只能基于 sample_bundle.evidence_blocks 中给出的论文证据判断，不能使用外部知识，不能凭常识补事实。

核心原则：
1. 宁可不修改，也不要提出有风险的修改。
2. 只有证据明确支持时，才提出 patch。
3. 不要重写整篇 JSON，不要输出完整 text_extraction.json。
4. 只检查当前 sample_bundle 对应的 sample 及其关联记录。
5. 重点关注 sample 归属、alloy/process 绑定、下游 structures/properties/performance/interfaces/processing_steps 是否错挂。
6. 低置信度问题只写入 issues，不要提出会被应用的 patch。

允许的 patch 操作：
- replace_field：替换已有记录中的某个字段值。
- move_record_to_sample：把已有下游记录移动到另一个已存在 sample_id。
- drop_record：删除明显重复或明显错误的下游记录。禁止删除 papers/alloys/processes/samples。
- append_record：只有 append_record_enabled=true 时才允许；否则不要使用。

patch 路径格式必须严格遵守：
- replace_field.path 示例：samples[sample_id=sample_3cu].process_id
- move_record_to_sample.record_path 示例：properties[property_set_id=prop_12]
- drop_record.record_path 示例：structures[structure_id=struct_duplicate]

每个 patch 必须包含：
- op
- evidence_refs：至少一个 evidence block id，例如 ["b0017"]
- reason：简短中文理由，说明证据如何支持该修改
- confidence："high"、"medium" 或 "low"

输出要求：
只输出 JSON，不要 Markdown，不要解释性前后缀。JSON 顶层格式固定为：
{
  "paper_id": "...",
  "sample_id": "...",
  "verdict": "ok" 或 "needs_fix" 或 "uncertain",
  "issues": [
    {
      "issue_type": "...",
      "target_path": "...",
      "evidence_refs": ["b0001"],
      "reason": "..."
    }
  ],
  "patch_ops": [
    {
      "op": "move_record_to_sample",
      "record_path": "properties[property_set_id=prop_12]",
      "to_sample_id": "sample_x",
      "evidence_refs": ["b0001"],
      "reason": "...",
      "confidence": "high"
    }
  ],
  "confidence": "high" 或 "medium" 或 "low"
}

如果证据不足或当前 sample 看起来没有明确错误，返回 verdict="ok" 或 "uncertain"，patch_ops=[]。
"""
