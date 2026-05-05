#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
from typing import Dict, List

from paper_extractor.preprocess.image_groups import parse_markdown_file


def parse_markdown(md_path: Path) -> List[Dict]:
    return parse_markdown_file(md_path)


def collect_md_files(input_path: Path, recursive: bool) -> List[Path]:
    if input_path.is_file() and input_path.suffix.lower() == ".md":
        return [input_path]
    if input_path.is_dir():
        pattern = "**/*.md" if recursive else "*.md"
        return sorted(input_path.glob(pattern))
    raise FileNotFoundError(f"Input path not found or not supported: {input_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract image metadata from markdown files.")
    parser.add_argument("--input", required=True, help="Markdown file or directory path.")
    parser.add_argument("--output", help="Output JSON file path (single merged file).")
    parser.add_argument("--output-dir", help="Output directory, one JSON per paper.")
    parser.add_argument("--recursive", action="store_true", help="Recursively scan input directory.")
    args = parser.parse_args()

    input_path = Path(args.input).expanduser().resolve()
    if not args.output and not args.output_dir:
        raise ValueError("Please provide --output or --output-dir.")
    if args.output and args.output_dir:
        raise ValueError("Use only one of --output or --output-dir.")

    md_files = collect_md_files(input_path, args.recursive)
    if args.output_dir:
        output_dir = Path(args.output_dir).expanduser().resolve()
        output_dir.mkdir(parents=True, exist_ok=True)

        total_items = 0
        for md in md_files:
            paper_items = parse_markdown(md)
            total_items += len(paper_items)
            out_file = output_dir / f"{md.stem}.json"
            out_file.write_text(json.dumps(paper_items, ensure_ascii=False, indent=2), encoding="utf-8")

        print(f"Done. Extracted {total_items} grouped entries from {len(md_files)} markdown file(s).")
        print(f"Output directory: {output_dir}")
    else:
        output_path = Path(args.output).expanduser().resolve()
        all_items: List[Dict] = []
        for md in md_files:
            all_items.extend(parse_markdown(md))

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(all_items, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Done. Extracted {len(all_items)} grouped entries from {len(md_files)} markdown file(s).")
        print(f"Output: {output_path}")


if __name__ == "__main__":
    main()
