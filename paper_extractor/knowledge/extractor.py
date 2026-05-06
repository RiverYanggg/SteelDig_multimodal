import json
from typing import Any, Dict, List

from paper_extractor.common import extract_json_from_text
from paper_extractor.knowledge.chunker import Chunk
from paper_extractor.knowledge.prompts import build_claim_prompt, build_markdown_prompt, build_paper_map_prompt


class ExtractionParseError(ValueError):
    def __init__(self, message: str, raw_content: str):
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


def extract_chunk_claims(client: Any, model: str, paper_map: Dict[str, Any], chunk: Chunk) -> tuple[Dict[str, Any], str]:
    prompt = build_claim_prompt(paper_map=paper_map, chunk=chunk)
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
    record = {
        "paper_id": chunk.paper_id,
        "chunk_id": chunk.chunk_id,
        "section": chunk.section,
        "claims": claims,
    }
    return record, content


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
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )
    return completion.choices[0].message.content or ""
