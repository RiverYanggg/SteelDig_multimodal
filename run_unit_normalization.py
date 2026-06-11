#!/usr/bin/env python3
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from paper_extractor.unit_normalization import run_unit_normalization_for_paper


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Normalize units in final/text_extraction.json files.")
    parser.add_argument("--dataset-root", default="outputs_dataset", help="outputs_dataset root")
    parser.add_argument("--paper-ids", default=None, help="comma-separated paper ids, e.g. A0,A1")
    parser.add_argument("--workers", type=int, default=1, help="parallel workers")
    parser.add_argument("--force", action="store_true", help="rerun even if normalized output exists")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    dataset_root = Path(args.dataset_root).expanduser().resolve()
    paper_dirs = _select_paper_dirs(dataset_root, args.paper_ids)
    print(f"dataset_root: {dataset_root}", flush=True)
    print(f"papers: {len(paper_dirs)}", flush=True)

    results = []
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as executor:
        futures = {
            executor.submit(run_unit_normalization_for_paper, paper_dir, force=args.force): paper_dir
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
                f"{result.paper_id}: normalized={result.normalized_path} "
                f"converted={result.converted_count} ambiguous={result.ambiguous_count} skipped={result.skipped_count}",
                flush=True,
            )
    print(f"unit normalization complete: {len(results)} papers", flush=True)


def _select_paper_dirs(dataset_root: Path, paper_ids: str | None) -> list[Path]:
    if paper_ids:
        selected = [item.strip() for item in paper_ids.split(",") if item.strip()]
        return [dataset_root / paper_id for paper_id in selected]
    return sorted(path for path in dataset_root.iterdir() if (path / "final" / "text_extraction.json").is_file())


if __name__ == "__main__":
    main()
