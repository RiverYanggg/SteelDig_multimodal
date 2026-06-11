# Input Files

This directory documents the expected input format. Real papers should normally live in `dataset/` or another path passed with `--input`; raw/private data should not be committed.

## Recommended MinerU Layout

SteelDig expects Markdown generated from a paper PDF. The most reliable layout is:

```text
dataset/
└── <paper_id>/
    └── hybrid_auto/
        ├── <paper_id>.md
        ├── <paper_id>_content_list.json
        └── images/
            ├── image_001.jpg
            ├── image_002.jpg
            └── ...
```

Only the Markdown file is strictly required. `*_content_list.json` and `images/` improve cleaning and multimodal extraction.

## File Naming

The Markdown stem becomes `paper_id`.

Good:

```text
10.1002_srin.202200207.md
A0.md
paper_001.md
```

Bad:

```text
paper.md
paper.md
```

Duplicate stems are rejected because both would write to the same output directory.

## Markdown Requirements

The Markdown should contain:

- title and abstract when available,
- section headings,
- body text,
- figure captions close to their image links,
- image links relative to the Markdown file directory.

Example image syntax:

```markdown
![Figure 1](images/image_001.jpg)

Figure 1. SEM image of the alloy after annealing...
```

## Optional `content_list`

MinerU often emits a companion file:

```text
<paper_id>_content_list.json
```

When present, preprocess uses it to remove references, headers, footers, and copyright blocks more accurately than regex-only cleanup.

## Run With This Input

```bash
python3 steeldig.py pipeline -- \
  --config config/workflow.json \
  --input dataset \
  --output-root outputs_dataset \
  --recursive \
  --workers 4 \
  --resume-mode resume_partial
```

If your files are not under `dataset/`, pass the actual directory:

```bash
python3 steeldig.py pipeline -- \
  --config config/workflow.json \
  --input /path/to/mineru_outputs \
  --output-root outputs_dataset \
  --recursive
```

