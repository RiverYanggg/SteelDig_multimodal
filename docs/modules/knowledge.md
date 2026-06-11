# Knowledge Workflow Module

Implementation:

```text
paper_extractor/knowledge/
run_knowledge_workflow.py
```

## Purpose

The knowledge workflow compresses cleaned paper text and optional visual evidence into:

```text
final/text_claims.jsonl
final/text_knowledge.md
final/text_knowledge.meta.json
```

This is not a replacement for `text_extraction.json`. It is a higher-density knowledge card and claim dataset for downstream reading, training, or retrieval.

## Modes

- `text`: use cleaned text only.
- `fused`: use cleaned text plus `final/multimodal_figures.json`.

Use `fused` after full extraction with multimodal enabled. Use `text` when no figure JSON exists.

## Run

Existing paper output:

```bash
python3 steeldig.py knowledge -- \
  --config config/workflow.json \
  --run-dir outputs_dataset/A0 \
  --mode fused
```

Part of the full pipeline:

```bash
python3 steeldig.py pipeline -- \
  --config config/workflow.json \
  --input dataset \
  --output-root outputs_dataset \
  --knowledge-mode fused
```

## Intermediate Outputs

```text
intermediate/knowledge/
├── chunks_index.json
├── chunk_0001.raw.txt
├── paper_map.json
├── paper_map.raw.txt
├── synthesis_payload.json
└── validation_warnings.json
```

These files are useful when debugging missing claims, weak evidence, or poor Markdown synthesis.

