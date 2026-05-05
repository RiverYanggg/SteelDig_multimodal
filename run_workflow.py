#!/usr/bin/env python3
from pathlib import Path

from paper_extractor.config import default_workflow_settings, dump_workflow_settings, load_workflow_settings
from paper_extractor.workflow import run_workflow


PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "config" / "workflow.json"


if __name__ == "__main__":
    if not DEFAULT_CONFIG_PATH.exists():
        dump_workflow_settings(default_workflow_settings(PROJECT_ROOT), DEFAULT_CONFIG_PATH)
    run_workflow(load_workflow_settings(DEFAULT_CONFIG_PATH))
