# Project Structure

SteelDig Multimodal is organized as a staged paper-extraction pipeline. The public interface is the root CLI scripts and `steeldig.py`; implementation lives mostly under `paper_extractor/`, `verify/`, `verify_eval/`, and `evaluation_json2json/`.

## Top-Level Layout

```text
SteelDig_multimodal/
├── steeldig.py                         # unified command wrapper
├── run_paper_workflow.py               # extraction-only compatibility entry
├── run_paper_then_knowledge_workflow.py # recommended full pipeline entry
├── run_unit_normalization.py           # unit normalization entry
├── run_verify.py                       # evidence-based repair entry
├── run_verify_eval.py                  # no-truth quality scoring entry
├── run_evaluation.py                   # truth/pred JSON evaluation entry
├── run_knowledge_graph.py              # Neo4j graph import/export entry
├── config/                             # editable JSON configs
├── docs/                               # user and module documentation
├── input/                              # input format documentation
├── paper_extractor/                    # extraction, preprocess, units, knowledge, graph code
├── prompt/                             # extraction schema and prompts
├── verify/                             # conservative verification module
├── verify_eval/                        # evidence quality evaluation module
├── evaluation_json2json/               # truth/pred evaluation framework
└── tests/                              # regression tests
```

## Runtime Output Layout

The recommended output root is `outputs_dataset/` for post-processing and verification workflows, or `workflow_runs/` for the older extraction naming convention. Both contain one directory per paper:

```text
outputs_dataset/<paper_id>/
├── preprocess/
│   ├── cleaned_input.md
│   ├── image_groups.json
│   ├── references.json
│   └── summary.json
├── intermediate/
│   ├── text/text_extraction.txt
│   └── multimodal/figure_001.txt
├── final/
│   ├── text_extraction.json
│   ├── multimodal_figures.json
│   ├── text_claims.jsonl
│   └── text_knowledge.md
├── normalized/
│   ├── text_extraction_units.json
│   └── unit_normalization_report.json
├── verify/
│   ├── text_extraction_fixed.json
│   └── verify_report.json
└── verify_eval/
    ├── quality_report.json
    └── quality_report.md
```

## Source vs Runtime Files

Keep source files in Git:

- `paper_extractor/**`
- `verify/**`
- `verify_eval/**`
- `evaluation_json2json/**` except generated `output/` and `outputs_exp/`
- `config/*.json` only when they contain placeholders, not private keys
- `docs/**`, `prompt/**`, `tests/**`, root `run_*.py`, and `steeldig.py`

Do not commit runtime outputs or private inputs:

- `outputs_dataset/`
- `workflow_runs/`
- `dataset/`
- `input/raw/`
- `evaluation_json2json/output/`
- `evaluation_json2json/outputs_exp/`

