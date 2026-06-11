from __future__ import annotations

import json
import re
import unicodedata
from typing import Any, Iterable, Iterator


_WHITESPACE_RE = re.compile(r"\s+")
_NUMBER_RE = re.compile(r"(?P<op><=|>=|<|>)?\s*(?P<value>-?\d+(?:\.\d+)?)")
_TOKEN_RE = re.compile(r"[a-z0-9]+(?:\.[0-9]+)?")


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    text = unicodedata.normalize("NFKC", str(value)).strip().lower()
    replacements = {
        "℃": " c ",
        "°c": " c ",
        "°": " ",
        "–": "-",
        "—": "-",
        "−": "-",
        "×": "x",
        "µm": " um ",
        "μm": " um ",
        "㎛": " um ",
        "g/cm³": "g/cm^3",
        "cm³": "cm^3",
        "bal.": "balance",
    }
    for source, target in replacements.items():
        text = text.replace(source, target)
    text = _WHITESPACE_RE.sub(" ", text)
    return text.strip()


def normalize_identifier(value: Any) -> str:
    text = normalize_text(value)
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_")


def tokenize(value: Any) -> list[str]:
    tokens: list[str] = []
    for token in _TOKEN_RE.findall(normalize_text(value)):
        tokens.append(token)
        pieces = re.findall(r"[a-z]+|\d+(?:\.\d+)?", token)
        for piece in pieces:
            if piece != token:
                tokens.append(piece)
    return tokens


def token_set(value: Any, stopwords: Iterable[str] | None = None) -> set[str]:
    blocklist = set(stopwords or [])
    return {token for token in tokenize(value) if token not in blocklist}


def safe_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def extract_primary_number(value: Any) -> dict[str, Any] | None:
    text = normalize_text(value)
    if not text or text in {"none", "null", "na", "n/a", "balance"}:
        return None
    match = _NUMBER_RE.search(text)
    if not match:
        return None
    number = safe_float(match.group("value"))
    if number is None:
        return None
    return {"operator": match.group("op") or "", "value": number}


def extract_numbers(value: Any) -> list[float]:
    text = normalize_text(value)
    numbers: list[float] = []
    for match in _NUMBER_RE.finditer(text):
        number = safe_float(match.group("value"))
        if number is not None:
            numbers.append(number)
    return numbers


def stringify_scalar(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def iter_string_leaves(node: Any) -> Iterator[str]:
    if node is None:
        return
    if isinstance(node, str):
        if normalize_text(node):
            yield node
        return
    if isinstance(node, (int, float, bool)):
        yield stringify_scalar(node)
        return
    if isinstance(node, list):
        for item in node:
            yield from iter_string_leaves(item)
        return
    if isinstance(node, dict):
        for value in node.values():
            yield from iter_string_leaves(value)


def compact_text_fragments(node: Any, limit: int = 32) -> str:
    fragments = []
    for fragment in iter_string_leaves(node):
        normalized = normalize_text(fragment)
        if normalized:
            fragments.append(fragment)
        if len(fragments) >= limit:
            break
    return " ".join(fragments)
