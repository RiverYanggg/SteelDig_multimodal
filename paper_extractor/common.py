import json
import re
from pathlib import Path
from typing import Any, Dict


MAX_LOG_PREVIEW_CHARS = 3000


def load_text(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        raise ValueError(f"File is empty: {path}")
    return text


def extract_json_from_text(text: str) -> Any:
    text = text.strip()
    if not text:
        raise ValueError("Empty response content.")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    block = re.search(r"```(?:json)?\s*(.*?)\s*```", text, re.DOTALL | re.IGNORECASE)
    if block:
        return json.loads(block.group(1))
    matches = re.findall(r"\{[\s\S]*\}", text)
    if matches:
        for candidate in sorted(matches, key=len, reverse=True):
            try:
                return json.loads(candidate)
            except json.JSONDecodeError:
                continue
    raise ValueError("Cannot parse JSON from model response.")


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

