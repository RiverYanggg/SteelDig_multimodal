import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from paper_extractor.common import clean_text, extract_figure_id, extract_json_candidates, log_jsonl, truncate_text
from paper_extractor.config import WorkflowSettings


TOP_LEVEL_SCHEMA_KEYS = {
    "papers",
    "alloys",
    "processes",
    "samples",
    "processing_steps",
    "structures",
    "interfaces",
    "properties",
    "performance",
    "characterization_methods",
    "computational_details",
    "unmapped_findings",
}


@dataclass(frozen=True)
class ParseResult:
    parsed: Any
    method: str


def parse_request_index(request_stem: str) -> int:
    match = re.match(r"^figure_(\d+)$", request_stem)
    if match:
        return int(match.group(1))
    match = re.match(r"^request_(\d+)$", request_stem)
    if match:
        return int(match.group(1))
    raise ValueError(f"Invalid request file name: {request_stem}")


def run_post_parse(output_root: Path, settings: WorkflowSettings | None = None) -> Dict[str, int]:
    summary = {
        "papers_scanned": 0,
        "text_parse_success": 0,
        "text_parse_fail": 0,
        "multimodal_parse_success": 0,
        "multimodal_parse_fail": 0,
        "fallback_agent_used": 0,
    }

    fallback_client = _create_fallback_client(settings) if settings is not None else None

    for paper_dir in sorted(path for path in output_root.iterdir() if path.is_dir()):
        summary["papers_scanned"] += 1
        paper_summary = run_post_parse_for_paper(paper_dir, settings=settings, fallback_client=fallback_client)
        for key in (
            "text_parse_success",
            "text_parse_fail",
            "multimodal_parse_success",
            "multimodal_parse_fail",
            "fallback_agent_used",
        ):
            summary[key] += paper_summary[key]

    return summary


def run_post_parse_for_paper(
    paper_dir: Path,
    settings: WorkflowSettings | None = None,
    fallback_client: Any | None = None,
) -> Dict[str, int]:
    summary = {
        "text_parse_success": 0,
        "text_parse_fail": 0,
        "multimodal_parse_success": 0,
        "multimodal_parse_fail": 0,
        "fallback_agent_used": 0,
    }

    if fallback_client is None and settings is not None:
        fallback_client = _create_fallback_client(settings)

    paper_id = paper_dir.name
    # This function intentionally processes only one paper_dir. The sequential
    # extraction->post-parse->knowledge orchestrator depends on that isolation
    # to guarantee fused mode reads the current paper's finalized outputs only.
    logs_dir = paper_dir / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    post_parse_log = logs_dir / "post_parse.log.jsonl"

    intermediate_dir = paper_dir / "intermediate"
    final_dir = paper_dir / "final"
    final_dir.mkdir(parents=True, exist_ok=True)

    text_txt = intermediate_dir / "text" / "text_extraction.txt"
    if text_txt.exists():
        try:
            parse_result = parse_text_output(text_txt.read_text(encoding="utf-8"))
        except Exception as exc:
            parse_result = None
            parse_error = exc
        else:
            parse_error = None

        if parse_result is None and fallback_client is not None and settings is not None:
            try:
                parse_result = fallback_parse_with_agent(
                    fallback_client,
                    model=settings.text_model.model,
                    stage="text_post_parse",
                    raw_text=text_txt.read_text(encoding="utf-8"),
                    paper_id=paper_id,
                )
                summary["fallback_agent_used"] += 1
            except Exception as exc:
                parse_error = exc

        if parse_result is not None:
            out_json = final_dir / "text_extraction.json"
            out_json.write_text(json.dumps(parse_result.parsed, ensure_ascii=False, indent=2), encoding="utf-8")
            summary["text_parse_success"] += 1
            log_jsonl(
                post_parse_log,
                {
                    "ts": datetime.now().isoformat(),
                    "event": "model_output",
                    "stage": "text_post_parse",
                    "paper_id": paper_id,
                    "output_file": str(out_json),
                    "status": "success",
                    "method": parse_result.method,
                },
            )
        else:
            summary["text_parse_fail"] += 1
            log_jsonl(
                post_parse_log,
                {
                    "ts": datetime.now().isoformat(),
                    "event": "model_output",
                    "stage": "text_post_parse",
                    "paper_id": paper_id,
                    "output_file": str(text_txt),
                    "status": "error",
                    "error": str(parse_error),
                },
            )

    multimodal_groups_path = intermediate_dir / "multimodal" / "image_groups.json"
    groups = _load_groups(multimodal_groups_path)
    final_multimodal_items: List[Dict[str, Any]] = []

    for request_txt in sorted((intermediate_dir / "multimodal").glob("figure_*.txt")):
        try:
            request_index = parse_request_index(request_txt.stem)
            group = groups[request_index - 1] if 0 < request_index <= len(groups) else {}
            parse_result = parse_multimodal_output(
                request_txt.read_text(encoding="utf-8"),
                paper_id=paper_id,
                group=group,
                fallback_request_id=request_txt.stem,
            )
        except Exception as exc:
            parse_result = None
            parse_error = exc
        else:
            parse_error = None

        if parse_result is None and fallback_client is not None and settings is not None:
            try:
                parse_result = fallback_parse_with_agent(
                    fallback_client,
                    model=settings.text_model.model,
                    stage="multimodal_post_parse",
                    raw_text=request_txt.read_text(encoding="utf-8"),
                    paper_id=paper_id,
                    extra_context={
                        "group": group,
                        "fallback_request_id": request_txt.stem,
                    },
                )
                summary["fallback_agent_used"] += 1
                if isinstance(parse_result.parsed, dict):
                    parse_result = ParseResult(
                        parsed=normalize_figure_result(
                            parse_result.parsed,
                            paper_id=paper_id,
                            group=group,
                            fallback_request_id=request_txt.stem,
                        ),
                        method=parse_result.method,
                    )
            except Exception as exc:
                parse_error = exc

        if parse_result is not None:
            request_json = final_dir / f"{request_txt.stem}.json"
            request_json.write_text(json.dumps(parse_result.parsed, ensure_ascii=False, indent=2), encoding="utf-8")
            if isinstance(parse_result.parsed, dict):
                final_multimodal_items.append(parse_result.parsed)
            summary["multimodal_parse_success"] += 1
            log_jsonl(
                post_parse_log,
                {
                    "ts": datetime.now().isoformat(),
                    "event": "model_output",
                    "stage": "multimodal_post_parse",
                    "paper_id": paper_id,
                    "output_file": str(request_json),
                    "status": "success",
                    "method": parse_result.method,
                    "image_count": len(parse_result.parsed.get("image_paths", [])) if isinstance(parse_result.parsed, dict) else None,
                },
            )
        else:
            summary["multimodal_parse_fail"] += 1
            log_jsonl(
                post_parse_log,
                {
                    "ts": datetime.now().isoformat(),
                    "event": "model_output",
                    "stage": "multimodal_post_parse",
                    "paper_id": paper_id,
                    "output_file": str(request_txt),
                    "status": "error",
                    "error": str(parse_error),
                },
            )

    if final_multimodal_items:
        multimodal_summary_path = final_dir / "multimodal_figures.json"
        multimodal_summary_path.write_text(
            json.dumps(final_multimodal_items, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    return summary


def parse_text_output(raw_text: str) -> ParseResult:
    parsed = _parse_best_json_candidate(raw_text)
    if not isinstance(parsed, dict):
        raise ValueError("Text extraction output must parse to a JSON object.")
    return ParseResult(parsed=parsed, method="rule")


def parse_multimodal_output(raw_text: str, paper_id: str, group: Dict[str, Any], fallback_request_id: str) -> ParseResult:
    parsed = _parse_best_json_candidate(raw_text)
    if isinstance(parsed, list):
        if len(parsed) == 1 and isinstance(parsed[0], dict):
            parsed = parsed[0]
        else:
            parsed = _coalesce_figure_records(parsed)
    if not isinstance(parsed, dict):
        raise ValueError("Multimodal extraction output must parse to a JSON object.")
    normalized = normalize_figure_result(parsed, paper_id=paper_id, group=group, fallback_request_id=fallback_request_id)
    return ParseResult(parsed=normalized, method="rule")


def normalize_figure_result(parsed: Dict[str, Any], paper_id: str, group: Dict[str, Any], fallback_request_id: str) -> Dict[str, Any]:
    image_paths = group.get("image_paths", []) if isinstance(group, dict) else []
    if not isinstance(image_paths, list):
        image_paths = []
    caption = str(group.get("caption", "")) if isinstance(group, dict) else ""
    figure_id = clean_text(str(parsed.get("figure_id", ""))) or extract_figure_id(caption, fallback_request_id)
    image_type = clean_text(str(parsed.get("image_type", "")))
    description = clean_text(str(parsed.get("description", "")))
    confidence = _normalize_confidence(parsed.get("confidence", 0.0))
    return {
        "paper_id": paper_id,
        "figure_id": figure_id,
        "image_paths": [clean_text(str(path)) for path in image_paths],
        "image_count": len(image_paths),
        "image_type": image_type,
        "description": description,
        "confidence": confidence,
    }


def fallback_parse_with_agent(
    client: Any,
    model: str,
    stage: str,
    raw_text: str,
    paper_id: str,
    extra_context: Dict[str, Any] | None = None,
) -> ParseResult:
    prompt = build_fallback_parse_prompt(stage=stage, raw_text=raw_text, paper_id=paper_id, extra_context=extra_context)
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "你是结构化解析助手。你只负责把原始模型输出修复成合法 JSON，不补充无根据事实。"},
            {"role": "user", "content": prompt},
        ],
    )
    content = completion.choices[0].message.content or ""
    parsed = _parse_best_json_candidate(content)
    return ParseResult(parsed=parsed, method="fallback_agent")


def build_fallback_parse_prompt(stage: str, raw_text: str, paper_id: str, extra_context: Dict[str, Any] | None = None) -> str:
    context_json = json.dumps(extra_context or {}, ensure_ascii=False)
    return (
        "请把下面的原始模型输出修复为一个合法 JSON。\n"
        "要求：\n"
        "1. 只输出 JSON，不要解释，不要 Markdown，不要代码块。\n"
        "2. 输出必须能被 json.loads 直接解析；不要使用 NaN、Infinity、注释、尾随逗号或单引号。\n"
        "3. 不要编造原始输出中没有的信息；只能修复括号、引号、转义、字段类型、缺失的 null/[] 占位和外层包装问题。\n"
        "4. 若 stage=text_post_parse，则必须输出一个以既定 paper schema 为主体的 JSON object："
        "顶级键必须保留 papers, alloys, processes, samples, processing_steps, structures, interfaces, properties, performance, characterization_methods, computational_details, unmapped_findings。"
        "不得删除任何顶级键，不得改变既定主干数组/对象层级。"
        "优先将信息修复到 schema 现有字段；仅当某些高价值信息确实无法稳定放入现有字段时，才允许保留少量 schema 外扩展键，且不能破坏主干结构。"
        "同时尽量保留原始输出中的高信息密度字段、数值、单位、样品编号、工艺条件、组织/性能/机理关系。\n"
        "5. 若 stage=multimodal_post_parse，则输出一个 Figure 级 JSON object，字段应尽量包含 "
        "paper_id, figure_id, image_type, description, confidence；description 应保留原始输出中的视觉证据、caption 证据、子图关系、关键趋势、样品/图号/数值/单位。\n\n"
        f"paper_id: {paper_id}\n"
        f"stage: {stage}\n"
        f"context_json: {context_json}\n"
        "raw_model_output:\n"
        f"{raw_text}\n"
    )


def _parse_best_json_candidate(raw_text: str) -> Any:
    candidates = extract_json_candidates(raw_text)
    scored: List[tuple[int, int, str]] = []
    for candidate in candidates:
        try:
            parsed = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        score = _score_parsed_json(parsed)
        scored.append((score, len(candidate), candidate))
    if not scored:
        raise ValueError("No valid JSON candidate found.")
    scored.sort(reverse=True)
    return json.loads(scored[0][2])


def _score_parsed_json(parsed: Any) -> int:
    if isinstance(parsed, dict):
        return sum(1 for key in TOP_LEVEL_SCHEMA_KEYS if key in parsed) + sum(
            1 for key in ("paper_id", "figure_id", "image_type", "description", "confidence") if key in parsed
        )
    if isinstance(parsed, list):
        if parsed and isinstance(parsed[0], dict):
            return max(_score_parsed_json(item) for item in parsed if isinstance(item, dict))
        return 0
    return 0


def _coalesce_figure_records(items: List[Any]) -> Dict[str, Any]:
    records = [item for item in items if isinstance(item, dict)]
    if not records:
        raise ValueError("Empty multimodal records.")
    best = records[0]
    descriptions = [clean_text(str(item.get("description", ""))) for item in records if item.get("description")]
    description = " ".join(dict.fromkeys(desc for desc in descriptions if desc))
    confidences = [_normalize_confidence(item.get("confidence", 0.0)) for item in records]
    confidence = max(confidences) if confidences else 0.0
    return {
        "figure_id": best.get("figure_id"),
        "image_type": clean_text(str(best.get("image_type", ""))),
        "description": description or clean_text(str(best.get("description", ""))),
        "confidence": confidence,
    }


def _normalize_confidence(value: Any) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    text = clean_text(str(value))
    match = re.search(r"-?\d+(?:\.\d+)?", text)
    if not match:
        return 0.0
    return float(match.group(0))


def _load_groups(groups_path: Path) -> List[Dict[str, Any]]:
    if not groups_path.exists():
        return []
    try:
        loaded = json.loads(groups_path.read_text(encoding="utf-8"))
    except Exception:
        return []
    if isinstance(loaded, list):
        return [item for item in loaded if isinstance(item, dict)]
    return []


def _create_fallback_client(settings: WorkflowSettings) -> Any:
    from paper_extractor.client import create_client

    return create_client(settings.text_model)
