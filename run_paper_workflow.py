#!/usr/bin/env python3
import argparse
from pathlib import Path

from paper_extractor.config import (
    LocalModelConfig,
    WorkflowSettings,
    default_workflow_settings,
    dump_workflow_settings,
    load_workflow_settings,
)
from paper_extractor.workflow import run_workflow


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the paper extraction workflow with local OpenAI-compatible models.")
    parser.add_argument("--config", default="config/workflow.json", help="Workflow config JSON path.")
    parser.add_argument("--input", default=None, help="Markdown file or directory path.")
    parser.add_argument("--output-root", default=None, help="Workflow output root.")
    parser.add_argument("--recursive", action="store_true", help="Recursively scan markdown files.")
    parser.add_argument("--workers", type=int, default=None, help="Parallel papers count.")
    parser.add_argument("--limit-papers", type=int, default=None, help="0 means no limit.")
    parser.add_argument("--skip-existing", action="store_true", help="Skip papers with existing final outputs.")
    parser.add_argument("--skip-post-parse", action="store_true", help="Skip txt->json post-processing.")
    parser.add_argument("--skip-multimodal", action="store_true", help="Skip image analysis stage.")

    parser.add_argument("--text-model", default=None, help="Local text model name.")
    parser.add_argument("--text-base-url", default=None, help="Local text model base URL.")
    parser.add_argument("--text-api-key", default=None, help="Local text model API key.")

    parser.add_argument("--mm-model", default=None, help="Local multimodal model name. Defaults to text model.")
    parser.add_argument("--mm-base-url", default=None, help="Local multimodal model base URL. Defaults to text base URL.")
    parser.add_argument("--mm-api-key", default=None, help="Local multimodal model API key. Defaults to text API key.")
    return parser.parse_args()


def build_settings(args: argparse.Namespace) -> WorkflowSettings:
    config_path = Path(args.config).expanduser().resolve()
    if not config_path.exists():
        dump_workflow_settings(default_workflow_settings(Path.cwd()), config_path)
    settings = load_workflow_settings(config_path)

    text_model = LocalModelConfig(
        model=args.text_model or settings.text_model.model,
        base_url=args.text_base_url or settings.text_model.base_url,
        api_key=args.text_api_key or settings.text_model.api_key,
    )
    multimodal_model = LocalModelConfig(
        model=args.mm_model or settings.multimodal_model.model or text_model.model,
        base_url=args.mm_base_url or settings.multimodal_model.base_url or text_model.base_url,
        api_key=args.mm_api_key or settings.multimodal_model.api_key or text_model.api_key,
    )
    return WorkflowSettings(
        input_path=args.input or settings.input_path,
        output_root=args.output_root or settings.output_root,
        recursive=args.recursive or settings.recursive,
        workers=args.workers if args.workers is not None else settings.workers,
        limit_papers=args.limit_papers if args.limit_papers is not None else settings.limit_papers,
        skip_existing=args.skip_existing or settings.skip_existing,
        skip_post_parse=args.skip_post_parse or settings.skip_post_parse,
        skip_multimodal=args.skip_multimodal or settings.skip_multimodal,
        text_model=text_model,
        multimodal_model=multimodal_model,
    )


def main() -> None:
    args = parse_args()
    run_workflow(build_settings(args))


if __name__ == "__main__":
    main()
