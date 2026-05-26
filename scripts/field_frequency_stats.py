#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Count non-empty field frequencies in text_extraction.json files."
    )
    parser.add_argument(
        "--dataset-root",
        type=Path,
        default=Path("outputs_dataset"),
        help="Root directory containing per-paper output folders.",
    )
    parser.add_argument(
        "--schema",
        type=Path,
        default=Path("prompt/json_schema.json"),
        help="JSON schema-like template used to enumerate standard fields.",
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        default=Path("outputs_dataset/field_frequency_summary.json"),
        help="Path to write the unsorted frequency summary JSON.",
    )
    parser.add_argument(
        "--output-csv",
        type=Path,
        default=Path("outputs_dataset/field_frequency_summary.csv"),
        help="Path to write the unsorted frequency summary CSV.",
    )
    return parser.parse_args()


def is_non_empty(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return value.strip() != ""
    if isinstance(value, list):
        return any(is_non_empty(item) for item in value)
    if isinstance(value, dict):
        return any(is_non_empty(item) for item in value.values())
    return True


def schema_paths(node: Any, prefix: str = "") -> set[str]:
    paths: set[str] = set()
    if isinstance(node, dict):
        for key, value in node.items():
            path = f"{prefix}.{key}" if prefix else key
            paths.add(path)
            paths.update(schema_paths(value, path))
    elif isinstance(node, list) and node:
        item_prefix = f"{prefix}[]"
        paths.update(schema_paths(node[0], item_prefix))
    return paths


def count_fields(
    node: Any,
    prefix: str,
    occurrence_counts: Counter[str],
    observed_paths: set[str],
    paper_nonempty_paths: set[str],
) -> None:
    if isinstance(node, dict):
        for key, value in node.items():
            path = f"{prefix}.{key}" if prefix else key
            observed_paths.add(path)
            if is_non_empty(value):
                occurrence_counts[path] += 1
                paper_nonempty_paths.add(path)
            count_fields(value, path, occurrence_counts, observed_paths, paper_nonempty_paths)
    elif isinstance(node, list):
        if prefix:
            observed_paths.add(prefix)
            if is_non_empty(node):
                occurrence_counts[prefix] += 1
                paper_nonempty_paths.add(prefix)
        for item in node:
            item_prefix = f"{prefix}[]" if prefix else "[]"
            count_fields(item, item_prefix, occurrence_counts, observed_paths, paper_nonempty_paths)


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main() -> int:
    args = parse_args()
    dataset_root = args.dataset_root.resolve()
    schema_path = args.schema.resolve()
    output_json = args.output_json.resolve()
    output_csv = args.output_csv.resolve()

    extraction_files = sorted(dataset_root.glob("*/final/text_extraction.json"))
    if not extraction_files:
        raise SystemExit(f"No text_extraction.json files found under {dataset_root}")

    schema = load_json(schema_path)
    standard_paths = schema_paths(schema)

    occurrence_counts: Counter[str] = Counter()
    paper_counts: Counter[str] = Counter()
    observed_paths: set[str] = set()
    for path in extraction_files:
        paper_nonempty_paths: set[str] = set()
        try:
            payload = load_json(path)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"Failed to parse {path}: {exc}") from exc
        count_fields(payload, "", occurrence_counts, observed_paths, paper_nonempty_paths)
        for field_path in paper_nonempty_paths:
            paper_counts[field_path] += 1

    all_paths = sorted(standard_paths | observed_paths)
    rows = []
    for field_path in all_paths:
        rows.append(
            {
                "field_path": field_path,
                "occurrence_count": occurrence_counts.get(field_path, 0),
                "paper_count": paper_counts.get(field_path, 0),
                "in_schema": field_path in standard_paths,
                "observed_in_results": field_path in observed_paths,
            }
        )

    rows.sort(key=lambda row: (-row["paper_count"], -row["occurrence_count"], row["field_path"]))

    summary = {
        "dataset_root": str(dataset_root),
        "schema_path": str(schema_path),
        "files_scanned": len(extraction_files),
        "count_rule": (
            "Two metrics are reported for each field when its value is non-empty. "
            "occurrence_count increments every time a non-empty field instance appears in the "
            "dataset. paper_count increments once per paper if that paper contains at least one "
            "non-empty instance of the field. null, empty string, empty list, and empty object "
            "are not counted. Arrays and objects are counted at their own field path when they "
            "contain at least one non-empty descendant."
        ),
        "schema_field_count": len(standard_paths),
        "observed_field_count": len(observed_paths),
        "extra_observed_fields_not_in_schema": sorted(observed_paths - standard_paths),
        "field_frequencies": rows,
    }

    output_json.parent.mkdir(parents=True, exist_ok=True)
    with output_json.open("w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    with output_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "field_path",
                "paper_count",
                "occurrence_count",
                "in_schema",
                "observed_in_results",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    paper_sorted_rows = sorted(
        rows,
        key=lambda row: (-row["paper_count"], -row["occurrence_count"], row["field_path"]),
    )
    occurrence_sorted_rows = sorted(
        rows,
        key=lambda row: (-row["occurrence_count"], -row["paper_count"], row["field_path"]),
    )

    paper_sorted_json = output_json.with_name("field_frequency_by_paper_count.json")
    paper_sorted_csv = output_csv.with_name("field_frequency_by_paper_count.csv")
    occurrence_sorted_json = output_json.with_name("field_frequency_by_occurrence_count.json")
    occurrence_sorted_csv = output_csv.with_name("field_frequency_by_occurrence_count.csv")

    paper_payload = dict(summary)
    paper_payload["sort_order"] = "paper_count desc, occurrence_count desc, field_path asc"
    paper_payload["field_frequencies"] = paper_sorted_rows
    with paper_sorted_json.open("w", encoding="utf-8") as f:
        json.dump(paper_payload, f, ensure_ascii=False, indent=2)

    with paper_sorted_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "field_path",
                "paper_count",
                "occurrence_count",
                "in_schema",
                "observed_in_results",
            ],
        )
        writer.writeheader()
        writer.writerows(paper_sorted_rows)

    occurrence_payload = dict(summary)
    occurrence_payload["sort_order"] = "occurrence_count desc, paper_count desc, field_path asc"
    occurrence_payload["field_frequencies"] = occurrence_sorted_rows
    with occurrence_sorted_json.open("w", encoding="utf-8") as f:
        json.dump(occurrence_payload, f, ensure_ascii=False, indent=2)

    with occurrence_sorted_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "field_path",
                "paper_count",
                "occurrence_count",
                "in_schema",
                "observed_in_results",
            ],
        )
        writer.writeheader()
        writer.writerows(occurrence_sorted_rows)

    print(f"Scanned files: {len(extraction_files)}")
    print(f"Schema field paths: {len(standard_paths)}")
    print(f"Observed field paths: {len(observed_paths)}")
    print(f"JSON summary: {output_json}")
    print(f"CSV summary: {output_csv}")
    print(f"Paper-count JSON: {paper_sorted_json}")
    print(f"Paper-count CSV: {paper_sorted_csv}")
    print(f"Occurrence-count JSON: {occurrence_sorted_json}")
    print(f"Occurrence-count CSV: {occurrence_sorted_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
