import hashlib
import json
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List

from paper_extractor.knowledge.chunker import Chunk


def normalize_claims(raw_records: Iterable[Dict[str, Any]], chunks: List[Chunk]) -> tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    chunk_map = {chunk.chunk_id: chunk for chunk in chunks}
    normalized: List[Dict[str, Any]] = []
    warnings: List[Dict[str, Any]] = []
    seen = set()

    for record in raw_records:
        chunk_id = str(record.get("chunk_id", ""))
        chunk = chunk_map.get(chunk_id)
        for raw_claim in record.get("claims", []):
            if not isinstance(raw_claim, dict):
                continue
            claim_text = _clean(str(raw_claim.get("claim", "")))
            evidence_text = _clean(str(raw_claim.get("evidence_text", "")))
            if not claim_text:
                continue
            fingerprint = _fingerprint(claim_text)
            if fingerprint in seen:
                continue
            seen.add(fingerprint)

            evidence_start = -1
            evidence_end = -1
            validation_status = "missing_chunk"
            if chunk:
                evidence_start = _find_evidence(chunk.text, evidence_text)
                if evidence_start >= 0:
                    evidence_end = evidence_start + len(evidence_text)
                    validation_status = "matched"
                elif evidence_text:
                    validation_status = "evidence_not_found"
                else:
                    validation_status = "missing_evidence"

            confidence = str(raw_claim.get("confidence") or "medium").lower()
            if confidence not in {"high", "medium", "low"}:
                confidence = "medium"
            if validation_status != "matched":
                confidence = "low"
                warnings.append(
                    {
                        "chunk_id": chunk_id,
                        "claim": claim_text,
                        "validation_status": validation_status,
                        "evidence_text": evidence_text,
                    }
                )

            normalized.append(
                {
                    "claim_id": f"c_{len(normalized) + 1:05d}",
                    "paper_id": record.get("paper_id"),
                    "chunk_id": chunk_id,
                    "section": record.get("section"),
                    "claim_type": _clean(str(raw_claim.get("claim_type", "finding"))) or "finding",
                    "subject": _clean(str(raw_claim.get("subject", ""))),
                    "claim": claim_text,
                    "values": _string_list(raw_claim.get("values")),
                    "figures": _string_list(raw_claim.get("figures")),
                    "tables": _string_list(raw_claim.get("tables")),
                    "evidence_text": evidence_text,
                    "evidence_char_start_in_chunk": evidence_start,
                    "evidence_char_end_in_chunk": evidence_end,
                    "confidence": confidence,
                    "validation_status": validation_status,
                }
            )

    return normalized, warnings


def write_claims_jsonl(path: Path, claims: Iterable[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for claim in claims:
            f.write(json.dumps(claim, ensure_ascii=False) + "\n")


def _find_evidence(chunk_text: str, evidence_text: str) -> int:
    if not evidence_text:
        return -1
    exact = chunk_text.find(evidence_text)
    if exact >= 0:
        return exact
    normalized_chunk = _space_normalize(chunk_text)
    normalized_evidence = _space_normalize(evidence_text)
    normalized_index = normalized_chunk.find(normalized_evidence)
    if normalized_index < 0:
        return -1
    return _approx_original_offset(chunk_text, normalized_index)


def _approx_original_offset(text: str, normalized_index: int) -> int:
    count = 0
    in_space = False
    for index, char in enumerate(text):
        if char.isspace():
            if not in_space:
                if count == normalized_index:
                    return index
                count += 1
                in_space = True
            continue
        in_space = False
        if count == normalized_index:
            return index
        count += 1
    return -1


def _space_normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _clean(text: str) -> str:
    text = text.replace("\u0004", " ").replace("\u0001", " ")
    return re.sub(r"\s+", " ", text).strip()


def _string_list(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [_clean(str(item)) for item in value if _clean(str(item))]
    text = _clean(str(value))
    return [text] if text else []


def _fingerprint(text: str) -> str:
    normalized = re.sub(r"\W+", "", text.lower())
    return hashlib.sha1(normalized.encode("utf-8")).hexdigest()

