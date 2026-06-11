# Data Contract

This document describes the stable files passed between modules.

## Paper ID Rule

`paper_id` is the Markdown filename without `.md`.

Example:

```text
dataset/10.1002_srin.202200207/hybrid_auto/10.1002_srin.202200207.md
```

becomes:

```text
paper_id = 10.1002_srin.202200207
```

Paper IDs must be unique within one run. Duplicate Markdown stems are rejected.

## Required Input Contract

Minimum:

```text
dataset/<paper_id>/hybrid_auto/<paper_id>.md
```

Recommended:

```text
dataset/<paper_id>/hybrid_auto/
├── <paper_id>.md
├── <paper_id>_content_list.json
└── images/
    ├── image_001.jpg
    └── image_002.jpg
```

Markdown image paths should be relative to the Markdown file directory, for example:

```markdown
![Figure 1](images/image_001.jpg)
```

## Stage Contracts

### Preprocess

Input:

```text
<paper_id>.md
```

Output:

```text
preprocess/cleaned_input.md
preprocess/image_groups.json
preprocess/references.json
preprocess/summary.json
```

### Text Extraction

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

### Multimodal Extraction

Input:

```text
preprocess/image_groups.json
images/*
```

Output:

```text
intermediate/multimodal/figure_001.txt
```

### Postprocess

Input:

```text
intermediate/text/text_extraction.txt
intermediate/multimodal/figure_*.txt
```

Output:

```text
final/text_extraction.json
final/figure_001.json
final/multimodal_figures.json
```

### Unit Normalization

Input:

```text
final/text_extraction.json
```

Output:

```text
normalized/text_extraction_units.json
normalized/unit_normalization_report.json
```

### Verify

Input:

```text
normalized/text_extraction_units.json
preprocess/cleaned_input.md
prompt/json_schema.json
```

Fallback input:

```text
final/text_extraction.json
```

Output:

```text
verify/text_extraction_fixed.json
verify/verify_report.json
```

### Verify Eval

Input priority:

```text
verify/text_extraction_fixed.json
normalized/text_extraction_units.json
final/text_extraction.json
```

Output:

```text
verify_eval/quality_report.json
verify_eval/quality_report.md
```

