from __future__ import annotations

import json
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from evaluation.config import EvaluationSettings, load_field_rules, sanitize_settings
from evaluation.eval_log import EvaluationProgress
from evaluation.loader import PaperPair, SECTIONS, detect_empty_prediction, load_paper_pairs
from evaluation.matcher import MatchCandidate, SectionAlignment, build_id_map
from evaluation.scoring import build_sample_context, compare_sections, flatten_section_records, record_section_metrics, record_structure_metrics_for_section
from evaluation.normalize import normalize_identifier

_THREAD_LOCAL = threading.local()


@dataclass(frozen=True)
class OutputDirs:
    papers: Path
    diagnostics: Path
    canonical: Path
    field_judge: Path


@dataclass(frozen=True)
class PaperArtifactPaths:
    evaluation: Path
    diagnostics: Path
    canonical: Path
    field_judge: Path


@dataclass
class PaperProcessResult:
    paper_key: str
    skipped: bool
    empty_prediction: bool
    clean_paper_report: dict[str, Any]
    paths: PaperArtifactPaths
    section_metrics: dict[str, Any]
    bridge_alloy_matches: int = 0
    bridge_process_matches: int = 0
    bridge_sample_matches: int = 0
    bridge_error: str | None = None


def _paper_artifact_paths(paper_key: str, dirs: OutputDirs) -> PaperArtifactPaths:
    return PaperArtifactPaths(
        evaluation=dirs.papers / f"{paper_key}.evaluation.json",
        diagnostics=dirs.diagnostics / f"{paper_key}.diagnostics.json",
        canonical=dirs.canonical / f"{paper_key}.canonical.json",
        field_judge=dirs.field_judge / f"{paper_key}.field_judge.json",
    )


def _paper_results_complete(paths: PaperArtifactPaths) -> bool:
    """四件套（evaluation / diagnostics / canonical / field_judge）均存在才视为最终结果。"""
    return all(
        path.is_file()
        for path in (paths.evaluation, paths.diagnostics, paths.canonical, paths.field_judge)
    )


def _get_thread_llm_clients(settings: EvaluationSettings) -> tuple[Any | None, Any | None]:
    if not settings.llm_bridge.enabled:
        return None, None
    if getattr(_THREAD_LOCAL, "llm_ready", False):
        return _THREAD_LOCAL.llm_bridge, _THREAD_LOCAL.field_judge
    from evaluation.llm_bridge import FieldLLMJudge, SampleLLMBridge

    bridge = SampleLLMBridge(settings.llm_bridge)
    judge_prompt = str(Path(settings.llm_bridge.prompt_path).with_name("field_judge_prompt.md"))
    judge = FieldLLMJudge(settings.llm_bridge, prompt_path=judge_prompt)
    _THREAD_LOCAL.llm_bridge = bridge
    _THREAD_LOCAL.field_judge = judge
    _THREAD_LOCAL.llm_ready = True
    return bridge, judge


def _section_metric_summary(section_metrics: dict[str, Any]) -> tuple[float | None, float | None]:
    structure_f1 = [
        item.get("structure_f1")
        for item in section_metrics.values()
        if item.get("structure_f1") is not None
    ]
    fact_f1 = [
        item.get("fact_f1")
        for item in section_metrics.values()
        if item.get("fact_f1") is not None
    ]
    return (
        (sum(structure_f1) / len(structure_f1)) if structure_f1 else None,
        (sum(fact_f1) / len(fact_f1)) if fact_f1 else None,
    )


def run_evaluation(
    settings: EvaluationSettings,
    *,
    verbose: bool = True,
    use_progress_bar: bool = True,
    workers: int | None = None,
) -> dict[str, Any]:
    worker_count = max(1, workers if workers is not None else settings.workers)
    field_rules = load_field_rules(settings.field_rules_path)
    pairs = load_paper_pairs(settings.truth_dir, settings.prediction_root)
    if settings.paper_ids:
        selected = {paper_id.strip() for paper_id in settings.paper_ids if paper_id.strip()}
        pairs = [pair for pair in pairs if pair.paper_key in selected]
    progress = EvaluationProgress(total=len(pairs), quiet=not verbose, use_progress_bar=use_progress_bar)

    llm_bridge_probe = None
    field_judge_probe = None
    llm_bridge_init_error = None
    if settings.llm_bridge.enabled:
        try:
            from evaluation.llm_bridge import FieldLLMJudge, SampleLLMBridge

            llm_bridge_probe = SampleLLMBridge(settings.llm_bridge)
            field_judge_prompt_path = str(Path(settings.llm_bridge.prompt_path).with_name("field_judge_prompt.md"))
            field_judge_probe = FieldLLMJudge(settings.llm_bridge, prompt_path=field_judge_prompt_path)
        except Exception as exc:
            llm_bridge_init_error = str(exc)

    progress.info(f"共 {len(pairs)} 篇论文待处理")
    progress.info(f"输出: {Path(settings.output_path).parent}")
    progress.info(f"并行 workers={worker_count}")
    if settings.force:
        progress.info("force=true，将重新评估已有输出的论文")
    else:
        progress.info("skip：仅当 papers/diagnostics/canonical/field_judge 四件套均已存在时跳过")
    if settings.llm_bridge.enabled:
        if llm_bridge_probe:
            progress.info(f"LLM 桥接已启用 — model={settings.llm_bridge.model}")
        else:
            progress.info(f"LLM 桥接启用失败: {llm_bridge_init_error}")
    else:
        progress.info("LLM 桥接未启用（仅规则对齐）")

    report: dict[str, Any] = {
        "global_evaluation": {},
        "meta": {
            "paper_count": len(pairs),
            "truth_model": settings.truth_model or None,
            "pred_model": settings.pred_model or None,
            "comparison_label": (
                f"truth={settings.truth_model},pred={settings.pred_model}"
                if settings.truth_model and settings.pred_model
                else None
            ),
            "workers": worker_count,
            "settings": sanitize_settings(settings),
            "llm_bridge_available": llm_bridge_probe is not None,
            "field_judge_available": field_judge_probe is not None,
            "llm_bridge_init_error": llm_bridge_init_error,
        },
        "dataset_summary": {},
        "paper_index": [],
    }
    paper_output_dir = Path(settings.per_paper_output_dir).expanduser().resolve()
    paper_output_dir.mkdir(parents=True, exist_ok=True)
    output_dirs = OutputDirs(
        papers=paper_output_dir,
        diagnostics=paper_output_dir.parent / "diagnostics",
        canonical=paper_output_dir.parent / "canonical",
        field_judge=paper_output_dir.parent / "field_judge",
    )
    output_dirs.diagnostics.mkdir(parents=True, exist_ok=True)
    output_dirs.canonical.mkdir(parents=True, exist_ok=True)
    output_dirs.field_judge.mkdir(parents=True, exist_ok=True)

    dataset_fact_sums = {section: {"truth": 0.0, "pred": 0.0, "correct": 0.0} for section in SECTIONS}
    structure_sums = {section: {"truth": 0, "pred": 0, "matched": 0} for section in SECTIONS}
    dataset_error_summary: dict[str, dict[str, int]] = {section: {} for section in SECTIONS}
    paper_macro_metrics: list[dict[str, Any]] = []

    def _apply_result(result: PaperProcessResult) -> None:
        if result.empty_prediction:
            progress.paper_empty_prediction(result.paper_key, skipped=result.skipped)
        if result.skipped:
            progress.paper_skip(result.paper_key)
        else:
            if settings.llm_bridge.enabled:
                progress.paper_llm_bridge(
                    result.paper_key,
                    alloy_matches=result.bridge_alloy_matches,
                    process_matches=result.bridge_process_matches,
                    sample_matches=result.bridge_sample_matches,
                    error=result.bridge_error,
                )
            structure_f1, fact_f1 = _section_metric_summary(result.section_metrics)
            progress.paper_done(
                result.paper_key,
                structure_f1=structure_f1,
                fact_f1=fact_f1,
                prediction_empty=result.empty_prediction,
            )
        _accumulate_paper_report(
            report=report,
            paper_report=result.clean_paper_report,
            paper_report_path=result.paths.evaluation,
            paper_diagnostics_path=result.paths.diagnostics,
            paper_canonical_path=result.paths.canonical,
            paper_judge_path=result.paths.field_judge,
            structure_sums=structure_sums,
            dataset_fact_sums=dataset_fact_sums,
            dataset_error_summary=dataset_error_summary,
            paper_macro_metrics=paper_macro_metrics,
            skipped=result.skipped,
        )

    with ThreadPoolExecutor(max_workers=worker_count) as executor:
        futures = {
            executor.submit(_process_paper, pair, settings, field_rules, output_dirs): pair.paper_key
            for pair in pairs
        }
        for future in as_completed(futures):
            paper_key = futures[future]
            try:
                result = future.result()
            except Exception as exc:
                progress.info(f"{paper_key}: 失败 — {exc}")
                raise
            _apply_result(result)

    report["paper_index"].sort(key=lambda item: str(item.get("paper_id", "")))
    _refresh_dataset_report(
        report,
        structure_sums,
        dataset_fact_sums,
        dataset_error_summary,
        paper_macro_metrics,
        settings.output_path,
    )
    progress.finish("评估完成")
    progress.info(EvaluationProgress.format_global_summary(report))
    progress.info(f"总报告: {settings.output_path}")
    return report


def _process_paper(
    pair: PaperPair,
    settings: EvaluationSettings,
    field_rules: dict[str, Any],
    output_dirs: OutputDirs,
) -> PaperProcessResult:
    paths = _paper_artifact_paths(pair.paper_key, output_dirs)
    if _paper_results_complete(paths) and not settings.force:
        existing_report = _read_report(paths.evaluation)
        return PaperProcessResult(
            paper_key=pair.paper_key,
            skipped=True,
            empty_prediction=bool(existing_report.get("prediction_empty", False)),
            clean_paper_report=existing_report,
            paths=paths,
            section_metrics=existing_report.get("section_metrics", {}),
        )
    return _evaluate_paper_fresh(pair, settings, field_rules, paths)


def _evaluate_paper_fresh(
    pair: PaperPair,
    settings: EvaluationSettings,
    field_rules: dict[str, Any],
    paths: PaperArtifactPaths,
) -> PaperProcessResult:
    llm_bridge, field_judge = _get_thread_llm_clients(settings)
    truth = pair.truth
    prediction = pair.prediction or {section: [] for section in SECTIONS}
    empty_prediction = detect_empty_prediction(pair.prediction)

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

    llm_bridge_result: dict[str, Any] | None = None
    bridge_alloy_matches = 0
    bridge_process_matches = 0
    bridge_sample_matches = 0
    bridge_error: str | None = None
    if llm_bridge:
        bridge_result = llm_bridge.align(
            paper_key=pair.paper_key,
            truth_alloys=truth["alloys"],
            prediction_alloys=prediction["alloys"],
            truth_processes=truth["processes"],
            prediction_processes=prediction["processes"],
            truth_samples=truth["samples"],
            prediction_samples=prediction["samples"],
            truth_context=truth_context,
            pred_context=pred_context,
        )
        alloy_alignment, process_alignment, sample_alignment = _build_llm_alignments(
            truth=truth,
            prediction=prediction,
            bridge_result=bridge_result,
        )
        bridge_alloy_matches = len(bridge_result.alloy_matches)
        bridge_process_matches = len(bridge_result.process_matches)
        bridge_sample_matches = len(bridge_result.matches)
        bridge_error = bridge_result.error
        llm_bridge_result = {
            "error": bridge_result.error,
            "raw_response": bridge_result.raw_response,
            "alloy_matches": bridge_result.alloy_matches,
            "process_matches": bridge_result.process_matches,
            "matches": bridge_result.matches,
        }
    else:
        alloy_alignment = _empty_alignment("alloys", truth["alloys"], prediction["alloys"], "alloy_id")
        process_alignment = _empty_alignment("processes", truth["processes"], prediction["processes"], "process_id")
        sample_alignment = _empty_alignment("samples", truth["samples"], prediction["samples"], "sample_id")

    truth_alloy_map, pred_alloy_map = build_id_map(alloy_alignment)
    truth_process_map, pred_process_map = build_id_map(process_alignment)
    truth_sample_map, pred_sample_map = build_id_map(sample_alignment)

    canonical_map_truth = {**truth_alloy_map, **truth_process_map, **truth_sample_map}
    canonical_map_pred = {**pred_alloy_map, **pred_process_map, **pred_sample_map}
    _inject_identity_canonical_map(canonical_map_truth, truth)
    _inject_identity_canonical_map(canonical_map_pred, prediction)
    _inject_paper_canonical_map(canonical_map_truth, truth, pair.paper_key)
    _inject_paper_canonical_map(canonical_map_pred, prediction, pair.paper_key)
    canonical_payload = _build_canonical_payload(
        paper_key=pair.paper_key,
        truth=truth,
        prediction=prediction,
        truth_canonical_map=canonical_map_truth,
        pred_canonical_map=canonical_map_pred,
        llm_bridge_result=llm_bridge_result,
        field_rules=field_rules,
    )

    section_reports: dict[str, Any] = {}
    section_metrics: dict[str, Any] = {}
    field_judge_log: dict[str, Any] = {"paper_id": pair.paper_key, "sections": {}}
    alignments = {
        "alloys": alloy_alignment,
        "processes": process_alignment,
        "samples": sample_alignment,
    }

    for section in SECTIONS:
        if section in alignments:
            alignment = alignments[section]
            raw_metrics = record_section_metrics(
                truth_count=len(truth[section]),
                prediction_count=len(prediction[section]),
                matched_count=len(alignment.matched_pairs),
            )
            metrics = asdict(raw_metrics)
            section_reports[section] = {
                "structure_metrics": metrics,
                "structure_metrics_raw_pair_count": metrics,
                "alignment": {
                    "matched_pairs": [asdict(pair_item) for pair_item in alignment.matched_pairs],
                    "unmatched_truth_ids": alignment.unmatched_truth_ids,
                    "unmatched_prediction_ids": alignment.unmatched_prediction_ids,
                    "llm_candidates": alignment.llm_candidates,
                },
            }
        else:
            metrics = record_structure_metrics_for_section(
                section_name=section,
                truth_records=truth[section],
                pred_records=prediction[section],
                truth_to_canonical=canonical_map_truth,
                pred_to_canonical=canonical_map_pred,
            )
            section_reports[section] = {"structure_metrics": metrics}

        comparison = compare_sections(
            section_name=section,
            truth_records=truth[section],
            pred_records=prediction[section],
            truth_to_canonical=canonical_map_truth,
            pred_to_canonical=canonical_map_pred,
            field_rules=field_rules,
            paper_key=pair.paper_key,
            field_judge=field_judge,
        )
        field_judge_log["sections"][section] = _section_judge_log(comparison)
        section_reports[section]["fact_metrics"] = comparison
        fact_triplet = _metric_triplet(comparison.get("hard", comparison)) if comparison["truth_fact_count"] or comparison["prediction_fact_count"] else None
        section_metrics[section] = {
            "structure_f1": section_reports[section]["structure_metrics"]["f1"],
            "fact_f1": comparison["f1"] if fact_triplet is not None else None,
        }

    paper_report = {
        "paper_id": pair.paper_key,
        "truth_path": pair.truth_path,
        "prediction_path": pair.prediction_path,
        "prediction_empty": empty_prediction,
        "section_metrics": section_metrics,
        "sections": section_reports,
    }
    if llm_bridge_result is not None:
        paper_report["llm_bridge"] = llm_bridge_result
    paper_diagnostics = _build_paper_diagnostics(paper_report)
    clean_paper_report = _build_clean_paper_report(paper_report)
    _write_report(canonical_payload, str(paths.canonical))
    _write_report(field_judge_log, str(paths.field_judge))
    _write_report(clean_paper_report, str(paths.evaluation))
    _write_report(paper_diagnostics, str(paths.diagnostics))

    return PaperProcessResult(
        paper_key=pair.paper_key,
        skipped=False,
        empty_prediction=empty_prediction,
        clean_paper_report=clean_paper_report,
        paths=paths,
        section_metrics=section_metrics,
        bridge_alloy_matches=bridge_alloy_matches,
        bridge_process_matches=bridge_process_matches,
        bridge_sample_matches=bridge_sample_matches,
        bridge_error=bridge_error,
    )


def _build_llm_alignments(truth: dict[str, Any], prediction: dict[str, Any], bridge_result) -> tuple[SectionAlignment, SectionAlignment, SectionAlignment]:
    alloy_alignment = _alignment_from_llm_matches(
        section="alloys",
        truth_records=truth["alloys"],
        prediction_records=prediction["alloys"],
        truth_key="alloy_id",
        pred_key="pred_alloy_id",
        truth_match_key="truth_alloy_id",
        matches=bridge_result.alloy_matches,
    )
    process_alignment = _alignment_from_llm_matches(
        section="processes",
        truth_records=truth["processes"],
        prediction_records=prediction["processes"],
        truth_key="process_id",
        pred_key="pred_process_id",
        truth_match_key="truth_process_id",
        matches=bridge_result.process_matches,
    )
    sample_alignment = _alignment_from_llm_matches(
        section="samples",
        truth_records=truth["samples"],
        prediction_records=prediction["samples"],
        truth_key="sample_id",
        pred_key="pred_sample_id",
        truth_match_key="truth_sample_id",
        matches=bridge_result.matches,
    )
    return alloy_alignment, process_alignment, sample_alignment


def _alignment_from_llm_matches(
    section: str,
    truth_records: list[dict[str, Any]],
    prediction_records: list[dict[str, Any]],
    truth_key: str,
    pred_key: str,
    truth_match_key: str,
    matches: list[dict[str, Any]],
) -> SectionAlignment:
    truth_ids = _record_ids(truth_records, truth_key)
    pred_ids = _record_ids(prediction_records, truth_key)
    valid_truth = set(truth_ids)
    valid_pred = set(pred_ids)
    alignment = SectionAlignment(section=section)
    used_truth: set[str] = set()
    used_pred: set[str] = set()
    matched_truth: set[str] = set()
    matched_pred: set[str] = set()

    for item in matches:
        truth_id = str(item.get(truth_match_key, ""))
        pred_id = str(item.get(pred_key, ""))
        relation = str(item.get("relation", "same"))
        confidence = _safe_confidence(item.get("confidence"))
        if not truth_id or not pred_id:
            continue
        if truth_id not in valid_truth or pred_id not in valid_pred:
            continue
        if relation in {"same", "one_to_one"} and (truth_id in used_truth or pred_id in used_pred):
            continue
        if relation == "many_to_one" and pred_id in used_pred:
            continue
        if relation == "one_to_many" and truth_id in used_truth:
            continue
        alignment.matched_pairs.append(
            MatchCandidate(
                truth_id=truth_id,
                prediction_id=pred_id,
                score=confidence,
                reason=f"llm_alignment:{relation}:{item.get('reason') or item.get('evidence') or ''}",
            )
        )
        matched_truth.add(truth_id)
        matched_pred.add(pred_id)
        if relation != "many_to_one":
            used_truth.add(truth_id)
        if relation != "one_to_many":
            used_pred.add(pred_id)

    alignment.unmatched_truth_ids = [record_id for record_id in truth_ids if record_id not in matched_truth]
    alignment.unmatched_prediction_ids = [record_id for record_id in pred_ids if record_id not in matched_pred]
    return alignment


def _empty_alignment(section: str, truth_records: list[dict[str, Any]], prediction_records: list[dict[str, Any]], id_key: str) -> SectionAlignment:
    return SectionAlignment(
        section=section,
        unmatched_truth_ids=_record_ids(truth_records, id_key),
        unmatched_prediction_ids=_record_ids(prediction_records, id_key),
    )


def _record_ids(records: list[dict[str, Any]], id_key: str) -> list[str]:
    return [str(record.get(id_key)) for record in records if record.get(id_key)]


def _safe_confidence(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def _aggregate_section_metrics(section: str, structure_totals: dict[str, int], fact_totals: dict[str, float], error_summary: dict[str, int]) -> dict[str, Any]:
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
        "facts": {
            "precision": fact_prf["precision"],
            "recall": fact_prf["recall"],
            "f1": fact_prf["f1"],
            "truth_count": fact_prf["truth_count"],
            "prediction_count": fact_prf["prediction_count"],
            "matched_count": fact_prf["matched_count"],
            "error_summary": error_summary,
        },
    }


def _accumulate_paper_report(
    report: dict[str, Any],
    paper_report: dict[str, Any],
    paper_report_path: Path,
    paper_diagnostics_path: Path,
    paper_canonical_path: Path,
    paper_judge_path: Path,
    structure_sums: dict[str, dict[str, int]],
    dataset_fact_sums: dict[str, dict[str, float]],
    dataset_error_summary: dict[str, dict[str, int]],
    paper_macro_metrics: list[dict[str, Any]],
    skipped: bool,
) -> None:
    section_metrics = paper_report.get("section_metrics", {})
    for section in SECTIONS:
        clean_section = section_metrics.get(section, {})
        counts = clean_section.get("counts", {})
        if counts:
            structure_sums[section]["truth"] += int(counts.get("truth_records", 0) or 0)
            structure_sums[section]["pred"] += int(counts.get("prediction_records", 0) or 0)
            structure_sums[section]["matched"] += int(counts.get("matched_records", 0) or 0)
            dataset_fact_sums[section]["truth"] += float(counts.get("truth_facts", 0.0) or 0.0)
            dataset_fact_sums[section]["pred"] += float(counts.get("prediction_facts", 0.0) or 0.0)
            dataset_fact_sums[section]["correct"] += float(counts.get("correct_facts", 0.0) or 0.0)
            continue

        section_report = paper_report.get("sections", {}).get(section, {})
        structure_metrics = section_report.get("structure_metrics", {})
        fact_metrics = section_report.get("fact_metrics", {})
        if structure_metrics or fact_metrics:
            structure_sums[section]["truth"] += int(structure_metrics.get("truth_count", 0) or 0)
            structure_sums[section]["pred"] += int(structure_metrics.get("prediction_count", 0) or 0)
            structure_sums[section]["matched"] += int(structure_metrics.get("matched_count", 0) or 0)
            dataset_fact_sums[section]["truth"] += float(fact_metrics.get("truth_fact_count", 0.0) or 0.0)
            dataset_fact_sums[section]["pred"] += float(fact_metrics.get("prediction_fact_count", 0.0) or 0.0)
            dataset_fact_sums[section]["correct"] += float(fact_metrics.get("correct_fact_count", 0.0) or 0.0)
            _merge_error_summary(dataset_error_summary[section], fact_metrics.get("error_summary", {}))

    paper_macro_metrics.append(_paper_macro_metrics(str(paper_report.get("paper_id", "")), section_metrics))
    report["paper_index"].append(
        {
            "paper_id": paper_report.get("paper_id"),
            "report_path": str(paper_report_path),
            "diagnostics_path": str(paper_diagnostics_path),
            "canonical_path": str(paper_canonical_path),
            "field_judge_path": str(paper_judge_path),
            "prediction_empty": paper_report.get("prediction_empty", False),
            "section_metrics": section_metrics,
            "has_llm_bridge": bool(paper_report.get("llm_alignment", {}).get("available") or "llm_bridge" in paper_report),
            "skipped_existing": skipped,
        }
    )


def _refresh_dataset_report(
    report: dict[str, Any],
    structure_sums: dict[str, dict[str, int]],
    dataset_fact_sums: dict[str, dict[str, float]],
    dataset_error_summary: dict[str, dict[str, int]],
    paper_macro_metrics: list[dict[str, Any]],
    output_path: str,
) -> None:
    empty_prediction_paper_ids = sorted(
        str(item.get("paper_id", ""))
        for item in report.get("paper_index", [])
        if item.get("prediction_empty") and str(item.get("paper_id", "")).strip()
    )
    report["dataset_summary"] = {
        "empty_prediction_count": len(empty_prediction_paper_ids),
        "empty_prediction_paper_ids": empty_prediction_paper_ids,
        "processed_paper_count": len(report["paper_index"]),
        "section_summary": {
            section: _aggregate_section_metrics(section, structure_sums[section], dataset_fact_sums[section], dataset_error_summary[section])
            for section in SECTIONS
        },
        "macro_summary": _aggregate_macro_metrics(paper_macro_metrics),
    }
    report["global_evaluation"] = _global_metrics(structure_sums, dataset_fact_sums)
    _write_report(report, output_path)


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


def _global_metrics(
    structure_sums: dict[str, dict[str, int]],
    dataset_fact_sums: dict[str, dict[str, float]],
) -> dict[str, dict[str, float]]:
    structure_truth = sum(int(item.get("truth", 0) or 0) for item in structure_sums.values())
    structure_prediction = sum(int(item.get("pred", 0) or 0) for item in structure_sums.values())
    structure_matched = sum(int(item.get("matched", 0) or 0) for item in structure_sums.values())
    structure_metrics = _prf_from_totals(
        truth_count=structure_truth,
        pred_count=structure_prediction,
        matched_count=structure_matched,
    )
    return {
        "structure": _metric_triplet(structure_metrics),
        "facts": _global_fact_metrics(dataset_fact_sums),
    }


def _global_fact_metrics(dataset_fact_sums: dict[str, dict[str, float]]) -> dict[str, float]:
    truth_count = sum(float(item.get("truth", 0.0) or 0.0) for item in dataset_fact_sums.values())
    prediction_count = sum(float(item.get("pred", 0.0) or 0.0) for item in dataset_fact_sums.values())
    matched_count = sum(float(item.get("correct", 0.0) or 0.0) for item in dataset_fact_sums.values())
    metrics = _prf_from_totals(
        truth_count=int(truth_count),
        pred_count=int(prediction_count),
        matched_count=int(matched_count),
    )
    return {
        "precision": metrics["precision"],
        "recall": metrics["recall"],
        "f1": metrics["f1"],
    }


def _merge_error_summary(target: dict[str, int], source: dict[str, int]) -> None:
    for key, value in source.items():
        target[key] = target.get(key, 0) + int(value)


def _build_paper_diagnostics(paper_report: dict[str, Any]) -> dict[str, Any]:
    diagnostics = {
        "paper_id": paper_report["paper_id"],
        "truth_path": paper_report["truth_path"],
        "prediction_path": paper_report["prediction_path"],
        "prediction_empty": paper_report["prediction_empty"],
        "section_diagnostics": {},
    }
    for section, section_report in paper_report.get("sections", {}).items():
        fact_metrics = section_report.get("fact_metrics", {})
        diagnostics["section_diagnostics"][section] = {
            "structure_metrics": section_report.get("structure_metrics", {}),
            "error_summary": fact_metrics.get("error_summary", {}),
            "missing_truth_fact_examples": fact_metrics.get("missing_truth_fact_examples", []),
            "extra_prediction_fact_examples": fact_metrics.get("extra_prediction_fact_examples", []),
            "mismatched_fact_examples": fact_metrics.get("mismatched_fact_examples", []),
            "llm_judge_candidate_count": fact_metrics.get("llm_judge_candidate_count", 0),
            "llm_judge_candidates": fact_metrics.get("llm_judge_candidates", []),
            "match_method_summary": fact_metrics.get("match_method_summary", {}),
        }
    return diagnostics


def _build_clean_paper_report(paper_report: dict[str, Any]) -> dict[str, Any]:
    section_scores = {}
    for section, section_report in paper_report.get("sections", {}).items():
        structure = section_report.get("structure_metrics", {})
        facts = section_report.get("fact_metrics", {})
        section_scores[section] = {
            "structure": _metric_triplet(structure),
            "facts": _metric_triplet(facts.get("hard", facts)) if facts.get("truth_fact_count", 0) or facts.get("prediction_fact_count", 0) else None,
            "counts": {
                "truth_records": structure.get("truth_count", 0),
                "prediction_records": structure.get("prediction_count", 0),
                "matched_records": structure.get("matched_count", 0),
                "truth_facts": facts.get("truth_fact_count", 0),
                "prediction_facts": facts.get("prediction_fact_count", 0),
                "matched_fact_slots": facts.get("matched_fact_slots", 0),
                "correct_facts": facts.get("correct_fact_count", 0),
            },
        }
    return {
        "paper_id": paper_report["paper_id"],
        "truth_path": paper_report["truth_path"],
        "prediction_path": paper_report["prediction_path"],
        "prediction_empty": paper_report["prediction_empty"],
        "average_metrics": _clean_average_metrics(section_scores),
        "section_metrics": section_scores,
        "llm_alignment": _clean_llm_alignment_summary(paper_report.get("llm_bridge")),
    }


def _build_canonical_payload(
    paper_key: str,
    truth: dict[str, Any],
    prediction: dict[str, Any],
    truth_canonical_map: dict[str, str],
    pred_canonical_map: dict[str, str],
    llm_bridge_result: dict[str, Any] | None,
    field_rules: dict[str, Any],
) -> dict[str, Any]:
    return {
        "paper_id": paper_key,
        "canonical_maps": {
            "truth": truth_canonical_map,
            "prediction": pred_canonical_map,
        },
        "alignment": {
            "alloy_matches": (llm_bridge_result or {}).get("alloy_matches", []),
            "process_matches": (llm_bridge_result or {}).get("process_matches", []),
            "sample_matches": (llm_bridge_result or {}).get("matches", []),
            "error": (llm_bridge_result or {}).get("error"),
        },
        "flattened_sections": {
            section: {
                "truth": flatten_section_records(section, truth.get(section, []), truth_canonical_map, field_rules),
                "prediction": flatten_section_records(section, prediction.get(section, []), pred_canonical_map, field_rules),
            }
            for section in SECTIONS
        },
    }


def _section_judge_log(comparison: dict[str, Any]) -> dict[str, Any]:
    result = comparison.get("llm_judge_result")
    return {
        "candidate_count": comparison.get("llm_judge_candidate_count", 0),
        "result_count": len((result or {}).get("decisions", {})) if isinstance(result, dict) else 0,
        "error": (result or {}).get("error") if isinstance(result, dict) else None,
        "raw_response": (result or {}).get("raw_response") if isinstance(result, dict) else None,
        "decisions": (result or {}).get("decisions", {}) if isinstance(result, dict) else {},
        "input_candidates": (result or {}).get("input_candidates", []) if isinstance(result, dict) else [],
        "candidates": comparison.get("llm_judge_candidates", []),
    }


def _metric_triplet(payload: dict[str, Any]) -> dict[str, float]:
    return {
        "precision": float(payload.get("precision", 0.0) or 0.0),
        "recall": float(payload.get("recall", 0.0) or 0.0),
        "f1": float(payload.get("f1", 0.0) or 0.0),
    }


def _clean_average_metrics(section_scores: dict[str, Any]) -> dict[str, Any]:
    sections = list(section_scores.values())
    return {
        "structure": _average_triplets([item["structure"] for item in sections]),
        "facts": _average_triplets([item["facts"] for item in sections if item["facts"] is not None]),
    }


def _average_triplets(items: list[dict[str, float]]) -> dict[str, float]:
    if not items:
        return {"precision": 0.0, "recall": 0.0, "f1": 0.0}
    return {
        "precision": sum(item["precision"] for item in items) / len(items),
        "recall": sum(item["recall"] for item in items) / len(items),
        "f1": sum(item["f1"] for item in items) / len(items),
    }


def _clean_llm_alignment_summary(llm_bridge_result: dict[str, Any] | None) -> dict[str, Any]:
    if not llm_bridge_result:
        return {"available": False}
    return {
        "available": True,
        "error": llm_bridge_result.get("error"),
        "alloy_match_count": len(llm_bridge_result.get("alloy_matches", [])),
        "process_match_count": len(llm_bridge_result.get("process_matches", [])),
        "sample_match_count": len(llm_bridge_result.get("matches", [])),
    }


def _paper_macro_metrics(paper_id: str, section_metrics: dict[str, Any]) -> dict[str, Any]:
    values = list(section_metrics.values())
    return {
        "paper_id": paper_id,
        "structure_f1": _avg_nested_f1(values, "structure", fallback_key="structure_f1"),
        "fact_f1": _avg_nested_f1(values, "facts", fallback_key="fact_f1"),
    }


def _aggregate_macro_metrics(paper_metrics: list[dict[str, Any]]) -> dict[str, float]:
    return {
        "paper_count": len(paper_metrics),
        "structure_f1": _avg_metric(paper_metrics, "structure_f1"),
        "fact_f1": _avg_metric(paper_metrics, "fact_f1"),
    }


def _avg_metric(items: list[dict[str, Any]], key: str) -> float:
    values = [float(item.get(key, 0.0) or 0.0) for item in items]
    return sum(values) / len(values) if values else 0.0


def _avg_nested_f1(items: list[dict[str, Any]], first: str, second: str | None = None, fallback_key: str | None = None) -> float:
    values = []
    for item in items:
        if fallback_key and fallback_key in item:
            value = item.get(fallback_key)
            if value is not None:
                values.append(float(value or 0.0))
            continue
        payload = item.get(first, {})
        if payload is None:
            continue
        if second:
            payload = payload.get(second, {}) if isinstance(payload, dict) else {}
        values.append(float(payload.get("f1", 0.0) or 0.0) if isinstance(payload, dict) else 0.0)
    return sum(values) / len(values) if values else 0.0


def _write_report(report: dict[str, Any], output_path: str) -> None:
    path = Path(output_path).expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")


def _read_report(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _inject_paper_canonical_map(target: dict[str, str], data: dict[str, Any], paper_key: str) -> None:
    for record in data.get("papers", []):
        paper_id = record.get("paper_id")
        if paper_id:
            target[normalize_identifier(paper_id)] = paper_key


def _inject_identity_canonical_map(target: dict[str, str], data: dict[str, Any]) -> None:
    for section, id_key in {"alloys": "alloy_id", "processes": "process_id", "samples": "sample_id"}.items():
        for record in data.get(section, []):
            record_id = record.get(id_key)
            if record_id:
                target.setdefault(normalize_identifier(record_id), str(record_id))
