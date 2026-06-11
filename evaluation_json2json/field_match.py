from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from typing import Any

from evaluation.normalize import normalize_text


@dataclass(frozen=True)
class MatchResult:
    matched: bool
    method: str
    truth_normalized: str
    prediction_normalized: str
    reason: str
    score: float = 1.0
    needs_llm_judge: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class Quantity:
    low: float
    high: float
    unit: str
    kind: str


_NUMBER = r"-?\d+(?:\.\d+)?"
_RANGE_RE = re.compile(rf"(?P<a>{_NUMBER})\s*(?:-|~|to)\s*(?P<b>{_NUMBER})\s*(?P<unit>[a-zA-Z%°℃μµ/³^0-9.-]+)?")
_SCALAR_RE = re.compile(rf"(?P<value>{_NUMBER})\s*(?P<unit>[a-zA-Z%°℃μµ/³^0-9.-]+)?")

_UNIT_ALIASES = {
    "": "",
    "c": "C",
    "°c": "C",
    "℃": "C",
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
    "second": "s",
    "seconds": "s",
    "%": "%",
    "pct": "%",
    "percent": "%",
    "mpa": "MPa",
    "gpa": "GPa",
    "pa": "Pa",
    "hv": "HV",
    "um": "um",
    "μm": "um",
    "µm": "um",
    "nm": "nm",
    "mm": "mm",
    "m": "m",
    "g/cm^3": "g/cm^3",
    "g/cm³": "g/cm^3",
    "mg/cm^2": "mg/cm^2",
    "mg/cm²": "mg/cm^2",
    "mj/m^2": "mJ/m^2",
    "mj/m²": "mJ/m^2",
}

_BASE_UNITS = {
    "temperature": "C",
    "duration": "h",
    "stress": "MPa",
    "length": "um",
    "percent": "%",
    "hardness": "HV",
    "density": "g/cm^3",
    "mass_gain": "mg/cm^2",
    "energy_density": "mJ/m^2",
    "number": "",
}

_LABEL_SYNONYMS = {
    "bal": "balance",
    "balance": "balance",
    "balanced": "balance",
    "ys": "yield_strength",
    "yield strength": "yield_strength",
    "yield stress": "yield_strength",
    "ultimate tensile strength": "ultimate_tensile_strength",
    "uts": "ultimate_tensile_strength",
    "tensile strength": "ultimate_tensile_strength",
    "elongation": "elongation",
    "total elongation": "elongation",
    "water quench": "water_quench",
    "water quenched": "water_quench",
    "water quenching": "water_quench",
    "wq": "water_quench",
    "air cooling": "air_cooling",
    "air cooled": "air_cooling",
    "ac": "air_cooling",
    "solution treatment": "solution_treatment",
    "solution treated": "solution_treatment",
    "solution-treatment": "solution_treatment",
    "aging": "aging",
    "aged": "aging",
    "cold rolling": "cold_rolling",
    "cold rolled": "cold_rolling",
    "hot rolling": "hot_rolling",
    "hot rolled": "hot_rolling",
    "homogenization": "homogenization",
    "homogenized": "homogenization",
    "austenite": "austenite",
    "gamma": "austenite",
    "gamma phase": "austenite",
    "γ": "austenite",
    "γ phase": "austenite",
    "ferrite": "ferrite",
    "alpha": "ferrite",
    "alpha phase": "ferrite",
    "α": "ferrite",
    "α phase": "ferrite",
    "kappa carbide": "kappa_carbide",
    "k-carbide": "kappa_carbide",
    "κ-carbide": "kappa_carbide",
    "κ carbide": "kappa_carbide",
}


def match_field_value(key: str, truth_value: Any, pred_value: Any, field_rules: dict[str, Any]) -> MatchResult:
    truth_text = normalize_text(truth_value)
    pred_text = normalize_text(pred_value)
    if truth_text == pred_text:
        return MatchResult(True, "normalized_exact", truth_text, pred_text, "normalized strings are identical")

    field_type = infer_field_type(key, truth_text, pred_text)
    if field_type == "semantic_text":
        return MatchResult(
            False,
            "llm_judge_required",
            truth_text,
            pred_text,
            "long or semantic text differs after deterministic normalization",
            score=0.0,
            needs_llm_judge=True,
        )

    if field_type in _BASE_UNITS:
        result = _match_quantity(truth_text, pred_text, field_type, _tolerance_for_key(key, field_rules))
        if result is not None:
            return result

    if field_type in _BASE_UNITS or field_type in {"label", "phase_label", "process_label", "property_label", "unit_label"}:
        truth_label = canonical_label(truth_text)
        pred_label = canonical_label(pred_text)
        if truth_label and truth_label == pred_label:
            return MatchResult(True, f"{field_type}_synonym", truth_label, pred_label, "canonical labels are identical")

    if _is_long_text_key(key):
        return MatchResult(
            False,
            "llm_judge_required",
            truth_text,
            pred_text,
            "long or semantic text differs after deterministic normalization",
            score=0.0,
            needs_llm_judge=True,
        )

    return MatchResult(False, "deterministic_mismatch", truth_text, pred_text, "no deterministic matcher accepted the values", score=0.0)


def infer_field_type(key: str, truth_text: str, pred_text: str) -> str:
    lowered = key.lower()
    if _is_long_text_key(lowered):
        return "semantic_text"
    if any(marker in lowered for marker in ("alloy_name", "title", "journal", "doi", "paper_id", "sample_id", "alloy_id", "process_id")):
        return "label"
    if "temperature" in lowered:
        return "temperature"
    if "duration" in lowered or "time" in lowered:
        return "duration"
    if "reduction_ratio" in lowered or "percent" in lowered or "fraction" in lowered:
        return "percent"
    if "weight_percent" in lowered or "atomic_percent" in lowered:
        return "percent"
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
    unit_kind = _kind_from_unit_text(f"{truth_text} {pred_text}")
    if unit_kind:
        return unit_kind
    if "unit" in lowered:
        return "unit_label"
    if "phase_name" in lowered or "phase_1_name" in lowered or "phase_2_name" in lowered:
        return "phase_label"
    if "cooling_medium" in lowered or ".method" in lowered or ".type" in lowered:
        return "process_label"
    if "property" in lowered and ("name" in lowered or "type" in lowered):
        return "property_label"
    return "label"


def _kind_from_unit_text(text: str) -> str | None:
    normalized = normalize_text(text)
    units = { _canonical_unit(match.group("unit") or "") for match in _SCALAR_RE.finditer(normalized) }
    if units & {"GPa", "MPa", "Pa"}:
        return "stress"
    if units & {"um", "nm", "mm", "m"}:
        return "length"
    if units & {"h", "min", "s"}:
        return "duration"
    if units & {"C", "K"}:
        return "temperature"
    if units & {"%"}:
        return "percent"
    if units & {"HV"}:
        return "hardness"
    if units & {"g/cm^3"}:
        return "density"
    if units & {"mg/cm^2"}:
        return "mass_gain"
    if units & {"mJ/m^2"}:
        return "energy_density"
    return None


def canonical_label(value: Any) -> str:
    text = normalize_text(value)
    text = text.replace("γ", " gamma ").replace("α", " alpha ").replace("κ", " kappa ")
    text = re.sub(r"[_/]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip(" -")
    if text in _LABEL_SYNONYMS:
        return _LABEL_SYNONYMS[text]
    singular = text[:-1] if text.endswith("s") else text
    if singular in _LABEL_SYNONYMS:
        return _LABEL_SYNONYMS[singular]
    return re.sub(r"[^a-z0-9]+", "_", text).strip("_")


def _match_quantity(truth_text: str, pred_text: str, kind: str, tolerance: dict[str, float]) -> MatchResult | None:
    truth_quantity = parse_quantity(truth_text, kind)
    pred_quantity = parse_quantity(pred_text, kind)
    if truth_quantity is None or pred_quantity is None:
        return None
    if truth_quantity.kind != pred_quantity.kind:
        return MatchResult(False, "quantity_kind_mismatch", _format_quantity(truth_quantity), _format_quantity(pred_quantity), "quantity kinds differ", score=0.0)

    abs_tol = float(tolerance.get("abs", 0.0))
    rel_tol = float(tolerance.get("rel", 0.0))
    low_tol = max(abs_tol, abs(truth_quantity.low) * rel_tol)
    high_tol = max(abs_tol, abs(truth_quantity.high) * rel_tol)
    matched = abs(truth_quantity.low - pred_quantity.low) <= low_tol and abs(truth_quantity.high - pred_quantity.high) <= high_tol
    return MatchResult(
        matched,
        "quantity_with_unit",
        _format_quantity(truth_quantity),
        _format_quantity(pred_quantity),
        f"compared as {kind} with abs_tol={abs_tol}, rel_tol={rel_tol}",
        score=1.0 if matched else 0.0,
    )


def parse_quantity(value: Any, kind: str) -> Quantity | None:
    text = normalize_text(value)
    if not text or text in {"balance", "bal"}:
        return None
    match = _RANGE_RE.search(text)
    if match:
        low = float(match.group("a"))
        high = float(match.group("b"))
        unit = _canonical_unit(match.group("unit") or _default_unit(kind))
        return _to_base_quantity(min(low, high), max(low, high), unit, kind)
    match = _SCALAR_RE.search(text)
    if not match:
        return None
    number = float(match.group("value"))
    unit = _canonical_unit(match.group("unit") or _default_unit(kind))
    return _to_base_quantity(number, number, unit, kind)


def _to_base_quantity(low: float, high: float, unit: str, kind: str) -> Quantity:
    base = _BASE_UNITS.get(kind, "")
    if kind == "temperature" and unit == "K":
        return Quantity(low - 273.15, high - 273.15, base, kind)
    factor = _conversion_factor(unit, base)
    return Quantity(low * factor, high * factor, base, kind)


def _conversion_factor(unit: str, base: str) -> float:
    if unit == base or not base:
        return 1.0
    table = {
        ("min", "h"): 1 / 60,
        ("s", "h"): 1 / 3600,
        ("GPa", "MPa"): 1000,
        ("Pa", "MPa"): 1 / 1_000_000,
        ("nm", "um"): 1 / 1000,
        ("mm", "um"): 1000,
        ("m", "um"): 1_000_000,
    }
    return table.get((unit, base), 1.0)


def _canonical_unit(value: str) -> str:
    text = normalize_text(value).replace(" ", "")
    return _UNIT_ALIASES.get(text, text)


def _default_unit(kind: str) -> str:
    return _BASE_UNITS.get(kind, "")


def _tolerance_for_key(key: str, field_rules: dict[str, Any]) -> dict[str, float]:
    tolerances = field_rules.get("numeric_tolerances", {})
    chosen = tolerances.get("default", {"abs": 0.0, "rel": 0.0})
    for pattern, tolerance in tolerances.items():
        if pattern == "default":
            continue
        if _pattern_matches(pattern, key):
            chosen = tolerance
            break
    return chosen


def _pattern_matches(pattern: str, key: str) -> bool:
    normalized_pattern = pattern.replace("[*]", "").replace("*", "")
    normalized_key = re.sub(r"\[\d+\]", "", key)
    return normalized_pattern in normalized_key


def _format_quantity(quantity: Quantity) -> str:
    if quantity.low == quantity.high:
        return f"{quantity.low:g} {quantity.unit}".strip()
    return f"{quantity.low:g}-{quantity.high:g} {quantity.unit}".strip()


def _contains_number(value: str) -> bool:
    return bool(_SCALAR_RE.search(value))


def _is_long_text_key(key: str) -> bool:
    return any(
        marker in key
        for marker in (
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
        )
    )
