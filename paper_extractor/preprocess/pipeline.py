import json
from pathlib import Path
from typing import Dict, Iterable

from .content_list import load_content_list
from .image_groups import parse_markdown_text
from .markdown_cleaner import clean_markdown_with_content_list, clean_markdown_without_content_list
from .models import PreprocessArtifacts


def preprocess_paper(
    md_path: Path,
    output_dir: Path | None = None,
    extra_drop_categories: Iterable[str] | None = None,
) -> PreprocessArtifacts:
    paper_id = md_path.stem
    source_json_path = _find_content_list_path(md_path)
    markdown_text = md_path.read_text(encoding="utf-8")
    content_items = load_content_list(source_json_path) if source_json_path else []

    if content_items:
        cleaned_markdown, references, removed_categories, removed_blocks = clean_markdown_with_content_list(
            markdown_text,
            content_items,
            extra_drop_categories=extra_drop_categories,
        )
        used_content_list = True
    else:
        cleaned_markdown, references, removed_categories, removed_blocks = clean_markdown_without_content_list(markdown_text)
        used_content_list = False

    image_groups = parse_markdown_text(cleaned_markdown)
    artifacts = PreprocessArtifacts(
        paper_id=paper_id,
        source_md_path=md_path,
        source_json_path=source_json_path,
        cleaned_markdown=cleaned_markdown,
        references=references,
        image_groups=image_groups,
        removed_categories=removed_categories,
        removed_blocks=removed_blocks,
        reference_count=len(references),
        used_content_list=used_content_list,
    )

    if output_dir is not None:
        write_preprocess_outputs(output_dir, artifacts)

    return artifacts


def write_preprocess_outputs(output_dir: Path, artifacts: PreprocessArtifacts) -> Dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    cleaned_md_path = output_dir / "cleaned_input.md"
    references_json_path = output_dir / "references.json"
    image_groups_path = output_dir / "image_groups.json"
    summary_path = output_dir / "summary.json"

    cleaned_md_path.write_text(artifacts.cleaned_markdown, encoding="utf-8")
    references_json_path.write_text(json.dumps(artifacts.references, ensure_ascii=False, indent=2), encoding="utf-8")
    image_groups_path.write_text(json.dumps(artifacts.image_groups, ensure_ascii=False, indent=2), encoding="utf-8")
    summary_path.write_text(
        json.dumps(
            {
                "paper_id": artifacts.paper_id,
                "source_md_path": str(artifacts.source_md_path),
                "source_json_path": str(artifacts.source_json_path) if artifacts.source_json_path else None,
                "used_content_list": artifacts.used_content_list,
                "removed_categories": artifacts.removed_categories,
                "removed_blocks": artifacts.removed_blocks,
                "reference_count": artifacts.reference_count,
                "image_group_count": len(artifacts.image_groups),
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    return {
        "cleaned_markdown": str(cleaned_md_path),
        "references_json": str(references_json_path),
        "image_groups_json": str(image_groups_path),
        "summary_json": str(summary_path),
    }


def _find_content_list_path(md_path: Path) -> Path | None:
    candidate = md_path.with_name(f"{md_path.stem}_content_list.json")
    if candidate.exists():
        return candidate
    return None
