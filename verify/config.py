from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from verify.common import SharedLLMSettings


@dataclass(frozen=True)
class VerifySettings:
    dataset_root: str
    output_summary_path: str
    schema_path: str
    force: bool = False
    workers: int = 2
    max_evidence_chars: int = 80_000
    append_record_enabled: bool = False
    llm_enabled: bool = True
    llm: SharedLLMSettings = SharedLLMSettings()


def default_verify_config_path(project_root: Path) -> Path:
    return project_root / "config" / "verify_config.json"


def load_verify_settings(path: str | Path) -> VerifySettings:
    config_path = Path(path).expanduser().resolve()
    data = json.loads(config_path.read_text(encoding="utf-8"))
    return verify_settings_from_dict(data, base_dir=config_path.parent)


def verify_settings_from_dict(data: dict[str, Any], *, base_dir: Path) -> VerifySettings:
    default_dataset_root = base_dir.parent / "outputs_dataset"
    dataset_root = _resolve_path(
        str(data.get("dataset_root", default_dataset_root)),
        base_dir,
    )
    schema_path = _resolve_path(str(data.get("schema_path", "../prompt/json_schema.json")), base_dir)
    llm_data = dict(data.get("llm") or data.get("llm_bridge") or {})
    return VerifySettings(
        dataset_root=dataset_root,
        output_summary_path=_resolve_path(
            str(data.get("output_summary_path", "verify_eval_summary.json")),
            Path(dataset_root),
        ),
        schema_path=schema_path,
        force=bool(data.get("force", False)),
        workers=max(1, int(data.get("workers", 2) or 2)),
        max_evidence_chars=int(data.get("max_evidence_chars", 80_000) or 80_000),
        append_record_enabled=bool(data.get("append_record_enabled", False)),
        llm_enabled=bool(data.get("llm_enabled", True)),
        llm=SharedLLMSettings(
            model=str(_config_or_env(llm_data.get("model"), "EVAL_LLM_MODEL", "DEEPSEEK_MODEL", "deepseek-v4-flash")),
            base_url=str(_config_or_env(llm_data.get("base_url"), "EVAL_LLM_BASE_URL", "DEEPSEEK_BASE_URL", "https://api.deepseek.com")),
            api_key=str(_config_or_env(llm_data.get("api_key"), "EVAL_LLM_API_KEY", "DEEPSEEK_API_KEY", "EMPTY")),
            temperature=float(llm_data.get("temperature", 0.0)),
            verify_ssl=bool(llm_data.get("verify_ssl", True)),
            max_retries=max(1, int(llm_data.get("max_retries", 3) or 3)),
        ),
    )


def dump_verify_settings(settings: VerifySettings, path: str | Path) -> None:
    target = Path(path).expanduser().resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "dataset_root": settings.dataset_root,
        "output_summary_path": settings.output_summary_path,
        "schema_path": settings.schema_path,
        "force": settings.force,
        "workers": settings.workers,
        "max_evidence_chars": settings.max_evidence_chars,
        "append_record_enabled": settings.append_record_enabled,
        "llm_enabled": settings.llm_enabled,
        "llm": {
            "model": settings.llm.model,
            "base_url": settings.llm.base_url,
            "api_key": settings.llm.api_key,
            "temperature": settings.llm.temperature,
            "verify_ssl": settings.llm.verify_ssl,
            "max_retries": settings.llm.max_retries,
        },
    }
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def settings_with_overrides(
    settings: VerifySettings,
    *,
    dataset_root: str | None = None,
    force: bool | None = None,
    workers: int | None = None,
    llm_enabled: bool | None = None,
) -> VerifySettings:
    root = str(Path(dataset_root).expanduser().resolve()) if dataset_root else settings.dataset_root
    return VerifySettings(
        dataset_root=root,
        output_summary_path=settings.output_summary_path,
        schema_path=settings.schema_path,
        force=settings.force if force is None else force,
        workers=settings.workers if workers is None else max(1, workers),
        max_evidence_chars=settings.max_evidence_chars,
        append_record_enabled=settings.append_record_enabled,
        llm_enabled=settings.llm_enabled if llm_enabled is None else llm_enabled,
        llm=settings.llm,
    )


def _resolve_path(value: str, base_dir: Path) -> str:
    path = Path(value).expanduser()
    if path.is_absolute():
        return str(path.resolve())
    return str((base_dir / path).resolve())


def _config_or_env(value: Any, primary_env: str, secondary_env: str, default: str) -> str:
    if value is not None:
        text = str(value).strip()
        if text and text.upper() != "EMPTY":
            return text
    return os.getenv(primary_env) or os.getenv(secondary_env) or default
