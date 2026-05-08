import argparse
import json
from pathlib import Path

from paper_extractor.config import default_workflow_settings, load_workflow_settings
from paper_extractor.knowledge.workflow import run_knowledge_workflow


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run knowledge Markdown extraction workflow.")
    parser.add_argument("--config", default="config/workflow.json", help="Workflow config JSON path.")
    parser.add_argument("--input", dest="input_path", help="Markdown file or directory. Overrides config.")
    parser.add_argument("--output-root", help="Output root. Overrides config.")
    parser.add_argument("--run-dir", help="Existing workflow_runs/<paper_id> directory with preprocess/cleaned_input.md.")
    parser.add_argument("--mode", choices=["text", "fused"], default="text", help="Use text only or fuse existing figure JSON.")
    parser.add_argument("--mock-model", action="store_true", help="Run an offline smoke test with deterministic mock extraction.")
    parser.add_argument("--recursive", action="store_true", help="Recursively scan input directory.")
    parser.add_argument("--limit-papers", type=int, default=None, help="Limit number of papers.")
    parser.add_argument("--max-chunk-chars", type=int, default=24000, help="Hard max chars per chunk.")
    parser.add_argument("--target-chunks", type=int, default=5, help="Preferred chunk count per paper.")
    parser.add_argument("--max-chunks", type=int, default=8, help="Soft max chunk count per paper.")
    parser.add_argument("--min-chunk-chars", type=int, default=6000, help="Small chunks below this size are merged when possible.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    project_root = Path(__file__).resolve().parent
    config_path = Path(args.config)
    settings = load_workflow_settings(config_path) if config_path.exists() else default_workflow_settings(project_root)

    updates = {}
    if args.input_path:
        updates["input_path"] = str(Path(args.input_path).expanduser().resolve())
    if args.output_root:
        updates["output_root"] = str(Path(args.output_root).expanduser().resolve())
    if args.recursive:
        updates["recursive"] = True
    if args.limit_papers is not None:
        updates["limit_papers"] = args.limit_papers
    if updates:
        settings = settings.__class__(**{**settings.__dict__, **updates})

    result = run_knowledge_workflow(
        settings=settings,
        run_dir=args.run_dir,
        mode=args.mode,
        max_chunk_chars=args.max_chunk_chars,
        target_chunks=args.target_chunks,
        max_chunks=args.max_chunks,
        min_chunk_chars=args.min_chunk_chars,
        mock_model=args.mock_model,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
