# Preprocess Module

Implementation:

```text
paper_extractor/preprocess/
```

Entry function:

```text
paper_extractor.preprocess.preprocess_paper
```

## Purpose

Preprocess turns MinerU-style Markdown into model-ready text. It removes obvious layout noise, extracts references, and builds figure groups for multimodal extraction.

## Input

Required:

```text
<paper_dir>/<paper_id>.md
```

Optional:

```text
<paper_dir>/<paper_id>_content_list.json
<paper_dir>/images/*
```

If `*_content_list.json` exists, category-aware cleanup is used. Without it, regex and Markdown heuristics are used.

## Output

```text
<output_root>/<paper_id>/preprocess/
├── cleaned_input.md
├── image_groups.json
├── references.json
└── summary.json
```

## How Figure Grouping Works

`image_groups.py` scans Markdown image links, nearby captions, and figure references. Each group contains:

- `image_paths`
- `caption`
- `paper_title`
- `paper_abstract`
- `citation_sentences`

This is why multimodal extraction works at figure level, not single-image level.

## When To Use Directly

Normally you do not run this module alone. It is automatically called by:

```bash
python3 steeldig.py extract -- ...
python3 steeldig.py pipeline -- ...
```

Inspect it directly when:

- `cleaned_input.md` loses important text.
- figure captions are mismatched.
- references remain in model input.

