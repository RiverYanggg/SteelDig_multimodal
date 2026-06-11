# Module Overview

This page summarizes every major module and points to detailed module documents.

## Pipeline Modules

- `paper_extractor.preprocess`: cleans Markdown, extracts references, and groups figures.
- `paper_extractor.workflow`: calls text and multimodal models and writes raw outputs.
- `paper_extractor.postprocess`: parses raw model outputs into stable JSON files.
- `paper_extractor.unit_normalization`: converts explicit units to canonical engineering units.
- `paper_extractor.knowledge`: builds claim records and `text_knowledge.md`.
- `verify`: performs evidence-based conservative repair.
- `verify_eval`: scores whether fields are supported by paper evidence without ground truth.
- `evaluation_json2json`: compares one extraction result set against another.
- `paper_extractor.knowledge_graph`: converts extraction outputs into Neo4j nodes and relationships.

## Recommended Data Flow

```text
input Markdown
  -> preprocess/cleaned_input.md
  -> intermediate/text/text_extraction.txt
  -> final/text_extraction.json
  -> normalized/text_extraction_units.json
  -> verify/text_extraction_fixed.json
  -> verify_eval/quality_report.json
  -> knowledge graph or downstream evaluation
```

## Module Documents

- [Preprocess](preprocess.md)
- [Extraction And Postprocess](extraction.md)
- [Unit Normalization](unit_normalization.md)
- [Knowledge Workflow](knowledge.md)
- [Verify](verify.md)
- [Verify Eval](verify_eval.md)
- [Evaluation](evaluation.md)
- [Knowledge Graph](knowledge_graph.md)

