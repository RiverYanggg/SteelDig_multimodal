You are aligning extracted objects between a ground-truth JSON and a prediction JSON for one materials-science paper.

Rules:
1. First align alloys using alloy name, aliases, base element, alloying elements, and nominal composition.
2. Then align processes using process description, linked alloy context, linked sample IDs, treatment route, temperature, time, deformation amount, cooling route, and computation settings when relevant.
3. Finally align samples. A truth sample and prediction sample are the same sample when their referenced alloy and process are semantically the same.
4. sample_id text is only supporting evidence. Do not align samples just because sample_id strings look similar.
5. Do not invent IDs. Only use IDs present in the input JSON.
6. If a prediction omits a truth alloy/process/sample, leave it unmatched.
7. If a prediction splits or merges a condition, use relation "many_to_one" or "one_to_many" only when the semantic relationship is explicit.
8. Output JSON only.

Required output format:
{
  "paper_id": "<paper id>",
  "alloy_matches": [
    {
      "pred_alloy_id": "<prediction alloy id>",
      "truth_alloy_id": "<truth alloy id>",
      "relation": "same" | "many_to_one" | "one_to_many",
      "confidence": 0.0,
      "reason": "<short reason>"
    }
  ],
  "process_matches": [
    {
      "pred_process_id": "<prediction process id>",
      "truth_process_id": "<truth process id>",
      "relation": "same" | "many_to_one" | "one_to_many",
      "confidence": 0.0,
      "reason": "<short reason>"
    }
  ],
  "matches": [
    {
      "pred_sample_id": "<prediction sample id>",
      "truth_sample_id": "<truth sample id>",
      "relation": "same" | "many_to_one" | "one_to_many",
      "confidence": 0.0,
      "reason": "<short reason>"
    }
  ],
  "unmatched_prediction_alloys": ["<prediction alloy id>"],
  "unmatched_truth_alloys": ["<truth alloy id>"],
  "unmatched_prediction_processes": ["<prediction process id>"],
  "unmatched_truth_processes": ["<truth process id>"],
  "unmatched_prediction_samples": ["<prediction sample id>"],
  "unmatched_truth_samples": ["<truth sample id>"]
}

Input JSON:
{{INPUT_JSON}}
