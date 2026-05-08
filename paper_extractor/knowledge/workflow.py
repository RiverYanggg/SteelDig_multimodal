import json
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, List

from paper_extractor.client import create_client
from paper_extractor.common import log_jsonl, truncate_text
from paper_extractor.config import WorkflowSettings
from paper_extractor.knowledge.chunker import Chunk, split_markdown_into_chunks, write_chunks
from paper_extractor.knowledge.extractor import (
    CONTEXT_UPDATE_KEYS,
    ExtractionParseError,
    ModelResponseError,
    extract_chunk_claims,
    generate_paper_map,
    synthesize_markdown,
)
from paper_extractor.knowledge.markdown_writer import write_knowledge_outputs
from paper_extractor.knowledge.normalizer import normalize_claims, write_claims_jsonl
from paper_extractor.knowledge.synthesis_payload import build_synthesis_payload
from paper_extractor.preprocess import preprocess_paper
from paper_extractor.workflow import collect_md_files, validate_unique_paper_ids


def run_knowledge_workflow(
    settings: WorkflowSettings,
    run_dir: str | Path | None = None,
    mode: str = "text",
    max_chunk_chars: int = 24000,
    target_chunks: int = 5,
    max_chunks: int = 8,
    min_chunk_chars: int = 6000,
    mock_model: bool = False,
) -> Dict[str, Any]:
    if mode not in {"text", "fused"}:
        raise ValueError("mode must be 'text' or 'fused'.")

    if run_dir:
        return run_existing_run_dir(
            settings=settings,
            run_dir=Path(run_dir).expanduser().resolve(),
            mode=mode,
            max_chunk_chars=max_chunk_chars,
            target_chunks=target_chunks,
            max_chunks=max_chunks,
            min_chunk_chars=min_chunk_chars,
            mock_model=mock_model,
        )

    input_path = Path(settings.input_path).expanduser().resolve()
    output_root = Path(settings.output_root).expanduser().resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    md_files = collect_md_files(input_path, settings.recursive)
    if settings.limit_papers > 0:
        md_files = md_files[: settings.limit_papers]
    if not md_files:
        raise ValueError("No markdown files found.")
    validate_unique_paper_ids(md_files)

    results = []
    for md_path in md_files:
        results.append(
            run_one_knowledge_paper(
                md_path=md_path,
                output_root=output_root,
                settings=settings,
                mode=mode,
                max_chunk_chars=max_chunk_chars,
                target_chunks=target_chunks,
                max_chunks=max_chunks,
                min_chunk_chars=min_chunk_chars,
                mock_model=mock_model,
            )
        )
    return {"papers": results, "paper_count": len(results)}


def run_existing_run_dir(
    settings: WorkflowSettings,
    run_dir: Path,
    mode: str,
    max_chunk_chars: int,
    target_chunks: int,
    max_chunks: int,
    min_chunk_chars: int,
    mock_model: bool,
) -> Dict[str, Any]:
    preprocess_dir = run_dir / "preprocess"
    summary_path = preprocess_dir / "summary.json"
    cleaned_md_path = preprocess_dir / "cleaned_input.md"
    if not cleaned_md_path.exists():
        raise FileNotFoundError(f"cleaned_input.md not found: {cleaned_md_path}")
    summary = json.loads(summary_path.read_text(encoding="utf-8")) if summary_path.exists() else {}
    source_md_path = Path(summary.get("source_md_path") or cleaned_md_path)
    return _run_from_cleaned_markdown(
        paper_id=run_dir.name,
        source_md_path=source_md_path,
        cleaned_md_path=cleaned_md_path,
        paper_dir=run_dir,
        settings=settings,
        mode=mode,
        max_chunk_chars=max_chunk_chars,
        target_chunks=target_chunks,
        max_chunks=max_chunks,
        min_chunk_chars=min_chunk_chars,
        mock_model=mock_model,
    )


def run_one_knowledge_paper(
    md_path: Path,
    output_root: Path,
    settings: WorkflowSettings,
    mode: str,
    max_chunk_chars: int,
    target_chunks: int,
    max_chunks: int,
    min_chunk_chars: int,
    mock_model: bool,
) -> Dict[str, Any]:
    paper_id = md_path.stem
    paper_dir = output_root / paper_id
    preprocess_dir = paper_dir / "preprocess"
    preprocess_dir.mkdir(parents=True, exist_ok=True)
    artifacts = preprocess_paper(md_path, output_dir=preprocess_dir)
    cleaned_md_path = preprocess_dir / "cleaned_input.md"
    return _run_from_cleaned_markdown(
        paper_id=paper_id,
        source_md_path=artifacts.source_md_path,
        cleaned_md_path=cleaned_md_path,
        paper_dir=paper_dir,
        settings=settings,
        mode=mode,
        max_chunk_chars=max_chunk_chars,
        target_chunks=target_chunks,
        max_chunks=max_chunks,
        min_chunk_chars=min_chunk_chars,
        mock_model=mock_model,
    )


def _run_from_cleaned_markdown(
    paper_id: str,
    source_md_path: Path,
    cleaned_md_path: Path,
    paper_dir: Path,
    settings: WorkflowSettings,
    mode: str,
    max_chunk_chars: int,
    target_chunks: int,
    max_chunks: int,
    min_chunk_chars: int,
    mock_model: bool,
) -> Dict[str, Any]:
    intermediate_dir = paper_dir / "intermediate" / "knowledge"
    final_dir = paper_dir / "final"
    logs_dir = paper_dir / "logs"
    intermediate_dir.mkdir(parents=True, exist_ok=True)
    final_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_file = logs_dir / "knowledge.log.jsonl"

    markdown_text = cleaned_md_path.read_text(encoding="utf-8")
    chunks = split_markdown_into_chunks(
        markdown_text,
        paper_id=paper_id,
        max_chars=max_chunk_chars,
        target_chunks=target_chunks,
        max_chunks=max_chunks,
        min_chars=min_chunk_chars,
    )
    write_chunks(intermediate_dir, cleaned_md_path, paper_id, chunks)
    log_jsonl(log_file, {"event": "chunks_written", "paper_id": paper_id, "chunk_count": len(chunks)})

    client = None if mock_model else create_client(settings.text_model)
    if mock_model:
        paper_map, paper_map_raw = _mock_paper_map(paper_id, markdown_text), "mock"
    else:
        try:
            paper_map, paper_map_raw = generate_paper_map(client, settings.text_model.model, paper_id, markdown_text)
        except Exception as exc:
            paper_map_raw = getattr(exc, "raw_content", "")
            paper_map = _fallback_paper_map(
                paper_id=paper_id,
                markdown_text=markdown_text,
                error=str(exc),
            )
            log_jsonl(
                log_file,
                {
                    "event": "paper_map_fallback",
                    "paper_id": paper_id,
                    "error": str(exc),
                    "preview": truncate_text(paper_map_raw),
                },
            )
    paper_map = _normalize_paper_map(paper_map, paper_id=paper_id, markdown_text=markdown_text)
    (intermediate_dir / "paper_map.json").write_text(json.dumps(paper_map, ensure_ascii=False, indent=2), encoding="utf-8")
    (intermediate_dir / "paper_map.raw.txt").write_text(paper_map_raw, encoding="utf-8")
    log_jsonl(log_file, {"event": "paper_map_written", "paper_id": paper_id, "preview": truncate_text(paper_map_raw)})

    raw_records: List[Dict[str, Any]] = []
    rolling_context = _empty_rolling_context()
    context_history: List[Dict[str, Any]] = []
    with (intermediate_dir / "claims_raw.jsonl").open("w", encoding="utf-8") as raw_file:
        for chunk in chunks:
            previous_context_summary = _render_rolling_context(rolling_context)
            if mock_model:
                record, raw_content = _mock_chunk_claims(chunk)
            else:
                try:
                    record, raw_content = extract_chunk_claims(
                        client,
                        settings.text_model.model,
                        paper_map,
                        chunk,
                        previous_context_summary=previous_context_summary,
                    )
                except (ExtractionParseError, ModelResponseError) as exc:
                    raw_content = exc.raw_content
                    record = {
                        "paper_id": paper_id,
                        "chunk_id": chunk.chunk_id,
                        "section": chunk.section,
                        "claims": [],
                        "context_update": _empty_context_update(),
                        "error": str(exc),
                    }
                    log_jsonl(
                        log_file,
                        {
                            "event": "chunk_claims_parse_error",
                            "paper_id": paper_id,
                            "chunk_id": chunk.chunk_id,
                            "error": str(exc),
                            "preview": truncate_text(raw_content),
                        },
                    )
                except Exception as exc:
                    raw_content = ""
                    record = {
                        "paper_id": paper_id,
                        "chunk_id": chunk.chunk_id,
                        "section": chunk.section,
                        "claims": [],
                        "context_update": _empty_context_update(),
                        "error": str(exc),
                    }
                    log_jsonl(
                        log_file,
                        {
                            "event": "chunk_claims_unexpected_error",
                            "paper_id": paper_id,
                            "chunk_id": chunk.chunk_id,
                            "error": str(exc),
                        },
                    )
            record = _normalize_claim_record(record, chunk)
            context_update = record.get("context_update", _empty_context_update())
            rolling_context = _update_rolling_context(rolling_context, context_update)
            context_history.append(
                {
                    "chunk_id": chunk.chunk_id,
                    "section": chunk.section,
                    "previous_context_summary": previous_context_summary,
                    "context_update": context_update,
                    "rolling_context_summary": _render_rolling_context(rolling_context),
                }
            )
            raw_records.append(record)
            raw_file.write(json.dumps(record, ensure_ascii=False) + "\n")
            (intermediate_dir / f"{chunk.chunk_id}.raw.txt").write_text(raw_content, encoding="utf-8")
            log_jsonl(
                log_file,
                {
                    "event": "chunk_claims_written",
                    "paper_id": paper_id,
                    "chunk_id": chunk.chunk_id,
                    "claim_count": len(record.get("claims", [])),
                    "context_summary_chars": len(previous_context_summary),
                    "preview": truncate_text(raw_content),
                },
            )
    (intermediate_dir / "context_history.json").write_text(
        json.dumps(context_history, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    normalized_claims, warnings = normalize_claims(raw_records, chunks)
    write_claims_jsonl(intermediate_dir / "claims_normalized.jsonl", normalized_claims)
    (intermediate_dir / "validation_warnings.json").write_text(
        json.dumps(warnings, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # In fused mode we only read visual evidence from the same paper_dir/final
    # that this knowledge run belongs to; no cross-paper lookup happens here.
    visual_evidence = _load_visual_evidence(final_dir / "multimodal_figures.json") if mode == "fused" else []
    synthesis_payload = build_synthesis_payload(
        paper_map=paper_map,
        claims=normalized_claims,
        visual_evidence=visual_evidence,
    )
    (intermediate_dir / "synthesis_payload.json").write_text(
        json.dumps(synthesis_payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    if mock_model:
        markdown, synthesis_prompt = _mock_markdown(paper_map, normalized_claims), "mock"
    else:
        try:
            markdown, synthesis_prompt = synthesize_markdown(
                client,
                settings.text_model.model,
                paper_map=paper_map,
                synthesis_payload=synthesis_payload,
                visual_evidence=visual_evidence,
            )
        except Exception as exc:
            synthesis_prompt = getattr(exc, "raw_content", "")
            markdown = _fallback_markdown(paper_map, normalized_claims, error=str(exc))
            log_jsonl(
                log_file,
                {
                    "event": "markdown_synthesis_fallback",
                    "paper_id": paper_id,
                    "error": str(exc),
                    "preview": truncate_text(synthesis_prompt),
                },
            )
    (intermediate_dir / "synthesis_prompt.txt").write_text(synthesis_prompt, encoding="utf-8")
    write_knowledge_outputs(
        final_dir=final_dir,
        paper_id=paper_id,
        source_md_path=source_md_path,
        cleaned_md_path=cleaned_md_path,
        paper_map=paper_map,
        claims=normalized_claims,
        markdown_text=markdown,
        model=settings.text_model.model,
    )
    return {
        "paper_id": paper_id,
        "chunk_count": len(chunks),
        "claim_count": len(normalized_claims),
        "warning_count": len(warnings),
        "knowledge_markdown": str(final_dir / "text_knowledge.md"),
        "claims": str(final_dir / "text_claims.jsonl"),
        "mock_model": mock_model,
    }


def _load_visual_evidence(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    if not isinstance(data, list):
        return []
    return [item for item in data if isinstance(item, dict)]


def _normalize_paper_map(paper_map: Any, paper_id: str, markdown_text: str) -> Dict[str, Any]:
    if not isinstance(paper_map, dict):
        return _fallback_paper_map(
            paper_id=paper_id,
            markdown_text=markdown_text,
            error=f"paper_map is {type(paper_map).__name__}, expected dict",
        )

    normalized = dict(paper_map)
    normalized["paper_id"] = str(normalized.get("paper_id") or paper_id)
    normalized["title"] = str(normalized.get("title") or _infer_title(paper_id, markdown_text))
    for key in ("material_systems", "main_process_variables", "sample_aliases", "expected_information_axis", "key_sections"):
        if not isinstance(normalized.get(key), list):
            normalized[key] = []
    return normalized


def _normalize_claim_record(record: Any, chunk: Chunk) -> Dict[str, Any]:
    if not isinstance(record, dict):
        return {
            "paper_id": chunk.paper_id,
            "chunk_id": chunk.chunk_id,
            "section": chunk.section,
            "claims": [],
            "context_update": _empty_context_update(),
            "error": f"claim record is {type(record).__name__}, expected dict",
        }
    normalized = dict(record)
    normalized["paper_id"] = str(normalized.get("paper_id") or chunk.paper_id)
    normalized["chunk_id"] = str(normalized.get("chunk_id") or chunk.chunk_id)
    normalized["section"] = str(normalized.get("section") or chunk.section)
    claims = normalized.get("claims")
    normalized["claims"] = claims if isinstance(claims, list) else []
    normalized["context_update"] = _normalize_context_update(normalized.get("context_update"))
    return normalized


def _empty_context_update() -> Dict[str, Any]:
    return {
        "summary": "",
        "material_systems": [],
        "sample_aliases": [],
        "processing_route": [],
        "key_variables": [],
        "microstructure": [],
        "properties": [],
        "mechanisms": [],
        "figures_or_tables": [],
        "unresolved_terms": [],
    }


def _empty_rolling_context() -> Dict[str, Any]:
    return _empty_context_update()


def _normalize_context_update(value: Any) -> Dict[str, Any]:
    if not isinstance(value, dict):
        value = {}
    normalized = _empty_context_update()
    for key in CONTEXT_UPDATE_KEYS:
        raw = value.get(key)
        if key == "summary":
            normalized[key] = str(raw or "").strip()
        elif isinstance(raw, list):
            normalized[key] = _dedupe_text_items(raw, limit=12)
        elif raw:
            normalized[key] = _dedupe_text_items([raw], limit=12)
    return normalized


def _update_rolling_context(rolling_context: Dict[str, Any], context_update: Dict[str, Any]) -> Dict[str, Any]:
    merged = _normalize_context_update(rolling_context)
    update = _normalize_context_update(context_update)
    merged["summary"] = _merge_summary_text(str(merged.get("summary") or ""), str(update.get("summary") or ""))
    for key in CONTEXT_UPDATE_KEYS:
        if key == "summary":
            continue
        merged[key] = _dedupe_text_items(list(merged.get(key, [])) + list(update.get(key, [])), limit=12)
    return merged


def _render_rolling_context(rolling_context: Dict[str, Any], max_chars: int = 3200) -> str:
    context = _normalize_context_update(rolling_context)
    parts: List[str] = []
    summary = str(context.get("summary") or "").strip()
    if summary:
        parts.append(f"Summary: {summary}")
    labels = {
        "material_systems": "Material systems",
        "sample_aliases": "Sample aliases",
        "processing_route": "Processing route",
        "key_variables": "Key variables",
        "microstructure": "Microstructure",
        "properties": "Properties",
        "mechanisms": "Mechanisms",
        "figures_or_tables": "Figures or tables",
        "unresolved_terms": "Unresolved terms",
    }
    for key, label in labels.items():
        values = context.get(key) or []
        if values:
            parts.append(f"{label}: " + "; ".join(str(value) for value in values[:8]))
    text = "\n".join(parts).strip()
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rsplit("\n", 1)[0].strip() or text[:max_chars].strip()


def _merge_summary_text(previous: str, update: str, max_chars: int = 1400) -> str:
    pieces = [piece for piece in (previous.strip(), update.strip()) if piece]
    merged = " ".join(pieces)
    if len(merged) <= max_chars:
        return merged
    return merged[-max_chars:].split(". ", 1)[-1].strip()


def _dedupe_text_items(items: List[Any], limit: int) -> List[str]:
    deduped: List[str] = []
    seen = set()
    for item in items:
        text = " ".join(str(item).split())
        if not text:
            continue
        key = text.lower()
        if key in seen:
            continue
        seen.add(key)
        deduped.append(text)
        if len(deduped) >= limit:
            break
    return deduped


def _fallback_paper_map(paper_id: str, markdown_text: str, error: str) -> Dict[str, Any]:
    return {
        "paper_id": paper_id,
        "title": _infer_title(paper_id, markdown_text),
        "abstract_summary": "",
        "research_objective": "",
        "material_systems": [],
        "main_process_variables": [],
        "sample_aliases": [],
        "expected_information_axis": ["composition", "processing", "microstructure", "properties", "mechanism"],
        "key_sections": [],
        "fallback_reason": error,
    }


def _fallback_markdown(paper_map: Dict[str, Any], claims: List[Dict[str, Any]], error: str) -> str:
    lines = [
        f"# {paper_map.get('title') or paper_map.get('paper_id') or 'Knowledge Extraction'}",
        "",
        f"paper_id: {paper_map.get('paper_id')}",
        "",
        "> Markdown synthesis fell back to a deterministic summary because the model response was invalid.",
        f"> Error: {error}",
        "",
        "## Claims",
        "",
    ]
    if not claims:
        lines.append("No normalized claims were extracted.")
    for claim in claims:
        lines.append(
            f"- [{claim.get('claim_id', '')}] {claim.get('claim', '')} "
            f"(`{claim.get('chunk_id', '')}`, {claim.get('section', '')})"
        )
    return "\n".join(lines).strip() + "\n"


def _infer_title(paper_id: str, markdown_text: str) -> str:
    return next((line.lstrip("# ").strip() for line in markdown_text.splitlines() if line.startswith("# ")), paper_id)


def _mock_paper_map(paper_id: str, markdown_text: str) -> Dict[str, Any]:
    title = next((line.lstrip("# ").strip() for line in markdown_text.splitlines() if line.startswith("# ")), paper_id)
    return {
        "paper_id": paper_id,
        "title": title,
        "abstract_summary": "Mock paper map for offline workflow validation.",
        "research_objective": "Validate the knowledge Markdown workflow without remote model calls.",
        "material_systems": [],
        "main_process_variables": [],
        "sample_aliases": [],
        "expected_information_axis": ["composition", "processing", "microstructure", "properties", "mechanism"],
        "key_sections": [],
    }


def _mock_chunk_claims(chunk: Chunk) -> tuple[Dict[str, Any], str]:
    sentence = _first_scientific_sentence(chunk.text)
    claims = []
    if sentence:
        claims.append(
            {
                "claim_type": "mock_finding",
                "subject": chunk.section,
                "claim": sentence,
                "values": [],
                "evidence_text": sentence,
                "figures": [],
                "tables": [],
                "confidence": "medium",
            }
        )
    context_update = _empty_context_update()
    context_update["summary"] = sentence or ""
    return {
        "paper_id": chunk.paper_id,
        "chunk_id": chunk.chunk_id,
        "section": chunk.section,
        "claims": claims,
        "context_update": context_update,
    }, "mock"


def _mock_markdown(paper_map: Dict[str, Any], claims: List[Dict[str, Any]]) -> str:
    title = paper_map.get("title") or paper_map.get("paper_id") or "Knowledge Extraction"
    lines = [
        "---",
        f"paper_id: {paper_map.get('paper_id')}",
        f"title: {title}",
        "source_type: text_only",
        "workflow_validation: mock_model",
        "---",
        "",
        "# Paper Summary",
        "",
        str(paper_map.get("abstract_summary") or ""),
        "",
        "# Extracted Claims",
        "",
    ]
    for claim in claims:
        lines.append(f"- [{claim['claim_id']}] {claim['claim']} (`{claim['chunk_id']}`, {claim['section']})")
    lines.extend(["", "# Evidence Map", "", "| Claim | Chunk | Evidence |", "|---|---|---|"])
    for claim in claims:
        evidence = str(claim.get("evidence_text", "")).replace("|", "\\|")
        lines.append(f"| {claim['claim_id']} | {claim['chunk_id']} | {evidence} |")
    return "\n".join(lines)


def _first_scientific_sentence(text: str) -> str:
    for raw in text.replace("\n", " ").split("."):
        sentence = " ".join(raw.split()).strip()
        if len(sentence) < 40:
            continue
        if any(token in sentence.lower() for token in ["steel", "alloy", "phase", "temperature", "specimen", "microstructure"]):
            return sentence + "."
    return ""
