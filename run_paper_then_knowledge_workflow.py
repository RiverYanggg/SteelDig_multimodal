#!/usr/bin/env python3
import argparse
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from paper_extractor.config import (
    LocalModelConfig,
    WorkflowSettings,
    default_workflow_settings,
    dump_workflow_settings,
    load_workflow_settings,
)
from paper_extractor.knowledge.workflow import run_knowledge_workflow
from paper_extractor.postprocess import run_post_parse_for_paper
from paper_extractor.workflow import (
    DEFAULT_IMAGE_TYPE_PROMPT_PATH,
    DEFAULT_TEXT_PROMPT_PATH,
    DEFAULT_TEXT_SCHEMA_PATH,
    collect_md_files,
    load_text,
    run_one_paper,
    validate_unique_paper_ids,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run extraction then knowledge workflow sequentially for each paper."
    )
    parser.add_argument("--config", default="config/workflow.json", help="Workflow config JSON path.")
    parser.add_argument("--input", default=None, help="Markdown file or directory path.")
    parser.add_argument("--output-root", default=None, help="Workflow output root.")
    parser.add_argument("--recursive", action="store_true", help="Recursively scan markdown files.")
    parser.add_argument("--workers", type=int, default=None, help="Parallel papers count.")
    parser.add_argument("--limit-papers", type=int, default=None, help="0 means no limit.")
    parser.add_argument("--skip-post-parse", action="store_true", help="Skip txt->json post-processing.")
    parser.add_argument("--skip-multimodal", action="store_true", help="Skip image analysis stage.")
    parser.add_argument("--knowledge-mode", choices=["text", "fused"], default="fused", help="Knowledge mode.")
    parser.add_argument("--knowledge-max-chunk-chars", type=int, default=9000, help="Approximate max chars per chunk.")
    parser.add_argument("--knowledge-mock-model", action="store_true", help="Run knowledge workflow with mock model.")
    parser.add_argument(
        "--resume-mode",
        choices=["none", "skip_completed", "resume_partial"],
        default="resume_partial",
        help="Skip completed papers or resume from missing stages.",
    )

    parser.add_argument("--text-model", default=None, help="Local text model name.")
    parser.add_argument("--text-base-url", default=None, help="Local text model base URL.")
    parser.add_argument("--text-api-key", default=None, help="Local text model API key.")

    parser.add_argument("--mm-model", default=None, help="Local multimodal model name. Defaults to text model.")
    parser.add_argument("--mm-base-url", default=None, help="Local multimodal model base URL. Defaults to text base URL.")
    parser.add_argument("--mm-api-key", default=None, help="Local multimodal model API key. Defaults to text API key.")
    return parser.parse_args()


def _paper_stage_status(paper_dir: Path, knowledge_mode: str) -> dict:
    final_dir = paper_dir / "final"
    extraction_done = (paper_dir / "intermediate" / "text" / "text_extraction.txt").exists()
    text_json_done = (final_dir / "text_extraction.json").exists()
    multimodal_done = (final_dir / "multimodal_figures.json").exists()
    knowledge_done = (final_dir / "text_knowledge.md").exists() and (final_dir / "text_claims.jsonl").exists()
    post_parse_done = text_json_done and (multimodal_done if knowledge_mode == "fused" else True)
    return {
        "extraction_done": extraction_done,
        "post_parse_done": post_parse_done,
        "knowledge_done": knowledge_done,
        "fully_done": extraction_done and post_parse_done and knowledge_done,
    }


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
        skip_existing=settings.skip_existing,
        skip_post_parse=args.skip_post_parse or settings.skip_post_parse,
        skip_multimodal=args.skip_multimodal or settings.skip_multimodal,
        text_model=text_model,
        multimodal_model=multimodal_model,
    )


def run_pipeline_for_paper(
    md_path: Path,
    output_root: Path,
    text_prompt: str,
    schema_text: str,
    image_type_prompt: str,
    settings: WorkflowSettings,
    paper_index: int,
    paper_total: int,
    knowledge_mode: str,
    knowledge_max_chunk_chars: int,
    knowledge_mock_model: bool,
    resume_mode: str,
) -> dict:
    paper_id = md_path.stem
    # A paper is the smallest orchestration unit: inside one paper we keep a
    # strict stage order so fused knowledge always consumes that paper's own
    # finalized multimodal outputs.
    paper_dir = output_root / paper_id
    stage_status = _paper_stage_status(paper_dir, knowledge_mode=knowledge_mode)
    if resume_mode == "skip_completed" and stage_status["fully_done"]:
        print(f"[PIPELINE {paper_index}/{paper_total}] [{paper_id}] skipped completed")
        return {
            "paper_id": paper_id,
            "skipped": True,
            "skip_reason": "completed",
            "stage_status": stage_status,
        }

    extraction_result = None
    if resume_mode == "resume_partial" and stage_status["extraction_done"]:
        print(f"[PIPELINE {paper_index}/{paper_total}] [{paper_id}] extraction skipped existing")
    else:
        print(f"[PIPELINE {paper_index}/{paper_total}] [{paper_id}] extraction start")
        extraction_result = run_one_paper(
            md_path=md_path,
            output_root=output_root,
            text_prompt=text_prompt,
            schema_text=schema_text,
            image_type_prompt=image_type_prompt,
            settings=settings,
            paper_index=paper_index,
            paper_total=paper_total,
        )
        stage_status = _paper_stage_status(paper_dir, knowledge_mode=knowledge_mode)

    post_parse_summary = None
    if not settings.skip_post_parse:
        if resume_mode == "resume_partial" and stage_status["post_parse_done"]:
            print(f"[PIPELINE {paper_index}/{paper_total}] [{paper_id}] post_parse skipped existing")
        else:
            post_parse_summary = run_post_parse_for_paper(paper_dir, settings=settings)
            print(
                f"[PIPELINE {paper_index}/{paper_total}] [{paper_id}] post_parse done "
                f"text_ok={post_parse_summary['text_parse_success']} "
                f"mm_ok={post_parse_summary['multimodal_parse_success']}"
            )
            stage_status = _paper_stage_status(paper_dir, knowledge_mode=knowledge_mode)
    else:
        print(f"[PIPELINE {paper_index}/{paper_total}] [{paper_id}] post_parse skipped by config")

    knowledge_result = None
    if resume_mode == "resume_partial" and stage_status["knowledge_done"]:
        print(f"[PIPELINE {paper_index}/{paper_total}] [{paper_id}] knowledge skipped existing")
    else:
        knowledge_result = run_knowledge_workflow(
            settings=settings,
            run_dir=paper_dir,
            mode=knowledge_mode,
            max_chunk_chars=knowledge_max_chunk_chars,
            mock_model=knowledge_mock_model,
        )
        print(f"[PIPELINE {paper_index}/{paper_total}] [{paper_id}] knowledge done")
        stage_status = _paper_stage_status(paper_dir, knowledge_mode=knowledge_mode)

    return {
        "paper_id": paper_id,
        "skipped": False,
        "extraction": extraction_result,
        "post_parse": post_parse_summary,
        "knowledge": knowledge_result,
        "stage_status": stage_status,
    }


def main() -> None:
    args = parse_args()
    settings = build_settings(args)
    if args.knowledge_mode == "fused" and settings.skip_post_parse:
        raise ValueError("knowledge_mode='fused' requires post-parse outputs. Remove --skip-post-parse.")

    input_path = Path(settings.input_path).expanduser().resolve()
    output_root = Path(settings.output_root).expanduser().resolve()
    output_root.mkdir(parents=True, exist_ok=True)

    text_prompt = load_text(DEFAULT_TEXT_PROMPT_PATH)
    schema_text = load_text(DEFAULT_TEXT_SCHEMA_PATH)
    image_type_prompt = load_text(DEFAULT_IMAGE_TYPE_PROMPT_PATH)

    md_files = collect_md_files(input_path, settings.recursive)
    if settings.limit_papers > 0:
        md_files = md_files[: settings.limit_papers]
    if not md_files:
        raise ValueError("No markdown files found.")
    validate_unique_paper_ids(md_files)

    total = len(md_files)
    workers = max(1, settings.workers)
    results = []
    failures = []
    print(
        f"Sequential-per-paper workflow started. papers={total}, workers={workers}, "
        f"knowledge_mode={args.knowledge_mode}, resume_mode={args.resume_mode}"
    )

    indexed_files = list(enumerate(md_files, start=1))
    with ThreadPoolExecutor(max_workers=workers) as executor:
        future_map = {
            executor.submit(
                run_pipeline_for_paper,
                md_path=md_path,
                output_root=output_root,
                text_prompt=text_prompt,
                schema_text=schema_text,
                image_type_prompt=image_type_prompt,
                settings=settings,
                paper_index=index,
                paper_total=total,
                knowledge_mode=args.knowledge_mode,
                knowledge_max_chunk_chars=args.knowledge_max_chunk_chars,
                knowledge_mock_model=args.knowledge_mock_model,
                resume_mode=args.resume_mode,
            ): (index, md_path)
            for index, md_path in indexed_files
        }
        # Parallelism is paper-level only. Each future owns exactly one paper_id
        # and writes only under output_root/paper_id, which prevents cross-paper
        # output mixing during large batch runs.
        for future in as_completed(future_map):
            index, md_path = future_map[future]
            paper_id = md_path.stem
            try:
                result = future.result()
                results.append(result)
                print(f"[PIPELINE OK] [{paper_id}]")
            except Exception as exc:
                failures.append({"paper_id": paper_id, "error": str(exc), "paper_index": index})
                print(f"[PIPELINE ERR] [{paper_id}] {exc}")

    results.sort(key=lambda item: item["paper_id"])
    failures.sort(key=lambda item: item["paper_index"])

    print(
        json.dumps(
            {
                "papers": results,
                "paper_count": len(results),
                "failure_count": len(failures),
                "failures": failures,
                "workers": workers,
                "knowledge_mode": args.knowledge_mode,
                "resume_mode": args.resume_mode,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
