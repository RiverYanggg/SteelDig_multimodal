import json
import time
from typing import Any, Dict, List

from paper_extractor.common import extract_json_from_text
from paper_extractor.knowledge.chunker import Chunk
from paper_extractor.knowledge.prompts import build_claim_prompt, build_markdown_prompt, build_paper_map_prompt


class ExtractionParseError(ValueError):
    def __init__(self, message: str, raw_content: str):
        super().__init__(message)
        self.raw_content = raw_content


class ModelResponseError(RuntimeError):
    def __init__(self, message: str, raw_content: str = ""):
        super().__init__(message)
        self.raw_content = raw_content


def generate_paper_map(client: Any, model: str, paper_id: str, markdown_text: str) -> tuple[Dict[str, Any], str]:
    prompt = build_paper_map_prompt(paper_id=paper_id, markdown_text=markdown_text)
    content = _chat(client, model, "你是论文全局信息规划助手。", prompt)
    try:
        parsed = extract_json_from_text(content)
    except Exception as exc:
        raise ExtractionParseError(f"Cannot parse paper_map JSON: {exc}", content) from exc
    if not isinstance(parsed, dict):
        raise ExtractionParseError("paper_map output must be a JSON object.", content)
    return parsed, content


CONTEXT_UPDATE_KEYS = (
    "summary",
    "material_systems",
    "sample_aliases",
    "processing_route",
    "key_variables",
    "microstructure",
    "properties",
    "mechanisms",
    "figures_or_tables",
    "unresolved_terms",
)


def extract_chunk_claims(
    client: Any,
    model: str,
    paper_map: Dict[str, Any],
    chunk: Chunk,
    previous_context_summary: str = "",
) -> tuple[Dict[str, Any], str]:
    prompt = build_claim_prompt(
        paper_map=paper_map,
        chunk=chunk,
        previous_context_summary=previous_context_summary,
    )
    content = _chat(client, model, "你是论文局部事实抽取助手。", prompt)
    try:
        parsed = extract_json_from_text(content)
    except Exception as exc:
        raise ExtractionParseError(f"Cannot parse claim JSON for {chunk.chunk_id}: {exc}", content) from exc
    if not isinstance(parsed, dict):
        raise ExtractionParseError(f"claim output for {chunk.chunk_id} must be a JSON object.", content)
    claims = parsed.get("claims", [])
    if not isinstance(claims, list):
        claims = []
    context_update = _normalize_context_update(parsed.get("context_update"))
    record = {
        "paper_id": chunk.paper_id,
        "chunk_id": chunk.chunk_id,
        "section": chunk.section,
        "claims": claims,
        "context_update": context_update,
    }
    return record, content


def _normalize_context_update(value: Any) -> Dict[str, Any]:
    if not isinstance(value, dict):
        value = {}
    normalized: Dict[str, Any] = {}
    for key in CONTEXT_UPDATE_KEYS:
        raw = value.get(key)
        if key == "summary":
            normalized[key] = str(raw or "").strip()
        elif isinstance(raw, list):
            normalized[key] = [str(item).strip() for item in raw if str(item).strip()]
        elif raw:
            normalized[key] = [str(raw).strip()]
        else:
            normalized[key] = []
    return normalized


def synthesize_markdown(
    client: Any,
    model: str,
    paper_map: Dict[str, Any],
    synthesis_payload: Dict[str, Any],
    visual_evidence: List[Dict[str, Any]] | None = None,
) -> tuple[str, str]:
    prompt = build_markdown_prompt(
        paper_map=paper_map,
        synthesis_payload=synthesis_payload,
        visual_evidence=visual_evidence,
    )
    content = _chat(client, model, "你是材料科学论文知识卡片写作助手。", prompt)
    return content, prompt


def _chat(client: Any, model: str, system: str, user: str) -> str:
    last_error: ModelResponseError | None = None
    for attempt in range(3):
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )
        try:
            return _extract_chat_content(completion)
        except ModelResponseError as exc:
            last_error = exc
            if attempt < 2:
                time.sleep(1 + attempt)

    if last_error is not None:
        raise last_error
    raise ModelResponseError("Model response validation failed without details.")


def _extract_chat_content(completion: Any) -> str:
    choices = getattr(completion, "choices", None)
    if not choices:
        raise ModelResponseError("Model response has no choices.", _safe_dump_model_response(completion))

    first_choice = choices[0]
    message = getattr(first_choice, "message", None)
    if message is None:
        raise ModelResponseError("Model response choice has no message.", _safe_dump_model_response(completion))

    content = getattr(message, "content", None)
    if content is None:
        raise ModelResponseError("Model response message has no content.", _safe_dump_model_response(completion))
    return str(content)


def _safe_dump_model_response(response: Any) -> str:
    if response is None:
        return "None"
    try:
        if hasattr(response, "model_dump_json"):
            return response.model_dump_json()
        if hasattr(response, "model_dump"):
            return json.dumps(response.model_dump(), ensure_ascii=False)
    except Exception:
        pass
    return repr(response)
