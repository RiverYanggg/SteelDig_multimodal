from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from evaluation.config import MatchingSettings
from evaluation.metrics import jaccard_similarity, token_overlap_score
from evaluation.normalize import compact_text_fragments, normalize_identifier, normalize_text, token_set


@dataclass(frozen=True)
class MatchCandidate:
    truth_id: str
    prediction_id: str
    score: float
    reason: str


@dataclass
class SectionAlignment:
    section: str
    matched_pairs: list[MatchCandidate] = field(default_factory=list)
    unmatched_truth_ids: list[str] = field(default_factory=list)
    unmatched_prediction_ids: list[str] = field(default_factory=list)
    llm_candidates: list[dict[str, Any]] = field(default_factory=list)


def align_alloys(
    truth_alloys: list[dict[str, Any]],
    pred_alloys: list[dict[str, Any]],
    settings: MatchingSettings,
    stopwords: list[str],
) -> SectionAlignment:
    return _greedy_match_records(
        section="alloys",
        truth_records=truth_alloys,
        pred_records=pred_alloys,
        truth_key="alloy_id",
        pred_key="alloy_id",
        scorer=lambda truth, pred: alloy_similarity(truth, pred, stopwords),
        threshold=settings.alloy_threshold,
        unique_margin=settings.unique_margin,
    )


def align_processes(
    truth_processes: list[dict[str, Any]],
    pred_processes: list[dict[str, Any]],
    truth_samples: list[dict[str, Any]],
    pred_samples: list[dict[str, Any]],
    truth_alloy_map: dict[str, str],
    pred_alloy_map: dict[str, str],
    truth_steps: list[dict[str, Any]],
    pred_steps: list[dict[str, Any]],
    settings: MatchingSettings,
    stopwords: list[str],
) -> SectionAlignment:
    truth_step_index = _steps_by_process(truth_steps, truth_samples)
    pred_step_index = _steps_by_process(pred_steps, pred_samples)
    return _greedy_match_records(
        section="processes",
        truth_records=truth_processes,
        pred_records=pred_processes,
        truth_key="process_id",
        pred_key="process_id",
        scorer=lambda truth, pred: process_similarity(
            truth,
            pred,
            truth_alloy_map=truth_alloy_map,
            pred_alloy_map=pred_alloy_map,
            truth_step_index=truth_step_index,
            pred_step_index=pred_step_index,
            stopwords=stopwords,
        ),
        threshold=settings.process_threshold,
        unique_margin=settings.unique_margin,
    )


def align_samples(
    truth_samples: list[dict[str, Any]],
    pred_samples: list[dict[str, Any]],
    truth_alloy_match: dict[str, str],
    pred_alloy_match: dict[str, str],
    truth_process_match: dict[str, str],
    pred_process_match: dict[str, str],
    truth_context: dict[str, dict[str, Any]],
    pred_context: dict[str, dict[str, Any]],
    settings: MatchingSettings,
    stopwords: list[str],
    context_stopwords: list[str],
) -> SectionAlignment:
    alignment = SectionAlignment(section="samples")
    scored_pairs: list[MatchCandidate] = []
    truth_ids = [_record_id(record, "sample_id") for record in truth_samples]
    pred_ids = [_record_id(record, "sample_id") for record in pred_samples]

    for truth in truth_samples:
        truth_id = _record_id(truth, "sample_id")
        if not truth_id:
            continue
        for pred in pred_samples:
            pred_id = _record_id(pred, "sample_id")
            if not pred_id:
                continue
            score, reason = sample_similarity(
                truth,
                pred,
                truth_alloy_match=truth_alloy_match,
                pred_alloy_match=pred_alloy_match,
                truth_process_match=truth_process_match,
                pred_process_match=pred_process_match,
                truth_context=truth_context.get(truth_id, {}),
                pred_context=pred_context.get(pred_id, {}),
                stopwords=stopwords,
                context_stopwords=context_stopwords,
            )
            if score >= settings.sample_soft_threshold:
                scored_pairs.append(MatchCandidate(truth_id=truth_id, prediction_id=pred_id, score=score, reason=reason))

    by_truth = _group_best(scored_pairs, key="truth")
    by_pred = _group_best(scored_pairs, key="pred")

    matched_truth: set[str] = set()
    matched_pred: set[str] = set()

    for candidate in sorted(scored_pairs, key=lambda item: item.score, reverse=True):
        if candidate.truth_id in matched_truth or candidate.prediction_id in matched_pred:
            continue
        truth_gap = _gap(by_truth.get(candidate.truth_id, []))
        pred_gap = _gap(by_pred.get(candidate.prediction_id, []))
        if candidate.score >= settings.sample_strong_threshold and truth_gap >= settings.unique_margin and pred_gap >= settings.unique_margin:
            alignment.matched_pairs.append(candidate)
            matched_truth.add(candidate.truth_id)
            matched_pred.add(candidate.prediction_id)

    unresolved_truth = [record for record in truth_samples if _record_id(record, "sample_id") not in matched_truth]
    unresolved_pred = [record for record in pred_samples if _record_id(record, "sample_id") not in matched_pred]

    for truth in unresolved_truth:
        truth_id = _record_id(truth, "sample_id")
        candidates = [candidate for candidate in by_truth.get(truth_id, []) if candidate.prediction_id not in matched_pred]
        if candidates and candidates[0].score >= settings.sample_soft_threshold:
            alignment.llm_candidates.append(
                {
                    "truth_id": truth_id,
                    "prediction_candidates": [
                        {"prediction_id": candidate.prediction_id, "score": candidate.score, "reason": candidate.reason}
                        for candidate in candidates[:6]
                    ],
                }
            )

    alignment.unmatched_truth_ids = [record_id for record_id in truth_ids if record_id not in matched_truth]
    alignment.unmatched_prediction_ids = [record_id for record_id in pred_ids if record_id not in matched_pred]
    return alignment


def alloy_similarity(truth: dict[str, Any], pred: dict[str, Any], stopwords: list[str]) -> tuple[float, str]:
    name_score = token_overlap_score(truth.get("alloy_name"), pred.get("alloy_name"))
    alias_truth = " ".join(truth.get("aliases", []))
    alias_pred = " ".join(pred.get("aliases", []))
    alias_score = token_overlap_score(alias_truth, alias_pred)
    comp_truth = _composition_signature(truth)
    comp_pred = _composition_signature(pred)
    composition_score = jaccard_similarity(comp_truth, comp_pred)
    elements_score = jaccard_similarity(truth.get("alloying_elements", []), pred.get("alloying_elements", []))
    id_score = jaccard_similarity(
        token_set(truth.get("alloy_id"), stopwords),
        token_set(pred.get("alloy_id"), stopwords),
    )
    score = 0.38 * composition_score + 0.22 * elements_score + 0.2 * name_score + 0.1 * alias_score + 0.1 * id_score
    reason = (
        f"composition={composition_score:.2f}, elements={elements_score:.2f}, "
        f"name={name_score:.2f}, alias={alias_score:.2f}, id={id_score:.2f}"
    )
    return score, reason


def process_similarity(
    truth: dict[str, Any],
    pred: dict[str, Any],
    truth_alloy_map: dict[str, str],
    pred_alloy_map: dict[str, str],
    truth_step_index: dict[str, list[dict[str, Any]]],
    pred_step_index: dict[str, list[dict[str, Any]]],
    stopwords: list[str],
) -> tuple[float, str]:
    truth_text = _process_signature_text(truth, truth_step_index)
    pred_text = _process_signature_text(pred, pred_step_index)
    description_score = token_overlap_score(truth_text, pred_text)
    truth_alloy = truth_alloy_map.get(normalize_identifier(truth.get("alloy_id")))
    pred_alloy = pred_alloy_map.get(normalize_identifier(pred.get("alloy_id")))
    alloy_score = 1.0 if truth_alloy and pred_alloy and truth_alloy == pred_alloy else 0.0
    id_score = jaccard_similarity(
        token_set(truth.get("process_id"), stopwords),
        token_set(pred.get("process_id"), stopwords),
    )
    temperature_score = _numeric_overlap_score(truth_text, pred_text)
    score = 0.50 * description_score + 0.25 * alloy_score + 0.15 * temperature_score + 0.10 * id_score
    reason = (
        f"description={description_score:.2f}, alloy={alloy_score:.2f}, "
        f"numeric={temperature_score:.2f}, id={id_score:.2f}"
    )
    return score, reason


def sample_similarity(
    truth: dict[str, Any],
    pred: dict[str, Any],
    truth_alloy_match: dict[str, str],
    pred_alloy_match: dict[str, str],
    truth_process_match: dict[str, str],
    pred_process_match: dict[str, str],
    truth_context: dict[str, Any],
    pred_context: dict[str, Any],
    stopwords: list[str],
    context_stopwords: list[str],
) -> tuple[float, str]:
    truth_alloy = truth_alloy_match.get(normalize_identifier(truth.get("alloy_id")))
    pred_alloy = pred_alloy_match.get(normalize_identifier(pred.get("alloy_id")))
    alloy_score = 1.0 if truth_alloy and pred_alloy and truth_alloy == pred_alloy else None

    truth_process = truth_process_match.get(normalize_identifier(truth.get("process_id")))
    pred_process = pred_process_match.get(normalize_identifier(pred.get("process_id")))
    process_score = 1.0 if truth_process and pred_process and truth_process == pred_process else None

    id_score = jaccard_similarity(
        token_set(truth.get("sample_id"), stopwords),
        token_set(pred.get("sample_id"), stopwords),
    )
    context_score = jaccard_similarity(
        token_set(compact_text_fragments(truth_context), context_stopwords),
        token_set(compact_text_fragments(pred_context), context_stopwords),
    )
    process_hint_score = jaccard_similarity(
        token_set(_sample_condition_signature(truth), stopwords),
        token_set(_sample_condition_signature(pred), stopwords),
    )
    score = _weighted_mean(
        [
            (alloy_score, 0.30),
            (process_score, 0.20),
            (process_hint_score, 0.25),
            (context_score, 0.15),
            (id_score, 0.10),
        ]
    )
    reason = (
        f"alloy={_fmt_score(alloy_score)}, process={_fmt_score(process_score)}, "
        f"context={context_score:.2f}, id={id_score:.2f}, process_hint={process_hint_score:.2f}"
    )
    return score, reason


def build_id_map(alignment: SectionAlignment) -> tuple[dict[str, str], dict[str, str]]:
    truth_to_canonical: dict[str, str] = {}
    pred_to_canonical: dict[str, str] = {}
    for pair in alignment.matched_pairs:
        canonical = pair.truth_id
        truth_to_canonical[normalize_identifier(pair.truth_id)] = canonical
        pred_to_canonical[normalize_identifier(pair.prediction_id)] = canonical
    return truth_to_canonical, pred_to_canonical


def _greedy_match_records(
    section: str,
    truth_records: list[dict[str, Any]],
    pred_records: list[dict[str, Any]],
    truth_key: str,
    pred_key: str,
    scorer,
    threshold: float,
    unique_margin: float,
) -> SectionAlignment:
    alignment = SectionAlignment(section=section)
    candidates: list[MatchCandidate] = []

    for truth in truth_records:
        truth_id = _record_id(truth, truth_key)
        if not truth_id:
            continue
        for pred in pred_records:
            pred_id = _record_id(pred, pred_key)
            if not pred_id:
                continue
            score, reason = scorer(truth, pred)
            if score >= threshold:
                candidates.append(MatchCandidate(truth_id=truth_id, prediction_id=pred_id, score=score, reason=reason))

    by_truth = _group_best(candidates, key="truth")
    by_pred = _group_best(candidates, key="pred")
    matched_truth: set[str] = set()
    matched_pred: set[str] = set()

    for candidate in sorted(candidates, key=lambda item: item.score, reverse=True):
        if candidate.truth_id in matched_truth or candidate.prediction_id in matched_pred:
            continue
        if _gap(by_truth.get(candidate.truth_id, [])) < unique_margin:
            continue
        if _gap(by_pred.get(candidate.prediction_id, [])) < unique_margin:
            continue
        alignment.matched_pairs.append(candidate)
        matched_truth.add(candidate.truth_id)
        matched_pred.add(candidate.prediction_id)

    truth_ids = [_record_id(record, truth_key) for record in truth_records if _record_id(record, truth_key)]
    pred_ids = [_record_id(record, pred_key) for record in pred_records if _record_id(record, pred_key)]
    alignment.unmatched_truth_ids = [record_id for record_id in truth_ids if record_id not in matched_truth]
    alignment.unmatched_prediction_ids = [record_id for record_id in pred_ids if record_id not in matched_pred]
    return alignment


def _group_best(candidates: list[MatchCandidate], key: str) -> dict[str, list[MatchCandidate]]:
    groups: dict[str, list[MatchCandidate]] = {}
    for candidate in candidates:
        bucket = candidate.truth_id if key == "truth" else candidate.prediction_id
        groups.setdefault(bucket, []).append(candidate)
    for bucket in groups:
        groups[bucket].sort(key=lambda item: item.score, reverse=True)
    return groups


def _gap(candidates: list[MatchCandidate]) -> float:
    if len(candidates) < 2:
        return 1.0
    return candidates[0].score - candidates[1].score


def _steps_by_sample(steps: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    index: dict[str, list[dict[str, Any]]] = {}
    for step in steps:
        sample_id = normalize_identifier(step.get("sample_id"))
        if sample_id:
            index.setdefault(sample_id, []).append(step)
    return index


def _steps_by_process(steps: list[dict[str, Any]], samples: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    sample_to_process = {
        normalize_identifier(sample.get("sample_id")): normalize_identifier(sample.get("process_id"))
        for sample in samples
        if sample.get("sample_id") and sample.get("process_id")
    }
    process_index: dict[str, list[dict[str, Any]]] = {}
    for step in steps:
        sample_id = normalize_identifier(step.get("sample_id"))
        process_id = sample_to_process.get(sample_id)
        if process_id:
            process_index.setdefault(process_id, []).append(step)
    return process_index


def _composition_signature(record: dict[str, Any]) -> set[str]:
    signature: set[str] = set()
    for item in record.get("nominal_composition", []):
        element = normalize_text(item.get("element"))
        weight = normalize_text(item.get("weight_percent"))
        atomic = normalize_text(item.get("atomic_percent"))
        if element:
            signature.add(f"{element}:{weight}:{atomic}")
    return signature


def _process_signature_text(process: dict[str, Any], step_index: dict[str, list[dict[str, Any]]]) -> str:
    process_id = normalize_identifier(process.get("process_id"))
    parts = [process.get("description"), process.get("processes_notes")]
    for step in step_index.get(process_id, []):
        parts.append(step.get("type"))
        parts.append(step.get("method"))
        parts.append(step.get("temperature"))
        parts.append(step.get("duration"))
        parts.append(step.get("cooling_medium"))
    return " ".join(str(part) for part in parts if part is not None)


def _numeric_overlap_score(left_text: str, right_text: str) -> float:
    left_numbers = set(_number_tokens(left_text))
    right_numbers = set(_number_tokens(right_text))
    return jaccard_similarity(left_numbers, right_numbers)


def _number_tokens(text: str) -> list[str]:
    normalized = normalize_text(text)
    return [token for token in normalized.split() if any(char.isdigit() for char in token)]


def _sample_condition_signature(record: dict[str, Any]) -> str:
    return " ".join(
        str(part)
        for part in (
            record.get("sample_id"),
            record.get("process_id"),
            record.get("alloy_id"),
        )
        if part is not None
    )


def _weighted_mean(components: list[tuple[float | None, float]]) -> float:
    total_weight = 0.0
    weighted_sum = 0.0
    for value, weight in components:
        if value is None:
            continue
        total_weight += weight
        weighted_sum += value * weight
    return weighted_sum / total_weight if total_weight else 0.0


def _fmt_score(value: float | None) -> str:
    return "na" if value is None else f"{value:.2f}"


def _record_id(record: dict[str, Any], key: str) -> str:
    value = record.get(key)
    if value is None:
        return ""
    return str(value)
