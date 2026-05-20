from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from evaluation.metrics import bleu_score, precision_recall_f1, rouge_l_f1, scalar_exact_or_numeric_match
from evaluation.normalize import normalize_identifier, normalize_text


SECTION_ID_KEYS = {
    "papers": "paper_id",
    "alloys": "alloy_id",
    "processes": "process_id",
    "samples": "sample_id",
    "processing_steps": None,
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


def compare_sections(
    section_name: str,
    truth_records: list[Any],
    pred_records: list[Any],
    truth_to_canonical: dict[str, str],
    pred_to_canonical: dict[str, str],
    field_rules: dict[str, Any],
) -> dict[str, Any]:
    truth_flat = _flatten_records(section_name, truth_records, truth_to_canonical, field_rules)
    pred_flat = _flatten_records(section_name, pred_records, pred_to_canonical, field_rules)

    truth_keys = set(truth_flat)
    pred_keys = set(pred_flat)
    matched_keys = truth_keys & pred_keys

    exact_matches = 0
    text_scores: list[dict[str, float]] = []
    unmatched_truth_keys = sorted(truth_keys - pred_keys)
    unmatched_pred_keys = sorted(pred_keys - truth_keys)

    for key in matched_keys:
        truth_value = truth_flat[key]
        pred_value = pred_flat[key]
        if _value_match(key, truth_value, pred_value, field_rules):
            exact_matches += 1
        if _is_text_key(key, field_rules):
            truth_text = normalize_text(truth_value)
            pred_text = normalize_text(pred_value)
            text_scores.append(
                {
                    "bleu": bleu_score(truth_text, pred_text),
                    "rouge_l_f1": rouge_l_f1(truth_text, pred_text),
                }
            )

    prf = precision_recall_f1(
        tp=exact_matches,
        fp=max(len(pred_keys) - exact_matches, 0),
        fn=max(len(truth_keys) - exact_matches, 0),
    )
    return {
        "truth_fact_count": len(truth_keys),
        "prediction_fact_count": len(pred_keys),
        "matched_fact_slots": len(matched_keys),
        "correct_fact_count": exact_matches,
        "precision": prf["precision"],
        "recall": prf["recall"],
        "f1": prf["f1"],
        "avg_bleu": _average([item["bleu"] for item in text_scores]),
        "avg_rouge_l_f1": _average([item["rouge_l_f1"] for item in text_scores]),
        "missing_truth_fact_examples": unmatched_truth_keys[:20],
        "extra_prediction_fact_examples": unmatched_pred_keys[:20],
    }


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
        for key, value in node.items():
            next_prefix = f"{prefix}.{key}" if prefix else key
            yield from _walk(value, next_prefix)
        return
    if isinstance(node, list):
        for index, item in enumerate(node):
            next_prefix = f"{prefix}[{index}]"
            yield from _walk(item, next_prefix)
        return
    yield prefix, node


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


def _value_match(key: str, truth_value: str, pred_value: str, field_rules: dict[str, Any]) -> bool:
    tolerances = field_rules.get("numeric_tolerances", {})
    default_tolerance = tolerances.get("default", {"abs": 0.0, "rel": 0.0})
    chosen = default_tolerance
    for pattern, tolerance in tolerances.items():
        if pattern == "default":
            continue
        stripped = key.replace(".[", "[")
        if _pattern_matches(pattern, stripped):
            chosen = tolerance
            break
    return scalar_exact_or_numeric_match(
        truth_value,
        pred_value,
        abs_tol=float(chosen.get("abs", 0.0)),
        rel_tol=float(chosen.get("rel", 0.0)),
    )


def _pattern_matches(pattern: str, key: str) -> bool:
    normalized_pattern = pattern.replace("[*]", "").replace("*", "")
    normalized_key = key.replace("[0]", "").replace("[1]", "").replace("[2]", "").replace("[3]", "")
    return normalized_pattern in normalized_key


def _average(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0
