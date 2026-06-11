# Verify Eval Module

Implementation:

```text
verify_eval/
run_verify_eval.py
```

## Purpose

`verify_eval` scores extraction quality without a ground-truth JSON. It checks whether fields are structurally valid and supported by evidence in the cleaned paper text.

It does not modify extraction JSON.

## Input Priority

```text
verify/text_extraction_fixed.json
normalized/text_extraction_units.json
final/text_extraction.json
```

This priority lets it evaluate the best available post-processed artifact.

## Output

Per paper:

```text
verify_eval/
├── quality_report.json
├── quality_report.md
├── field_facts.json
├── evidence_blocks.json
├── sample_eval_report.json
└── gate_report.json
```

Dataset summary:

```text
outputs_dataset/verify_eval_summary.json
outputs_dataset/verify_eval_summary.md
```

## Run

```bash
python3 steeldig.py verify-eval -- \
  --dataset-root outputs_dataset \
  --paper-ids A0,A1 \
  --force
```

Compare original/fixed quality:

```bash
python3 steeldig.py verify-eval -- \
  --dataset-root outputs_dataset \
  --paper-ids A0 \
  --compare-verify \
  --force
```

## Interpretation

Use `quality_report.md` for human review and `quality_report.json` for automation. Low score usually means one of:

- fields have weak or missing evidence,
- IDs or sample links are inconsistent,
- text extraction hallucinated details,
- unit or numeric representation is inconsistent.

