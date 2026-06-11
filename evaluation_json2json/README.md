# Evaluation Framework

这个目录实现当前的结构化抽取评估流程。它比较两套 `text_extraction.json`，数据来自 `outputs_exp/` 下各模型的抽取结果目录。

当前 `outputs_exp/` 中可用的模型目录示例：`deepseek`、`doubao`、`kimi`（以实际存在的子目录为准）。

- 真值（truth）：`outputs_exp/<truth_model>/<paper_id>/final/text_extraction.json`
- 预测（pred）：`outputs_exp/<pred_model>/<paper_id>/final/text_extraction.json`

通过 `--truth` 与 `--pred` 可任意指定哪套模型作为真值、哪套作为预测。例如 `--truth doubao --pred deepseek` 表示以 doubao 为真值、以 deepseek 为预测进行评估。

当前评估的核心原则是：

- 论文级配对由目录名决定，例如 `A0`、`A1`。
- 先做对象对齐，尤其是 `alloy/process/sample`。
- 对齐后由代码展开同一个 canonical object 下的同一个字段。
- 代码先做确定性判断；只有语义不确定的同字段值才交给 LLM judge。
- LLM judge 只输出 `true/false`，不负责计算指标。
- Precision/Recall/F1 全部由代码根据最终字段匹配结果计算。

---

## Current Pipeline

### 1. Paper Pairing

`loader.py` 按 paper key 读取 truth 和 prediction。当前支持嵌套路径：

```text
outputs_exp/deepseek/A0/final/text_extraction.json
outputs_exp/doubao/A0/final/text_extraction.json
```

paper key 来自目录名 `A0`，不强依赖 JSON 内部 `paper_id`。这样可以避免 truth/pred 内部 ID 命名不同造成无意义失配。

### 2. Object Alignment

对象对齐由 `SampleLLMBridge` 完成，提示词在：

```text
evaluation_json2json/prompts/sample_bridge_prompt.md
```

一次对象对齐请求会把同一篇 paper 的以下信息发给 LLM：

- truth alloys
- prediction alloys
- truth processes
- prediction processes
- truth samples
- prediction samples
- 与 sample 相关的压缩上下文，例如 structures/properties/interfaces/processing_steps 摘要

LLM 输出三类对齐结果：

```json
{
  "alloy_matches": [],
  "process_matches": [],
  "matches": []
}
```

其中 `matches` 是 sample 对齐。每条对齐包含 prediction ID、truth ID、relation、confidence 和简短 reason。

### 3. Canonicalization

代码根据对象对齐结果生成 canonical map，把 truth 和 prediction 中不同命名的 ID 映射到同一个 canonical ID。

例如：

```json
{
  "truth": {
    "sample_3cu": "sample_3cu"
  },
  "prediction": {
    "sample_3cu_01": "sample_3cu"
  }
}
```

之后字段评估都基于 canonical ID，而不是原始 prediction ID。

中间文件保存到：

```text
evaluation_json2json/output/eval_truth_<truth>_pred_<pred>/canonical/<paper_id>.canonical.json
```

这个文件包含：

- `canonical_maps`
- LLM alignment 原始结构化结果
- 每个 section 展平后的 truth fields
- 每个 section 展平后的 prediction fields

canonical ID 不是新生成的随机 ID，而是以 truth 侧 ID 作为标准 ID；prediction 侧 ID 通过 LLM 对齐结果映射到这个 truth ID。未被对齐的对象会保留自己的原始 ID，不会被强行映射。

### 4. Field Expansion

`scoring.py` 会把每个 section 的 JSON 展平成字段事实。

例如：

```text
structures.sample_3cu.overall_structure
structures.sample_3cu.microstructure_list[2].phases_present[carbide].morphology
alloys.alloy_3cu.nominal_composition[cu].weight_percent
```

字段展开时会跳过纯 ID 字段，例如：

```text
sample_id
alloy_id
process_id
paper_id
uuid
```

如果字段是 `{value, unit}` 或 `{temperature, unit}`，代码会合并成：

```text
value_with_unit
temperature_with_unit
```

这样后续可以做单位归一和数值比较。

### 5. Deterministic Matching

同一个 canonical object 下，只有 truth path 和 prediction path 完全一致时，才会形成候选字段对。

代码先做确定性判断，包括：

- 归一化后完全一致
- 数值匹配
- 单位换算
- 容差匹配
- 简单同义词匹配
- 标签归一，例如 `γ`/`gamma`/`austenite`
- `bal` 和 `balance`
- `WQ` 和 `water quench`

这些规则在：

```text
evaluation_json2json/field_match.py
../config/field_rules.json
```

### 6. Field-Level LLM Judge

只有满足以下条件的字段才会交给 LLM judge：

```text
same_sample = true
same_path = true
代码确定性规则无法判断
字段属于语义文本类字段
```

LLM judge 不做字段匹配，也不计算指标。它只判断已经配好的同字段值是否语义等价。

输入示例：

```json
{
  "id": "structures:2:structures_sample_3cu_overall_structure",
  "section": "structures",
  "canonical_object": "sample_3cu",
  "field": "overall_structure",
  "field_path": "overall_structure",
  "truth_path": "structures.sample_3cu.overall_structure",
  "prediction_path": "structures.sample_3cu.overall_structure",
  "same_sample": true,
  "same_path": true,
  "truth_value": "Austenitic matrix with coherent κ-carbide and Cu-rich phase.",
  "prediction_value": "Austenitic matrix with co-precipitated Cu-rich phase and κ-carbide particles."
}
```

输出格式很小：

```json
{
  "results": [
    {
      "id": "structures:2:structures_sample_3cu_overall_structure",
      "matched": true
    }
  ]
}
```

字段级 judge 的提示词在：

```text
evaluation_json2json/prompts/field_judge_prompt.md
```

### 7. Metric Calculation

LLM 只决定共同字段对是否 `matched=true/false`。最终指标由代码计算。

对每个 section：

```text
TP = truth 和 prediction 都有该字段，且字段值匹配
FP = prediction 多出的字段 + 共同字段但判断为 false
FN = truth 缺失字段 + 共同字段但判断为 false
```

因此：

```text
precision = TP / prediction_field_count
recall = TP / truth_field_count
f1 = 2 * precision * recall / (precision + recall)
```

代码不让 LLM 直接输出 precision、recall 或 f1。

---

## Request Count

一篇 paper 的 LLM 请求数为：

```text
1 次 alloy/process/sample 对齐
+ N 次字段级 judge
```

其中 `N` 是该 paper 中触发语义判断的 section 数量。每个 section 最多一次字段级 judge。没有不确定字段的 section 不请求。

例如 A0 实际触发过：

```text
papers
structures
interfaces
characterization_methods
unmapped_findings
```

因此 A0 是：

```text
1 次对象对齐 + 5 次字段 judge = 6 次 LLM 请求
```

---

## Output Files

全量评估后，输出在：

```text
evaluation_json2json/output/eval_truth_<truth>_pred_<pred>/
├── evaluation_report.json
├── papers/
│   ├── A0.evaluation.json
│   └── ...
├── diagnostics/
│   ├── A0.diagnostics.json
│   └── ...
├── canonical/
│   ├── A0.canonical.json
│   └── ...
└── field_judge/
    ├── A0.field_judge.json
    └── ...
```

目录名由真值/预测模型自动拼接，例如 `eval_truth_doubao_pred_deepseek` 表示 truth=doubao、pred=deepseek。

### `evaluation_report.json`

这是数据集级总报告。当前文件开头先展示全局结构级和字段级评估：

```json
{
  "global_evaluation": {
    "structure": {
      "precision": 0.7124958786679855,
      "recall": 0.40033345683586513,
      "f1": 0.5126319535049223
    },
    "facts": {
      "precision": 0.37215121390410494,
      "recall": 0.24287227469326508,
      "f1": 0.2939244224863133
    }
  }
}
```

它还包含：

- `meta`
- `dataset_summary`
- `paper_index`

### `global_evaluation`

这是所有 section、所有 paper 汇总后的全局指标。

含义：

- `structure`：对象级全局 Precision/Recall/F1，衡量记录是否抽出并对齐。
- `facts`：字段级全局 Precision/Recall/F1，衡量字段值是否正确覆盖。
- `precision`：prediction 中有多少被判断为正确。
- `recall`：truth 中有多少被 prediction 正确覆盖。
- `f1`：precision 和 recall 的调和平均。

### `dataset_summary.section_summary`

这里按 section 汇总结构级和字段级指标。

每个 section 有两类指标：

```json
{
  "structure": {
    "truth_count": 0,
    "prediction_count": 0,
    "matched_count": 0,
    "precision": 0.0,
    "recall": 0.0,
    "f1": 0.0
  },
  "facts": {
    "truth_count": 0,
    "prediction_count": 0,
    "matched_count": 0,
    "precision": 0.0,
    "recall": 0.0,
    "f1": 0.0
  }
}
```

`structure` 表示对象层面的数量和对齐情况。`facts` 表示字段值层面的正确性。

### `paper_index`

这是总报告到单篇文件的索引。每篇包含：

- `paper_id`
- `report_path`
- `diagnostics_path`
- `canonical_path`
- `field_judge_path`
- `prediction_empty`
- `section_metrics`
- `has_llm_bridge`
- `skipped_existing`

如果你要分析某篇低分 paper，先从这里找到对应文件路径。

### `papers/<paper_id>.evaluation.json`

这是最干净的单篇指标文件。它只保留：

- paper 基本路径
- `average_metrics`
- `section_metrics`
- LLM alignment 是否可用及匹配数量

它适合快速查看一篇 paper 的各 section 得分，不适合看详细错误原因。

### `diagnostics/<paper_id>.diagnostics.json`

这是单篇诊断文件。它包含：

- section structure metrics
- missing truth fact examples
- extra prediction fact examples
- mismatched fact examples
- LLM judge candidate count
- match method summary

这个文件适合分析为什么某个 section 低分。

### `canonical/<paper_id>.canonical.json`

这是对象对齐后的中间文件。重点看：

- `canonical_maps.truth`
- `canonical_maps.prediction`
- `alignment.alloy_matches`
- `alignment.process_matches`
- `alignment.sample_matches`
- `flattened_sections`

如果你怀疑 sample 对齐错了，优先看这个文件。

### `field_judge/<paper_id>.field_judge.json`

这是字段级 LLM judge 日志。重点看：

- `sections.<section>.input_candidates`
- `sections.<section>.raw_response`
- `sections.<section>.decisions`
- `sections.<section>.candidates`

`input_candidates` 是真实发送给 LLM 的内容。每条都包含：

- `id`
- `section`
- `canonical_object`
- `truth_path`
- `prediction_path`
- `same_sample`
- `same_path`
- `truth_value`
- `prediction_value`

`candidates` 是合并 LLM 判断后的字段结果。

---

## How To Analyze Results

### Step 1: 先看全局指标

打开：

```text
evaluation_json2json/output/eval_truth_<truth>_pred_<pred>/evaluation_report.json
```

先看：

```text
global_evaluation.structure.precision
global_evaluation.structure.recall
global_evaluation.structure.f1
global_evaluation.facts.precision
global_evaluation.facts.recall
global_evaluation.facts.f1
```

当前全量结果是：

```text
structure.precision = 0.7124958786679855
structure.recall    = 0.40033345683586513
structure.f1        = 0.5126319535049223

facts.precision     = 0.37215121390410494
facts.recall        = 0.24287227469326508
facts.f1            = 0.2939244224863133
```

解释：

- structure recall 低：truth 中很多对象没有被 prediction 正确抽出或对齐。
- facts precision 低：prediction 字段中有较多 extra 或错误字段。
- facts recall 低：truth 字段中有大量字段没有被正确覆盖。
- facts recall 明显低于 facts precision：主要问题更偏漏抽取或对象/字段没有对齐上，而不是单纯错值。

### Step 2: 看 section summary

继续看：

```text
dataset_summary.section_summary
```

建议优先看这些 section：

- `alloys`
- `processes`
- `samples`
- `processing_steps`
- `structures`
- `properties`
- `performance`

判断方式：

- `structure.f1` 低：对象没抽出来、抽多了、粒度不同、sample/process 对齐困难。
- `facts.f1` 低：对象存在后，字段值不正确、字段缺失、字段路径不一致。
- `structure.f1` 高但 `facts.f1` 低：对象识别可用，字段抽取质量不足。
- `structure.f1` 低且 `facts.f1` 低：优先排查对象抽取和对齐，而不是字段值。

### Step 3: 定位低分 paper

从 `paper_index` 找到低分 paper 的路径：

```text
paper_index[].report_path
paper_index[].diagnostics_path
paper_index[].canonical_path
paper_index[].field_judge_path
```

建议顺序：

1. 打开 `papers/<paper_id>.evaluation.json` 看哪个 section 低。
2. 打开 `canonical/<paper_id>.canonical.json` 看 sample/alloy/process 是否对齐正确。
3. 打开 `diagnostics/<paper_id>.diagnostics.json` 看 missing/extra/mismatch。
4. 打开 `field_judge/<paper_id>.field_judge.json` 看 LLM 判断是否合理。

### Step 4: 判断是对齐问题还是抽取问题

如果 `canonical_maps.prediction` 中 sample 映射明显错误，说明是对象对齐问题。

如果 sample 对齐正确，但 `missing_truth_fact_examples` 很多，说明预测 JSON 漏字段。

如果 `extra_prediction_fact_examples` 很多，说明预测 JSON 多抽或路径结构和 truth 不一致。

如果 `field_judge.input_candidates` 中 LLM 对同字段判断不合理，说明需要调整 `field_judge_prompt.md`。

---

## Common Failure Modes

### 1. Prediction 没有抽出来

表现：

- `prediction_empty = true`
- `prediction_count` 很低
- 大量 missing truth facts

处理：

- 这通常是上游抽取问题，不是 evaluation 对齐问题。

### 2. Sample 或 Process 粒度不一致

表现：

- `samples.structure.f1` 或 `processes.structure.f1` 低
- truth 和 prediction 的 sample/process 数量差异大
- `canonical` 文件中出现 many-to-one 或 one-to-many

处理：

- 先看 `canonical/<paper_id>.canonical.json`
- 判断 LLM 对齐是否合理
- 如果 prediction 真的把多个 truth 条件合并了，低 recall 是合理结果

### 3. 同一个 sample 下字段 path 对不上

表现：

- LLM judge 候选少
- missing 和 extra 都很多
- truth 和 prediction 实际表达相近，但路径不同

例子：

```text
truth: structures.sample_3cu.phases_present[cu_rich_phase].morphology
pred:  structures.sample_3cu.precipitates[cu_rich_phase].morphology
```

当前规则不会把不同 path 发给 LLM。因为评估原则是：

```text
same_sample + same_path 才能判断字段值是否匹配
```

这种情况会体现为 missing/extra，而不是 LLM false。

### 4. 同字段语义接近但文字不同

表现：

- `field_judge/<paper_id>.field_judge.json` 中有 input candidates
- `method = llm_field_judge`

例子：

```text
truth: dots or bars
pred: dot, bar shape
```

这种交给 LLM judge 判断 true/false。

### 5. 非语义字段不一致

表现：

- 不进入 LLM judge
- 直接 `deterministic_mismatch`

例子：

```text
truth: 550 °C
pred: 500 °C
```

这类由代码数值规则判断，不需要 LLM。

---

## Configuration

### 目录结构

```text
evaluation_json2json/     # 本项目根目录
├── run_evaluation.py     # 命令行入口
├── outputs_exp/          # 各模型抽取结果（输入）
│   ├── deepseek/
│   │   └── A0/final/text_extraction.json
│   ├── doubao/
│   └── kimi/
├── output/               # 评估结果（输出，按对比组合分子目录）
│   └── eval_truth_<truth>_pred_<pred>/
├── config/
│   └── code files
└── prompts/
```

运行配置统一放在项目顶层：

```text
../config/
├── eval_config.json
├── eval_config_llm.json
└── field_rules.json
```

### 默认配置

```text
../config/eval_config.json
```

关键字段：

```json
{
  "outputs_exp_root": "../evaluation_json2json/outputs_exp",
  "truth_model": "deepseek",
  "pred_model": "doubao",
  "output_root": "../evaluation_json2json/output",
  "field_rules_path": "field_rules.json",
  "force": false,
  "llm_bridge": {
    "enabled": false,
    "model": "deepseek-v4-flash",
    "base_url": "https://api.deepseek.com",
    "api_key": "EMPTY",
    "temperature": 0.0,
    "prompt_path": "../evaluation_json2json/prompts/sample_bridge_prompt.md",
    "verify_ssl": true
  }
}
```

说明：

- `truth_model` / `pred_model`：分别对应 `outputs_exp/<模型名>/`；命令行 `--truth` / `--pred` 会覆盖配置文件。
- 输出目录自动为 `output/eval_truth_<truth>_pred_<pred>/`，不同对比实验互不覆盖。
- `force=false` 时，若单篇 evaluation、diagnostics、canonical、field_judge 均已存在则跳过。
- `force=true` 或 `--force` 强制重评。
- `llm_bridge.api_key` 建议 `EMPTY`，用环境变量 `EVAL_LLM_API_KEY` 或 `DEEPSEEK_API_KEY` 注入。
- 字段 judge 使用 `prompts/field_judge_prompt.md`。

如果要把 API 参数写入配置文件，编辑：

```text
../config/eval_config_llm.json
```

填写其中的 `llm_bridge.model`、`llm_bridge.base_url` 和 `llm_bridge.api_key`。

仍支持旧版 `truth_dir` + `prediction_root` 显式路径，但不与 `truth_model` / `pred_model` 同时使用。

---

## How To Run

在本项目根目录（`evaluation_json2json/`）执行：

```bash
cd /path/to/evaluation_json2json
```

### 查看可用模型

```bash
ls outputs_exp
```

### 全量评估（deepseek 为真值，doubao 为预测）

```bash
python3 run_evaluation.py --truth deepseek --pred doubao
```

输出：

```text
output/eval_truth_deepseek_pred_doubao/
```

### 反向对比（doubao 为真值，deepseek 为预测）

```bash
python3 run_evaluation.py --truth doubao --pred deepseek
```

输出：

```text
output/eval_truth_doubao_pred_deepseek/
```

### 使用配置文件默认值

```bash
python3 run_evaluation.py --config ../config/eval_config.json
```

### 单篇调试

```bash
python3 run_evaluation.py --truth deepseek --pred doubao --paper-ids A0 --force
```

### 启用 LLM

```bash
python3 run_evaluation.py \
  --truth deepseek \
  --pred kimi \
  --enable-llm-bridge \
  --llm-api-key "$DEEPSEEK_API_KEY"
```

### 终端日志与进度

默认在 stderr 输出带时间戳的日志，并在 TTY 下显示单行进度条，例如：

```text
[eval    0.1s] 共 82 篇论文待处理
[eval    9.3s] A0: LLM 桥接 OK — alloy=2, process=2, sample=2
[eval   32.6s] A0: 完成 | structure_f1=0.542 | fact_f1=0.295
[==============================--]  50% (41/82) eval A41
```

- `--quiet`：关闭进度与详细日志
- `--no-progress-bar`：保留逐行日志，不使用单行进度条

### 并行与跳过

- 默认 `--workers 4`，多线程并行评估各篇论文（LLM 请求为 IO 密集型）
- **Skip 规则**：仅当以下四个文件**均已存在**时跳过该篇（除非 `--force`）：
  - `papers/<paper_id>.evaluation.json`
  - `diagnostics/<paper_id>.diagnostics.json`
  - `canonical/<paper_id>.canonical.json`
  - `field_judge/<paper_id>.field_judge.json`
- 配置文件 `../config/eval_config.json` 中可设置 `"workers": 4`

```bash
python3 run_evaluation.py --truth deepseek --pred doubao --workers 8
```

### 参数一览

| 参数 | 说明 |
|------|------|
| `--truth` | 真值模型名 → `outputs_exp/<name>/` |
| `--pred` | 预测模型名 → `outputs_exp/<name>/` |
| `--config` | 配置文件路径 |
| `--outputs-exp-root` | 覆盖模型输出根目录 |
| `--output-root` | 覆盖评估结果根目录 |
| `--truth-dir` / `--prediction-root` | 直接指定目录（高级） |
| `--paper-ids` | 逗号分隔，只评指定论文 |
| `--force` | 强制重跑 |
| `--workers` | 并行线程数，默认 4 |
| `--quiet` | 静默模式 |
| `--no-progress-bar` | 仅逐行日志 |

---

## Implementation Map

主要文件：

- `framework.py`：主流程、逐篇写入、skip、总报告聚合。
- `llm_bridge.py`：对象对齐与字段 judge。
- `scoring.py`：字段展开与指标计算。
- `field_match.py`：确定性字段匹配。
- `loader.py`：truth/prediction 配对。
- `config.py`：配置、模型路径与输出目录命名。
- `run_evaluation.py`：命令行入口。

Prompt 文件：

- `prompts/sample_bridge_prompt.md`
- `prompts/field_judge_prompt.md`

---

## Practical Checklist

分析一次评估时，建议按这个顺序：

1. 看 `evaluation_report.json.global_evaluation`，判断全局质量。
2. 看 `dataset_summary.section_summary`，找最差 section。
3. 看 `paper_index`，定位低分 paper。
4. 打开 `papers/<paper_id>.evaluation.json`，确认低分来自哪个 section。
5. 打开 `canonical/<paper_id>.canonical.json`，检查 object/sample 对齐。
6. 打开 `diagnostics/<paper_id>.diagnostics.json`，检查 missing/extra/mismatch。
7. 打开 `field_judge/<paper_id>.field_judge.json`，核查 LLM true/false 是否合理。

如果要判断某个低分是否合理，优先回答两个问题：

```text
1. same_sample 是否成立？
2. same_path 是否成立？
```

只有两者都成立，字段值才会进入 LLM judge。否则它应当被视为 missing/extra 或对象/路径结构问题。
