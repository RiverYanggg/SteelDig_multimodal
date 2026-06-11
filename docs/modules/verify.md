# Verify Module

Implementation:

```text
verify/
run_verify.py
```

## Purpose

`verify` is a conservative evidence-based repair stage. It does not re-extract the whole paper. It validates structure, builds sample-level evidence bundles, asks an LLM for limited patch proposals when enabled, and applies only patches that pass code-side checks.

## Input Priority

```text
normalized/text_extraction_units.json
final/text_extraction.json
```

`run_verify.py` automatically runs unit normalization first unless `--skip-unit-normalization` is used.

Required evidence:

```text
preprocess/cleaned_input.md
prompt/json_schema.json
```

## Output

```text
verify/
├── text_extraction_fixed.json
├── verify_report.json
├── deterministic_report.json
├── deterministic_report_after.json
├── evidence_blocks.json
├── sample_bundles/
├── sample_inputs/
├── sample_raw_outputs/
└── patches/
```

`text_extraction_fixed.json` is a full JSON file, not a diff.

## Run

```bash
python3 steeldig.py verify -- \
  --dataset-root outputs_dataset \
  --paper-ids A0,A1 \
  --force
```

No-LLM smoke test:

```bash
python3 steeldig.py verify -- \
  --dataset-root outputs_dataset \
  --paper-ids A0 \
  --no-llm \
  --force
```

## When To Use

Run verify after unit normalization and before quality scoring or graph import when you need a more reliable `text_extraction_fixed.json`.

