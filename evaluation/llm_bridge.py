from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib import error, parse, request

from evaluation.config import LLMBridgeSettings
from evaluation.normalize import compact_text_fragments


@dataclass(frozen=True)
class LLMBridgeResult:
    matches: list[dict[str, Any]]
    raw_response: str
    error: str | None = None


class SampleLLMBridge:
    def __init__(self, settings: LLMBridgeSettings) -> None:
        self.settings = settings
        self.endpoint = _chat_completions_url(settings.base_url)
        self.api_key = settings.api_key or "EMPTY"
        self.prompt_template = Path(settings.prompt_path).read_text(encoding="utf-8")

    def bridge(
        self,
        paper_key: str,
        truth_records: list[dict[str, Any]],
        prediction_records: list[dict[str, Any]],
        truth_context: dict[str, dict[str, Any]],
        pred_context: dict[str, dict[str, Any]],
        candidates: list[dict[str, Any]],
    ) -> LLMBridgeResult:
        payload = {
            "paper_id": paper_key,
            "truth_samples": [self._summarize_record(record, truth_context) for record in truth_records[: self.settings.max_component_records]],
            "prediction_samples": [self._summarize_record(record, pred_context) for record in prediction_records[: self.settings.max_component_records]],
            "candidate_hints": candidates[: self.settings.max_component_records],
        }
        prompt = self.prompt_template.replace("{{INPUT_JSON}}", json.dumps(payload, ensure_ascii=False, indent=2))
        try:
            raw = self._request_chat_completion(
                messages=[
                    {"role": "system", "content": "You are a precise JSON alignment engine."},
                    {"role": "user", "content": prompt},
                ]
            )
        except Exception as exc:  # pragma: no cover - network dependent
            return LLMBridgeResult(matches=[], raw_response="", error=str(exc))

        try:
            parsed = _extract_json(raw)
        except Exception as exc:
            return LLMBridgeResult(matches=[], raw_response=raw, error=f"Invalid JSON response: {exc}")

        matches = parsed.get("matches", []) if isinstance(parsed, dict) else []
        if not isinstance(matches, list):
            return LLMBridgeResult(matches=[], raw_response=raw, error="Response missing matches list.")
        return LLMBridgeResult(matches=matches, raw_response=raw, error=None)

    def _summarize_record(self, record: dict[str, Any], context_index: dict[str, dict[str, Any]]) -> dict[str, Any]:
        sample_id = str(record.get("sample_id", ""))
        return {
            "sample_id": sample_id,
            "alloy_id": record.get("alloy_id"),
            "process_id": record.get("process_id"),
            "context_text": compact_text_fragments(context_index.get(sample_id, {}), limit=24),
        }

    def _request_chat_completion(self, messages: list[dict[str, str]]) -> str:
        payload = {
            "model": self.settings.model,
            "temperature": self.settings.temperature,
            "messages": messages,
        }
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        req = request.Request(
            self.endpoint,
            data=body,
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
        )
        try:
            with request.urlopen(req, timeout=180) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"HTTP {exc.code}: {detail}") from exc
        except error.URLError as exc:
            raise RuntimeError(f"Network error: {exc.reason}") from exc

        content = (
            data.get("choices", [{}])[0]
            .get("message", {})
            .get("content", "")
        )
        if not isinstance(content, str) or not content.strip():
            raise RuntimeError(f"Empty completion content: {json.dumps(data, ensure_ascii=False)[:1000]}")
        return content


def _extract_json(text: str) -> dict[str, Any]:
    candidate = text.strip()
    if candidate.startswith("```"):
        lines = candidate.splitlines()
        if len(lines) >= 3:
            candidate = "\n".join(lines[1:-1])
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
