import json
import math
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, List


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    paper_id: str
    section: str
    section_index: int
    paragraph_start: int
    paragraph_end: int
    char_start: int
    char_end: int
    token_estimate: int
    text: str


_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")


def split_markdown_into_chunks(
    markdown_text: str,
    paper_id: str,
    max_chars: int = 24000,
    overlap_paragraphs: int = 1,
    target_chunks: int = 5,
    max_chunks: int = 8,
    min_chars: int = 6000,
) -> List[Chunk]:
    """Split Markdown into a small number of structure-aware chunks.

    The splitter prefers level-1 headings as primary boundaries, uses level-2
    headings only to break oversized sections, and falls back to paragraph-size
    slicing when a section is still too large.
    """
    max_chars = max(1000, int(max_chars or 24000))
    target_chunks = max(1, int(target_chunks or 5))
    max_chunks = max(target_chunks, int(max_chunks or target_chunks))
    min_chars = max(0, min(int(min_chars or 0), max_chars))
    overlap_paragraphs = max(0, int(overlap_paragraphs or 0))

    items = _sectioned_paragraphs(markdown_text)
    if not items:
        return []

    total_chars = sum(len(item[3]) for item in items)
    target_chars = min(max_chars, max(min_chars, math.ceil(total_chars / target_chunks)))
    blocks = _build_structure_blocks(items, max_chars=max_chars, target_chars=target_chars)
    blocks = _merge_blocks(blocks, target_chunks=target_chunks, max_chunks=max_chunks, max_chars=max_chars, min_chars=min_chars)

    chunks: List[Chunk] = []
    for index, block in enumerate(blocks):
        chunk_items = list(block)
        if overlap_paragraphs > 0 and index > 0:
            overlap = blocks[index - 1][-overlap_paragraphs:]
            chunk_items = overlap + chunk_items
        chunks.append(_make_chunk(chunk_items, paper_id, len(chunks) + 1))
    return chunks


def _sectioned_paragraphs(markdown_text: str) -> List[tuple[int, int, int, str, str, int, int]]:
    paragraphs = _paragraphs_with_offsets(markdown_text)
    current_section = "Front Matter"
    current_section_index = 0
    items: List[tuple[int, int, int, str, str, int, int]] = []

    for para_index, char_start, char_end, paragraph in paragraphs:
        heading = _HEADING_RE.match(paragraph.strip())
        heading_level = 0
        if heading:
            heading_level = len(heading.group(1))
            heading_text = heading.group(2).strip()
            if heading_level <= 2:
                current_section_index += 1
                current_section = heading_text
            elif current_section == "Front Matter":
                current_section = heading_text

        items.append((para_index, char_start, char_end, paragraph, current_section, current_section_index, heading_level))
    return items


def _build_structure_blocks(
    items: List[tuple[int, int, int, str, str, int, int]],
    max_chars: int,
    target_chars: int,
) -> List[List[tuple[int, int, int, str, str, int, int]]]:
    blocks: List[List[tuple[int, int, int, str, str, int, int]]] = []
    for primary_block in _split_on_heading_levels(items, {1}):
        if _block_chars(primary_block) <= max_chars:
            blocks.append(primary_block)
            continue
        secondary_blocks = _split_on_heading_levels(primary_block, {2})
        for secondary_block in secondary_blocks:
            if _block_chars(secondary_block) <= max_chars:
                blocks.append(secondary_block)
            else:
                blocks.extend(_split_by_chars(secondary_block, max_chars=max_chars, target_chars=target_chars))
    return [block for block in blocks if block]


def _split_on_heading_levels(
    items: List[tuple[int, int, int, str, str, int, int]],
    heading_levels: set[int],
) -> List[List[tuple[int, int, int, str, str, int, int]]]:
    blocks: List[List[tuple[int, int, int, str, str, int, int]]] = []
    current: List[tuple[int, int, int, str, str, int, int]] = []
    for item in items:
        heading_level = item[6]
        if current and heading_level in heading_levels:
            blocks.append(current)
            current = []
        current.append(item)
    if current:
        blocks.append(current)
    return blocks


def _split_by_chars(
    items: List[tuple[int, int, int, str, str, int, int]],
    max_chars: int,
    target_chars: int,
) -> List[List[tuple[int, int, int, str, str, int, int]]]:
    blocks: List[List[tuple[int, int, int, str, str, int, int]]] = []
    current: List[tuple[int, int, int, str, str, int, int]] = []
    current_chars = 0
    limit = max(1, min(max_chars, target_chars))
    for item in items:
        item_chars = len(item[3])
        if current and current_chars + item_chars > limit:
            blocks.append(current)
            current = []
            current_chars = 0
        current.append(item)
        current_chars += item_chars
    if current:
        blocks.append(current)
    return blocks


def _merge_blocks(
    blocks: List[List[tuple[int, int, int, str, str, int, int]]],
    target_chunks: int,
    max_chunks: int,
    max_chars: int,
    min_chars: int,
) -> List[List[tuple[int, int, int, str, str, int, int]]]:
    merged: List[List[tuple[int, int, int, str, str, int, int]]] = []
    for block in blocks:
        if merged and (_block_chars(merged[-1]) < min_chars or len(merged) >= max_chunks):
            combined_chars = _block_chars(merged[-1]) + _block_chars(block)
            if combined_chars <= max_chars:
                merged[-1].extend(block)
                continue
        merged.append(list(block))

    while len(merged) > max_chunks or (len(merged) > target_chunks and _has_small_block(merged, min_chars)):
        pair_index = _best_merge_pair(merged, max_chars=max_chars)
        if pair_index is None:
            break
        merged[pair_index].extend(merged[pair_index + 1])
        del merged[pair_index + 1]
    return merged


def _best_merge_pair(blocks: List[List[tuple[int, int, int, str, str, int, int]]], max_chars: int) -> int | None:
    best_index: int | None = None
    best_size: int | None = None
    for index in range(len(blocks) - 1):
        combined_size = _block_chars(blocks[index]) + _block_chars(blocks[index + 1])
        if combined_size > max_chars:
            continue
        if best_size is None or combined_size < best_size:
            best_index = index
            best_size = combined_size
    return best_index


def _block_chars(block: List[tuple[int, int, int, str, str, int, int]]) -> int:
    return sum(len(item[3]) for item in block)


def _has_small_block(blocks: List[List[tuple[int, int, int, str, str, int, int]]], min_chars: int) -> bool:
    return any(_block_chars(block) < min_chars for block in blocks)


def write_chunks(output_dir: Path, source_file: Path, paper_id: str, chunks: Iterable[Chunk]) -> None:
    chunk_list = list(chunks)
    output_dir.mkdir(parents=True, exist_ok=True)
    chunks_path = output_dir / "chunks.jsonl"
    with chunks_path.open("w", encoding="utf-8") as f:
        for chunk in chunk_list:
            f.write(json.dumps(asdict(chunk), ensure_ascii=False) + "\n")

    index_payload = {
        "paper_id": paper_id,
        "source_file": str(source_file),
        "chunk_count": len(chunk_list),
        "chunks": [
            {
                "chunk_id": chunk.chunk_id,
                "section": chunk.section,
                "section_index": chunk.section_index,
                "paragraph_start": chunk.paragraph_start,
                "paragraph_end": chunk.paragraph_end,
                "char_start": chunk.char_start,
                "char_end": chunk.char_end,
                "token_estimate": chunk.token_estimate,
            }
            for chunk in chunk_list
        ],
    }
    (output_dir / "chunks_index.json").write_text(
        json.dumps(index_payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def _paragraphs_with_offsets(text: str) -> List[tuple[int, int, int, str]]:
    matches = list(re.finditer(r"\S(?:.*?)(?=\n\s*\n|\Z)", text, flags=re.DOTALL))
    paragraphs: List[tuple[int, int, int, str]] = []
    for index, match in enumerate(matches, start=1):
        paragraph = match.group(0).strip()
        if paragraph:
            paragraphs.append((index, match.start(), match.end(), paragraph))
    return paragraphs


def _make_chunk(items: List[tuple[int, int, int, str, str, int, int]], paper_id: str, serial: int) -> Chunk:
    text = "\n\n".join(item[3] for item in items)
    sections = [item[4] for item in items if item[4]]
    section = sections[0] if sections else "Unknown"
    section_index = items[0][5]
    return Chunk(
        chunk_id=f"chunk_{serial:04d}",
        paper_id=paper_id,
        section=section,
        section_index=section_index,
        paragraph_start=items[0][0],
        paragraph_end=items[-1][0],
        char_start=items[0][1],
        char_end=items[-1][2],
        token_estimate=max(1, len(text) // 4),
        text=text,
    )
