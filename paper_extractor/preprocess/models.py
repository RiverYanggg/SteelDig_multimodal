from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List


@dataclass(frozen=True)
class PreprocessArtifacts:
    paper_id: str
    source_md_path: Path
    source_json_path: Path | None
    cleaned_markdown: str
    references: List[Dict[str, Any]]
    image_groups: List[Dict[str, Any]]
    removed_categories: Dict[str, int]
    removed_blocks: int
    reference_count: int
    used_content_list: bool
