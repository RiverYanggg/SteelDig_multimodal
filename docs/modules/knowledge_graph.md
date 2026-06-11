# Knowledge Graph Module

Implementation:

```text
paper_extractor/knowledge_graph/
run_knowledge_graph.py
```

## Purpose

Convert extraction outputs into a Neo4j graph for cross-paper querying.

## Input

```text
outputs_dataset/<paper_id>/final/text_extraction.json
outputs_dataset/<paper_id>/final/multimodal_figures.json
```

If `verify/text_extraction_fixed.json` is preferred in your downstream workflow, run graph import after copying or adapting the graph builder input policy. The current graph builder reads from `final/`.

## Main Node Types

- `Paper`
- `Alloy`
- `Element`
- `Process`
- `Sample`
- `ProcessingStep`
- `Structure`
- `PhaseOccurrence`
- `Phase`
- `PropertySet`
- `PropertyMeasurement`
- `Characterization`
- `Figure`
- `Finding`

## Dry Run

```bash
python3 steeldig.py graph -- \
  --dataset-root outputs_dataset \
  --dry-run \
  --export-json outputs_dataset/graph_payload.json
```

## Import To Neo4j

```bash
python3 steeldig.py graph -- \
  --dataset-root outputs_dataset \
  --uri bolt://127.0.0.1:7687 \
  --username neo4j \
  --password '<your-password>'
```

Useful queries are documented in:

```text
docs/neo4j_queries.md
```

