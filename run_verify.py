#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


def _ensure_evaluation_package() -> Path:
    root = Path(__file__).resolve().parent
    return root


_ROOT = _ensure_evaluation_package()

from verify.common import SharedLLMClient, load_schema_spec  # noqa: E402
from verify.config import default_verify_config_path, load_verify_settings, settings_with_overrides  # noqa: E402
from verify.core import run_verify_for_paper  # noqa: E402
from paper_extractor.unit_normalization import run_unit_normalization_for_paper  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run conservative evidence-based verify for outputs_dataset papers.")
    parser.add_argument("--config", default=str(default_verify_config_path(_ROOT)), help="verify config path")
    parser.add_argument("--dataset-root", default=None, help="outputs_dataset root")
    parser.add_argument("--paper-ids", default=None, help="comma-separated paper ids, e.g. A0,A1")
    parser.add_argument("--workers", type=int, default=None, help="parallel workers")
    parser.add_argument("--force", action="store_true", help="rerun even if verify output exists")
    parser.add_argument("--no-llm", action="store_true", help="skip LLM calls and only write validation/evidence/fixed copy")
    parser.add_argument("--skip-unit-normalization", action="store_true", help="verify final/text_extraction.json without creating normalized units")
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
    schema_spec = load_schema_spec(settings.schema_path)
    paper_dirs = _select_paper_dirs(dataset_root, args.paper_ids)
    llm_client = SharedLLMClient(settings.llm) if settings.llm_enabled and settings.llm.api_key != "EMPTY" else None
    print(f"dataset_root: {dataset_root}", flush=True)
    print(f"papers: {len(paper_dirs)}", flush=True)
    print(f"llm: enabled={llm_client is not None}, model={settings.llm.model}", flush=True)

    if not args.skip_unit_normalization:
        for paper_dir in paper_dirs:
            unit_result = run_unit_normalization_for_paper(paper_dir, force=settings.force)
            print(
                f"{unit_result.paper_id}: units converted={unit_result.converted_count} "
                f"ambiguous={unit_result.ambiguous_count} skipped={unit_result.skipped_count}",
                flush=True,
            )

    results = []
    with ThreadPoolExecutor(max_workers=settings.workers) as executor:
        futures = {
            executor.submit(
                run_verify_for_paper,
                paper_dir,
                llm_client=llm_client,
                force=settings.force,
                append_enabled=settings.append_record_enabled,
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
                f"{result.paper_id}: fixed={result.fixed_path} accepted={result.accepted_patch_count} "
                f"rejected={result.rejected_patch_count} errors {result.before_error_count}->{result.after_error_count}",
                flush=True,
            )
    print(f"verify complete: {len(results)} papers", flush=True)


def _select_paper_dirs(dataset_root: Path, paper_ids: str | None) -> list[Path]:
    if paper_ids:
        selected = [item.strip() for item in paper_ids.split(",") if item.strip()]
        return [dataset_root / paper_id for paper_id in selected]
    return sorted(path for path in dataset_root.iterdir() if (path / "final" / "text_extraction.json").is_file())


if __name__ == "__main__":
    main()
