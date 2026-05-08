import base64
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from paper_extractor.client import create_client
from paper_extractor.common import clean_text, extract_figure_id, load_text, log_jsonl, truncate_text
from paper_extractor.config import WorkflowSettings
from paper_extractor.postprocess import run_post_parse
from paper_extractor.preprocess import preprocess_paper


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


def validate_unique_paper_ids(md_files: List[Path]) -> None:
    duplicates: Dict[str, List[str]] = {}
    for md_path in md_files:
        paper_id = md_path.stem
        duplicates.setdefault(paper_id, []).append(str(md_path))

    conflicts = {paper_id: paths for paper_id, paths in duplicates.items() if len(paths) > 1}
    if not conflicts:
        return

    lines = ["Duplicate paper_id detected from Markdown filenames. Rename files to unique stems before running:"]
    for paper_id, paths in sorted(conflicts.items()):
        lines.append(f"- paper_id={paper_id}")
        for path in paths:
            lines.append(f"  - {path}")
    raise ValueError("\n".join(lines))


def is_paper_extraction_complete(output_root: Path, paper_id: str, skip_multimodal: bool) -> bool:
    final_dir = output_root / paper_id / "final"
    if not (final_dir / "text_extraction.json").exists():
        return False
    if skip_multimodal:
        return True
    return (final_dir / "multimodal_figures.json").exists()


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
        "你是材料科学论文组图信息提取助手。你当前处理的是同一张 Figure 下的组图，请把整组图作为一个整体理解，"
        "目标是提取高信息密度、证据充分、可服务后续知识融合的 Figure 级信息。\n"
        "你需要结合图像像素、caption、citation_sentences 与论文上下文，输出一个 Figure 级 JSON 对象。\n"
        "严格输出 JSON（不要 markdown、不要代码块、不要额外文字）。第一个非空白字符必须是 `{`，最后一个非空白字符必须是 `}`。\n"
        "输出必须能被 json.loads 直接解析；不要使用 NaN、Infinity、注释、尾随逗号或单引号。\n"
        "输出必须且只能是一个对象，字段仅包含：image_type, description, confidence。\n"
        "不要逐张子图分别输出，不要输出数组，不要输出 paper_id、figure_id、image_paths、image_count，这些字段由后处理程序补齐。\n"
        "description 必须是信息饱满的英文自然语言，建议 120-220 words，但仍作为一个 JSON 字符串输出。\n"
        "description 应包含：1) 图像/图表实际展示了什么；2) 每个可识别子图或曲线/谱峰/显微区域的角色；"
        "3) 可从图像或 caption 明确读出的材料体系、样品编号、处理条件、相/组织/缺陷/性能指标；"
        "4) 关键趋势、对比关系、峰位/曲线变化/形貌差异/失效特征；5) 该 Figure 支持的核心科学结论。\n"
        "如果存在数值、单位、样品名、相名、图例、坐标轴、标尺、温度/时间/成分等可见信息，优先保留原文表达。\n"
        "若某信息仅由 caption 给出而图像中不可直接验证，应写成 caption states/reports；不要把不可见细节伪装成视觉观察。\n"
        "如果图像分辨率不足或局部文字无法辨认，应明确写出 unreadable/partially readable，并只总结可确认信息。\n"
        "如果组图内部有多种图像类型，image_type 选择最能代表整组图主要科学作用的那个类型。\n"
        "confidence 只能是 high、medium、low。视觉和 caption 都清晰一致时 high；部分可读或依赖 caption 时 medium；难以判读时 low。\n"
        "image_type 必须且只能从以下分类体系中选择（原样输出，不可自造新值）：\n"
        f"{image_type_prompt}\n\n"
        f"image_count: {len(group['image_paths'])}\n"
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
    # Every artifact for a paper is rooted under one isolated paper_dir.
    # This directory boundary is the main reason paper-level parallelism does
    # not mix outputs across different papers.
    preprocess_dir = paper_dir / "preprocess"
    intermediate_dir = paper_dir / "intermediate"
    intermediate_text_dir = intermediate_dir / "text"
    intermediate_multimodal_dir = intermediate_dir / "multimodal"
    final_dir = paper_dir / "final"
    logs_dir = paper_dir / "logs"
    preprocess_dir.mkdir(parents=True, exist_ok=True)
    intermediate_text_dir.mkdir(parents=True, exist_ok=True)
    intermediate_multimodal_dir.mkdir(parents=True, exist_ok=True)
    final_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)

    text_client = create_client(settings.text_model)
    multimodal_client = None if settings.skip_multimodal else create_client(settings.multimodal_model)

    text_log_file = logs_dir / "text.log.jsonl"
    multimodal_log_file = logs_dir / "multimodal.log.jsonl"

    preprocess_artifacts = preprocess_paper(md_path, output_dir=preprocess_dir)
    cleaned_md_path = preprocess_dir / "cleaned_input.md"
    paper_text = cleaned_md_path.read_text(encoding="utf-8")
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
            "cleaned_md_path": str(cleaned_md_path),
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
    text_result_path = intermediate_text_dir / "text_extraction.txt"
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

    groups = [clean_group(group) for group in preprocess_artifacts.image_groups]
    groups_path = intermediate_multimodal_dir / "image_groups.json"
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

        request_id = f"figure_{index:03d}"
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
            request_path = intermediate_multimodal_dir / f"{request_id}.txt"
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
        "multimodal_dir": str(intermediate_multimodal_dir),
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
    validate_unique_paper_ids(md_files)
    if settings.skip_existing:
        original_count = len(md_files)
        md_files = [
            md_path
            for md_path in md_files
            if not is_paper_extraction_complete(output_root, md_path.stem, settings.skip_multimodal)
        ]
        skipped = original_count - len(md_files)
        print(f"Skip-existing enabled. skipped={skipped}, remaining={len(md_files)}")
        if not md_files:
            print("Workflow finished. No remaining papers to process.")
            return

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
        # Futures are scheduled per paper instead of per figure/chunk, which
        # keeps resource accounting and output isolation simple.
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
        parse_summary = run_post_parse(output_root, settings=settings)
        print(
            "Post-parse done. "
            f"papers_scanned={parse_summary['papers_scanned']}, "
            f"text_parse_success={parse_summary['text_parse_success']}, "
            f"text_parse_fail={parse_summary['text_parse_fail']}, "
            f"multimodal_parse_success={parse_summary['multimodal_parse_success']}, "
            f"multimodal_parse_fail={parse_summary['multimodal_parse_fail']}"
        )

    print(f"Workflow finished. output_root={output_root}")
