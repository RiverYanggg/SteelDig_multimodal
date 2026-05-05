import re
from typing import Dict, Iterable, List, Sequence, Tuple

from .content_list import get_category, get_text


DROP_CATEGORIES = {
    "ref_text",
    "reference",
    "references",
    "bibliography",
    "footer",
    "header",
    "page_footer",
    "page_header",
    "page_number",
    "copyright",
    "license",
    "orcid",
}

REFERENCE_CATEGORIES = {
    "ref_text",
    "reference",
    "references",
    "bibliography",
}


def clean_markdown_with_content_list(
    markdown_text: str,
    items: Sequence[dict],
    extra_drop_categories: Iterable[str] | None = None,
) -> Tuple[str, List[Dict[str, str]], Dict[str, int], int]:
    drop_categories = {value.lower() for value in DROP_CATEGORIES}
    if extra_drop_categories:
        drop_categories.update(value.lower() for value in extra_drop_categories)

    cleaned = markdown_text
    removed_categories: Dict[str, int] = {}
    references: List[Dict[str, str]] = []
    removed_blocks = 0

    for item in items:
        category = get_category(item).strip()
        category_key = category.lower()
        text = get_text(item).strip()
        if not category_key or not text:
            continue

        if category_key in REFERENCE_CATEGORIES:
            references.append({"category": category, "text": text})

        if category_key not in drop_categories:
            continue

        updated = _remove_block_text(cleaned, text)
        if updated != cleaned:
            cleaned = updated
            removed_blocks += 1
            removed_categories[category] = removed_categories.get(category, 0) + 1

    cleaned = _strip_trailing_reference_lines(cleaned)
    cleaned = _strip_common_noise_sections(cleaned)
    cleaned = _normalize_spacing(cleaned)
    return cleaned, references, removed_categories, removed_blocks


def clean_markdown_without_content_list(markdown_text: str) -> Tuple[str, List[Dict[str, str]], Dict[str, int], int]:
    references, cleaned = _extract_reference_lines(markdown_text)
    cleaned = _strip_common_noise_sections(cleaned)
    cleaned = _normalize_spacing(cleaned)
    removed_categories = {"ref_text": len(references)} if references else {}
    return cleaned, references, removed_categories, len(references)


def _remove_block_text(markdown_text: str, block_text: str) -> str:
    if block_text in markdown_text:
        return markdown_text.replace(block_text, "\n")

    escaped = re.escape(block_text)
    escaped = escaped.replace(r"\ ", r"\s+")
    escaped = escaped.replace(r"\\\n", r"\s*")
    pattern = re.compile(escaped, re.MULTILINE)
    return pattern.sub("\n", markdown_text, count=1)


def _extract_reference_lines(markdown_text: str) -> Tuple[List[Dict[str, str]], str]:
    lines = markdown_text.splitlines()
    first_reference_index = None
    for index, line in enumerate(lines):
        if re.match(r"^\[\d+\]\s+", line.strip()):
            first_reference_index = index
            break

    if first_reference_index is None:
        return [], markdown_text

    reference_lines = [line.rstrip() for line in lines[first_reference_index:] if line.strip()]
    references = [{"category": "ref_text", "text": line} for line in reference_lines]
    cleaned_lines = lines[:first_reference_index]
    return references, "\n".join(cleaned_lines)


def _strip_trailing_reference_lines(markdown_text: str) -> str:
    lines = markdown_text.splitlines()
    while lines and re.match(r"^\[\d+\]\s+", lines[-1].strip()):
        lines.pop()
    return "\n".join(lines)


def _strip_common_noise_sections(markdown_text: str) -> str:
    noise_headings = {
        "acknowledgements",
        "acknowledgments",
        "conflict of interest",
        "data availability statement",
        "keywords",
    }
    lines = markdown_text.splitlines()
    kept: List[str] = []
    skip_mode = False

    for line in lines:
        stripped = line.strip().lower()
        if stripped.startswith("# "):
            heading = stripped[2:].strip()
            skip_mode = heading in noise_headings
            if skip_mode:
                continue
        if skip_mode:
            continue
        if stripped.startswith("received:") or stripped.startswith("revised:") or stripped.startswith("published online:"):
            continue
        kept.append(line)
    return "\n".join(kept)


def _normalize_spacing(markdown_text: str) -> str:
    text = markdown_text.replace("\r\n", "\n")
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"
