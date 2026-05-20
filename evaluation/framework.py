from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from evaluation.config import EvaluationSettings, load_field_rules, sanitize_settings
from evaluation.loader import SECTIONS, detect_empty_prediction, load_paper_pairs
from evaluation.matcher import (
    MatchCandidate,
    align_alloys,
    align_processes,
    align_samples,
    build_id_map,
)
from evaluation.scoring import build_sample_context, compare_sections, record_section_metrics
from evaluation.normalize import normalize_identifier


def run_evaluation(settings: EvaluationSettings) -> dict[str, Any]:
    field_rules = load_field_rules(settings.field_rules_path)
    pairs = load_paper_pairs(settings.truth_dir, settings.prediction_root)
    if settings.paper_ids:
        selected = {paper_id.strip() for paper_id in settings.paper_ids if paper_id.strip()}
        pairs = [pair for pair in pairs if pair.paper_key in selected]
    llm_bridge = None
    llm_bridge_init_error = None
    if settings.llm_bridge.enabled:
        try:
            from evaluation.llm_bridge import SampleLLMBridge

            llm_bridge = SampleLLMBridge(settings.llm_bridge)
        except Exception as exc:
            llm_bridge_init_error = str(exc)

    report: dict[str, Any] = {
        "meta": {
            "paper_count": len(pairs),
            "settings": sanitize_settings(settings),
            "llm_bridge_available": llm_bridge is not None,
            "llm_bridge_init_error": llm_bridge_init_error,
        },
        "dataset_summary": {},
        "paper_index": [],
    }
    paper_output_dir = Path(settings.per_paper_output_dir).expanduser().resolve()
    paper_output_dir.mkdir(parents=True, exist_ok=True)

    dataset_fact_sums = {section: {"truth": 0, "pred": 0, "correct": 0} for section in SECTIONS}
    structure_sums = {section: {"truth": 0, "pred": 0, "matched": 0} for section in SECTIONS}
    empty_predictions = 0

    for pair in pairs:
        truth = pair.truth
        prediction = pair.prediction or {section: [] for section in SECTIONS}
        if detect_empty_prediction(pair.prediction):
            empty_predictions += 1

        alloy_alignment = align_alloys(
            truth_alloys=truth["alloys"],
            pred_alloys=prediction["alloys"],
            settings=settings.matching,
            stopwords=field_rules.get("sample_id_stopwords", []),
        )
        truth_alloy_map, pred_alloy_map = build_id_map(alloy_alignment)

        process_alignment = align_processes(
            truth_processes=truth["processes"],
            pred_processes=prediction["processes"],
            truth_samples=truth["samples"],
            pred_samples=prediction["samples"],
            truth_alloy_map=truth_alloy_map,
            pred_alloy_map=pred_alloy_map,
            truth_steps=truth["processing_steps"],
            pred_steps=prediction["processing_steps"],
            settings=settings.matching,
            stopwords=field_rules.get("process_stopwords", []),
        )
        truth_process_map, pred_process_map = build_id_map(process_alignment)

        truth_context = build_sample_context(
            truth["samples"],
            truth["structures"],
            truth["properties"],
            truth["performance"],
            truth["interfaces"],
            truth["processing_steps"],
        )
        pred_context = build_sample_context(
            prediction["samples"],
            prediction["structures"],
            prediction["properties"],
            prediction["performance"],
            prediction["interfaces"],
            prediction["processing_steps"],
        )

        sample_alignment = align_samples(
            truth_samples=truth["samples"],
            pred_samples=prediction["samples"],
            truth_alloy_match=truth_alloy_map,
            pred_alloy_match=pred_alloy_map,
            truth_process_match=truth_process_map,
            pred_process_match=pred_process_map,
            truth_context=truth_context,
            pred_context=pred_context,
            settings=settings.matching,
            stopwords=field_rules.get("sample_id_stopwords", []),
            context_stopwords=field_rules.get("sample_context_stopwords", []),
        )

        llm_bridge_result: dict[str, Any] | None = None
        if llm_bridge and sample_alignment.llm_candidates:
            llm_bridge_result = _run_llm_bridge_batches(
                llm_bridge=llm_bridge,
                paper_key=pair.paper_key,
                truth_samples=truth["samples"],
                prediction_samples=prediction["samples"],
                truth_context=truth_context,
                pred_context=pred_context,
                sample_alignment=sample_alignment,
                batch_size=settings.llm_bridge.max_component_records,
            )

        truth_sample_map, pred_sample_map = build_id_map(sample_alignment)
        canonical_map_truth = {**truth_alloy_map, **truth_process_map, **truth_sample_map}
        canonical_map_pred = {**pred_alloy_map, **pred_process_map, **pred_sample_map}
        _inject_paper_canonical_map(canonical_map_truth, truth, pair.paper_key)
        _inject_paper_canonical_map(canonical_map_pred, prediction, pair.paper_key)

        section_reports: dict[str, Any] = {}
        section_metrics: dict[str, Any] = {}
        alignments = {
            "alloys": alloy_alignment,
            "processes": process_alignment,
            "samples": sample_alignment,
        }

        for section in SECTIONS:
            if section in alignments:
                alignment = alignments[section]
                metrics = record_section_metrics(
                    truth_count=len(truth[section]),
                    prediction_count=len(prediction[section]),
                    matched_count=len(alignment.matched_pairs),
                )
                section_reports[section] = {
                    "structure_metrics": asdict(metrics),
                    "alignment": {
                        "matched_pairs": [asdict(pair_item) for pair_item in alignment.matched_pairs],
                        "unmatched_truth_ids": alignment.unmatched_truth_ids,
                        "unmatched_prediction_ids": alignment.unmatched_prediction_ids,
                        "llm_candidates": alignment.llm_candidates,
                    },
                }
            else:
                metrics = record_section_metrics(
                    truth_count=len(truth[section]),
                    prediction_count=len(prediction[section]),
                    matched_count=min(len(truth[section]), len(prediction[section])),
                )
                section_reports[section] = {"structure_metrics": asdict(metrics)}

            comparison = compare_sections(
                section_name=section,
                truth_records=truth[section],
                pred_records=prediction[section],
                truth_to_canonical=canonical_map_truth,
                pred_to_canonical=canonical_map_pred,
                field_rules=field_rules,
            )
            section_reports[section]["fact_metrics"] = comparison
            section_metrics[section] = {
                "structure_f1": section_reports[section]["structure_metrics"]["f1"],
                "fact_f1": comparison["f1"],
            }

            structure_sums[section]["truth"] += len(truth[section])
            structure_sums[section]["pred"] += len(prediction[section])
            structure_sums[section]["matched"] += section_reports[section]["structure_metrics"]["matched_count"]
            dataset_fact_sums[section]["truth"] += comparison["truth_fact_count"]
            dataset_fact_sums[section]["pred"] += comparison["prediction_fact_count"]
            dataset_fact_sums[section]["correct"] += comparison["correct_fact_count"]

        paper_report = {
            "paper_id": pair.paper_key,
            "truth_path": pair.truth_path,
            "prediction_path": pair.prediction_path,
            "prediction_empty": detect_empty_prediction(pair.prediction),
            "section_metrics": section_metrics,
            "sections": section_reports,
        }
        if llm_bridge_result is not None:
            paper_report["llm_bridge"] = llm_bridge_result
        paper_report_path = paper_output_dir / f"{pair.paper_key}.evaluation.json"
        _write_report(paper_report, str(paper_report_path))
        report["paper_index"].append(
            {
                "paper_id": pair.paper_key,
                "report_path": str(paper_report_path),
                "prediction_empty": paper_report["prediction_empty"],
                "section_metrics": section_metrics,
                "has_llm_bridge": llm_bridge_result is not None,
            }
        )

    report["dataset_summary"] = {
        "empty_prediction_count": empty_predictions,
        "section_summary": {
            section: _aggregate_section_metrics(section, structure_sums[section], dataset_fact_sums[section])
            for section in SECTIONS
        },
    }
    _write_report(report, settings.output_path)
    return report


def _merge_llm_sample_matches(sample_alignment, matches: list[dict[str, Any]]) -> None:
    matched_truth = {pair.truth_id for pair in sample_alignment.matched_pairs}
    matched_pred = {pair.prediction_id for pair in sample_alignment.matched_pairs}

    for item in matches:
        truth_id = str(item.get("truth_sample_id", ""))
        pred_id = str(item.get("pred_sample_id", ""))
        relation = str(item.get("relation", "one_to_one"))
        confidence = float(item.get("confidence", 0.0) or 0.0)
        if not truth_id or not pred_id:
            continue
        if truth_id in matched_truth or pred_id in matched_pred:
            continue
        if relation not in {"one_to_one", "many_to_one", "one_to_many"}:
            continue
        sample_alignment.matched_pairs.append(
            MatchCandidate(
                truth_id=truth_id,
                prediction_id=pred_id,
                score=confidence,
                reason=f"llm_bridge:{relation}",
            )
        )
        matched_truth.add(truth_id)
        matched_pred.add(pred_id)

    sample_alignment.unmatched_truth_ids = [item for item in sample_alignment.unmatched_truth_ids if item not in matched_truth]
    sample_alignment.unmatched_prediction_ids = [item for item in sample_alignment.unmatched_prediction_ids if item not in matched_pred]


def _aggregate_section_metrics(section: str, structure_totals: dict[str, int], fact_totals: dict[str, int]) -> dict[str, Any]:
    structure_prf = _prf_from_totals(
        truth_count=structure_totals["truth"],
        pred_count=structure_totals["pred"],
        matched_count=structure_totals["matched"],
    )
    fact_prf = _prf_from_totals(
        truth_count=fact_totals["truth"],
        pred_count=fact_totals["pred"],
        matched_count=fact_totals["correct"],
    )
    return {
        "section": section,
        "structure": structure_prf,
        "facts": fact_prf,
    }


def _prf_from_totals(truth_count: int, pred_count: int, matched_count: int) -> dict[str, Any]:
    tp = matched_count
    fp = max(pred_count - matched_count, 0)
    fn = max(truth_count - matched_count, 0)
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if precision and recall else 0.0
    return {
        "truth_count": truth_count,
        "prediction_count": pred_count,
        "matched_count": matched_count,
        "precision": precision,
        "recall": recall,
        "f1": f1,
    }


def _write_report(report: dict[str, Any], output_path: str) -> None:
    path = Path(output_path).expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")


def _inject_paper_canonical_map(target: dict[str, str], data: dict[str, Any], paper_key: str) -> None:
    for record in data.get("papers", []):
        paper_id = record.get("paper_id")
        if paper_id:
            target[normalize_identifier(paper_id)] = paper_key


def _run_llm_bridge_batches(
    llm_bridge,
    paper_key: str,
    truth_samples: list[dict[str, Any]],
    prediction_samples: list[dict[str, Any]],
    truth_context: dict[str, dict[str, Any]],
    pred_context: dict[str, dict[str, Any]],
    sample_alignment,
    batch_size: int,
) -> dict[str, Any]:
    truth_index = {str(record.get("sample_id")): record for record in truth_samples if record.get("sample_id")}
    pred_index = {str(record.get("sample_id")): record for record in prediction_samples if record.get("sample_id")}
    batches = []
    all_matches: list[dict[str, Any]] = []
    errors: list[str] = []

    for start in range(0, len(sample_alignment.llm_candidates), batch_size):
        batch_candidates = sample_alignment.llm_candidates[start : start + batch_size]
        truth_ids = [item["truth_id"] for item in batch_candidates if item.get("truth_id") in truth_index]
        pred_ids = []
        seen_pred: set[str] = set()
        for item in batch_candidates:
            for candidate in item.get("prediction_candidates", [])[:4]:
                pred_id = candidate.get("prediction_id")
                if pred_id in pred_index and pred_id not in seen_pred:
                    seen_pred.add(pred_id)
                    pred_ids.append(pred_id)

        bridge_result = llm_bridge.bridge(
            paper_key=paper_key,
            truth_records=[truth_index[truth_id] for truth_id in truth_ids],
            prediction_records=[pred_index[pred_id] for pred_id in pred_ids],
            truth_context=truth_context,
            pred_context=pred_context,
            candidates=batch_candidates,
        )
        _merge_llm_sample_matches(sample_alignment, bridge_result.matches)
        all_matches.extend(bridge_result.matches)
        if bridge_result.error:
            errors.append(bridge_result.error)
        batches.append(
            {
                "truth_ids": truth_ids,
                "prediction_ids": pred_ids,
                "error": bridge_result.error,
                "raw_response": bridge_result.raw_response,
                "match_count": len(bridge_result.matches),
            }
        )

    return {
        "batch_count": len(batches),
        "errors": errors,
        "matches": all_matches,
        "batches": batches,
    }
