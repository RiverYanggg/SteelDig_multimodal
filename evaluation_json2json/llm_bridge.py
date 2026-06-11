from __future__ import annotations

import json
import ssl
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib import error, parse, request

from evaluation.config import LLMBridgeSettings
from evaluation.normalize import compact_text_fragments


@dataclass(frozen=True)
class LLMBridgeResult:
    alloy_matches: list[dict[str, Any]]
    process_matches: list[dict[str, Any]]
    matches: list[dict[str, Any]]
    raw_response: str
    error: str | None = None


@dataclass(frozen=True)
class FieldJudgeResult:
    decisions: dict[str, bool]
    raw_response: str
    error: str | None = None


class SampleLLMBridge:
    def __init__(self, settings: LLMBridgeSettings) -> None:
        self.settings = settings
        self.endpoint = _chat_completions_url(settings.base_url)
        self.api_key = settings.api_key or "EMPTY"
        self.prompt_template = Path(settings.prompt_path).read_text(encoding="utf-8")

    def align(
        self,
        paper_key: str,
        truth_alloys: list[dict[str, Any]],
        prediction_alloys: list[dict[str, Any]],
        truth_processes: list[dict[str, Any]],
        prediction_processes: list[dict[str, Any]],
        truth_samples: list[dict[str, Any]],
        prediction_samples: list[dict[str, Any]],
        truth_context: dict[str, dict[str, Any]],
        pred_context: dict[str, dict[str, Any]],
    ) -> LLMBridgeResult:
        payload = {
            "paper_id": paper_key,
            "truth": {
                "alloys": truth_alloys,
                "processes": self._summarize_processes(truth_processes, truth_samples),
                "samples": [self._summarize_sample(record, truth_context) for record in truth_samples],
            },
            "prediction": {
                "alloys": prediction_alloys,
                "processes": self._summarize_processes(prediction_processes, prediction_samples),
                "samples": [self._summarize_sample(record, pred_context) for record in prediction_samples],
            },
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
            return LLMBridgeResult(alloy_matches=[], process_matches=[], matches=[], raw_response="", error=str(exc))

        try:
            parsed = _extract_json(raw)
        except Exception as exc:
            return LLMBridgeResult(
                alloy_matches=[],
                process_matches=[],
                matches=[],
                raw_response=raw,
                error=f"Invalid JSON response: {exc}",
            )

        alloy_matches = parsed.get("alloy_matches", []) if isinstance(parsed, dict) else []
        process_matches = parsed.get("process_matches", []) if isinstance(parsed, dict) else []
        matches = parsed.get("matches", []) if isinstance(parsed, dict) else []
        if not isinstance(alloy_matches, list):
            return LLMBridgeResult(alloy_matches=[], process_matches=[], matches=[], raw_response=raw, error="Response missing alloy_matches list.")
        if not isinstance(process_matches, list):
            return LLMBridgeResult(alloy_matches=[], process_matches=[], matches=[], raw_response=raw, error="Response missing process_matches list.")
        if not isinstance(matches, list):
            return LLMBridgeResult(alloy_matches=[], process_matches=[], matches=[], raw_response=raw, error="Response missing matches list.")
        return LLMBridgeResult(alloy_matches=alloy_matches, process_matches=process_matches, matches=matches, raw_response=raw, error=None)

    def _summarize_processes(self, processes: list[dict[str, Any]], samples: list[dict[str, Any]]) -> list[dict[str, Any]]:
        samples_by_process: dict[str, list[str]] = {}
        for sample in samples:
            process_id = str(sample.get("process_id", ""))
            sample_id = str(sample.get("sample_id", ""))
            if process_id and sample_id:
                samples_by_process.setdefault(process_id, []).append(sample_id)
        summarized = []
        for process in processes:
            process_id = str(process.get("process_id", ""))
            item = dict(process)
            item["linked_sample_ids"] = samples_by_process.get(process_id, [])
            summarized.append(item)
        return summarized

    def _summarize_sample(self, record: dict[str, Any], context_index: dict[str, dict[str, Any]]) -> dict[str, Any]:
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
            context = None if self.settings.verify_ssl else ssl._create_unverified_context()
            with request.urlopen(req, timeout=180, context=context) as resp:
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


class FieldLLMJudge:
    def __init__(self, settings: LLMBridgeSettings, prompt_path: str | None = None) -> None:
        self.settings = settings
        self.endpoint = _chat_completions_url(settings.base_url)
        self.api_key = settings.api_key or "EMPTY"
        template_path = Path(prompt_path or settings.prompt_path)
        self.prompt_template = template_path.read_text(encoding="utf-8")

    def judge_fields(self, paper_key: str, section_name: str, candidates: list[dict[str, Any]]) -> dict[str, Any]:
        if not candidates:
            return {"decisions": {}, "raw_response": "", "error": None}
        payload = {
            "paper_id": paper_key,
            "section": section_name,
            "fields": candidates,
        }
        prompt = self.prompt_template.replace("{{INPUT_JSON}}", json.dumps(payload, ensure_ascii=False, indent=2))
        try:
            raw = self._request_chat_completion(
                messages=[
                    {"role": "system", "content": "You are a strict boolean field equivalence judge."},
                    {"role": "user", "content": prompt},
                ]
            )
            parsed = _extract_json(raw)
            results = parsed.get("results", []) if isinstance(parsed, dict) else []
            decisions = _parse_field_decisions(results, candidates)
            return {"decisions": decisions, "raw_response": raw, "error": None}
        except Exception as exc:  # pragma: no cover - network dependent
            return {
                "decisions": {str(item.get("id")): False for item in candidates if item.get("id")},
                "raw_response": "",
                "error": str(exc),
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
            context = None if self.settings.verify_ssl else ssl._create_unverified_context()
            with request.urlopen(req, timeout=180, context=context) as resp:
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


def _parse_field_decisions(results: Any, candidates: list[dict[str, Any]]) -> dict[str, bool]:
    candidate_ids = {str(item.get("id")) for item in candidates if item.get("id")}
    decisions = {candidate_id: False for candidate_id in candidate_ids}
    if not isinstance(results, list):
        return decisions
    for item in results:
        if not isinstance(item, dict):
            continue
        item_id = str(item.get("id", ""))
        if item_id not in candidate_ids:
            continue
        decisions[item_id] = bool(item.get("matched", False))
    return decisions


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
