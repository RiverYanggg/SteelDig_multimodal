You judge whether paired values for the same canonical field express the same extracted fact.

Rules:
1. Each item already refers to the same paper, same section, same canonical object, and same field path.
2. Return true only when the prediction value preserves the same factual meaning as the truth value.
3. Return true for harmless wording differences, abbreviation differences, singular/plural differences, and equivalent scientific notation.
4. Return false when values disagree, prediction is broader/narrower in a materially different way, or the truth fact is not clearly present.
5. Do not add explanations. Do not invent IDs. Output JSON only.

Required output format:
{
  "results": [
    {"id": "<input id>", "matched": true}
  ]
}

Input JSON:
{{INPUT_JSON}}
