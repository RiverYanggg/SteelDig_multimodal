import json
from pathlib import Path
from typing import Any, Dict, Iterable, List


CONTENT_LIST_CONTAINER_KEYS = ("items", "blocks", "content_list", "data", "content")
CATEGORY_KEYS = ("category", "type", "block_type", "section_type", "label")
TEXT_KEYS = ("markdown", "md", "text", "content", "raw_text", "value")


def load_content_list(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    raw = path.read_text(encoding="utf-8").strip()
    if not raw:
        return []

    parsed = _parse_json_like(raw)
    items = _normalize_items(parsed)
    return [item for item in items if isinstance(item, dict)]


def get_category(item: Dict[str, Any]) -> str:
    for key in CATEGORY_KEYS:
        value = item.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def get_text(item: Dict[str, Any]) -> str:
    for key in TEXT_KEYS:
        value = item.get(key)
        if isinstance(value, str) and value.strip():
            return value
    return ""


def iter_category_counts(items: Iterable[Dict[str, Any]]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for item in items:
        category = get_category(item) or "<missing>"
        counts[category] = counts.get(category, 0) + 1
    return counts


def _parse_json_like(raw: str) -> Any:
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass

    records: List[Any] = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        records.append(json.loads(line))
    return records


def _normalize_items(parsed: Any) -> List[Any]:
    if isinstance(parsed, list):
        return parsed
    if isinstance(parsed, dict):
        for key in CONTENT_LIST_CONTAINER_KEYS:
            value = parsed.get(key)
            if isinstance(value, list):
                return value
        return [parsed]
    return []
