#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from evaluation.config import (
    EvaluationSettings,
    LLMBridgeSettings,
    MatchingSettings,
    default_evaluation_settings,
    dump_evaluation_settings,
    load_evaluation_settings,
)
from evaluation.framework import run_evaluation


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate prediction JSON files against ground-truth JSON files.")
    parser.add_argument("--config", default="evaluation/config/eval_config.json", help="Evaluation config JSON path.")
    parser.add_argument("--truth-dir", default=None, help="Ground-truth JSON directory.")
    parser.add_argument("--prediction-root", default=None, help="Prediction root directory.")
    parser.add_argument("--output-path", default=None, help="Output report JSON path.")
    parser.add_argument("--per-paper-output-dir", default=None, help="Directory for per-paper evaluation JSON files.")
    parser.add_argument("--field-rules-path", default=None, help="Field rules JSON path.")
    parser.add_argument(
        "--paper-ids",
        default=None,
        help="Comma-separated paper ids to evaluate, for example A0,A19,A28.",
    )

    parser.add_argument("--enable-llm-bridge", action="store_true", help="Enable LLM-based sample ambiguity bridging.")
    parser.add_argument("--llm-model", default=None, help="LLM bridge model name.")
    parser.add_argument("--llm-base-url", default=None, help="LLM bridge base URL.")
    parser.add_argument("--llm-api-key", default=None, help="LLM bridge API key.")
    parser.add_argument("--llm-prompt-path", default=None, help="LLM bridge prompt template path.")
    return parser.parse_args()


def build_settings(args: argparse.Namespace) -> EvaluationSettings:
    config_path = Path(args.config).expanduser().resolve()
    if not config_path.exists():
        dump_evaluation_settings(default_evaluation_settings(Path.cwd()), config_path)
    settings = load_evaluation_settings(config_path)
    llm = settings.llm_bridge
    paper_ids = tuple(
        item.strip()
        for item in (args.paper_ids.split(",") if args.paper_ids else settings.paper_ids)
        if item and item.strip()
    )
    return EvaluationSettings(
        truth_dir=args.truth_dir or settings.truth_dir,
        prediction_root=args.prediction_root or settings.prediction_root,
        output_path=args.output_path or settings.output_path,
        per_paper_output_dir=args.per_paper_output_dir or settings.per_paper_output_dir,
        field_rules_path=args.field_rules_path or settings.field_rules_path,
        paper_ids=paper_ids,
        matching=MatchingSettings(**vars(settings.matching)),
        llm_bridge=LLMBridgeSettings(
            enabled=args.enable_llm_bridge or llm.enabled,
            model=args.llm_model or llm.model,
            base_url=args.llm_base_url or llm.base_url,
            api_key=args.llm_api_key or llm.api_key,
            temperature=llm.temperature,
            max_component_records=llm.max_component_records,
            prompt_path=args.llm_prompt_path or llm.prompt_path,
        ),
    )


def main() -> None:
    args = parse_args()
    run_evaluation(build_settings(args))


if __name__ == "__main__":
    main()
