from __future__ import annotations

import json
import re
import ssl
import time
import unicodedata
from http.client import IncompleteRead
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any
from urllib import error, parse, request

SECTIONS = [
    "papers",
    "alloys",
    "processes",
    "samples",
    "processing_steps",
    "structures",
    "interfaces",
    "properties",
    "performance",
    "characterization_methods",
    "computational_details",
    "unmapped_findings",
]

SECTION_ID_KEYS = {
    "papers": "paper_id",
    "alloys": "alloy_id",
    "processes": "process_id",
    "samples": "sample_id",
    "processing_steps": "sample_id",
    "structures": "sample_id",
    "interfaces": "sample_id",
    "properties": "sample_id",
    "performance": "sample_id",
    "characterization_methods": None,
    "computational_details": None,
    "unmapped_findings": None,
}

DEFAULT_FIELD_RULES = {
    "id_fields": []
}

_WHITESPACE_RE = re.compile(r"\s+")


SAMPLE_LINKED_SECTIONS = (
    "processing_steps",
    "structures",
    "interfaces",
    "properties",
    "performance",
)


@dataclass(frozen=True)
class SharedLLMSettings:
    model: str = "deepseek-v4-flash"
    base_url: str = "https://api.deepseek.com"
    api_key: str = "EMPTY"
    temperature: float = 0.0
    verify_ssl: bool = True
    max_retries: int = 3


@dataclass(frozen=True)
class SchemaSpec:
    sections: tuple[str, ...]
    section_id_keys: dict[str, str | None]
    id_fields: tuple[str, ...]
    sample_linked_sections: tuple[str, ...]


@dataclass(frozen=True)
class EvidenceBlock:
    block_id: str
    text: str
    char_start: int
    char_end: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(payload: Any, path: str | Path) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def load_schema_spec(path: str | Path = "prompt/json_schema.json") -> SchemaSpec:
    schema_path = Path(path).expanduser().resolve()
    if not schema_path.exists():
        return SchemaSpec(
            sections=tuple(SECTIONS),
            section_id_keys=dict(SECTION_ID_KEYS),
            id_fields=tuple(_default_id_fields()),
            sample_linked_sections=tuple(SAMPLE_LINKED_SECTIONS),
        )
    data = json.loads(schema_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"schema root must be an object: {schema_path}")
    sections = tuple(str(key) for key, value in data.items() if isinstance(value, list))
    section_id_keys = {section: _infer_section_id_key(section, data.get(section)) for section in sections}
    id_fields = tuple(sorted(_collect_id_fields(data) | set(_default_id_fields())))
    sample_linked_sections = tuple(
        section
        for section in sections
        if section not in {"papers", "alloys", "processes", "samples"}
        and _section_template_has_key(data.get(section), "sample_id")
    )
    return SchemaSpec(
        sections=sections,
        section_id_keys=section_id_keys,
        id_fields=id_fields,
        sample_linked_sections=sample_linked_sections,
    )


def load_field_rules(path: str | Path, schema_spec: SchemaSpec | None = None) -> dict[str, Any]:
    rules_path = Path(path).expanduser().resolve()
    schema_ids = list((schema_spec or load_schema_spec()).id_fields)
    if not rules_path.exists():
        return {**DEFAULT_FIELD_RULES, "id_fields": schema_ids}
    data = json.loads(rules_path.read_text(encoding="utf-8"))
    merged = {**DEFAULT_FIELD_RULES, "id_fields": schema_ids}
    for key, value in data.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = {**merged[key], **value}
        elif key == "id_fields" and isinstance(value, list):
            merged[key] = sorted(set(schema_ids) | {str(item) for item in value})
        else:
            merged[key] = value
    return merged


def _default_id_fields() -> list[str]:
    return [
        "paper_id",
        "alloy_id",
        "process_id",
        "sample_id",
        "structure_id",
        "interface_set_id",
        "interface_id",
        "interaction_id",
        "property_set_id",
        "property_id",
        "performance_id",
        "characterization_id",
        "computation_id",
        "uuid",
        "microstructure_uuid",
        "precipitate_id",
    ]


def _infer_section_id_key(section: str, template: Any) -> str | None:
    item = template[0] if isinstance(template, list) and template else None
    if not isinstance(item, dict):
        return None
    if section != "samples" and "sample_id" in item:
        return "sample_id"
    preferred = f"{section[:-1]}_id" if section.endswith("s") else f"{section}_id"
    if preferred in item:
        return preferred
    for candidate in ("sample_id", "process_id", "alloy_id", "paper_id", "method_name"):
        if candidate in item:
            return candidate
    for key in item:
        if str(key).endswith("_id"):
            return str(key)
    return None


def _collect_id_fields(node: Any) -> set[str]:
    fields: set[str] = set()
    if isinstance(node, dict):
        for key, value in node.items():
            if str(key).endswith("_id") or key == "uuid" or str(key).endswith("_uuid"):
                fields.add(str(key))
            fields.update(_collect_id_fields(value))
    elif isinstance(node, list):
        for item in node:
            fields.update(_collect_id_fields(item))
    return fields


def _section_template_has_key(template: Any, key: str) -> bool:
    item = template[0] if isinstance(template, list) and template else None
    return isinstance(item, dict) and key in item


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
    return _WHITESPACE_RE.sub(" ", text).strip()


def normalize_identifier(value: Any) -> str:
    text = normalize_text(value)
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_")


def ensure_schema(data: dict[str, Any] | None, schema_spec: SchemaSpec | None = None) -> dict[str, Any]:
    schema = schema_spec or load_schema_spec()
    payload = dict(data or {})
    for section in schema.sections:
        value = payload.get(section)
        payload[section] = value if isinstance(value, list) else []
    return payload


def flatten_section_records(
    section_name: str,
    records: list[Any],
    canonical_map: dict[str, str],
    field_rules: dict[str, Any],
    schema_spec: SchemaSpec | None = None,
) -> dict[str, str]:
    flat: dict[str, str] = {}
    schema = schema_spec or load_schema_spec()
    id_key = schema.section_id_keys.get(section_name)
    for index, record in enumerate(records):
        if isinstance(record, dict):
            anchor = _resolve_anchor(section_name, record, index, id_key, canonical_map)
            for path, value in _walk_record(record):
                if _is_empty(value):
                    continue
                if _skip_path(path, field_rules):
                    continue
                flat[f"{section_name}.{anchor}.{path}"] = str(value)
        else:
            flat[f"{section_name}.idx_{index}.value"] = str(record)
    return flat


def _resolve_anchor(
    section_name: str,
    record: dict[str, Any],
    index: int,
    id_key: str | None,
    canonical_map: dict[str, str],
) -> str:
    if id_key and record.get(id_key):
        record_id = str(record.get(id_key))
        return canonical_map.get(normalize_identifier(record_id), record_id)
    for candidate_key in ("sample_id", "process_id", "alloy_id", "paper_id", "method_name"):
        value = record.get(candidate_key)
        if value:
            return canonical_map.get(normalize_identifier(str(value)), str(value))
    return f"idx_{index}"


def _walk_record(node: Any, prefix: str = ""):
    if isinstance(node, dict):
        combined_paths = _combined_quantity_paths(node)
        for name, value in combined_paths.items():
            next_prefix = f"{prefix}.{name}" if prefix else name
            yield next_prefix, value
        skip_keys = _combined_quantity_source_keys(combined_paths)
        for key, value in node.items():
            if key in skip_keys:
                continue
            next_prefix = f"{prefix}.{key}" if prefix else key
            yield from _walk_record(value, next_prefix)
        return
    if isinstance(node, list):
        for index, item in enumerate(node):
            anchor = _list_item_anchor(item)
            next_prefix = f"{prefix}[{anchor}]" if anchor else f"{prefix}[{index}]"
            yield from _walk_record(item, next_prefix)
        return
    yield prefix, node


def _combined_quantity_paths(node: dict[str, Any]) -> dict[str, str]:
    combined: dict[str, str] = {}
    unit = node.get("unit")
    if unit and not _is_empty(unit):
        for key in ("value", "temperature"):
            value = node.get(key)
            if not _is_empty(value):
                combined[f"{key}_with_unit"] = f"{value} {unit}"
    return combined


def _combined_quantity_source_keys(combined_paths: dict[str, str]) -> set[str]:
    skip: set[str] = set()
    for combined_key in combined_paths:
        if combined_key == "value_with_unit":
            skip.update({"value", "unit"})
        if combined_key == "temperature_with_unit":
            skip.update({"temperature", "unit"})
    return skip


def _list_item_anchor(item: Any) -> str | None:
    if not isinstance(item, dict):
        return None
    for key in (
        "element",
        "phase_name",
        "phase_1_name",
        "phase_2_name",
        "property_name",
        "property_type",
        "method",
        "type",
        "direction",
        "region",
        "sequence",
        "sequence_order",
        "related_sequence",
        "coherence",
    ):
        value = item.get(key)
        if value:
            return normalize_identifier(value)
    return None


def _skip_path(path: str, field_rules: dict[str, Any]) -> bool:
    final_key = path.split(".")[-1]
    return final_key in set(field_rules.get("id_fields", []))


def _is_empty(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return normalize_text(value) in {"", "none", "null", "na", "n/a"}
    if isinstance(value, list):
        return not value
    if isinstance(value, dict):
        return not value
    return False


def build_evidence_blocks(markdown: str, *, max_block_chars: int = 1800) -> list[EvidenceBlock]:
    blocks: list[EvidenceBlock] = []
    for match in re.finditer(r"\S(?:.*?(?:\n\s*\n|$))", markdown, flags=re.S):
        text = match.group(0).strip()
        if not text:
            continue
        parts = _split_long_block(text, max_block_chars=max_block_chars)
        cursor = match.start()
        for part in parts:
            part_start = markdown.find(part[: min(len(part), 80)], cursor)
            if part_start < 0:
                part_start = cursor
            part_end = part_start + len(part)
            blocks.append(
                EvidenceBlock(
                    block_id=f"b{len(blocks) + 1:04d}",
                    text=part,
                    char_start=part_start,
                    char_end=part_end,
                )
            )
            cursor = part_end
    return blocks


def _split_long_block(text: str, *, max_block_chars: int) -> list[str]:
    if len(text) <= max_block_chars:
        return [text]
    sentences = re.split(r"(?<=[.!?。！？])\s+", text)
    chunks: list[str] = []
    current = ""
    for sentence in sentences:
        if current and len(current) + len(sentence) + 1 > max_block_chars:
            chunks.append(current.strip())
            current = sentence
        else:
            current = f"{current} {sentence}".strip()
    if current:
        chunks.append(current.strip())
    return chunks or [text[:max_block_chars]]


def compact_evidence_for_terms(
    blocks: list[EvidenceBlock],
    terms: list[str],
    *,
    max_total_chars: int = 80_000,
    neighbor_count: int = 1,
) -> list[dict[str, Any]]:
    if sum(len(block.text) for block in blocks) <= max_total_chars:
        return [block.to_dict() for block in blocks]

    normalized_terms = [normalize_text(term) for term in terms if normalize_text(term)]
    selected_indexes: set[int] = set()
    for index, block in enumerate(blocks):
        text = normalize_text(block.text)
        if any(term and term in text for term in normalized_terms):
            for neighbor in range(index - neighbor_count, index + neighbor_count + 1):
                if 0 <= neighbor < len(blocks):
                    selected_indexes.add(neighbor)

    selected_indexes.update(range(min(3, len(blocks))))
    ordered: list[dict[str, Any]] = []
    total_chars = 0
    for index in sorted(selected_indexes):
        block = blocks[index]
        if total_chars + len(block.text) > max_total_chars and ordered:
            break
        ordered.append(block.to_dict())
        total_chars += len(block.text)
    return ordered


def validation_report(data: dict[str, Any], schema_spec: SchemaSpec | None = None) -> dict[str, Any]:
    schema = schema_spec or load_schema_spec()
    issues: list[dict[str, Any]] = []
    for section in schema.sections:
        if section not in data:
            issues.append(_issue("missing_section", section, "section is missing", severity="error"))
        elif not isinstance(data.get(section), list):
            issues.append(_issue("invalid_section_type", section, "section must be a list", severity="error"))

    payload = ensure_schema(data, schema)
    _check_unique_ids(payload, "alloys", "alloy_id", issues)
    _check_unique_ids(payload, "processes", "process_id", issues)
    _check_unique_ids(payload, "samples", "sample_id", issues)
    _check_unique_ids(payload, "structures", "structure_id", issues)
    _check_unique_ids(payload, "properties", "property_set_id", issues)

    alloy_ids = _ids(payload["alloys"], "alloy_id")
    process_ids = _ids(payload["processes"], "process_id")
    sample_ids = _ids(payload["samples"], "sample_id")

    for index, sample in enumerate(payload["samples"]):
        if not isinstance(sample, dict):
            issues.append(_issue("invalid_record_type", f"samples[{index}]", "sample record must be an object", severity="error"))
            continue
        _check_ref(sample, "alloy_id", alloy_ids, f"samples[{index}].alloy_id", issues)
        _check_ref(sample, "process_id", process_ids, f"samples[{index}].process_id", issues)

    for section in schema.sample_linked_sections:
        for index, record in enumerate(payload[section]):
            if not isinstance(record, dict):
                issues.append(_issue("invalid_record_type", f"{section}[{index}]", "record must be an object", severity="error"))
                continue
            _check_optional_ref(record, "sample_id", sample_ids, f"{section}[{index}].sample_id", issues)

    empty_paths = []
    for section in schema.sections:
        for index, record in enumerate(payload[section]):
            for path, value in _walk_leaves(record):
                if isinstance(value, str) and normalize_text(value) in {"", "none", "null", "na", "n/a"}:
                    empty_paths.append(f"{section}[{index}].{path}")
    if empty_paths:
        issues.append(
            {
                "issue_type": "empty_string_values",
                "path": "*",
                "message": f"{len(empty_paths)} empty-like string values found",
                "severity": "warning",
                "examples": empty_paths[:20],
            }
        )

    return {
        "ok": not any(item.get("severity") == "error" for item in issues),
        "issue_count": len(issues),
        "error_count": sum(1 for item in issues if item.get("severity") == "error"),
        "warning_count": sum(1 for item in issues if item.get("severity") == "warning"),
        "issues": issues,
    }


def _issue(issue_type: str, path: str, message: str, *, severity: str) -> dict[str, Any]:
    return {"issue_type": issue_type, "path": path, "message": message, "severity": severity}


def _ids(records: list[Any], key: str) -> set[str]:
    return {str(record.get(key)) for record in records if isinstance(record, dict) and record.get(key)}


def _check_unique_ids(data: dict[str, Any], section: str, id_key: str, issues: list[dict[str, Any]]) -> None:
    seen: dict[str, int] = {}
    for index, record in enumerate(data[section]):
        if not isinstance(record, dict):
            continue
        value = record.get(id_key)
        if not value:
            continue
        text = str(value)
        if text in seen:
            issues.append(
                _issue(
                    "duplicate_id",
                    f"{section}[{index}].{id_key}",
                    f"duplicate {id_key}: {text}",
                    severity="error",
                )
            )
        seen[text] = index


def _check_ref(record: dict[str, Any], key: str, valid_ids: set[str], path: str, issues: list[dict[str, Any]]) -> None:
    value = record.get(key)
    if not value:
        issues.append(_issue("missing_reference", path, f"{key} is missing", severity="error"))
    elif str(value) not in valid_ids:
        issues.append(_issue("broken_reference", path, f"{key} does not exist: {value}", severity="error"))


def _check_optional_ref(record: dict[str, Any], key: str, valid_ids: set[str], path: str, issues: list[dict[str, Any]]) -> None:
    value = record.get(key)
    if value and str(value) not in valid_ids:
        issues.append(_issue("broken_reference", path, f"{key} does not exist: {value}", severity="error"))


def _walk_leaves(node: Any, prefix: str = ""):
    if isinstance(node, dict):
        for key, value in node.items():
            next_prefix = f"{prefix}.{key}" if prefix else str(key)
            yield from _walk_leaves(value, next_prefix)
    elif isinstance(node, list):
        for index, value in enumerate(node):
            next_prefix = f"{prefix}[{index}]"
            yield from _walk_leaves(value, next_prefix)
    else:
        yield prefix, node


def sample_terms(sample_bundle: dict[str, Any]) -> list[str]:
    terms: list[str] = []
    for key in ("sample_id", "alloy_id", "process_id"):
        value = sample_bundle.get("sample", {}).get(key)
        if value:
            terms.append(str(value))
    alloy = sample_bundle.get("alloy") or {}
    terms.extend(str(item) for item in [alloy.get("alloy_name"), *alloy.get("aliases", [])] if item)
    process = sample_bundle.get("process") or {}
    terms.extend(str(item) for item in [process.get("description"), process.get("process_id")] if item)
    return terms


class SharedLLMClient:
    def __init__(self, settings: SharedLLMSettings) -> None:
        self.settings = settings
        self.endpoint = _chat_completions_url(settings.base_url)

    def complete_json(self, *, system: str, prompt: str) -> dict[str, Any]:
        last_error: Exception | None = None
        for attempt in range(max(1, self.settings.max_retries)):
            try:
                raw = self.complete(system=system, prompt=prompt)
                return extract_json(raw)
            except Exception as exc:
                last_error = exc
                if attempt + 1 >= max(1, self.settings.max_retries):
                    break
                time.sleep(2 + attempt * 4)
        raise RuntimeError(f"LLM JSON completion failed after {self.settings.max_retries} attempts: {last_error}")

    def complete(self, *, system: str, prompt: str) -> str:
        payload = {
            "model": self.settings.model,
            "temperature": self.settings.temperature,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
        }
        req = request.Request(
            self.endpoint,
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.settings.api_key or 'EMPTY'}",
            },
        )
        try:
            context = None if self.settings.verify_ssl else ssl._create_unverified_context()
            with request.urlopen(req, timeout=240, context=context) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"HTTP {exc.code}: {detail}") from exc
        except error.URLError as exc:
            raise RuntimeError(f"Network error: {exc.reason}") from exc
        except (OSError, IncompleteRead) as exc:
            raise RuntimeError(f"Network read error: {exc}") from exc
        content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        if not isinstance(content, str) or not content.strip():
            raise RuntimeError(f"Empty completion content: {json.dumps(data, ensure_ascii=False)[:1000]}")
        return content


def extract_json(text: str) -> dict[str, Any]:
    candidate = text.strip()
    if candidate.startswith("```"):
        lines = candidate.splitlines()
        if len(lines) >= 3:
            candidate = "\n".join(lines[1:-1]).strip()
            if candidate.startswith("json\n"):
                candidate = candidate[5:].strip()
    return json.loads(candidate)


def _chat_completions_url(base_url: str) -> str:
    normalized = base_url.rstrip("/")
    if normalized.endswith("/chat/completions"):
        return normalized
    parsed = parse.urlparse(normalized)
    path = parsed.path.rstrip("/")
    if path.endswith("/v1"):
        new_path = f"{path}/chat/completions"
    elif path:
        new_path = f"{path}/chat/completions"
    else:
        new_path = "/chat/completions"
    return parse.urlunparse(parsed._replace(path=new_path))


def normalized_record_signature(record: Any) -> str:
    return normalize_identifier(json.dumps(record, ensure_ascii=False, sort_keys=True))
