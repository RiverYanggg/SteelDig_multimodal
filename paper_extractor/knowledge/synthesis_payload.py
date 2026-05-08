import json
import re
from typing import Any, Dict, Iterable, List, Tuple


CORE_BUCKET_ORDER = [
    "material_system",
    "processing",
    "structure",
    "properties",
    "mechanisms",
    "characterization",
]

MAX_ITEMS_PER_BUCKET = {
    "material_system": 8,
    "processing": 12,
    "structure": 12,
    "properties": 10,
    "mechanisms": 10,
    "characterization": 6,
}

CLAIM_TYPE_BUCKET_KEYWORDS = {
    "material_system": ("material", "composition", "alloy", "design"),
    "processing": ("process", "processing", "rolling", "heat_treatment", "homogenization", "cooling"),
    "structure": ("microstructure", "phase", "fracture_mode", "fracture_analysis", "phase_identification"),
    "properties": ("property", "tensile", "strength", "elongation", "hardness", "density"),
    "mechanisms": ("mechanism", "kinetics", "failure"),
    "characterization": ("characterization",),
}

NOISE_CLAIM_TYPE_KEYWORDS = (
    "specimen_preparation",
    "equipment",
    "apparatus",
)


def build_synthesis_payload(
    paper_map: Dict[str, Any],
    claims: Iterable[Dict[str, Any]] | None,
    visual_evidence: List[Dict[str, Any]] | None = None,
) -> Dict[str, Any]:
    safe_paper_map = paper_map if isinstance(paper_map, dict) else {}
    selected = _select_claims([claim for claim in (claims or []) if isinstance(claim, dict)])
    grouped = _group_claims(selected)
    trimmed_visual = _trim_visual_evidence([item for item in (visual_evidence or []) if isinstance(item, dict)])
    return {
        "paper_focus": {
            "title": safe_paper_map.get("title"),
            "research_objective": safe_paper_map.get("research_objective"),
            "material_systems": _safe_list(safe_paper_map.get("material_systems")),
            "main_process_variables": _safe_list(safe_paper_map.get("main_process_variables")),
            "expected_information_axis": _safe_list(safe_paper_map.get("expected_information_axis")),
        },
        "core_facts": grouped,
        "visual_evidence": trimmed_visual,
    }


def _select_claims(claims: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    deduped: Dict[Tuple[str, str], Dict[str, Any]] = {}
    for claim in claims:
        if not isinstance(claim, dict):
            continue
        compact = _compact_claim(claim)
        if compact is None:
            continue
        key = (_normalize_text(compact["subject"]), _normalize_text(compact["claim"]))
        current = deduped.get(key)
        if current is None or compact["_score"] > current["_score"]:
            deduped[key] = compact

    ordered = sorted(deduped.values(), key=lambda item: (-item["_score"], item["section"], item["id"]))
    bucket_counts = {bucket: 0 for bucket in CORE_BUCKET_ORDER}
    kept: List[Dict[str, Any]] = []
    for item in ordered:
        bucket = item["topic"]
        limit = MAX_ITEMS_PER_BUCKET[bucket]
        if bucket_counts[bucket] >= limit:
            continue
        bucket_counts[bucket] += 1
        kept.append(_strip_private_fields(item))
    return kept


def _compact_claim(claim: Dict[str, Any]) -> Dict[str, Any] | None:
    claim_type = str(claim.get("claim_type") or "").strip()
    subject = _clean_text(str(claim.get("subject") or ""))
    claim_text = _clean_text(str(claim.get("claim") or ""))
    section = _clean_text(str(claim.get("section") or "Unknown"))
    if not claim_text:
        return None

    validation_status = str(claim.get("validation_status") or "")
    confidence = str(claim.get("confidence") or "low").lower()
    refs = _merge_refs(claim.get("figures"), claim.get("tables"))
    bucket = _bucket_for_claim(claim_type, subject, claim_text)
    if bucket is None:
        return None

    # 这一部分的用处是什么？Bucket的分类依据是什么？写死的吗？
    if _is_noise_claim(claim_type, subject, claim_text, bucket):
        return None

    support_direct = validation_status == "matched"
    if not support_direct and confidence == "low" and not refs and bucket == "characterization":
        return None
    if not support_direct and confidence == "low" and bucket not in {"processing", "structure", "properties", "mechanisms"}:
        return None

    evidence_short = _compress_evidence(
        _clean_text(str(claim.get("evidence_text") or "")),
        claim_text=claim_text,
    )
    score = _score_claim(bucket=bucket, confidence=confidence, support_direct=support_direct, refs=refs)

    payload = {
        "id": str(claim.get("claim_id") or ""),
        "section": section,
        "type": claim_type or "finding",
        "topic": bucket,
        "subject": subject,
        "claim": claim_text,
        "support": "direct" if support_direct else "weak",
        "refs": refs,
        "evidence": evidence_short,
        "_score": score,
    }
    if not payload["id"]:
        return None
    return payload


def _group_claims(claims: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    grouped: Dict[str, List[Dict[str, Any]]] = {bucket: [] for bucket in CORE_BUCKET_ORDER}
    for claim in claims:
        bucket = claim.get("topic")
        if bucket not in grouped:
            continue
        grouped[bucket].append(claim)
    return {bucket: grouped[bucket] for bucket in CORE_BUCKET_ORDER if grouped[bucket]}


def _trim_visual_evidence(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    trimmed = []
    for item in items:
        if not isinstance(item, dict):
            continue
        figure_id = _clean_text(str(item.get("figure_id") or ""))
        image_type = _clean_text(str(item.get("image_type") or ""))
        description = _clean_text(str(item.get("description") or ""))
        if not figure_id or not description:
            continue
        trimmed.append(
            {
                "figure_id": figure_id,
                "image_type": image_type,
                "description": _truncate(description, 220),
            }
        )
    return trimmed[:8]


def _bucket_for_claim(claim_type: str, subject: str, claim_text: str) -> str | None:
    text = " ".join([claim_type, subject, claim_text]).lower()
    for bucket, keywords in CLAIM_TYPE_BUCKET_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            return bucket
    # 这一部分可以结合到CLAIM_TYPE_BUCKET_KEYWORDS?
    if any(token in text for token in ("sem", "tem", "xrd", "ebsd")):
        return "characterization"
    return None


def _is_noise_claim(claim_type: str, subject: str, claim_text: str, bucket: str) -> bool:
    text = " ".join([claim_type, subject, claim_text]).lower()
    if any(keyword in text for keyword in NOISE_CLAIM_TYPE_KEYWORDS):
        return True
    if bucket == "characterization" and any(
        token in text for token in ("astm", "instron", "step scan", "cross head speed", "etched", "polished")
    ):
        return True
    return False


def _score_claim(bucket: str, confidence: str, support_direct: bool, refs: List[str]) -> int:
    bucket_bonus = {
        "material_system": 30,
        "processing": 28,
        "structure": 28,
        "properties": 28,
        "mechanisms": 26,
        "characterization": 12,
    }[bucket]
    confidence_bonus = {"high": 12, "medium": 7, "low": 0}.get(confidence, 0)
    support_bonus = 12 if support_direct else 0
    ref_bonus = 6 if refs else 0
    return bucket_bonus + confidence_bonus + support_bonus + ref_bonus


def _compress_evidence(evidence_text: str, claim_text: str) -> str:
    if not evidence_text:
        return ""
    if _normalize_text(evidence_text) == _normalize_text(claim_text):
        return ""
    return _truncate(evidence_text, 160)


def _merge_refs(figures: Any, tables: Any) -> List[str]:
    merged: List[str] = []
    for source in (figures, tables):
        if isinstance(source, list):
            items = source
        elif source:
            items = [source]
        else:
            items = []
        for item in items:
            cleaned = _clean_text(str(item))
            if cleaned and cleaned not in merged:
                merged.append(cleaned)
    return merged[:6]


def _strip_private_fields(claim: Dict[str, Any]) -> Dict[str, Any]:
    payload = {
        "id": str(claim.get("id") or ""),
        "section": str(claim.get("section") or "Unknown"),
        "type": str(claim.get("type") or "finding"),
        "subject": str(claim.get("subject") or ""),
        "claim": str(claim.get("claim") or ""),
        "support": str(claim.get("support") or "weak"),
    }
    if claim.get("refs"):
        payload["refs"] = claim["refs"]
    if claim.get("evidence"):
        payload["evidence"] = claim["evidence"]
    return payload


def _clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _safe_list(value: Any) -> List[Any]:
    return value if isinstance(value, list) else []


def _normalize_text(text: str) -> str:
    return re.sub(r"\W+", "", text.lower())


def _truncate(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    shortened = text[:limit].rsplit(" ", 1)[0].strip()
    return shortened + "..."
