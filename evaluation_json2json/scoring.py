from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

from evaluation.field_match import match_field_value
from evaluation.metrics import bleu_score, precision_recall_f1, rouge_l_f1
from evaluation.normalize import normalize_identifier, normalize_text


SECTION_ID_KEYS = {
    "papers": "paper_id",
    "alloys": "alloy_id",
    "processes": "process_id",
    "samples": "sample_id",
    "processing_steps": "sample_id",
    "structures": "sample_id",
    "interfaces": "sample_id",
    "properties": "sample_id",
    "performance": "sample_id",
    "characterization_methods": None,
    "computational_details": None,
    "unmapped_findings": None,
}


@dataclass(frozen=True)
class SectionMetrics:
    truth_count: int
    prediction_count: int
    matched_count: int
    precision: float
    recall: float
    f1: float


class FieldJudge(Protocol):
    def judge_fields(self, paper_key: str, section_name: str, candidates: list[dict[str, Any]]) -> dict[str, Any]:
        ...


def record_section_metrics(truth_count: int, prediction_count: int, matched_count: int) -> SectionMetrics:
    prf = precision_recall_f1(
        tp=matched_count,
        fp=max(prediction_count - matched_count, 0),
        fn=max(truth_count - matched_count, 0),
    )
    return SectionMetrics(
        truth_count=truth_count,
        prediction_count=prediction_count,
        matched_count=matched_count,
        precision=prf["precision"],
        recall=prf["recall"],
        f1=prf["f1"],
    )


def record_structure_metrics_for_section(
    section_name: str,
    truth_records: list[Any],
    pred_records: list[Any],
    truth_to_canonical: dict[str, str],
    pred_to_canonical: dict[str, str],
) -> dict[str, Any]:
    truth_anchors = _structure_anchors(section_name, truth_records, truth_to_canonical)
    pred_anchors = _structure_anchors(section_name, pred_records, pred_to_canonical)
    matched = sorted(set(truth_anchors) & set(pred_anchors))
    prf = precision_recall_f1(
        tp=len(matched),
        fp=max(len(set(pred_anchors)) - len(matched), 0),
        fn=max(len(set(truth_anchors)) - len(matched), 0),
    )
    return {
        "truth_count": len(set(truth_anchors)),
        "prediction_count": len(set(pred_anchors)),
        "matched_count": len(matched),
        "precision": prf["precision"],
        "recall": prf["recall"],
        "f1": prf["f1"],
        "matched_anchors": matched[:50],
        "unmatched_truth_anchors": sorted(set(truth_anchors) - set(pred_anchors))[:50],
        "unmatched_prediction_anchors": sorted(set(pred_anchors) - set(truth_anchors))[:50],
    }


def compare_sections(
    section_name: str,
    truth_records: list[Any],
    pred_records: list[Any],
    truth_to_canonical: dict[str, str],
    pred_to_canonical: dict[str, str],
    field_rules: dict[str, Any],
    paper_key: str = "",
    field_judge: FieldJudge | None = None,
) -> dict[str, Any]:
    truth_flat = _flatten_records(section_name, truth_records, truth_to_canonical, field_rules)
    pred_flat = _flatten_records(section_name, pred_records, pred_to_canonical, field_rules)

    truth_keys = set(truth_flat)
    pred_keys = set(pred_flat)
    matched_keys = truth_keys & pred_keys

    correct_count = 0
    text_scores: list[dict[str, float]] = []
    match_details: list[dict[str, Any]] = []
    llm_judge_candidates: list[dict[str, Any]] = []
    unmatched_truth_keys = sorted(truth_keys - pred_keys)
    unmatched_pred_keys = sorted(pred_keys - truth_keys)

    pending_llm_details: list[dict[str, Any]] = []
    for key in sorted(matched_keys):
        truth_value = truth_flat[key]
        pred_value = pred_flat[key]
        match_result = match_field_value(key, truth_value, pred_value, field_rules)
        if match_result.matched:
            correct_count += 1
        detail = {
            "key": key,
            "truth_path": key,
            "prediction_path": key,
            "canonical_object": _canonical_object_from_key(key),
            "field_path": _field_path_from_key(key),
            "same_sample": True,
            "same_path": True,
            "truth_value": truth_value,
            "prediction_value": pred_value,
            "error_type": _error_type_for_match(key, match_result),
            **match_result.to_dict(),
        }
        match_details.append(detail)
        if match_result.needs_llm_judge:
            llm_judge_candidates.append(detail)
            pending_llm_details.append(detail)
        if _is_text_key(key, field_rules):
            truth_text = normalize_text(truth_value)
            pred_text = normalize_text(pred_value)
            text_scores.append(
                {
                    "bleu": bleu_score(truth_text, pred_text),
                    "rouge_l_f1": rouge_l_f1(truth_text, pred_text),
                }
            )

    llm_judge_result: dict[str, Any] | None = None
    if field_judge and pending_llm_details:
        judge_candidates = [
            _build_judge_candidate(section_name, index, item)
            for index, item in enumerate(pending_llm_details)
            if item.get("same_sample") is True and item.get("same_path") is True
        ]
        llm_judge_result = {"decisions": {}, "raw_response": "", "error": None, "input_candidates": judge_candidates}
        if judge_candidates:
            llm_judge_result = field_judge.judge_fields(paper_key=paper_key, section_name=section_name, candidates=judge_candidates)
            llm_judge_result["input_candidates"] = judge_candidates
            decisions = llm_judge_result.get("decisions", {}) if isinstance(llm_judge_result, dict) else {}
            detail_by_id = {str(item.get("llm_input_id")): item for item in pending_llm_details}
            for candidate in judge_candidates:
                detail = detail_by_id.get(str(candidate["id"]))
                if not detail:
                    continue
                matched = bool(decisions.get(candidate["id"], False))
                detail["matched"] = matched
                detail["method"] = "llm_field_judge"
                detail["error_type"] = "correct" if matched else "value_mismatch"
                detail["reason"] = "LLM judged same-field values as semantically matched." if matched else "LLM judged same-field values as not semantically matched."
                detail["score"] = 1.0 if matched else 0.0
                detail["needs_llm_judge"] = False
                if matched:
                    correct_count += 1

    prf = precision_recall_f1(
        tp=correct_count,
        fp=max(len(pred_keys) - correct_count, 0),
        fn=max(len(truth_keys) - correct_count, 0),
    )
    error_summary = _summarize_error_types(match_details, unmatched_truth_keys, unmatched_pred_keys)
    return {
        "truth_fact_count": len(truth_keys),
        "prediction_fact_count": len(pred_keys),
        "matched_fact_slots": len(matched_keys),
        "correct_fact_count": correct_count,
        "precision": prf["precision"],
        "recall": prf["recall"],
        "f1": prf["f1"],
        "avg_bleu": _average([item["bleu"] for item in text_scores]),
        "avg_rouge_l_f1": _average([item["rouge_l_f1"] for item in text_scores]),
        "error_summary": error_summary,
        "missing_truth_fact_examples": unmatched_truth_keys[:20],
        "extra_prediction_fact_examples": unmatched_pred_keys[:20],
        "match_method_summary": _summarize_match_methods(match_details),
        "matched_fact_examples": [item for item in match_details if item["matched"]][:20],
        "mismatched_fact_examples": [item for item in match_details if not item["matched"]][:20],
        "llm_judge_candidate_count": len(llm_judge_candidates),
        "llm_judge_candidates": llm_judge_candidates[:20],
        "llm_judge_result": llm_judge_result,
        "field_match_log": {
            "matched_slots": match_details,
            "missing_truth_facts": unmatched_truth_keys,
            "extra_prediction_facts": unmatched_pred_keys,
        },
    }


def flatten_section_records(
    section_name: str,
    records: list[Any],
    canonical_map: dict[str, str],
    field_rules: dict[str, Any],
) -> dict[str, str]:
    return _flatten_records(section_name, records, canonical_map, field_rules)


def build_sample_context(
    samples: list[dict[str, Any]],
    structures: list[dict[str, Any]],
    properties: list[dict[str, Any]],
    performance: list[dict[str, Any]],
    interfaces: list[dict[str, Any]],
    processing_steps: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    context = {str(sample.get("sample_id")): {} for sample in samples if sample.get("sample_id")}

    for collection_name, records in {
        "structures": structures,
        "properties": properties,
        "performance": performance,
        "interfaces": interfaces,
        "processing_steps": processing_steps,
    }.items():
        for record in records:
            sample_id = str(record.get("sample_id", ""))
            if sample_id and sample_id in context:
                context[sample_id].setdefault(collection_name, []).append(record)
    return context


def _flatten_records(
    section_name: str,
    records: list[Any],
    canonical_map: dict[str, str],
    field_rules: dict[str, Any],
) -> dict[str, str]:
    flat: dict[str, str] = {}
    id_key = SECTION_ID_KEYS.get(section_name)
    for index, record in enumerate(records):
        if isinstance(record, dict):
            anchor = _resolve_anchor(section_name, record, index, id_key, canonical_map)
            for path, value in _walk(record):
                if _is_empty(value):
                    continue
                if _skip_path(path, field_rules):
                    continue
                key = f"{section_name}.{anchor}.{path}"
                flat[key] = str(value)
        else:
            flat[f"{section_name}.idx_{index}.value"] = str(record)
    return flat


def _structure_anchors(section_name: str, records: list[Any], canonical_map: dict[str, str]) -> list[str]:
    id_key = SECTION_ID_KEYS.get(section_name)
    anchors: list[str] = []
    for index, record in enumerate(records):
        if isinstance(record, dict):
            anchor = _resolve_anchor(section_name, record, index, id_key, canonical_map)
            anchors.append(_record_structure_anchor(section_name, anchor, record, canonical_map))
        else:
            anchors.append(f"{section_name}.idx_{index}")
    return anchors


def _record_structure_anchor(section_name: str, anchor: str, record: dict[str, Any], canonical_map: dict[str, str]) -> str:
    if section_name == "processing_steps":
        sample_ref = _canonical_record_ref(record.get("sample_id"), canonical_map, anchor)
        return ".".join(
            item
            for item in (
                section_name,
                sample_ref,
                normalize_identifier(record.get("sequence") or record.get("sequence_order") or ""),
                normalize_identifier(record.get("type") or ""),
                normalize_identifier(record.get("method") or ""),
                normalize_identifier(record.get("temperature") or ""),
            )
            if item
        )
    if section_name == "characterization_methods":
        return ".".join(item for item in (section_name, normalize_identifier(record.get("method_name") or record.get("method") or anchor)) if item)
    if section_name == "computational_details":
        return ".".join(item for item in (section_name, normalize_identifier(record.get("method") or record.get("software") or anchor)) if item)
    if section_name == "unmapped_findings":
        return f"{section_name}.{normalize_identifier(record.get('finding') or record.get('claim') or anchor)}"
    return f"{section_name}.{anchor}"


def _canonical_record_ref(value: Any, canonical_map: dict[str, str], fallback: str) -> str:
    if not value:
        return fallback
    return normalize_identifier(canonical_map.get(normalize_identifier(value), str(value)))


def _resolve_anchor(
    section_name: str,
    record: dict[str, Any],
    index: int,
    id_key: str | None,
    canonical_map: dict[str, str],
) -> str:
    if id_key and record.get(id_key):
        record_id = str(record.get(id_key))
        return canonical_map.get(normalize_identifier(record_id), record_id)
    for candidate_key in ("sample_id", "process_id", "alloy_id", "paper_id", "method_name"):
        value = record.get(candidate_key)
        if value:
            return canonical_map.get(normalize_identifier(str(value)), str(value))
    return f"idx_{index}"


def _walk(node: Any, prefix: str = ""):
    if isinstance(node, dict):
        combined_paths = _combined_quantity_paths(node)
        for name, value in combined_paths.items():
            next_prefix = f"{prefix}.{name}" if prefix else name
            yield next_prefix, value
        skip_keys = _combined_quantity_source_keys(combined_paths)
        for key, value in node.items():
            if key in skip_keys:
                continue
            next_prefix = f"{prefix}.{key}" if prefix else key
            yield from _walk(value, next_prefix)
        return
    if isinstance(node, list):
        for index, item in enumerate(node):
            anchor = _list_item_anchor(item)
            next_prefix = f"{prefix}[{anchor}]" if anchor else f"{prefix}[{index}]"
            yield from _walk(item, next_prefix)
        return
    yield prefix, node


def _combined_quantity_paths(node: dict[str, Any]) -> dict[str, str]:
    combined: dict[str, str] = {}
    unit = node.get("unit")
    if unit and not _is_empty(unit):
        for key in ("value", "temperature"):
            value = node.get(key)
            if not _is_empty(value):
                combined[f"{key}_with_unit"] = f"{value} {unit}"
    return combined


def _combined_quantity_source_keys(combined_paths: dict[str, str]) -> set[str]:
    skip: set[str] = set()
    for combined_key in combined_paths:
        if combined_key == "value_with_unit":
            skip.update({"value", "unit"})
        if combined_key == "temperature_with_unit":
            skip.update({"temperature", "unit"})
    return skip


def _list_item_anchor(item: Any) -> str | None:
    if not isinstance(item, dict):
        return None
    for key in (
        "element",
        "phase_name",
        "phase_1_name",
        "phase_2_name",
        "property_name",
        "property_type",
        "method",
        "type",
        "direction",
        "region",
        "sequence",
        "sequence_order",
        "related_sequence",
        "coherence",
    ):
        value = item.get(key)
        if value:
            return normalize_identifier(value)
    return None


def _skip_path(path: str, field_rules: dict[str, Any]) -> bool:
    final_key = path.split(".")[-1]
    return final_key in set(field_rules.get("id_fields", []))


def _is_empty(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return normalize_text(value) in {"", "none", "null", "na", "n/a"}
    if isinstance(value, list):
        return not value
    if isinstance(value, dict):
        return not value
    return False


def _is_text_key(key: str, field_rules: dict[str, Any]) -> bool:
    return any(marker in key for marker in ("title", "description", "notes", "journal", "alloy_name", "findings", "purpose"))


def _average(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def _summarize_match_methods(match_details: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    summary: dict[str, dict[str, int]] = {}
    for item in match_details:
        method = str(item.get("method", "unknown"))
        bucket = summary.setdefault(method, {"matched": 0, "mismatched": 0})
        if item.get("matched"):
            bucket["matched"] += 1
        else:
            bucket["mismatched"] += 1
    return summary


def _field_name_from_key(key: str) -> str:
    tail = key.split(".")[-1]
    if "]" in tail:
        tail = tail.split("]")[-1].lstrip(".")
    return tail or key


def _build_judge_candidate(section_name: str, index: int, detail: dict[str, Any]) -> dict[str, Any]:
    input_id = _stable_input_id(section_name, index, str(detail["key"]))
    detail["llm_input_id"] = input_id
    return {
        "id": input_id,
        "section": section_name,
        "canonical_object": detail.get("canonical_object", ""),
        "field": _field_name_from_key(str(detail["key"])),
        "field_path": detail.get("field_path", ""),
        "truth_path": detail.get("truth_path", detail["key"]),
        "prediction_path": detail.get("prediction_path", detail["key"]),
        "same_sample": detail.get("same_sample") is True,
        "same_path": detail.get("same_path") is True,
        "truth_value": detail["truth_value"],
        "prediction_value": detail["prediction_value"],
    }


def _stable_input_id(section_name: str, index: int, key: str) -> str:
    safe_key = normalize_identifier(key).replace(".", "_")
    if len(safe_key) > 80:
        safe_key = safe_key[-80:]
    return f"{section_name}:{index}:{safe_key}"


def _canonical_object_from_key(key: str) -> str:
    parts = key.split(".")
    return parts[1] if len(parts) > 1 else ""


def _field_path_from_key(key: str) -> str:
    parts = key.split(".")
    return ".".join(parts[2:]) if len(parts) > 2 else key


def _error_type_for_match(key: str, match_result) -> str:
    if match_result.matched:
        return "correct"
    if match_result.needs_llm_judge:
        return "semantic_judge_needed"
    method = str(match_result.method)
    if "quantity" in method:
        return "value_or_unit_mismatch"
    if "label" in method or "synonym" in method:
        return "label_mismatch"
    if _is_text_key(key, {}):
        return "text_mismatch"
    return "value_mismatch"


def _summarize_error_types(
    match_details: list[dict[str, Any]],
    unmatched_truth_keys: list[str],
    unmatched_pred_keys: list[str],
) -> dict[str, int]:
    summary: dict[str, int] = {
        "missing_fact": len(unmatched_truth_keys),
        "extra_fact": len(unmatched_pred_keys),
    }
    for item in match_details:
        error_type = str(item.get("error_type", "unknown"))
        summary[error_type] = summary.get(error_type, 0) + 1
    return summary
