import json
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
    max_chars: int = 9000,
    overlap_paragraphs: int = 1,
) -> List[Chunk]:
    """Split Markdown by section and paragraph while retaining source offsets."""
    paragraphs = _paragraphs_with_offsets(markdown_text)
    chunks: List[Chunk] = []
    current_section = "Front Matter"
    current_section_index = 0
    buffer: List[tuple[int, int, int, str, str, int]] = []
    buffer_chars = 0

    def flush_buffer(force: bool = False) -> None:
        nonlocal buffer, buffer_chars
        if not buffer:
            return
        if not force and buffer_chars < max_chars:
            return
        chunk_items = buffer if force else _items_until_limit(buffer, max_chars)
        if not chunk_items:
            chunk_items = [buffer[0]]
        chunks.append(_make_chunk(chunk_items, paper_id, len(chunks) + 1))
        keep = chunk_items[-overlap_paragraphs:] if overlap_paragraphs > 0 else []
        remaining = buffer[len(chunk_items):]
        buffer = keep + remaining
        buffer_chars = sum(len(item[3]) for item in buffer)

    for para_index, char_start, char_end, paragraph in paragraphs:
        heading = _HEADING_RE.match(paragraph.strip())
        if heading:
            flush_buffer(force=True)
            current_section_index += 1
            current_section = heading.group(2).strip()

        item = (para_index, char_start, char_end, paragraph, current_section, current_section_index)
        if buffer and buffer_chars + len(paragraph) > max_chars:
            flush_buffer(force=False)
        buffer.append(item)
        buffer_chars += len(paragraph)

    flush_buffer(force=True)
    return chunks


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


def _items_until_limit(items: List[tuple[int, int, int, str, str, int]], max_chars: int) -> List[tuple[int, int, int, str, str, int]]:
    selected: List[tuple[int, int, int, str, str, int]] = []
    total = 0
    for item in items:
        if selected and total + len(item[3]) > max_chars:
            break
        selected.append(item)
        total += len(item[3])
    return selected


def _make_chunk(items: List[tuple[int, int, int, str, str, int]], paper_id: str, serial: int) -> Chunk:
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

