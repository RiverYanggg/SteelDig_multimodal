#!/usr/bin/env python3
import os
from pathlib import Path

from paper_extractor.config import LocalModelConfig, WorkflowSettings
from paper_extractor.workflow import run_workflow


PROJECT_ROOT = Path(__file__).resolve().parent
VLLM_MODEL_NAME = os.getenv("VLLM_MODEL_NAME", "./Qwen3.5-9B")


# 直接修改这里
SETTINGS = WorkflowSettings(
    input_path=str(PROJECT_ROOT / "dataset"),
    output_root=str(PROJECT_ROOT / "workflow_runs"),
    recursive=True,
    workers=1,
    limit_papers=0,
    skip_post_parse=False,
    skip_multimodal=False,
    text_model=LocalModelConfig(
        model=VLLM_MODEL_NAME,
        base_url="http://127.0.0.1:8000/v1",
        api_key="EMPTY",
    ),
    multimodal_model=LocalModelConfig(
        model=VLLM_MODEL_NAME,
        base_url="http://127.0.0.1:8000/v1",
        api_key="EMPTY",
    ),
)


if __name__ == "__main__":
    run_workflow(SETTINGS)
