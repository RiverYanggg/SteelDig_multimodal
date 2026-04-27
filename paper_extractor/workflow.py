import base64
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from extract_image_info import parse_markdown
from paper_extractor.client import create_client
from paper_extractor.common import clean_text, extract_figure_id, load_text, log_jsonl, truncate_text
from paper_extractor.config import WorkflowSettings
from paper_extractor.postprocess import run_post_parse


DEFAULT_TEXT_PROMPT_PATH = Path(__file__).resolve().parent.parent / "prompt" / "text_extractor_prompt.md"
DEFAULT_TEXT_SCHEMA_PATH = Path(__file__).resolve().parent.parent / "prompt" / "json_schema.json"
DEFAULT_IMAGE_TYPE_PROMPT_PATH = Path(__file__).resolve().parent.parent / "prompt" / "image_type_prompt.md"


def collect_md_files(input_path: Path, recursive: bool) -> List[Path]:
    if input_path.is_file() and input_path.suffix.lower() == ".md":
        return [input_path]
    if input_path.is_dir():
        pattern = "**/*.md" if recursive else "*.md"
        candidates = sorted(input_path.glob(pattern))
        hybrid_auto_candidates = [path for path in candidates if "hybrid_auto" in path.parts]
        return hybrid_auto_candidates if hybrid_auto_candidates else candidates
    raise FileNotFoundError(f"Input path not found or not supported: {input_path}")


def build_text_prompt(base_prompt: str, schema_text: str, paper_id: str, paper_text: str) -> str:
    return (
        f"{base_prompt}\n\n"
        "【程序附带 JSON 对象模板】\n"
        f"{schema_text}\n\n"
        "【待抽取文献信息】\n"
        f"paper_id: {paper_id}\n"
        "paper_markdown_content:\n"
        f"{paper_text}\n"
    )


def clean_group(group: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "image_paths": [clean_text(str(path)) for path in group.get("image_paths", [])],
        "caption": clean_text(str(group.get("caption", ""))),
        "paper_abstract": clean_text(str(group.get("paper_abstract", ""))),
        "paper_title": clean_text(str(group.get("paper_title", ""))),
        "citation_sentences": [clean_text(str(sentence)) for sentence in group.get("citation_sentences", [])],
    }


def image_to_data_url(image_path: Path) -> str:
    suffix = image_path.suffix.lower().lstrip(".") or "png"
    mime = "jpeg" if suffix == "jpg" else suffix
    encoded = base64.b64encode(image_path.read_bytes()).decode("utf-8")
    return f"data:image/{mime};base64,{encoded}"


def make_multimodal_prompt(group: Dict[str, Any], image_type_prompt: str, text_extraction: Dict[str, Any]) -> str:
    return (
        "你是材料科学论文图像信息提取助手。请基于图像和论文上下文，逐张识别 image_type 并给出简短描述。\n"
        "严格输出 JSON（不要 markdown、不要代码块、不要额外文字），输出对象或数组均可。\n"
        "每条记录仅需包含字段：image_type, description, confidence。\n"
        "如果本次有多张图，请为每张图输出一条记录，记录数量必须与输入图像数量一致。\n"
        "不要输出 paper_id、image_path、image_url、figure_id，这些字段由后处理程序补齐。\n"
        "image_type 必须且只能从以下分类体系中选择（原样输出，不可自造新值）：\n"
        f"{image_type_prompt}\n\n"
        f"paper_title: {group['paper_title']}\n"
        f"paper_abstract: {group['paper_abstract']}\n"
        f"caption: {group['caption']}\n"
        f"citation_sentences: {json.dumps(group['citation_sentences'], ensure_ascii=False)}\n"
        f"text_extraction_summary_json: {json.dumps(text_extraction, ensure_ascii=False)}\n"
    )


def build_loggable_content(content: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    preview: List[Dict[str, Any]] = []
    for part in content:
        if part.get("type") == "image_url":
            url = str(part.get("image_url", {}).get("url", ""))
            preview.append(
                {
                    "type": "image_url",
                    "image_url_preview": f"{url[:120]}...<truncated>" if len(url) > 120 else url,
                    "image_url_length": len(url),
                }
            )
            continue
        if part.get("type") == "text":
            text = str(part.get("text", ""))
            preview.append(
                {
                    "type": "text",
                    "text_preview": truncate_text(text),
                    "text_length": len(text),
                }
            )
            continue
        preview.append(part)
    return preview


def run_one_paper(
    md_path: Path,
    output_root: Path,
    text_prompt: str,
    schema_text: str,
    image_type_prompt: str,
    settings: WorkflowSettings,
    paper_index: int,
    paper_total: int,
) -> Dict[str, Any]:
    paper_id = md_path.stem
    paper_dir = output_root / paper_id
    text_dir = paper_dir / "text_extraction"
    multimodal_dir = paper_dir / "multimodal_extraction"
    logs_dir = paper_dir / "logs"
    text_dir.mkdir(parents=True, exist_ok=True)
    multimodal_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)

    text_client = create_client(settings.text_model)
    multimodal_client = None if settings.skip_multimodal else create_client(settings.multimodal_model)

    text_log_file = logs_dir / "text.log.jsonl"
    multimodal_log_file = logs_dir / "multimodal.log.jsonl"

    paper_text = md_path.read_text(encoding="utf-8")
    text_user_prompt = build_text_prompt(text_prompt, schema_text, paper_id, paper_text)
    text_messages = [
        {"role": "system", "content": "你是论文文本信息抽取助手。"},
        {"role": "user", "content": text_user_prompt},
    ]
    log_jsonl(
        text_log_file,
        {
            "ts": datetime.now().isoformat(),
            "event": "model_input",
            "stage": "text_extraction",
            "paper_id": paper_id,
            "paper_md_path": str(md_path),
            "model": settings.text_model.model,
            "messages": [
                text_messages[0],
                {
                    "role": "user",
                    "content_preview": truncate_text(text_user_prompt),
                    "content_length": len(text_user_prompt),
                },
            ],
        },
    )
    print(f"[PAPER {paper_index}/{paper_total}] [{paper_id}] text_extraction start")
    text_completion = text_client.chat.completions.create(model=settings.text_model.model, messages=text_messages)
    text_raw = text_completion.choices[0].message.content or ""
    text_result_path = text_dir / "result.txt"
    text_result_path.write_text(text_raw, encoding="utf-8")
    log_jsonl(
        text_log_file,
        {
            "ts": datetime.now().isoformat(),
            "event": "model_output",
            "stage": "text_extraction",
            "paper_id": paper_id,
            "output_file": str(text_result_path),
            "raw_output_length": len(text_raw),
            "raw_output_preview": truncate_text(text_raw),
        },
    )
    print(f"[PAPER {paper_index}/{paper_total}] [{paper_id}] text_extraction done")

    groups = [clean_group(group) for group in parse_markdown(md_path)]
    groups_path = multimodal_dir / "groups.json"
    groups_path.write_text(json.dumps(groups, ensure_ascii=False, indent=2), encoding="utf-8")

    groups_with_images = sum(1 for group in groups if group.get("image_paths"))
    total_images = sum(len(group.get("image_paths", [])) for group in groups if isinstance(group.get("image_paths", []), list))
    request_success = 0
    request_fail = 0
    images_success = 0
    images_fail = 0

    if settings.skip_multimodal:
        log_jsonl(
            multimodal_log_file,
            {
                "ts": datetime.now().isoformat(),
                "event": "stage_skipped",
                "stage": "multimodal_extraction",
                "paper_id": paper_id,
                "reason": "skip_multimodal=True",
            },
        )
        print(f"[PAPER {paper_index}/{paper_total}] [{paper_id}] multimodal_extraction skipped")

    for index, group in enumerate(groups, start=1):
        image_paths = group["image_paths"]
        if not image_paths or settings.skip_multimodal:
            continue

        request_id = f"request_{index:03d}"
        try:
            image_root = md_path.parent
            image_abs_paths = [image_root / path for path in image_paths]
            for image_path in image_abs_paths:
                if not image_path.exists():
                    raise FileNotFoundError(f"Image not found: {image_path}")

            figure_id = extract_figure_id(group["caption"], request_id)
            prompt = make_multimodal_prompt(group, image_type_prompt, {"raw_text_output": text_raw})
            content: List[Dict[str, Any]] = [
                {"type": "image_url", "image_url": {"url": image_to_data_url(image_path)}} for image_path in image_abs_paths
            ]
            content.append({"type": "text", "text": prompt})
            messages = [
                {"role": "system", "content": "你是论文图像分析助手。"},
                {"role": "user", "content": content},
            ]
            log_jsonl(
                multimodal_log_file,
                {
                    "ts": datetime.now().isoformat(),
                    "event": "model_input",
                    "stage": "multimodal_extraction",
                    "paper_id": paper_id,
                    "request_id": request_id,
                    "figure_id": figure_id,
                    "model": settings.multimodal_model.model,
                    "image_count": len(image_paths),
                    "image_paths": image_paths,
                    "image_abs_paths": [str(path) for path in image_abs_paths],
                    "prompt": prompt,
                    "messages_preview": [
                        messages[0],
                        {"role": "user", "content": build_loggable_content(content)},
                    ],
                },
            )
            print(f"[PAPER {paper_index}/{paper_total}] [{paper_id}] request {index}/{len(groups)} start images={len(image_paths)}")
            completion = multimodal_client.chat.completions.create(
                model=settings.multimodal_model.model,
                messages=messages,
            )
            raw_text = completion.choices[0].message.content or ""
            request_path = multimodal_dir / f"{request_id}.txt"
            request_path.write_text(raw_text, encoding="utf-8")
            log_jsonl(
                multimodal_log_file,
                {
                    "ts": datetime.now().isoformat(),
                    "event": "model_output",
                    "stage": "multimodal_extraction",
                    "paper_id": paper_id,
                    "request_id": request_id,
                    "output_file": str(request_path),
                    "raw_output_length": len(raw_text),
                    "raw_output_preview": truncate_text(raw_text),
                    "status": "success",
                },
            )
            request_success += 1
            images_success += len(image_paths)
            print(
                f"[PAPER {paper_index}/{paper_total}] [{paper_id}] request {index}/{len(groups)} done "
                f"ok_req={request_success} fail_req={request_fail}"
            )
        except Exception as exc:
            request_fail += 1
            images_fail += len(image_paths)
            log_jsonl(
                multimodal_log_file,
                {
                    "ts": datetime.now().isoformat(),
                    "event": "model_output",
                    "stage": "multimodal_extraction",
                    "paper_id": paper_id,
                    "request_id": request_id,
                    "image_count": len(image_paths),
                    "image_paths": image_paths,
                    "status": "error",
                    "error": str(exc),
                },
            )
            print(f"[PAPER {paper_index}/{paper_total}] [{paper_id}] request {index}/{len(groups)} error={exc}")

    return {
        "paper_id": paper_id,
        "groups_total": len(groups),
        "groups_with_images": groups_with_images,
        "images_total": total_images,
        "multimodal_request_success": request_success,
        "multimodal_request_fail": request_fail,
        "images_success": images_success,
        "images_fail": images_fail,
        "text_output": str(text_result_path),
        "multimodal_dir": str(multimodal_dir),
    }


def run_workflow(settings: WorkflowSettings) -> None:
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

    total_ok = 0
    total_fail = 0
    total_groups = 0
    total_groups_with_images = 0
    total_images = 0
    total_request_ok = 0
    total_request_fail = 0
    total_images_ok = 0
    total_images_fail = 0
    workers = max(1, settings.workers)

    print(f"Workflow started. papers={len(md_files)}, workers={workers}")
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [
            executor.submit(
                run_one_paper,
                md_path=md_file,
                output_root=output_root,
                text_prompt=text_prompt,
                schema_text=schema_text,
                image_type_prompt=image_type_prompt,
                settings=settings,
                paper_index=index + 1,
                paper_total=len(md_files),
            )
            for index, md_file in enumerate(md_files)
        ]
        for future in as_completed(futures):
            try:
                result = future.result()
                total_ok += 1
                total_groups += result["groups_total"]
                total_groups_with_images += result["groups_with_images"]
                total_images += result["images_total"]
                total_request_ok += result["multimodal_request_success"]
                total_request_fail += result["multimodal_request_fail"]
                total_images_ok += result["images_success"]
                total_images_fail += result["images_fail"]
                print(
                    f"[OK] {result['paper_id']} text={result['text_output']} "
                    f"mm_req_ok={result['multimodal_request_success']} "
                    f"mm_req_fail={result['multimodal_request_fail']} "
                    f"images_ok={result['images_success']} "
                    f"images_fail={result['images_fail']}"
                )
            except Exception as exc:
                total_fail += 1
                print(f"[ERR] {exc}")

    print(
        "Extraction done. "
        f"papers_ok={total_ok}, papers_fail={total_fail}, "
        f"groups_total={total_groups}, groups_with_images={total_groups_with_images}, "
        f"images_total={total_images}, images_ok={total_images_ok}, images_fail={total_images_fail}, "
        f"mm_req_ok={total_request_ok}, mm_req_fail={total_request_fail}"
    )

    if not settings.skip_post_parse:
        parse_summary = run_post_parse(output_root)
        print(
            "Post-parse done. "
            f"papers_scanned={parse_summary['papers_scanned']}, "
            f"text_parse_success={parse_summary['text_parse_success']}, "
            f"text_parse_fail={parse_summary['text_parse_fail']}, "
            f"multimodal_parse_success={parse_summary['multimodal_parse_success']}, "
            f"multimodal_parse_fail={parse_summary['multimodal_parse_fail']}"
        )

    print(f"Workflow finished. output_root={output_root}")
