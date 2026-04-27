from dataclasses import dataclass


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
