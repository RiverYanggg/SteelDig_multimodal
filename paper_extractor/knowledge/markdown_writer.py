import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


def write_knowledge_outputs(
    final_dir: Path,
    paper_id: str,
    source_md_path: Path,
    cleaned_md_path: Path,
    paper_map: Dict[str, Any],
    claims: List[Dict[str, Any]],
    markdown_text: str,
    model: str,
) -> None:
    final_dir.mkdir(parents=True, exist_ok=True)
    (final_dir / "text_knowledge.md").write_text(markdown_text.strip() + "\n", encoding="utf-8")
    with (final_dir / "text_claims.jsonl").open("w", encoding="utf-8") as f:
        for claim in claims:
            f.write(json.dumps(claim, ensure_ascii=False) + "\n")
    meta = {
        "paper_id": paper_id,
        "source_md_path": str(source_md_path),
        "cleaned_md_path": str(cleaned_md_path),
        "model": model,
        "created_at": datetime.now().isoformat(),
        "claim_count": len(claims),
        "source_type": "text_only",
        "paper_map": paper_map,
    }
    (final_dir / "text_knowledge.meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

