You are resolving ambiguous sample alignment between a ground-truth JSON and a prediction JSON for one materials-science paper.

Rules:
1. Only align records that are genuinely the same sample condition or a justified split/merge view of the same sample.
2. Favor alignment based on alloy identity, process condition, temperature, time, cooling route, and sample context.
3. A prediction sample may be a split view of one truth sample, for example tensile-only vs impact-only.
4. Do not invent IDs. Only use IDs present in the input JSON.
5. If uncertain, leave the item unmatched.
6. Output JSON only.

Required output format:
{
  "paper_id": "<paper id>",
  "matches": [
    {
      "pred_sample_id": "<prediction sample id>",
      "truth_sample_id": "<truth sample id>",
      "relation": "one_to_one" | "many_to_one" | "one_to_many",
      "confidence": 0.0,
      "reason": "<short reason>"
    }
  ],
  "unmatched_pred": ["<prediction sample id>"],
  "unmatched_truth": ["<truth sample id>"]
}

Input JSON:
{{INPUT_JSON}}
