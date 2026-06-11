#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


def _ensure_evaluation_package() -> Path:
    root = Path(__file__).resolve().parent
    return root


_ROOT = _ensure_evaluation_package()

from verify.common import SharedLLMClient, load_field_rules, load_schema_spec, write_json  # noqa: E402
from verify.config import default_verify_config_path, load_verify_settings, settings_with_overrides  # noqa: E402
from verify_eval.core import run_verify_compare_for_paper, run_verify_eval_for_paper  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run no-truth evidence quality evaluation for outputs_dataset papers.")
    parser.add_argument("--config", default=str(default_verify_config_path(_ROOT)), help="verify config path")
    parser.add_argument("--dataset-root", default=None, help="outputs_dataset root")
    parser.add_argument("--paper-ids", default=None, help="comma-separated paper ids, e.g. A0,A1")
    parser.add_argument("--field-rules-path", default=str(_ROOT / "config" / "field_rules.json"))
    parser.add_argument("--workers", type=int, default=None, help="parallel workers")
    parser.add_argument("--force", action="store_true", help="rerun even if verify_eval output exists")
    parser.add_argument("--no-llm", action="store_true", help="skip LLM calls; fields become unknown")
    parser.add_argument(
        "--compare-verify",
        action="store_true",
        help="score final/text_extraction.json and verify/text_extraction_fixed.json with the same method, then report delta",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    settings = load_verify_settings(args.config)
    settings = settings_with_overrides(
        settings,
        dataset_root=args.dataset_root,
        force=args.force or None,
        workers=args.workers,
        llm_enabled=False if args.no_llm else None,
    )
    dataset_root = Path(settings.dataset_root).expanduser().resolve()
    paper_dirs = _select_paper_dirs(dataset_root, args.paper_ids)
    schema_spec = load_schema_spec(settings.schema_path)
    field_rules = load_field_rules(args.field_rules_path, schema_spec=schema_spec)
    llm_client = SharedLLMClient(settings.llm) if settings.llm_enabled and settings.llm.api_key != "EMPTY" else None
    print(f"dataset_root: {dataset_root}", flush=True)
    print(f"papers: {len(paper_dirs)}", flush=True)
    print(f"llm: enabled={llm_client is not None}, model={settings.llm.model}", flush=True)

    results = []
    with ThreadPoolExecutor(max_workers=settings.workers) as executor:
        futures = {
            executor.submit(
                run_verify_compare_for_paper if args.compare_verify else run_verify_eval_for_paper,
                paper_dir,
                field_rules=field_rules,
                llm_client=llm_client,
                force=settings.force,
                max_evidence_chars=settings.max_evidence_chars,
                schema_spec=schema_spec,
            ): paper_dir
            for paper_dir in paper_dirs
        }
        for future in as_completed(futures):
            paper_dir = futures[future]
            try:
                result = future.result()
            except Exception as exc:
                print(f"{paper_dir.name}: failed: {exc}", flush=True)
                raise
            results.append(result)
            print(
                f"{result.paper_id}: score={result.paper_score:.2f} fields={result.field_count} "
                f"target={result.target_kind} gate_ok={result.gate_ok}",
                flush=True,
            )
    summary = _summary(results)
    write_json(summary, dataset_root / "verify_eval_summary.json")
    (dataset_root / "verify_eval_summary.md").write_text(_summary_markdown(summary), encoding="utf-8")
    print(f"summary: {dataset_root / 'verify_eval_summary.json'}", flush=True)


def _select_paper_dirs(dataset_root: Path, paper_ids: str | None) -> list[Path]:
    if paper_ids:
        selected = [item.strip() for item in paper_ids.split(",") if item.strip()]
        return [dataset_root / paper_id for paper_id in selected]
    return sorted(path for path in dataset_root.iterdir() if (path / "final" / "text_extraction.json").is_file())


def _summary(results) -> dict:
    scores = [item.paper_score for item in results]
    return {
        "paper_count": len(results),
        "avg_paper_score": sum(scores) / len(scores) if scores else 0.0,
        "gate_failed_count": sum(1 for item in results if not item.gate_ok),
        "papers": [
            {
                "paper_id": item.paper_id,
                "paper_score": item.paper_score,
                "field_count": item.field_count,
                "target_kind": item.target_kind,
                "gate_ok": item.gate_ok,
                "report_path": str(item.report_path),
            }
            for item in sorted(results, key=lambda value: value.paper_id)
        ],
    }


def _summary_markdown(summary: dict) -> str:
    lines = [
        "# Verify Eval Summary",
        "",
        f"- paper_count: {summary['paper_count']}",
        f"- avg_paper_score: {summary['avg_paper_score']:.2f}",
        f"- gate_failed_count: {summary['gate_failed_count']}",
        "",
        "| paper | score | fields | target | gate |",
        "|---|---:|---:|---|---|",
    ]
    for item in summary["papers"]:
        lines.append(
            f"| {item['paper_id']} | {item['paper_score']:.2f} | {item['field_count']} | "
            f"{item['target_kind']} | {item['gate_ok']} |"
        )
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    main()
