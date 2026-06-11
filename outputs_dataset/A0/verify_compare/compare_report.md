# Verify Compare Report: A0

## Scores

| target | score | fields | gate |
|---|---:|---:|---|
| before final | 89.00 | 108 | True |
| after verify | 89.87 | 108 | True |
| delta | +0.87 | +0 | - |

- llm_error_count: 0

## Formula

- yes=1.0, partial=0.6, unknown=0.3, no=0.0
- field_score = correctness_score * evidence_confidence * 100
- sample_score = sum(field_score * field_weight) / sum(field_weight)
- paper_score = sum(sample_score * sample_weight) / sum(sample_weight)

## Detail Reports

- before: /Users/mac/Desktop/SteelDig/SteelDig_multimodal/outputs_dataset/A0/verify_compare/before_final/quality_report.json
- after: /Users/mac/Desktop/SteelDig/SteelDig_multimodal/outputs_dataset/A0/verify_compare/after_verify/quality_report.json
