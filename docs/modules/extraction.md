# Extraction And Postprocess Modules

Implementation:

```text
paper_extractor/workflow.py
paper_extractor/postprocess.py
prompt/text_extractor_prompt.md
prompt/image_type_prompt.md
prompt/json_schema.json
```

## Purpose

Extraction calls OpenAI-compatible text and multimodal models. Postprocess parses raw model responses into stable JSON files.

## Text Extraction

Input:

```text
preprocess/cleaned_input.md
prompt/text_extractor_prompt.md
prompt/json_schema.json
```

Output:

```text
intermediate/text/text_extraction.txt
```

The prompt asks the model to emit JSON following `prompt/json_schema.json`, but the raw response is saved first for auditability.

## Multimodal Extraction

Input:

```text
preprocess/image_groups.json
prompt/image_type_prompt.md
images/*
```

Output:

```text
intermediate/multimodal/figure_001.txt
intermediate/multimodal/image_groups.json
```

Each request handles one figure group. If `--skip-multimodal` is set, this stage is skipped.

## Postprocess

Postprocess reads raw `.txt` outputs and writes JSON:

```text
final/text_extraction.json
final/figure_001.json
final/multimodal_figures.json
```

It handles common model output issues:

- Markdown code fences.
- `<think>...</think>` blocks.
- extra explanation around JSON.
- single-object versus list output for figures.

## How To Run

Extraction only:

```bash
python3 steeldig.py extract -- \
  --config config/workflow.json \
  --input dataset \
  --output-root outputs_dataset \
  --recursive
```

Recommended complete pipeline:

```bash
python3 steeldig.py pipeline -- \
  --config config/workflow.json \
  --input dataset \
  --output-root outputs_dataset \
  --recursive \
  --resume-mode resume_partial
```

