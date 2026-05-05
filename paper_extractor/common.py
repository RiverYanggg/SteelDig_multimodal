import json
import re
from pathlib import Path
from typing import Any, Dict, List


MAX_LOG_PREVIEW_CHARS = 3000


def load_text(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        raise ValueError(f"File is empty: {path}")
    return text


def extract_json_from_text(text: str) -> Any:
    candidates = extract_json_candidates(text)
    for candidate in candidates:
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            continue
    raise ValueError("Cannot parse JSON from model response.")


def extract_json_candidates(text: str) -> List[str]:
    text = text.strip()
    if not text:
        raise ValueError("Empty response content.")

    candidates: List[str] = []
    candidates.extend(_build_candidate_variants(text))

    block_matches = re.findall(r"```(?:json)?\s*(.*?)\s*```", text, re.DOTALL | re.IGNORECASE)
    for block in block_matches:
        candidates.extend(_build_candidate_variants(block.strip()))

    json_fragments = _extract_balanced_json_fragments(text)
    for fragment in sorted(json_fragments, key=len, reverse=True):
        candidates.extend(_build_candidate_variants(fragment))

    deduped: List[str] = []
    seen = set()
    for candidate in candidates:
        normalized = candidate.strip()
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        deduped.append(normalized)
    return deduped


def log_jsonl(log_file: Path, payload: Dict[str, Any]) -> None:
    log_file.parent.mkdir(parents=True, exist_ok=True)
    with log_file.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")


def truncate_text(text: str, max_chars: int = MAX_LOG_PREVIEW_CHARS) -> str:
    if len(text) <= max_chars:
        return text
    return f"{text[:max_chars]}...<truncated,len={len(text)}>"


def clean_text(text: str) -> str:
    text = text.replace("\u0004", " ").replace("\u0001", " ")
    return re.sub(r"\s+", " ", text).strip()


def extract_figure_id(caption: str, fallback: str) -> str:
    m = re.search(r"\bFigure\s+(\d+)\b", caption, re.IGNORECASE)
    return f"Figure {m.group(1)}" if m else fallback


def _build_candidate_variants(text: str) -> List[str]:
    variants = [text.strip()]
    stripped = _strip_reasoning_wrappers(text)
    if stripped != text.strip():
        variants.append(stripped)
    return variants


def _strip_reasoning_wrappers(text: str) -> str:
    stripped = re.sub(r"<think>[\s\S]*?</think>", "", text, flags=re.IGNORECASE).strip()
    stripped = re.sub(r"^\s*```(?:json)?", "", stripped, flags=re.IGNORECASE).strip()
    stripped = re.sub(r"```\s*$", "", stripped).strip()
    first_object = stripped.find("{")
    first_array = stripped.find("[")
    positions = [pos for pos in (first_object, first_array) if pos >= 0]
    if positions:
        start = min(positions)
        stripped = stripped[start:].strip()
    return stripped


def _extract_balanced_json_fragments(text: str) -> List[str]:
    fragments: List[str] = []
    stack: List[str] = []
    start_index: int | None = None
    in_string = False
    escape = False

    for index, char in enumerate(text):
        if in_string:
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == '"':
                in_string = False
            continue

        if char == '"':
            in_string = True
            continue

        if char in "{[":
            if not stack:
                start_index = index
            stack.append("}" if char == "{" else "]")
            continue

        if char in "}]":
            if not stack or char != stack[-1]:
                stack.clear()
                start_index = None
                continue
            stack.pop()
            if not stack and start_index is not None:
                fragments.append(text[start_index:index + 1])
                start_index = None

    return fragments
