# Truth/Prediction Evaluation Module

Implementation:

```text
evaluation_json2json/
run_evaluation.py
```

## Purpose

This module compares two complete extraction result sets. It is for benchmarking model outputs, not for repairing a single paper.

## Expected Input

```text
evaluation_json2json/outputs_exp/<truth_model>/<paper_id>/final/text_extraction.json
evaluation_json2json/outputs_exp/<pred_model>/<paper_id>/final/text_extraction.json
```

Example:

```text
evaluation_json2json/outputs_exp/deepseek/A0/final/text_extraction.json
evaluation_json2json/outputs_exp/doubao/A0/final/text_extraction.json
```

## Matching Strategy

- Pair papers by directory name.
- Align alloy/process/sample objects.
- Canonicalize IDs.
- Expand JSON into field facts.
- Match numeric fields deterministically, including unit-aware comparisons.
- Use LLM only for uncertain semantic field equivalence when enabled.

## Run

```bash
python3 steeldig.py evaluate -- \
  --config config/eval_config.json \
  --truth deepseek \
  --pred doubao \
  --force
```

## Output

```text
evaluation_json2json/output/eval_truth_<truth>_pred_<pred>/
├── evaluation_report.json
├── papers/
├── canonical/
├── diagnostics/
└── field_judge/
```

The top-level report contains precision, recall, and F1 by section and overall.

