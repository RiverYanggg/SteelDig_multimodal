#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent


COMMANDS = {
    "extract": {
        "script": "run_paper_workflow.py",
        "help": "Run text extraction, optional multimodal extraction, and post-parse.",
    },
    "pipeline": {
        "script": "run_paper_then_knowledge_workflow.py",
        "help": "Run the recommended per-paper pipeline: extract -> post-parse -> units -> knowledge.",
    },
    "knowledge": {
        "script": "run_knowledge_workflow.py",
        "help": "Run knowledge-card generation for existing paper outputs or Markdown input.",
    },
    "units": {
        "script": "run_unit_normalization.py",
        "help": "Normalize explicit units in final/text_extraction.json.",
    },
    "verify": {
        "script": "run_verify.py",
        "help": "Run conservative evidence-based verification and patching.",
    },
    "verify-eval": {
        "script": "run_verify_eval.py",
        "help": "Run no-truth evidence quality evaluation.",
    },
    "evaluate": {
        "script": "run_evaluation.py",
        "help": "Compare two model extraction result sets.",
    },
    "graph": {
        "script": "run_knowledge_graph.py",
        "help": "Build or import a Neo4j knowledge graph from extraction outputs.",
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Unified SteelDig command wrapper. Use '--' before options passed to the selected command."
    )
    parser.add_argument("command", choices=sorted(COMMANDS), help="Workflow command to run.")
    parser.add_argument("args", nargs=argparse.REMAINDER, help="Arguments forwarded to the underlying run_*.py script.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    forwarded = args.args[1:] if args.args[:1] == ["--"] else args.args
    script = ROOT / COMMANDS[args.command]["script"]
    completed = subprocess.run([sys.executable, str(script), *forwarded], cwd=ROOT)
    raise SystemExit(completed.returncode)


if __name__ == "__main__":
    main()
