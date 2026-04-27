import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from paper_extractor.common import clean_text, extract_figure_id, extract_json_from_text, log_jsonl


def parse_request_index(request_stem: str) -> int:
    match = re.match(r"request_(\d+)$", request_stem)
    if not match:
        raise ValueError(f"Invalid request file name: {request_stem}")
    return int(match.group(1))


def normalize_multimodal_result(parsed: Any, paper_id: str, figure_id: str, image_paths: List[str]) -> List[Dict[str, Any]]:
    if isinstance(parsed, dict):
        items = [parsed]
    elif isinstance(parsed, list):
        items = parsed
    else:
        raise ValueError("Model JSON must be object or array.")

    safe_image_paths = image_paths or [""]
    normalized: List[Dict[str, Any]] = []
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            continue
        image_path = safe_image_paths[min(index, len(safe_image_paths) - 1)]
        normalized.append(
            {
                "paper_id": paper_id,
                "figure_id": figure_id,
                "image_path": image_path,
                "image_url": image_path,
                "image_type": clean_text(str(item.get("image_type", ""))),
                "description": clean_text(str(item.get("description", ""))),
                "confidence": item.get("confidence", 0.0),
            }
        )

    if normalized:
        return normalized

    return [
        {
            "paper_id": paper_id,
            "figure_id": figure_id,
            "image_path": safe_image_paths[0],
            "image_url": safe_image_paths[0],
            "image_type": "",
            "description": "",
            "confidence": 0.0,
        }
    ]


def run_post_parse(output_root: Path) -> Dict[str, int]:
    summary = {
        "papers_scanned": 0,
        "text_parse_success": 0,
        "text_parse_fail": 0,
        "multimodal_parse_success": 0,
        "multimodal_parse_fail": 0,
    }

    for paper_dir in sorted(path for path in output_root.iterdir() if path.is_dir()):
        summary["papers_scanned"] += 1
        paper_id = paper_dir.name
        logs_dir = paper_dir / "logs"
        logs_dir.mkdir(parents=True, exist_ok=True)
        post_parse_log = logs_dir / "post_parse.log.jsonl"

        text_txt = paper_dir / "text_extraction" / "result.txt"
        if text_txt.exists():
            try:
                parsed = extract_json_from_text(text_txt.read_text(encoding="utf-8"))
                out_json = paper_dir / "text_extraction" / "result.json"
                out_json.write_text(json.dumps(parsed, ensure_ascii=False, indent=2), encoding="utf-8")
                summary["text_parse_success"] += 1
                log_jsonl(
                    post_parse_log,
                    {
                        "ts": datetime.now().isoformat(),
                        "event": "model_output",
                        "stage": "text_post_parse",
                        "paper_id": paper_id,
                        "output_file": str(out_json),
                        "status": "success",
                    },
                )
            except Exception as exc:
                summary["text_parse_fail"] += 1
                log_jsonl(
                    post_parse_log,
                    {
                        "ts": datetime.now().isoformat(),
                        "event": "model_output",
                        "stage": "text_post_parse",
                        "paper_id": paper_id,
                        "output_file": str(text_txt),
                        "status": "error",
                        "error": str(exc),
                    },
                )

        multimodal_dir = paper_dir / "multimodal_extraction"
        groups_path = multimodal_dir / "groups.json"
        groups: List[Dict[str, Any]] = []
        if groups_path.exists():
            try:
                loaded = json.loads(groups_path.read_text(encoding="utf-8"))
                if isinstance(loaded, list):
                    groups = loaded
            except Exception:
                groups = []

        for request_txt in sorted(multimodal_dir.glob("request_*.txt")):
            try:
                request_index = parse_request_index(request_txt.stem)
                group = groups[request_index - 1] if 0 < request_index <= len(groups) else {}
                image_paths = group.get("image_paths", []) if isinstance(group, dict) else []
                if not isinstance(image_paths, list):
                    image_paths = []
                caption = str(group.get("caption", "")) if isinstance(group, dict) else ""
                figure_id = extract_figure_id(caption, request_txt.stem)
                parsed = extract_json_from_text(request_txt.read_text(encoding="utf-8"))
                normalized = normalize_multimodal_result(parsed, paper_id, figure_id, image_paths)
                request_json = request_txt.with_suffix(".json")
                request_json.write_text(json.dumps(normalized, ensure_ascii=False, indent=2), encoding="utf-8")
                summary["multimodal_parse_success"] += 1
                log_jsonl(
                    post_parse_log,
                    {
                        "ts": datetime.now().isoformat(),
                        "event": "model_output",
                        "stage": "multimodal_post_parse",
                        "paper_id": paper_id,
                        "output_file": str(request_json),
                        "status": "success",
                        "image_count": len(image_paths),
                    },
                )
            except Exception as exc:
                summary["multimodal_parse_fail"] += 1
                log_jsonl(
                    post_parse_log,
                    {
                        "ts": datetime.now().isoformat(),
                        "event": "model_output",
                        "stage": "multimodal_post_parse",
                        "paper_id": paper_id,
                        "output_file": str(request_txt),
                        "status": "error",
                        "error": str(exc),
                    },
                )

    return summary
