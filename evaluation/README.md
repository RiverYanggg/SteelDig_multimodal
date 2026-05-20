# Evaluation Framework

这个目录提供一套专门用于比较两套结构化抽取 JSON 的评估框架，目标是评估：

- 标准答案目录：`json_truth/*.json`
- 预测结果目录：`output/<paper_id>/final/text_extraction.json`

框架默认按论文目录名或文件名 `A0`、`A1` 这类 `paper_key` 进行论文级配对，然后在论文内部做：

1. `alloy` 对齐
2. `process` 对齐
3. `sample` 对齐
4. 各 section 的结构级和事实级评分

这个设计是为了处理一个实际问题：预测 JSON 和标注 JSON 中，`sample_id`、`process_id` 的命名和粒度经常不一致，不能直接按 ID 或列表顺序比较。

---

## Directory Layout

```text
evaluation/
├── __init__.py
├── README.md
├── config/
│   ├── eval_config.json
│   └── field_rules.json
├── output/
│   ├── evaluation_report.json
│   └── papers/
│       ├── A0.evaluation.json
│       └── ...
├── prompts/
│   └── sample_bridge_prompt.md
├── config.py
├── framework.py
├── llm_bridge.py
├── loader.py
├── matcher.py
├── metrics.py
├── normalize.py
└── scoring.py
```

入口脚本在仓库根目录：

- [run_evaluation.py](/org/caep-xuben/yangzijiang/yzj/SteelDig_multimodal/run_evaluation.py)

---

## Core Design

### 1. 论文级配对

直接使用：

- truth 文件名，例如 `A28.json`
- prediction 目录名，例如 `output/A28/final/text_extraction.json`

也就是说，论文级主键是 `A28`，而不是 JSON 内部的 `paper_id`。这是因为真实数据里常见：

- truth: `paper_a28`
- prediction: `A28`

如果强依赖内部 `paper_id`，会造成大量无意义失配。

### 2. 桥接式匹配

#### alloy 匹配

综合以下信息打分：

- `nominal_composition`
- `alloying_elements`
- `alloy_name`
- `aliases`
- `alloy_id` token

#### process 匹配

综合以下信息打分：

- `description`
- `processes_notes`
- 从 `processing_steps` 聚合出来的工艺上下文
- 已匹配的 `alloy`
- 温度和时间等数字 token

注意：`processing_steps` 自己只有 `sample_id`，没有 `process_id`。因此代码里先通过 `sample -> process` 关系反推每个 process 对应的步骤上下文。

#### sample 匹配

综合以下信息打分：

- 已匹配的 `alloy`
- 已匹配的 `process`，如果有
- `sample_id` token
- `sample_id/process_id/alloy_id` 拼出的条件签名
- 来自 `structures/properties/performance/interfaces/processing_steps` 的 sample 上下文

这样可以覆盖几类典型问题：

- truth 和 prediction 的 `sample_id` 命名不同
- prediction 把一个 truth sample 拆成 tensile/impact 两个 sample
- prediction 的 process 粒度比 truth 更粗

### 3. LLM 歧义桥接

当规则匹配不能形成高置信一对一结果时，框架会把候选样本交给 LLM 做歧义消解。

当前实现特点：

- LLM 只参与 `sample` 桥接
- 输入不是整篇 JSON，而是压缩后的候选摘要
- 输出格式要求严格 JSON
- 如果本地缺依赖或接口不可用，会自动降级回规则匹配
- 降级原因会写入最终报告 `meta.llm_bridge_init_error`

---

## Metrics

框架同时输出两类指标。

### 1. 结构级指标

结构级指标回答的问题是：

- 这个 section 的记录数和记录对齐情况怎么样

使用：

- Precision
- Recall
- F1

例如 `alloys`、`processes`、`samples` 的结构级评分，依赖前面的桥接匹配结果。

### 2. 事实级指标

事实级指标回答的问题是：

- 对齐后的 JSON 中，具体字段值提取得对不对

实现方式：

- 先把 JSON 展平为事实槽位
- 用 canonical anchor 生成事实 key
- 再做 truth/pred 的事实比较

主指标：

- Precision
- Recall
- F1

辅助文本指标：

- BLEU
- ROUGE-L F1

数值字段支持容差比较，例如：

- 成分
- 温度
- 时长
- 各类材料性能数值

容差规则在：

- [field_rules.json](/org/caep-xuben/yangzijiang/yzj/SteelDig_multimodal/evaluation/config/field_rules.json)

---

## Current Behavior On This Dataset

基于当前 `Al_82` 数据集的实际结构，框架设计时已经验证过以下现象：

- 共 82 篇论文
- prediction 文件都存在
- 至少 1 篇 prediction 是空结果
- 很多论文的 `samples/processes` 数量和 truth 不一致
- `sample` 和 `process` 的粒度不一致是主要难点

这意味着：

- `papers`、`alloys` 的评估通常较稳定
- `processes`、`samples` 的结构级评分对桥接算法敏感
- 如果启用 LLM 桥接，`samples` 的可解释匹配会更有帮助

---

## Configuration

默认配置文件：

- [eval_config.json](/org/caep-xuben/yangzijiang/yzj/SteelDig_multimodal/evaluation/config/eval_config.json)

主要字段：

```json
{
  "truth_dir": ".../json_truth",
  "prediction_root": ".../output",
  "output_path": ".../evaluation/output/evaluation_report.json",
  "per_paper_output_dir": ".../evaluation/output/papers",
  "field_rules_path": ".../evaluation/config/field_rules.json",
  "matching": {
    "alloy_threshold": 0.55,
    "process_threshold": 0.5,
    "sample_strong_threshold": 0.72,
    "sample_soft_threshold": 0.45,
    "unique_margin": 0.08
  },
  "llm_bridge": {
    "enabled": true,
    "model": "Qwen/Qwen3.5-9B",
    "base_url": "http://127.0.0.1:8000/v1",
    "api_key": "EMPTY",
    "prompt_path": ".../evaluation/prompts/sample_bridge_prompt.md"
  }
}
```

### LLM 配置说明

你可以把下面三个字段替换成你自己的服务配置：

- `base_url`
- `model`
- `api_key`

也可以通过命令行覆盖。

如果需要真正启用 LLM 桥接，本地 Python 环境还需要具备当前仓库依赖：

- `openai`
- `httpx`

如果缺少依赖，主评估仍然会运行，只是 LLM 桥接不可用。

---

## How To Run

### 1. 使用默认配置运行

```bash
python3 run_evaluation.py --config evaluation/config/eval_config.json
```

### 2. 覆盖路径运行

```bash
python3 run_evaluation.py \
  --config evaluation/config/eval_config.json \
  --truth-dir /path/to/json_truth \
  --prediction-root /path/to/output \
  --output-path evaluation/output/evaluation_report.json
```

### 3. 命令行启用或覆盖 LLM 桥接

```bash
python3 run_evaluation.py \
  --config evaluation/config/eval_config.json \
  --enable-llm-bridge \
  --llm-model your-model \
  --llm-base-url http://127.0.0.1:8000/v1 \
  --llm-api-key YOUR_KEY
```

---

## Report Format

输出文件默认是：

- [evaluation_report.json](/org/caep-xuben/yangzijiang/yzj/SteelDig_multimodal/evaluation/output/evaluation_report.json)
- `evaluation/output/papers/<paper_id>.evaluation.json`

顶层结构：

```json
{
  "meta": {},
  "dataset_summary": {},
  "paper_index": []
}
```

### `meta`

记录：

- 总论文数
- 使用的配置
- LLM 桥接是否成功启用
- LLM 桥接初始化失败原因

### `dataset_summary`

按 section 汇总：

- `papers`
- `alloys`
- `processes`
- `samples`
- `processing_steps`
- `structures`
- `interfaces`
- `properties`
- `performance`
- `characterization_methods`
- `computational_details`
- `unmapped_findings`

每个 section 会同时给：

- `structure`
- `facts`

两个维度的 `truth_count/prediction_count/matched_count/precision/recall/f1`。

### `paper_index`

总报告不会内嵌所有论文的完整详情，而是提供索引。每条索引包含：

- `paper_id`
- `report_path`
- `prediction_empty`
- `section_metrics`
- `has_llm_bridge`

### 单篇报告文件

每篇论文的完整评估细节单独写入：

- `evaluation/output/papers/<paper_id>.evaluation.json`

这里会包含：

- `truth_path`
- `prediction_path`
- `prediction_empty`
- `sections`
- `llm_bridge`

其中 `sections.<section>.alignment` 会保留：

- 已匹配对
- truth 未匹配 ID
- pred 未匹配 ID
- 待 LLM 消解候选

这部分对分析桥接失败原因很有用。

---

## How To Read Results

这一节只回答三个问题：

1. 先看哪里
2. 哪些字段最重要
3. 怎么判断问题属于哪一类

### Step 1: 先看总报告

先打开总报告：

- [evaluation_report.json](/org/caep-xuben/yangzijiang/yzj/SteelDig_multimodal/evaluation/output/evaluation_report.json)

优先看这几个位置：

- `meta`
- `dataset_summary.section_summary`
- `paper_index`

建议阅读顺序：

1. 先看 `meta.llm_bridge_available`
2. 再看 `dataset_summary.section_summary`
3. 最后根据 `paper_index` 找低分论文的单篇报告

如果 `meta.llm_bridge_available` 是 `false`，说明这次运行没有真正启用 LLM 歧义桥接，此时 `samples/processes` 的结构结果通常会偏保守。

### Step 2: 关注最重要的 section

并不是所有 section 的权重都一样。

如果你的目标是判断“抽取流程是否靠谱”，建议优先看：

- `papers`
- `alloys`
- `samples`
- `processes`
- `properties`
- `processing_steps`

一般解释如下：

- `papers`：看论文元数据是否基本正确。
- `alloys`：看合金对象是否识别对、成分是否接近正确。
- `samples`：看桥接是否成功，这是整个评估里最关键的关系层。
- `processes`：看热处理和工艺条件是否被正确分组。
- `properties`：看机械性能、物理性能等核心数值有没有抽对。
- `processing_steps`：看工艺过程拆分是否细致、温度和时间是否正确。

如果你做的是材料数据库构建，通常最重要的是：

- `alloys`
- `samples`
- `processes`
- `properties`

### Step 3: 先看结构，再看事实

每个 section 都分成两层：

- `structure`
- `facts`

建议这样理解：

- `structure`：对象有没有找对、数量对不对、桥接对不对。
- `facts`：对象找对之后，字段值本身对不对。

判断顺序建议固定为：

1. 先看 `structure.f1`
2. 再看 `facts.f1`

典型含义：

- `structure` 高，`facts` 低：对象基本找对了，但字段值抽取质量不够。
- `structure` 低，`facts` 高不起来：通常是桥接、粒度或对象识别有问题。
- `structure` 和 `facts` 都高：这部分整体比较稳。
- `structure` 和 `facts` 都低：这部分是优先排查对象。

---

## Key Fields To Watch

### 总报告中的关键字段

#### `meta.llm_bridge_available`

表示这次评估是否真正启用了 LLM 桥接。

- `true`：`samples` 歧义匹配里会用到 LLM。
- `false`：只用了规则桥接。

#### `meta.llm_bridge_init_error`

如果 LLM 没启起来，这里会告诉你原因。

常见情况：

- API key 没生效
- base_url 不通
- 依赖缺失

#### `dataset_summary.empty_prediction_count`

表示有多少篇论文的 prediction 基本是空的。

如果这个值大于 0，说明有一部分低分不是“抽错”，而是“根本没产出结果”。

#### `dataset_summary.section_summary.<section>.structure`

这里是对象层面的总分。

最重要字段：

- `truth_count`
- `prediction_count`
- `matched_count`
- `precision`
- `recall`
- `f1`

怎么读：

- `prediction_count` 明显大于 `truth_count`：过抽取、过拆分。
- `prediction_count` 明显小于 `truth_count`：漏抽取、过合并。
- `matched_count` 很低：桥接或对象识别有问题。

#### `dataset_summary.section_summary.<section>.facts`

这里是字段层面的总分。

最重要字段：

- `truth_count`
- `prediction_count`
- `matched_count`
- `precision`
- `recall`
- `f1`

怎么读：

- `structure` 不错但 `facts` 差：字段值抽取质量不足。
- `facts.precision` 低：预测里错值或噪声多。
- `facts.recall` 低：漏掉了很多 truth 字段。

#### `paper_index`

这是你从总报告跳到问题论文的入口。

每条记录里重点看：

- `paper_id`
- `report_path`
- `prediction_empty`
- `section_metrics`
- `has_llm_bridge`

推荐用法：

- 先按 `samples.structure_f1`、`processes.structure_f1` 找最差论文
- 再打开对应 `report_path`

### 单篇报告中的关键字段

单篇报告里最重要的是：

- `prediction_empty`
- `sections.<section>.structure_metrics`
- `sections.<section>.fact_metrics`
- `sections.<section>.alignment`
- `llm_bridge`

#### `prediction_empty`

如果是 `true`，这篇论文的大部分低分都不需要再深究字段值，问题在上游抽取产物为空。

#### `sections.<section>.structure_metrics`

这是单篇论文里某个 section 的结构分。

最常用的是：

- `sections.samples.structure_metrics`
- `sections.processes.structure_metrics`
- `sections.properties.structure_metrics`

#### `sections.<section>.fact_metrics`

这是单篇论文里某个 section 的字段分。

最值得看的是：

- `f1`
- `missing_truth_fact_examples`
- `extra_prediction_fact_examples`
- `avg_bleu`
- `avg_rouge_l_f1`

怎么用：

- `missing_truth_fact_examples`：看模型漏了哪些字段。
- `extra_prediction_fact_examples`：看模型多抽了哪些字段。
- `avg_bleu/avg_rouge_l_f1`：看自由文本字段大致接近程度。

#### `sections.<section>.alignment`

这是关系层调试最关键的部分。

最重要字段：

- `matched_pairs`
- `unmatched_truth_ids`
- `unmatched_prediction_ids`
- `llm_candidates`

怎么读：

- `matched_pairs`：说明系统认为哪些对象是一一对应的。
- `unmatched_truth_ids`：truth 里有，但 prediction 没对应上的。
- `unmatched_prediction_ids`：prediction 多出来或没对上的对象。
- `llm_candidates`：规则层拿不准，交给 LLM 的候选。

#### `llm_bridge`

如果这篇论文用了 LLM，这里会保留 LLM 桥接结果。

常看字段：

- `batch_count`
- `matches`
- `errors`
- `batches`

怎么读：

- `matches`：LLM 最终接受了哪些桥接关系。
- `errors`：这一篇是否有 API 或解析错误。
- `batches`：每一批发送给 LLM 的候选集合和原始返回状态。

---

## How To Analyze Typical Failure Modes

你可以把问题大致分成四类。

### 1. 上游没有抽出来

症状：

- `prediction_empty = true`
- 或者 `prediction_count` 非常小
- `unmatched_truth_ids` 很多

结论：

- 这通常不是桥接问题，而是抽取流程本身没有产出足够对象。

### 2. 抽出来了，但命名不同

症状：

- `prediction_count` 和 `truth_count` 接近
- `matched_pairs` 偏少
- `llm_candidates` 很多
- LLM 启用后分数明显变好

结论：

- 这是 ID/命名差异主导的问题，桥接层是主要优化点。

### 3. 抽出来了，但粒度不同

症状：

- `prediction_count` 明显大于或小于 `truth_count`
- `samples` 或 `processes` 的 `structure_f1` 偏低
- 单篇里会出现一对多或多对一场景

典型例子：

- truth 一个 sample，prediction 拆成 tensile 和 impact 两个 sample
- truth 多个 process，prediction 合成一个 process

结论：

- 这是最适合看 `alignment` 和 `llm_bridge.matches` 的情况。

### 4. 对象找对了，但字段值错了

症状：

- `structure_f1` 还可以
- `facts.f1` 明显更低
- `missing_truth_fact_examples` 和 `extra_prediction_fact_examples` 很多

结论：

- 这说明桥接层不是主要问题，重点要去看抽取 prompt、schema 约束和数值解析。

---

## Practical Analysis Workflow

如果你要快速分析一轮评估，我建议固定按下面的顺序：

1. 打开总报告，看 `meta.llm_bridge_available` 是否为 `true`。
2. 看 `dataset_summary.empty_prediction_count`，先排除空预测样本影响。
3. 看 `dataset_summary.section_summary`，找最低的几个 section。
4. 在 `paper_index` 里找这些 section 分数最低的论文。
5. 打开对应单篇报告，看 `alignment`。
6. 如果 `alignment` 没问题，再看 `fact_metrics`。
7. 如果 `llm_bridge.errors` 不为空，先解决桥接执行问题，再解释分数。

最推荐先盯这两个 section：

- `samples`
- `processes`

因为这两层一旦桥接不稳，后面的 `structures/properties/performance` 都会连带受影响。

---

## Matching And Fact Comparison Details

### 为什么 `samples` 的事实级数量可能是 0

`samples` section 本身目前只有桥接字段：

- `sample_id`
- `paper_id`
- `alloy_id`
- `process_id`

这些字段主要用于关系建模，不适合作为抽取事实本身打分。因此第一版里：

- `samples` 的核心价值是结构级对齐
- 真正的内容评分主要体现在 `properties/structures/interfaces/performance/processing_steps`

### 为什么 `processes` 和 `samples` 的 F1 可能偏低

这不是简单实现 bug，而是数据本身存在大量“粒度不一致”：

- truth 把每个热处理条件单列为一个 process/sample
- prediction 可能把多个条件压缩成一个 process
- 或者 prediction 按“温度 + tensile/impact”拆成多个 sample

因此这两部分是 LLM 桥接最重要的应用场景。

---

## Known Limitations

当前版本是第一版框架，已经能稳定输出报告，但还存在几类已知局限：

1. `sample` 的一对多、多对一目前主要体现在 LLM 候选层，规则层仍偏保守。
2. `fact` 展平比较目前按通用路径规则处理，某些复杂嵌套结构还可以做更细粒度的语义主键设计。
3. `process` 匹配对“多个 truth process 被 prediction 压成一个 process”的情况仍然偏严格。
4. 当前只输出 JSON 报告，没有额外导出 CSV 或 Markdown 报表。
5. 如果运行环境缺少 `httpx/openai`，LLM 桥接会自动降级。

---

## Recommended Next Improvements

如果你后续要继续增强，我建议按这个顺序做：

1. 为 `sample` 和 `process` 引入显式的 `group alignment` 结果表示，支持多对一和一对多结构级记分。
2. 为 `properties` 设计更强的子结构主键，例如按 `direction/region/property type` 聚合。
3. 为 `processing_steps` 加单位归一化和时间单位换算。
4. 增加 CSV 输出，方便横向分析每篇论文和每个 section。
5. 给 LLM 桥接增加缓存，避免重复调用。

---

## Files You Will Most Likely Edit

如果你要调参数或替换模型，通常只需要改这些文件：

- [eval_config.json](/org/caep-xuben/yangzijiang/yzj/SteelDig_multimodal/evaluation/config/eval_config.json)
- [field_rules.json](/org/caep-xuben/yangzijiang/yzj/SteelDig_multimodal/evaluation/config/field_rules.json)
- [sample_bridge_prompt.md](/org/caep-xuben/yangzijiang/yzj/SteelDig_multimodal/evaluation/prompts/sample_bridge_prompt.md)

如果你要改算法逻辑，重点看：

- [matcher.py](/org/caep-xuben/yangzijiang/yzj/SteelDig_multimodal/evaluation/matcher.py)
- [scoring.py](/org/caep-xuben/yangzijiang/yzj/SteelDig_multimodal/evaluation/scoring.py)
- [framework.py](/org/caep-xuben/yangzijiang/yzj/SteelDig_multimodal/evaluation/framework.py)

---

## Minimal Workflow

推荐的最小使用流程：

1. 在 `evaluation/config/eval_config.json` 中填写 truth/pred 路径。
2. 如果要启用 LLM 桥接，填写 `base_url/model/api_key`。
3. 执行 `python3 run_evaluation.py --config evaluation/config/eval_config.json`。
4. 查看 `evaluation/output/evaluation_report.json`。
5. 先看总报告里的 `paper_index`。
6. 再打开对应的单篇报告文件。
7. 重点检查 `sections.samples.alignment` 和 `sections.processes.alignment`。

这两部分最能帮助你判断模型问题到底是：

- 没抽出来
- 抽出来了但命名不同
- 抽出来了但粒度不同
- 抽出来了但字段值不一致
