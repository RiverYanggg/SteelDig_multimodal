#!/usr/bin/env python3
import argparse

from paper_extractor.config import LocalModelConfig, WorkflowSettings
from paper_extractor.workflow import run_workflow


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the paper extraction workflow with local OpenAI-compatible models.")
    parser.add_argument("--input", default="dataset", help="Markdown file or directory path.")
    parser.add_argument("--output-root", default="workflow_runs", help="Workflow output root.")
    parser.add_argument("--recursive", action="store_true", help="Recursively scan markdown files.")
    parser.add_argument("--workers", type=int, default=1, help="Parallel papers count.")
    parser.add_argument("--limit-papers", type=int, default=0, help="0 means no limit.")
    parser.add_argument("--skip-post-parse", action="store_true", help="Skip txt->json post-processing.")
    parser.add_argument("--skip-multimodal", action="store_true", help="Skip image analysis stage.")

    parser.add_argument("--text-model", default="Qwen/Qwen3.5-9B", help="Local text model name.")
    parser.add_argument("--text-base-url", default="http://127.0.0.1:8000/v1", help="Local text model base URL.")
    parser.add_argument("--text-api-key", default="EMPTY", help="Local text model API key.")

    parser.add_argument("--mm-model", default="", help="Local multimodal model name. Defaults to text model.")
    parser.add_argument("--mm-base-url", default="", help="Local multimodal model base URL. Defaults to text base URL.")
    parser.add_argument("--mm-api-key", default="", help="Local multimodal model API key. Defaults to text API key.")
    return parser.parse_args()


def build_settings(args: argparse.Namespace) -> WorkflowSettings:
    text_model = LocalModelConfig(
        model=args.text_model,
        base_url=args.text_base_url,
        api_key=args.text_api_key,
    )
    multimodal_model = LocalModelConfig(
        model=args.mm_model or args.text_model,
        base_url=args.mm_base_url or args.text_base_url,
        api_key=args.mm_api_key or args.text_api_key,
    )
    return WorkflowSettings(
        input_path=args.input,
        output_root=args.output_root,
        recursive=args.recursive,
        workers=args.workers,
        limit_papers=args.limit_papers,
        skip_post_parse=args.skip_post_parse,
        skip_multimodal=args.skip_multimodal,
        text_model=text_model,
        multimodal_model=multimodal_model,
    )


def main() -> None:
    args = parse_args()
    run_workflow(build_settings(args))


if __name__ == "__main__":
    main()
