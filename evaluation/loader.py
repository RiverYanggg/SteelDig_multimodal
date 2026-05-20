from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


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


@dataclass(frozen=True)
class PaperPair:
    paper_key: str
    truth_path: str
    prediction_path: str | None
    truth: dict[str, Any]
    prediction: dict[str, Any] | None


def load_paper_pairs(truth_dir: str | Path, prediction_root: str | Path) -> list[PaperPair]:
    truth_root = Path(truth_dir).expanduser().resolve()
    pred_root = Path(prediction_root).expanduser().resolve()
    pairs: list[PaperPair] = []

    for truth_path in sorted(truth_root.glob("*.json")):
        paper_key = truth_path.stem
        prediction_path = pred_root / paper_key / "final" / "text_extraction.json"
        prediction = _read_json(prediction_path) if prediction_path.exists() else None
        pairs.append(
            PaperPair(
                paper_key=paper_key,
                truth_path=str(truth_path),
                prediction_path=str(prediction_path) if prediction_path.exists() else None,
                truth=_ensure_schema(_read_json(truth_path)),
                prediction=_ensure_schema(prediction) if prediction is not None else None,
            )
        )
    return pairs


def detect_empty_prediction(data: dict[str, Any] | None) -> bool:
    if not data:
        return True
    return all(not data.get(section) for section in SECTIONS)


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _ensure_schema(data: dict[str, Any] | None) -> dict[str, Any]:
    payload = dict(data or {})
    for section in SECTIONS:
        payload.setdefault(section, [])
    return payload
