#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path
from typing import Dict, List


IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
FIGURE_NO_RE = re.compile(r"\bFigure\s+(\d+)\b", re.IGNORECASE)
FIGURE_REF_RE = re.compile(r"\b(?:Figure|Fig(?:ure)?)\s*\.?\s*(\d+)(?:[a-zA-Z\u0370-\u03FF]+)?", re.IGNORECASE)


def split_sentences(text: str) -> List[str]:
    parts = re.split(r"(?<=[\.\!\?])\s+", text.strip())
    return [p.strip() for p in parts if p.strip()]


def get_title(lines: List[str]) -> str:
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    return ""


def get_abstract(lines: List[str]) -> str:
    first_section_idx = len(lines)
    for i, line in enumerate(lines):
        if re.match(r"^#\s+\d+[\.\s]", line.strip()):
            first_section_idx = i
            break

    pre_section = lines[:first_section_idx]
    paragraphs: List[str] = []
    current: List[str] = []
    for raw in pre_section:
        line = raw.strip()
        if not line:
            if current:
                paragraphs.append(" ".join(current))
                current = []
            continue
        if line.startswith("#"):
            continue
        current.append(line)
    if current:
        paragraphs.append(" ".join(current))

    if not paragraphs:
        return ""

    # Pick the longest paragraph as abstract candidate.
    paragraphs.sort(key=len, reverse=True)
    return paragraphs[0]


def collect_figure_references(lines: List[str]) -> Dict[str, List[str]]:
    refs: Dict[str, List[str]] = {}
    for raw in lines:
        stripped = raw.strip()
        if not stripped:
            continue
        if stripped.startswith("Figure ") or stripped.startswith("#") or IMAGE_RE.search(stripped):
            continue
        nums = FIGURE_REF_RE.findall(stripped)
        if not nums:
            continue
        for n in nums:
            refs.setdefault(n, [])
            if stripped not in refs[n]:
                refs[n].append(stripped)
    return refs


def is_probable_noise_between_image_and_caption(line: str) -> bool:
    s = line.strip()
    if not s:
        return True
    # Common OCR/figure panel noise, e.g. "As-cast", "6h", "(a)", "a)"
    if len(s) <= 20 and re.fullmatch(r"[A-Za-z0-9\-\+\(\)\[\]/\s]+", s):
        return True
    # OCR legend fragments, e.g. "FCC: , BCC:"
    if len(s) <= 30 and re.fullmatch(r"[A-Za-z0-9\-\+\(\)\[\]/:;,\.\s]+", s):
        return True
    # Caption fragments leaked by OCR, e.g. "strip; (c), (d) for 5Cu steel strip"
    if len(s) <= 80 and re.search(r"\([a-z]\)", s, re.IGNORECASE):
        return True
    if len(s) <= 80 and re.search(r"\bfor\s+\d+\s*[A-Za-z]+\s+steel\s+strip\b", s, re.IGNORECASE):
        return True
    # Single token/label-like fragments.
    if len(s.split()) <= 3 and not any(p in s for p in [".", "?", "!", ":", ";"]):
        return True
    return False


def collect_multiline_caption(lines: List[str], start_idx: int) -> str:
    def caption_likely_incomplete(text: str) -> bool:
        t = text.strip()
        if not t:
            return False
        if t.endswith((",", ";", ":", "-", "(", "[", "{")):
            return True
        last_word = re.findall(r"[A-Za-z]+", t.lower())
        if last_word and last_word[-1] in {
            "the", "and", "or", "of", "for", "to", "in", "with",
            "is", "are", "was", "were", "be", "by", "on", "at",
        }:
            return True
        return False

    # Join Figure-start line with following wrapped lines until a clear boundary.
    chunks = [lines[start_idx].strip()]
    i = start_idx + 1
    blank_run = 0
    while i < len(lines):
        s = lines[i].strip()
        if not s:
            # OCR often inserts blank lines inside captions; tolerate short blank runs.
            blank_run += 1
            if blank_run > 2:
                break
            i += 1
            continue
        blank_run = 0
        if s.startswith("#") or s.lower().startswith("figure ") or IMAGE_RE.search(s):
            break
        if s.lower().startswith("this article is protected by copyright"):
            break
        # After an empty line, only keep extending if the current caption looks incomplete.
        # This avoids swallowing normal body paragraphs after a complete caption.
        if lines[i - 1].strip() == "" and not caption_likely_incomplete(" ".join(chunks)):
            break
        if len(s) > 180 and not caption_likely_incomplete(" ".join(chunks)):
            break
        chunks.append(s)
        i += 1
    return " ".join(chunks)


def parse_markdown(md_path: Path) -> List[Dict]:
    text = md_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    title = get_title(lines)
    abstract = get_abstract(lines)
    figure_refs = collect_figure_references(lines)

    results: List[Dict] = []
    pending_images: List[str] = []

    for idx, raw in enumerate(lines):
        line = raw.strip()
        if not line:
            continue

        h = HEADING_RE.match(line)
        if h:
            continue

        img_match = IMAGE_RE.search(line)
        if img_match:
            pending_images.append(img_match.group(1).strip())
            continue

        if pending_images and line.lower().startswith("figure "):
            caption = collect_multiline_caption(lines, idx)
            no_match = FIGURE_NO_RE.search(caption)
            fig_no = no_match.group(1) if no_match else None
            ref_sents = figure_refs.get(fig_no, []) if fig_no else []

            results.append(
                {
                    "image_paths": pending_images.copy(),
                    "caption": caption,
                    "paper_abstract": abstract,
                    "paper_title": title,
                    "citation_sentences": ref_sents,
                }
            )
            pending_images = []
            continue

        # Keep pending images when only short OCR/panel noise appears.
        if pending_images and is_probable_noise_between_image_and_caption(line):
            continue

        # If clear non-caption content appears, flush orphan images with empty caption.
        if pending_images:
            results.append(
                {
                    "image_paths": pending_images.copy(),
                    "caption": "",
                    "paper_abstract": abstract,
                    "paper_title": title,
                    "citation_sentences": [],
                }
            )
            pending_images = []

    # Final flush if file ends right after images
    if pending_images:
        results.append(
            {
                "image_paths": pending_images.copy(),
                "caption": "",
                "paper_abstract": abstract,
                "paper_title": title,
                "citation_sentences": [],
            }
        )

    return results


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
