import re
from pathlib import Path
from typing import Dict, List


IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
FIGURE_CAPTION_RE = re.compile(
    r"^\s*(?:fig(?:ure)?\.?|figure)\s*\.?\s*(\d+)(?:[a-zA-Z\u0370-\u03FF]+)?(?:[\.\):\-\s]|$)",
    re.IGNORECASE,
)
FIGURE_NO_RE = re.compile(
    r"\b(?:fig(?:ure)?\.?|figure)\s*\.?\s*(\d+)(?:[a-zA-Z\u0370-\u03FF]+)?\b",
    re.IGNORECASE,
)
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
    title_idx = None
    for i, line in enumerate(lines):
        if line.strip().startswith("# "):
            title_idx = i
            break

    start_idx = (title_idx + 1) if title_idx is not None else 0
    first_section_idx = len(lines)
    for i in range(start_idx, len(lines)):
        if HEADING_RE.match(lines[i].strip()):
            first_section_idx = i
            break

    pre_section = lines[start_idx:first_section_idx]
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
        if line.lower().startswith(("key words:", "keywords:", "received ", "revised ")):
            continue
        if line.startswith("\\*"):
            continue
        current.append(line)
    if current:
        paragraphs.append(" ".join(current))

    paragraphs = [paragraph for paragraph in paragraphs if len(paragraph) >= 80]
    if not paragraphs:
        return ""

    paragraphs.sort(key=len, reverse=True)
    return paragraphs[0]


def collect_figure_references(lines: List[str]) -> Dict[str, List[str]]:
    refs: Dict[str, List[str]] = {}
    for raw in lines:
        stripped = raw.strip()
        if not stripped:
            continue
        if FIGURE_CAPTION_RE.match(stripped) or stripped.startswith("#") or IMAGE_RE.search(stripped):
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
    if len(s) <= 20 and re.fullmatch(r"[A-Za-z0-9\-\+\(\)\[\]/\s]+", s):
        return True
    if len(s) <= 30 and re.fullmatch(r"[A-Za-z0-9\-\+\(\)\[\]/:;,\.\s]+", s):
        return True
    if len(s) <= 80 and re.search(r"\([a-z]\)", s, re.IGNORECASE):
        return True
    if len(s) <= 80 and re.search(r"\bfor\s+\d+\s*[A-Za-z]+\s+steel\s+strip\b", s, re.IGNORECASE):
        return True
    if len(s) <= 80 and re.search(r"\b(?:wt|vol|at)\s*\.?\s*%", s, re.IGNORECASE):
        return True
    if len(s) <= 80 and re.search(r"\b[A-Za-z]+\s*\([^)]*%\)", s):
        return True
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

    chunks = [lines[start_idx].strip()]
    i = start_idx + 1
    blank_run = 0
    while i < len(lines):
        s = lines[i].strip()
        if not s:
            blank_run += 1
            if blank_run > 2:
                break
            i += 1
            continue
        blank_run = 0
        if s.startswith("#") or FIGURE_CAPTION_RE.match(s) or IMAGE_RE.search(s):
            break
        if s.startswith("<details>") or s.startswith("<summary>") or s.startswith("</details>"):
            break
        if s.lower().startswith("this article is protected by copyright"):
            break
        if lines[i - 1].strip() == "" and not caption_likely_incomplete(" ".join(chunks)):
            break
        if len(s) > 180 and not caption_likely_incomplete(" ".join(chunks)):
            break
        chunks.append(s)
        i += 1
    return " ".join(chunks)


def collect_images(lines: List[str], start_idx: int) -> tuple[List[str], int]:
    chunks = [lines[start_idx].strip()]
    end_idx = start_idx
    while end_idx + 1 < len(lines) and ")" not in " ".join(chunks) and len(chunks) < 5:
        end_idx += 1
        chunks.append(lines[end_idx].strip())
    joined = "".join(chunks)
    return [match.strip() for match in IMAGE_RE.findall(joined)], end_idx


def skip_details_block(lines: List[str], start_idx: int) -> int:
    i = start_idx
    while i < len(lines):
        if lines[i].strip().startswith("</details>"):
            return i
        i += 1
    return start_idx


def parse_markdown_text(markdown_text: str) -> List[Dict]:
    lines = markdown_text.splitlines()

    title = get_title(lines)
    abstract = get_abstract(lines)
    figure_refs = collect_figure_references(lines)

    results: List[Dict] = []
    pending_images: List[str] = []

    idx = 0
    while idx < len(lines):
        raw = lines[idx]
        line = raw.strip()
        if not line:
            idx += 1
            continue

        h = HEADING_RE.match(line)
        if h:
            idx += 1
            continue

        if line.startswith("<details>"):
            idx = skip_details_block(lines, idx) + 1
            continue

        if IMAGE_RE.search(line) or line.startswith("![]("):
            image_paths, end_idx = collect_images(lines, idx)
            pending_images.extend(image_paths)
            idx = end_idx + 1
            continue

        if pending_images and FIGURE_CAPTION_RE.match(line):
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
            idx += 1
            continue

        if pending_images and is_probable_noise_between_image_and_caption(line):
            idx += 1
            continue

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
        idx += 1

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

    return backfill_missing_continued_captions(results)


def backfill_missing_continued_captions(groups: List[Dict]) -> List[Dict]:
    last_caption = ""
    last_citation_sentences: List[str] = []
    for group in groups:
        caption = group.get("caption", "")
        if caption:
            last_caption = caption
            last_citation_sentences = group.get("citation_sentences", [])
            continue
        if last_caption and re.search(r"\bcontinued\.?$", last_caption, re.IGNORECASE):
            group["caption"] = last_caption
            group["citation_sentences"] = list(last_citation_sentences)
    return groups


def parse_markdown_file(md_path: Path) -> List[Dict]:
    return parse_markdown_text(md_path.read_text(encoding="utf-8"))
