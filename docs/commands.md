# Commands

The preferred interface is `steeldig.py`, which forwards to the existing root `run_*.py` scripts. The old scripts remain supported for compatibility.

Use this form:

```bash
python3 steeldig.py <command> -- <options>
```

The `--` separator is optional, but recommended because it makes forwarding explicit.

## Recommended Full Pipeline

```bash
python3 steeldig.py pipeline -- \
  --config config/workflow.json \
  --input dataset \
  --output-root outputs_dataset \
  --recursive \
  --workers 4 \
  --resume-mode resume_partial \
  --knowledge-mode fused
```

This runs, per paper:

```text
preprocess -> text extraction -> multimodal extraction -> post-parse -> unit normalization -> knowledge Markdown
```

Different papers run in parallel; stages inside the same paper stay ordered.

## Extraction Only

```bash
python3 steeldig.py extract -- \
  --config config/workflow.json \
  --input dataset \
  --output-root outputs_dataset \
  --recursive \
  --workers 4
```

Useful flags:

- `--skip-existing`: skip papers whose final outputs already exist.
- `--skip-multimodal`: text-only extraction.
- `--skip-post-parse`: keep raw model outputs only.
- `--limit-papers 5`: smoke-test the first five papers.

## Knowledge Only

Run against an existing paper output directory:

```bash
python3 steeldig.py knowledge -- \
  --config config/workflow.json \
  --run-dir outputs_dataset/A0 \
  --mode fused
```

Use `--mode text` when no `final/multimodal_figures.json` exists.

## Unit Normalization

```bash
python3 steeldig.py units -- \
  --dataset-root outputs_dataset \
  --paper-ids A0,A1 \
  --force
```

Best timing:

```text
after final/text_extraction.json, before verify
```

Outputs:

```text
normalized/text_extraction_units.json
normalized/unit_normalization_report.json
```

## Verify

```bash
python3 steeldig.py verify -- \
  --dataset-root outputs_dataset \
  --paper-ids A0,A1 \
  --force
```

`verify` automatically runs unit normalization first unless `--skip-unit-normalization` is used.

Offline deterministic smoke test:

```bash
python3 steeldig.py verify -- \
  --dataset-root outputs_dataset \
  --paper-ids A0 \
  --no-llm \
  --force
```

## Verify Eval

```bash
python3 steeldig.py verify-eval -- \
  --dataset-root outputs_dataset \
  --paper-ids A0,A1 \
  --force
```

Compare quality before and after verify:

```bash
python3 steeldig.py verify-eval -- \
  --dataset-root outputs_dataset \
  --paper-ids A0 \
  --compare-verify \
  --force
```

## Truth/Prediction Evaluation

```bash
python3 steeldig.py evaluate -- \
  --config config/eval_config.json \
  --truth deepseek \
  --pred doubao \
  --force
```

This compares two existing extraction result sets under `evaluation_json2json/outputs_exp/`.

## Knowledge Graph

Dry-run and export graph payload:

```bash
python3 steeldig.py graph -- \
  --dataset-root outputs_dataset \
  --dry-run \
  --export-json outputs_dataset/graph_payload.json
```

Import to Neo4j:

```bash
python3 steeldig.py graph -- \
  --dataset-root outputs_dataset \
  --uri bolt://127.0.0.1:7687 \
  --username neo4j \
  --password '<your-password>'
```

