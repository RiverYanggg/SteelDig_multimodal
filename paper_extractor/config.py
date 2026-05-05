import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict


@dataclass(frozen=True)
class LocalModelConfig:
    model: str
    base_url: str
    api_key: str = "EMPTY"


@dataclass(frozen=True)
class WorkflowSettings:
    input_path: str = "dataset"
    output_root: str = "workflow_runs"
    recursive: bool = True
    workers: int = 1
    limit_papers: int = 0
    skip_post_parse: bool = False
    skip_multimodal: bool = True
    text_model: LocalModelConfig = LocalModelConfig(
        model="Qwen/Qwen3.5-9B",
        base_url="http://127.0.0.1:8000/v1",
    )
    multimodal_model: LocalModelConfig = LocalModelConfig(
        model="Qwen/Qwen3.5-9B",
        base_url="http://127.0.0.1:8000/v1",
    )


def load_workflow_settings(config_path: str | Path) -> WorkflowSettings:
    path = Path(config_path).expanduser().resolve()
    data = json.loads(path.read_text(encoding="utf-8"))
    return workflow_settings_from_dict(data, base_dir=path.parent)


def workflow_settings_from_dict(data: Dict[str, Any], base_dir: Path | None = None) -> WorkflowSettings:
    base_dir = base_dir or Path.cwd()
    text_model_data = dict(data.get("text_model", {}))
    multimodal_model_data = dict(data.get("multimodal_model", {}))

    input_path = _resolve_path(str(data.get("input_path", "dataset")), base_dir)
    output_root = _resolve_path(str(data.get("output_root", "workflow_runs")), base_dir)

    text_model = LocalModelConfig(
        model=str(text_model_data.get("model", "Qwen/Qwen3.5-9B")),
        base_url=str(text_model_data.get("base_url", "http://127.0.0.1:8000/v1")),
        api_key=str(text_model_data.get("api_key", "EMPTY")),
    )
    multimodal_model = LocalModelConfig(
        model=str(multimodal_model_data.get("model", text_model.model)),
        base_url=str(multimodal_model_data.get("base_url", text_model.base_url)),
        api_key=str(multimodal_model_data.get("api_key", text_model.api_key)),
    )

    return WorkflowSettings(
        input_path=input_path,
        output_root=output_root,
        recursive=bool(data.get("recursive", True)),
        workers=int(data.get("workers", 1)),
        limit_papers=int(data.get("limit_papers", 0)),
        skip_post_parse=bool(data.get("skip_post_parse", False)),
        skip_multimodal=bool(data.get("skip_multimodal", True)),
        text_model=text_model,
        multimodal_model=multimodal_model,
    )


def dump_workflow_settings(settings: WorkflowSettings, config_path: str | Path) -> None:
    path = Path(config_path).expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = asdict(settings)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def default_workflow_settings(project_root: Path) -> WorkflowSettings:
    return WorkflowSettings(
        input_path=str((project_root / "dataset").resolve()),
        output_root=str((project_root / "workflow_runs").resolve()),
        recursive=True,
        workers=1,
        limit_papers=0,
        skip_post_parse=False,
        skip_multimodal=False,
        text_model=LocalModelConfig(
            model="Qwen/Qwen3.5-9B",
            base_url="http://127.0.0.1:8000/v1",
            api_key="EMPTY",
        ),
        multimodal_model=LocalModelConfig(
            model="Qwen/Qwen3.5-9B",
            base_url="http://127.0.0.1:8000/v1",
            api_key="EMPTY",
        ),
    )


def _resolve_path(value: str, base_dir: Path) -> str:
    path = Path(value).expanduser()
    if path.is_absolute():
        return str(path.resolve())
    return str((base_dir / path).resolve())
