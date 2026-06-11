from __future__ import annotations

import copy
import json
import math
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


_NUMBER = r"-?\d+(?:\.\d+)?"
_SCALAR_WITH_UNIT_RE = re.compile(
    rf"^\s*(?P<value>{_NUMBER})\s*(?P<unit>[a-zA-Z%°℃μµ/³²^0-9./·*\-\s]+)?\s*$"
)
_RANGE_WITH_UNIT_RE = re.compile(
    rf"^\s*(?P<low>{_NUMBER})\s*(?:-|–|—|~|to)\s*(?P<high>{_NUMBER})\s*"
    rf"(?P<unit>[a-zA-Z%°℃μµ/³²^0-9./·*\-\s]+)?\s*$",
    re.IGNORECASE,
)

_UNIT_ALIASES = {
    "": "",
    "c": "°C",
    "°c": "°C",
    "℃": "°C",
    "k": "K",
    "h": "h",
    "hr": "h",
    "hrs": "h",
    "hour": "h",
    "hours": "h",
    "min": "min",
    "mins": "min",
    "minute": "min",
    "minutes": "min",
    "s": "s",
    "sec": "s",
    "secs": "s",
    "second": "s",
    "seconds": "s",
    "%": "%",
    "pct": "%",
    "percent": "%",
    "wt%": "%",
    "wt.%": "%",
    "at%": "%",
    "at.%": "%",
    "mpa": "MPa",
    "gpa": "GPa",
    "pa": "Pa",
    "hv": "HV",
    "um": "μm",
    "μm": "μm",
    "µm": "μm",
    "nm": "nm",
    "mm": "mm",
    "m": "m",
    "g/cm3": "g/cm^3",
    "g/cm^3": "g/cm^3",
    "g/cm³": "g/cm^3",
    "mg/cm2": "mg/cm^2",
    "mg/cm^2": "mg/cm^2",
    "mg/cm²": "mg/cm^2",
    "mj/m2": "mJ/m^2",
    "mj/m^2": "mJ/m^2",
    "mj/m²": "mJ/m^2",
    "mpa.m^0.5": "MPa·m^0.5",
    "mpa·m^0.5": "MPa·m^0.5",
    "mpa*m^0.5": "MPa·m^0.5",
    "mpam^1/2": "MPa·m^0.5",
    "mpa√m": "MPa·m^0.5",
    "s-1": "s^-1",
    "s^-1": "s^-1",
    "1/s": "s^-1",
}

_BASE_UNITS = {
    "temperature": "°C",
    "duration": "h",
    "stress": "MPa",
    "length": "μm",
    "percent": "%",
    "hardness": "HV",
    "density": "g/cm^3",
    "mass_gain": "mg/cm^2",
    "energy_density": "mJ/m^2",
    "fracture_toughness": "MPa·m^0.5",
    "rate": "s^-1",
}

_CONVERSION_FACTORS = {
    ("min", "h"): 1 / 60,
    ("s", "h"): 1 / 3600,
    ("GPa", "MPa"): 1000,
    ("Pa", "MPa"): 1 / 1_000_000,
    ("nm", "μm"): 1 / 1000,
    ("mm", "μm"): 1000,
    ("m", "μm"): 1_000_000,
}

_LONG_TEXT_MARKERS = (
    "description",
    "notes",
    "scope",
    "overall_structure",
    "application_relevance",
    "findings",
    "purpose",
    "morphology",
    "phase_evolution",
    "mechanism",
    "model_note",
    "parameters",
    "caption",
)


@dataclass(frozen=True)
class UnitNormalizationResult:
    paper_id: str
    source_path: Path
    normalized_path: Path
    report_path: Path
    converted_count: int
    unchanged_count: int
    skipped_count: int
    ambiguous_count: int


@dataclass(frozen=True)
class ParsedQuantity:
    low: float
    high: float
    unit: str
    is_range: bool


def run_unit_normalization(
    dataset_root: str | Path,
    *,
    paper_ids: str | list[str] | None = None,
    force: bool = False,
) -> list[UnitNormalizationResult]:
    root = Path(dataset_root).expanduser().resolve()
    results = []
    for paper_dir in _select_paper_dirs(root, paper_ids):
        results.append(run_unit_normalization_for_paper(paper_dir, force=force))
    return results


def run_unit_normalization_for_paper(
    paper_dir: str | Path,
    *,
    force: bool = False,
) -> UnitNormalizationResult:
    paper_path = Path(paper_dir).expanduser().resolve()
    paper_id = paper_path.name
    source_path = paper_path / "final" / "text_extraction.json"
    normalized_dir = paper_path / "normalized"
    normalized_path = normalized_dir / "text_extraction_units.json"
    report_path = normalized_dir / "unit_normalization_report.json"

    if normalized_path.exists() and report_path.exists() and not force:
        report = _read_json(report_path)
        summary = report.get("summary", {})
        return UnitNormalizationResult(
            paper_id=paper_id,
            source_path=source_path,
            normalized_path=normalized_path,
            report_path=report_path,
            converted_count=int(summary.get("converted_count", 0)),
            unchanged_count=int(summary.get("unchanged_count", 0)),
            skipped_count=int(summary.get("skipped_count", 0)),
            ambiguous_count=int(summary.get("ambiguous_count", 0)),
        )

    if not source_path.is_file():
        raise FileNotFoundError(f"missing final text_extraction.json: {source_path}")

    source = _read_json(source_path)
    normalized, report = normalize_units(source, paper_id=paper_id, source_path=source_path)
    _write_json(normalized, normalized_path)
    _write_json(report, report_path)
    summary = report["summary"]
    return UnitNormalizationResult(
        paper_id=paper_id,
        source_path=source_path,
        normalized_path=normalized_path,
        report_path=report_path,
        converted_count=int(summary["converted_count"]),
        unchanged_count=int(summary["unchanged_count"]),
        skipped_count=int(summary["skipped_count"]),
        ambiguous_count=int(summary["ambiguous_count"]),
    )


def normalize_units(
    data: dict[str, Any],
    *,
    paper_id: str | None = None,
    source_path: str | Path | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    working = copy.deepcopy(data)
    changes: list[dict[str, Any]] = []
    _normalize_node(working, path="$", changes=changes)
    summary = {
        "converted_count": sum(1 for item in changes if item["status"] == "converted"),
        "unchanged_count": sum(1 for item in changes if item["status"] == "unchanged"),
        "skipped_count": sum(1 for item in changes if item["status"] == "skipped"),
        "ambiguous_count": sum(1 for item in changes if item["status"] == "ambiguous"),
    }
    report = {
        "paper_id": paper_id,
        "source_path": str(source_path) if source_path is not None else None,
        "target_unit_policy": _BASE_UNITS,
        "summary": summary,
        "changes": changes,
    }
    return working, report


def _normalize_node(node: Any, *, path: str, changes: list[dict[str, Any]]) -> None:
    if isinstance(node, dict):
        _normalize_quantity_object(node, path=path, changes=changes)
        for key, value in node.items():
            _normalize_node(value, path=f"{path}.{key}", changes=changes)
        return
    if isinstance(node, list):
        for index, value in enumerate(node):
            _normalize_node(value, path=f"{path}[{index}]", changes=changes)


def _normalize_quantity_object(node: dict[str, Any], *, path: str, changes: list[dict[str, Any]]) -> None:
    if _is_long_text_path(path):
        return

    quantity_keys = [key for key in ("value", "temperature", "min", "max") if key in node and not _is_empty(node.get(key))]
    if "unit" in node and quantity_keys:
        kind = _infer_kind(path, node.get("unit"))
        if kind is None:
            changes.append(_change(path, None, None, "ambiguous", "cannot infer quantity kind"))
        else:
            _normalize_structured_quantity(node, path=path, kind=kind, changes=changes)

    for field in ("duration", "reduction_ratio", "weight_percent", "atomic_percent"):
        if field not in node:
            continue
        kind = _infer_kind(f"{path}.{field}", None)
        if kind is None:
            continue
        _normalize_inline_field(node, field, path=f"{path}.{field}", kind=kind, changes=changes)


def _normalize_structured_quantity(
    node: dict[str, Any],
    *,
    path: str,
    kind: str,
    changes: list[dict[str, Any]],
) -> None:
    original_unit = node.get("unit")
    source_unit = _canonical_unit(original_unit)
    base_unit = _BASE_UNITS[kind]
    value_keys = [key for key in ("value", "temperature", "min", "max") if key in node]
    if not value_keys:
        return

    original = {"unit": original_unit, **{key: node.get(key) for key in value_keys}}
    if not source_unit:
        changes.append(_change(path, original, None, "ambiguous", "unit is empty"))
        return
    if source_unit == "HV" and kind == "hardness":
        node["unit"] = "HV"
        changes.append(_change(path, original, {"unit": node["unit"], **{key: node.get(key) for key in value_keys}}, "unchanged", "hardness scale normalized only"))
        return
    if source_unit != base_unit and not _can_convert(source_unit, base_unit, kind):
        changes.append(_change(path, original, None, "skipped", f"unsupported conversion {source_unit} -> {base_unit}", kind=kind))
        return

    converted: dict[str, Any] = {}
    for key in value_keys:
        value = node.get(key)
        if _is_empty(value):
            converted[key] = value
            continue
        parsed = _parse_quantity(value, source_unit)
        if parsed is None:
            changes.append(_change(f"{path}.{key}", {"value": value, "unit": original_unit}, None, "ambiguous", "cannot parse numeric value"))
            return
        low, high = _convert_pair(parsed.low, parsed.high, source_unit, base_unit, kind)
        converted[key] = _format_range(low, high) if parsed.is_range else _format_number(low)

    for key, value in converted.items():
        node[key] = value
    node["unit"] = base_unit
    status = "converted" if {"unit": node["unit"], **converted} != original else "unchanged"
    reason = f"normalized {kind} to {base_unit}" if status == "converted" else "already canonical"
    changes.append(_change(path, original, {"unit": node["unit"], **converted}, status, reason, kind=kind))


def _normalize_inline_field(
    node: dict[str, Any],
    field: str,
    *,
    path: str,
    kind: str,
    changes: list[dict[str, Any]],
) -> None:
    value = node.get(field)
    if _is_empty(value) or not isinstance(value, str):
        return
    if _is_long_text_path(path):
        return
    parsed = _parse_inline_quantity(value, kind)
    if parsed is None:
        return
    base_unit = _BASE_UNITS[kind]
    if parsed.unit != base_unit and not _can_convert(parsed.unit, base_unit, kind):
        changes.append(_change(path, value, None, "skipped", f"unsupported conversion {parsed.unit} -> {base_unit}", kind=kind))
        return
    low, high = _convert_pair(parsed.low, parsed.high, parsed.unit, base_unit, kind)
    normalized_value = f"{_format_range(low, high) if parsed.is_range else _format_number(low)} {base_unit}".strip()
    if normalized_value == value:
        changes.append(_change(path, value, normalized_value, "unchanged", "already canonical", kind=kind))
        return
    node[field] = normalized_value
    changes.append(_change(path, value, normalized_value, "converted", f"normalized {kind} to {base_unit}", kind=kind))


def _parse_inline_quantity(value: str, kind: str) -> ParsedQuantity | None:
    match = _RANGE_WITH_UNIT_RE.match(value)
    if match:
        if not match.group("unit"):
            return None
        unit = _canonical_unit(match.group("unit"))
        return ParsedQuantity(float(match.group("low")), float(match.group("high")), unit, True)
    match = _SCALAR_WITH_UNIT_RE.match(value)
    if not match:
        return None
    if not match.group("unit"):
        return None
    unit = _canonical_unit(match.group("unit"))
    return ParsedQuantity(float(match.group("value")), float(match.group("value")), unit, False)


def _parse_quantity(value: Any, source_unit: str) -> ParsedQuantity | None:
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        number = float(value)
        return ParsedQuantity(number, number, source_unit, False)
    if not isinstance(value, str):
        return None
    match = _RANGE_WITH_UNIT_RE.match(value)
    if match:
        unit = _canonical_unit(match.group("unit") or source_unit)
        if unit and unit != source_unit:
            return None
        return ParsedQuantity(float(match.group("low")), float(match.group("high")), source_unit, True)
    match = _SCALAR_WITH_UNIT_RE.match(value)
    if not match:
        return None
    unit = _canonical_unit(match.group("unit") or source_unit)
    if unit and unit != source_unit:
        return None
    number = float(match.group("value"))
    return ParsedQuantity(number, number, source_unit, False)


def _convert_pair(low: float, high: float, source_unit: str, base_unit: str, kind: str) -> tuple[float, float]:
    if kind == "temperature" and source_unit == "K" and base_unit == "°C":
        return low - 273.15, high - 273.15
    factor = _CONVERSION_FACTORS.get((source_unit, base_unit), 1.0)
    return low * factor, high * factor


def _can_convert(source_unit: str, base_unit: str, kind: str) -> bool:
    if source_unit == base_unit:
        return True
    if kind == "temperature" and source_unit == "K" and base_unit == "°C":
        return True
    return (source_unit, base_unit) in _CONVERSION_FACTORS


def _infer_kind(path: str, unit: Any) -> str | None:
    lowered = path.lower()
    if "temperature" in lowered:
        return "temperature"
    if "duration" in lowered or "time" in lowered or "lifetime" in lowered:
        return "duration"
    if "reduction_ratio" in lowered or "percent" in lowered or "fraction" in lowered or "elongation" in lowered:
        return "percent"
    if "weight_percent" in lowered or "atomic_percent" in lowered:
        return "percent"
    if "fracture_toughness" in lowered:
        return "fracture_toughness"
    if "strain_hardening_rate" in lowered:
        return "stress"
    if "strength" in lowered or "stress" in lowered or "modulus" in lowered:
        return "stress"
    if "grain_size" in lowered or "thickness" in lowered or "diameter" in lowered or "length" in lowered or "size" in lowered:
        return "length"
    if "hardness" in lowered:
        return "hardness"
    if "density" in lowered:
        return "density"
    if "weight_gain" in lowered or "mass_gain" in lowered:
        return "mass_gain"
    if "energy" in lowered and ("density" in lowered or "absorption" in lowered):
        return "energy_density"
    if "rate" in lowered:
        return "rate"

    canonical_unit = _canonical_unit(unit)
    if canonical_unit in {"°C", "K"}:
        return "temperature"
    if canonical_unit in {"GPa", "MPa", "Pa"}:
        return "stress"
    if canonical_unit in {"μm", "nm", "mm", "m"}:
        return "length"
    if canonical_unit in {"h", "min", "s"}:
        return "duration"
    if canonical_unit == "%":
        return "percent"
    if canonical_unit == "HV":
        return "hardness"
    if canonical_unit == "g/cm^3":
        return "density"
    if canonical_unit == "mg/cm^2":
        return "mass_gain"
    if canonical_unit == "mJ/m^2":
        return "energy_density"
    if canonical_unit == "MPa·m^0.5":
        return "fracture_toughness"
    if canonical_unit == "s^-1":
        return "rate"
    return None


def _canonical_unit(value: Any) -> str:
    if value is None:
        return ""
    text = str(value).strip()
    text = text.replace("−", "-").replace("⁻", "-").replace("¹", "1").replace("²", "2").replace("³", "3")
    compact = re.sub(r"\s+", "", text).lower()
    compact = compact.replace("·", ".").replace("*", ".")
    return _UNIT_ALIASES.get(compact, _UNIT_ALIASES.get(text.lower(), text))


def _format_number(value: float) -> str:
    if not math.isfinite(value):
        return str(value)
    if abs(value) < 1e-12:
        value = 0.0
    return f"{value:.12g}"


def _format_range(low: float, high: float) -> str:
    return f"{_format_number(min(low, high))}-{_format_number(max(low, high))}"


def _change(
    path: str,
    original: Any,
    normalized: Any,
    status: str,
    reason: str,
    *,
    kind: str | None = None,
) -> dict[str, Any]:
    return {
        "path": path,
        "quantity_kind": kind,
        "status": status,
        "reason": reason,
        "original": original,
        "normalized": normalized,
    }


def _is_long_text_path(path: str) -> bool:
    lowered = path.lower()
    return any(marker in lowered for marker in _LONG_TEXT_MARKERS)


def _is_empty(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return value.strip().lower() in {"", "none", "null", "na", "n/a"}
    return False


def _select_paper_dirs(root: Path, paper_ids: str | list[str] | None) -> list[Path]:
    if isinstance(paper_ids, str):
        selected = [item.strip() for item in paper_ids.split(",") if item.strip()]
        return [root / paper_id for paper_id in selected]
    if paper_ids:
        return [root / paper_id for paper_id in paper_ids]
    return sorted(path for path in root.iterdir() if (path / "final" / "text_extraction.json").is_file())


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _write_json(payload: Any, path: str | Path) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
