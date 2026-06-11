# Configuration

SteelDig uses JSON configuration files under `config/`. Prefer committing examples with `api_key: "EMPTY"` and injecting real keys through environment variables or command-line overrides.

## Main Workflow Config

Default example:

```text
config/workflow.example.json
```

Typical local copy:

```bash
cp config/workflow.example.json config/workflow.json
```

Important fields:

```json
{
  "input_path": "../dataset",
  "output_root": "../outputs_dataset",
  "recursive": true,
  "workers": 1,
  "limit_papers": 0,
  "skip_post_parse": false,
  "skip_multimodal": false,
  "text_model": {
    "model": "deepseek-v4-pro",
    "base_url": "https://api.deepseek.com",
    "api_key": "EMPTY",
    "max_tokens": 128000
  },
  "multimodal_model": {
    "model": "kimi-k2.5",
    "base_url": "https://api.moonshot.cn/v1",
    "api_key": "EMPTY",
    "max_tokens": 65536
  }
}
```

Field meanings:

- `input_path`: Markdown file or directory. Relative paths are resolved from the config file directory.
- `output_root`: output directory containing `<paper_id>/...`.
- `recursive`: recursively scan Markdown files when `input_path` is a directory.
- `workers`: number of papers processed in parallel. Stages inside one paper remain sequential in the recommended pipeline.
- `limit_papers`: `0` means no limit.
- `skip_post_parse`: keep only raw model text, without writing `final/*.json`.
- `skip_multimodal`: skip figure image analysis.
- `text_model`: OpenAI-compatible chat endpoint for text extraction.
- `multimodal_model`: OpenAI-compatible chat endpoint for figure analysis.

## Verify Config

File:

```text
config/verify_config.json
```

It is used by both `verify` and `verify_eval`.

Important fields:

- `dataset_root`: output root containing `<paper_id>/final/text_extraction.json`.
- `schema_path`: normally `../prompt/json_schema.json`.
- `workers`: number of papers verified in parallel.
- `max_evidence_chars`: maximum cleaned text chars sent into evidence workflows.
- `append_record_enabled`: whether verify may append records rather than only patch existing ones.
- `llm_enabled`: disable for deterministic smoke runs.
- `llm`: OpenAI-compatible judge/fixer endpoint.

Environment variable fallback is supported for verify and evaluation:

```bash
export EVAL_LLM_MODEL="deepseek-v4-flash"
export EVAL_LLM_BASE_URL="https://api.deepseek.com"
export EVAL_LLM_API_KEY="..."
```

Equivalent `DEEPSEEK_MODEL`, `DEEPSEEK_BASE_URL`, and `DEEPSEEK_API_KEY` variables are also supported.

## Evaluation Config

File:

```text
config/eval_config.json
```

This config compares two model output sets:

```text
evaluation_json2json/outputs_exp/<truth_model>/<paper_id>/final/text_extraction.json
evaluation_json2json/outputs_exp/<pred_model>/<paper_id>/final/text_extraction.json
```

Important fields:

- `outputs_exp_root`: root of model output directories.
- `truth_model`: model directory treated as truth.
- `pred_model`: model directory treated as prediction.
- `output_root`: evaluation reports root.
- `field_rules_path`: numeric tolerances, ID-field rules, and text-field rules.
- `llm_bridge.enabled`: whether to use LLM for sample/alloy/process alignment and semantic field judging.

## Secret Handling

Do not commit real keys in config files. Recommended options:

- Use environment variables for verify/evaluation.
- Use command-line overrides for extraction, for example `--text-api-key "$TEXT_API_KEY"`.
- Keep private config copies as `config/*.local.json`, which are ignored by Git.

