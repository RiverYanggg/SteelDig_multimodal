"""Core package for local paper extraction workflow."""

from paper_extractor.config import LocalModelConfig, WorkflowSettings
from paper_extractor.workflow import run_workflow

__all__ = ["LocalModelConfig", "WorkflowSettings", "run_workflow"]
