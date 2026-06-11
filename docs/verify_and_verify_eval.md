# Verify 与 Verify Eval 模块说明

本文档说明 `verify` 和 `verify_eval` 两个后处理模块的设计、运行方式、输入输出、LLM 请求次数、评分公式和回溯方法。

这两个模块位于项目根目录下，和 `evaluation_json2json` 同级：

```text
SteelDig_multimodal/
  verify/
  verify_eval/
  run_verify.py
  run_verify_eval.py
  config/verify_config.json
```

它们服务于 `outputs_dataset/<paper_id>/final/text_extraction.json`，目标是让结构化抽取结果更可信、更可审计。

`verify` 和 `verify_eval` 是独立模块，不依赖 `evaluation_json2json` 的代码。它们内部维护自己的字段展开、结构检查、字段规则加载和 LLM 调用工具。

字段结构来源于：

```text
prompt/json_schema.json
```

也就是说，如果后续 `json_schema.json` 增加字段、删除字段或新增顶层 section，`verify_eval` 的字段展开会自动递归处理新的字段；`verify` / `verify_eval` 不需要为每个新字段改代码。

当前仍固定依赖少量关系锚点：

```text
paper_id
alloy_id
process_id
sample_id
```

这些锚点用于判断 alloy -> process -> sample -> downstream records 的引用关系。如果 schema 将来彻底改掉这几个关系字段，需要同步调整关系约束。

---

## 1. 总体关系

推荐执行顺序：

```text
outputs_dataset/<paper_id>/preprocess/cleaned_input.md
outputs_dataset/<paper_id>/final/text_extraction.json
        |
        v
unit_normalization
        |
        v
outputs_dataset/<paper_id>/normalized/text_extraction_units.json
        |
        v
verify
        |
        v
outputs_dataset/<paper_id>/verify/text_extraction_fixed.json
        |
        v
verify_eval
        |
        v
outputs_dataset/<paper_id>/verify_eval/quality_report.json
```

两个模块分工如下：

```text
verify:
  保守修复模块。它不重新抽取整篇论文，只在原始 text_extraction.json 基础上做证据驱动的受限 patch 修复。

verify_eval:
  无真值质量评估模块。它不修改 JSON，只判断字段是否被论文 evidence 支持，并输出可回溯的 paper_score。
```

如果 `verify/text_extraction_fixed.json` 存在，`verify_eval` 优先评估它；否则回退评估 `normalized/text_extraction_units.json`；如果 normalized 不存在，再回退评估 `final/text_extraction.json`。

---

## 2. 共享配置

两个模块共用同一个 LLM 配置文件：

```text
config/verify_config.json
```

示例结构：

```json
{
  "dataset_root": "/Users/mac/Desktop/SteelDig/SteelDig_multimodal/outputs_dataset",
  "force": false,
  "workers": 2,
  "append_record_enabled": false,
  "llm_enabled": true,
  "llm": {
    "model": "deepseek-v4-flash",
    "base_url": "https://api.deepseek.com",
    "api_key": "...",
    "temperature": 0.0,
    "verify_ssl": false
  }
}
```

设计原则：

```text
verify 和 verify_eval 使用同一个 LLM。
不单独引入 verify_llm、eval_llm、judge_llm。
```

---

## 3. Verify 模块

### 3.1 定位

`verify` 是一个保守修复模块。

它不是重新抽取器，不让 LLM 重写完整 `text_extraction.json`。它的目标是：

```text
读取已有 final/text_extraction.json
结合 cleaned_input.md 证据
发现明显结构错误、sample 错挂、引用错误、少量高置信字段错误
让 LLM 提出受限 patch
由代码校验 patch
只应用安全 patch
写出完整 text_extraction_fixed.json
```

### 3.2 输入

每篇 paper 的输入：

```text
outputs_dataset/<paper_id>/final/text_extraction.json
outputs_dataset/<paper_id>/preprocess/cleaned_input.md
```

运行时还会读取：

```text
prompt/json_schema.json
```

用于确定顶层 section、ID 字段、sample-linked section 和字段展开规则。

### 3.3 输出

每篇 paper 的输出目录：

```text
outputs_dataset/<paper_id>/verify/
```

主要文件：

```text
text_extraction_fixed.json
  修复后的完整 JSON。后续流程应优先使用该文件。

verify_report.json
  verify 总报告，包含修复前后结构问题数、accepted patches、rejected patches。

deterministic_report.json
  原始 JSON 的结构检查报告。

deterministic_report_after.json
  patch 应用后的结构检查报告。

evidence_blocks.json
  从 cleaned_input.md 切出的证据块。

sample_bundles/<sample_id>.json
  每个 sample 的局部工作单元。

sample_inputs/<sample_id>.json
  实际发送给 LLM 的输入。

sample_raw_outputs/<sample_id>.json
  LLM 原始 JSON 输出。

patches/<sample_id>.patch.json
  LLM 提出的 patch proposal。
```

最终产物是完整 JSON：

```text
outputs_dataset/<paper_id>/verify/text_extraction_fixed.json
```

它不是差量文件，可以直接替代 `final/text_extraction.json` 供后续模块使用。

### 3.4 LLM 请求次数

`verify` 的请求粒度是 sample。

```text
每篇 paper 的 verify LLM 请求数 = sample_count
```

例如 A0 有两个 sample：

```text
sample_0cu
sample_3cu
```

则 verify 发起 2 次 LLM 请求。

### 3.5 每次 Verify LLM 输入

每次请求输入一个 sample bundle。

示例结构：

```json
{
  "instruction": "中文 verify 提示词",
  "paper_id": "A0",
  "sample_bundle": {
    "sample_id": "sample_3cu",
    "sample": {},
    "alloy": {},
    "process": {},
    "processing_steps": [],
    "structures": [],
    "interfaces": [],
    "properties": [],
    "performance": [],
    "known_issues": [],
    "evidence_blocks": []
  },
  "allowed_patch_ops": [
    "replace_field",
    "move_record_to_sample",
    "drop_record",
    "append_record"
  ],
  "append_record_enabled": false
}
```

其中 evidence blocks 来自 `cleaned_input.md`。

### 3.6 每次 Verify LLM 输出

LLM 只输出 patch proposal，不输出完整 JSON。

无修复时：

```json
{
  "paper_id": "A0",
  "sample_id": "sample_3cu",
  "verdict": "ok",
  "issues": [],
  "patch_ops": [],
  "confidence": "high"
}
```

需要修复时：

```json
{
  "paper_id": "A0",
  "sample_id": "sample_3cu",
  "verdict": "needs_fix",
  "issues": [
    {
      "issue_type": "misassigned_property",
      "target_path": "properties[property_set_id=prop_12]",
      "evidence_refs": ["b0017"],
      "reason": "该性能记录属于 sample_0cu。"
    }
  ],
  "patch_ops": [
    {
      "op": "move_record_to_sample",
      "record_path": "properties[property_set_id=prop_12]",
      "to_sample_id": "sample_0cu",
      "evidence_refs": ["b0017"],
      "reason": "证据明确将该性能归属到 sample_0cu。",
      "confidence": "high"
    }
  ],
  "confidence": "high"
}
```

### 3.7 支持的 patch 操作

当前支持四类受限 patch：

```text
replace_field
  替换已有记录中的一个字段值。

move_record_to_sample
  把已有下游记录移动到另一个已存在 sample_id。

drop_record
  删除明显重复或明显错误的下游记录。
  禁止删除 papers/alloys/processes/samples 主对象。

append_record
  默认关闭。只有 append_record_enabled=true 时才允许。
```

默认关闭 `append_record` 是为了降低幻觉风险。

### 3.8 Patch 校验

LLM patch 不会直接应用。代码会做两层校验：

```text
Patch Schema Validation:
  op 是否支持
  path 是否可解析
  evidence_refs 是否存在
  to_sample_id 是否存在
  record_path 是否唯一匹配一条记录
  confidence 是否不是 low

Patch Safety Validation:
  不能制造重复 ID
  不能破坏 sample/alloy/process 引用
  不能删除核心对象
  不能让结构错误数量增加
```

通过校验的 patch 才会写入 `accepted_patches` 并应用。

---

## 4. Verify Eval 模块

### 4.1 定位

`verify_eval` 是无人工 truth JSON 的质量评估模块。

它不修改目标 JSON，只判断字段值是否被论文证据支持，并输出可回溯分数。

目标优先级：

```text
优先评估:
outputs_dataset/<paper_id>/verify/text_extraction_fixed.json

如果不存在，回退:
outputs_dataset/<paper_id>/final/text_extraction.json
```

### 4.2 输入

每篇 paper 的输入：

```text
outputs_dataset/<paper_id>/verify/text_extraction_fixed.json
或
outputs_dataset/<paper_id>/final/text_extraction.json

outputs_dataset/<paper_id>/verify/evidence_blocks.json
或
outputs_dataset/<paper_id>/preprocess/cleaned_input.md
```

当前实现中，每个 LLM 请求都会输入完整 evidence blocks，不做截断或检索筛选。

原因是当前 DeepSeek 上下文足够长，完整证据更稳定，尤其能避免 paper-level keywords、abstract、composition 等字段因证据筛选而误判 unknown。

字段事实来自对目标 JSON 的动态递归展开。展开逻辑不写死具体字段名，新增字段会自然进入 `field_facts.json` 和后续 LLM judge。

### 4.3 输出

每篇 paper 的输出目录：

```text
outputs_dataset/<paper_id>/verify_eval/
```

主要文件：

```text
quality_report.json
  最终质量报告，包含 paper_score、评分公式、sample 分数、字段级判断。

quality_report.md
  Markdown 版报告，方便人工浏览。

gate_report.json
  结构 gate 报告。

evidence_blocks.json
  本次评估使用的完整证据块。

field_facts.json
  从目标 JSON 展开的字段事实。

sample_inputs/<sample_id>.json
  每个 LLM 请求的输入。

sample_raw_outputs/<sample_id>.json
  LLM 原始输出。

sample_outputs/<sample_id>.json
  解析并打分后的字段结果。

sample_eval_report.json
  sample 级汇总。
```

跨 paper 汇总：

```text
outputs_dataset/verify_eval_summary.json
outputs_dataset/verify_eval_summary.md
```

如果需要验证 `verify` 是否真的提升质量，可以启用双路对比评估：

```bash
python3 run_verify_eval.py --paper-ids A1 --compare-verify --force --workers 1
```

该模式会用完全相同的 `verify_eval` 方法分别评估：

```text
before:
outputs_dataset/<paper_id>/final/text_extraction.json

after:
outputs_dataset/<paper_id>/verify/text_extraction_fixed.json
```

输出目录：

```text
outputs_dataset/<paper_id>/verify_compare/
  before_final/quality_report.json
  before_final/quality_report.md
  after_verify/quality_report.json
  after_verify/quality_report.md
  compare_report.json
  compare_report.md
```

`compare_report.json` 会包含：

```json
{
  "before": {
    "paper_score": 80.0
  },
  "after": {
    "paper_score": 84.0
  },
  "delta": {
    "paper_score": 4.0
  }
}
```

这样可以直接判断 verify 是否真实有效。如果 `delta.paper_score > 0`，说明修复后质量提升；如果小于 0，说明 verify 可能引入了问题，需要检查 accepted patches。

### 4.4 LLM 请求次数

当前 `verify_eval` 请求粒度是：

```text
paper_level + 每个 sample
```

因此：

```text
每篇 paper 的 verify_eval LLM 请求数 = 1 + sample_count
```

其中：

```text
paper_level
  包含 papers、alloys、processes、characterization_methods、computational_details、unmapped_findings 等没有 sample_id 的字段。

sample_x
  包含该 sample 下的 processing_steps、structures、interfaces、properties、performance 等字段。
```

这个设计是一个折中：

```text
比“每字段一次请求”成本低得多。
比“整篇一次请求”更容易回溯 sample 归属问题。
保持请求数稳定，报告结构清晰。
```

### 4.5 每次 Verify Eval LLM 输入

输入文件位置：

```text
outputs_dataset/<paper_id>/verify_eval/sample_inputs/<sample_id>.json
```

`paper_level` 示例：

```json
{
  "instruction": "中文 verify_eval 提示词",
  "paper_id": "A1",
  "sample_id": "paper_level",
  "sample_context": {
    "sample_id": "paper_level",
    "sample": {
      "sample_id": "paper_level"
    },
    "alloy": null,
    "process": null
  },
  "fields": [
    {
      "field_id": "F00005",
      "sample_id": "paper_level",
      "section": "papers",
      "path": "papers.A1.keywords[0]",
      "value": "Low density steels",
      "field_weight": 0.7,
      "candidate_evidence_refs": []
    }
  ],
  "evidence_blocks": [
    {
      "block_id": "b0001",
      "text": "...",
      "char_start": 0,
      "char_end": 100
    }
  ]
}
```

sample 示例：

```json
{
  "instruction": "中文 verify_eval 提示词",
  "paper_id": "A1",
  "sample_id": "sample_austenitic",
  "sample_context": {
    "sample_id": "sample_austenitic",
    "sample": {},
    "alloy": {},
    "process": {}
  },
  "fields": [
    {
      "field_id": "F00104",
      "sample_id": "sample_austenitic",
      "section": "processing_steps",
      "path": "processing_steps.sample_austenitic.temperature_with_unit",
      "value": "1100 °C",
      "field_weight": 1.3,
      "candidate_evidence_refs": []
    }
  ],
  "evidence_blocks": []
}
```

注意：当前每个输入里的 `evidence_blocks` 是完整 evidence blocks。

### 4.6 每次 Verify Eval LLM 输出

LLM 只输出字段判断，不输出总分。

```json
{
  "paper_id": "A1",
  "sample_id": "paper_level",
  "results": [
    {
      "field_id": "F00005",
      "is_correct": "yes",
      "evidence_confidence": 1.0,
      "evidence_refs": ["b0013"],
      "reason": "关键词列表中明确包含 Low density steels。"
    }
  ]
}
```

允许的 `is_correct`：

```text
yes
partial
unknown
no
```

字段含义：

```text
yes:
  字段值被证据明确支持。

partial:
  字段大体正确，但有细节缺失、范围不完整或表达略有偏差。

unknown:
  给定证据不足以判断。

no:
  字段值与证据冲突，或明显归属错误。
```

---

## 5. Verify Eval 评分公式

LLM 不输出 sample_score 或 paper_score。

分数全部由代码计算。

### 5.1 correctness 映射

```text
yes     = 1.0
partial = 0.6
unknown = 0.3
no      = 0.0
```

### 5.2 字段分数

```text
field_score = correctness_score * evidence_confidence * 100
```

例子：

```text
is_correct = partial
evidence_confidence = 0.8

field_score = 0.6 * 0.8 * 100 = 48
```

### 5.3 字段权重

当前权重：

```text
structures / properties / performance:
  1.5

samples / processing_steps / interfaces:
  1.3

papers / unmapped_findings:
  0.7

其他字段:
  1.0
```

权重设计意图：

```text
材料结构化抽取中 sample 下游事实更重要。
paper metadata 和 unmapped_findings 影响较小。
```

### 5.4 Sample 分数

```text
sample_score =
  sum(field_score * field_weight) / sum(field_weight)
```

`paper_level` 也按同样方式计算一个 score。

### 5.5 Paper 分数

```text
paper_score =
  sum(sample_score * sample_weight) / sum(sample_weight)
```

其中：

```text
sample_weight = 当前 sample 或 paper_level 下所有 field_weight 之和
```

### 5.6 Structure Gate

评估前会先做结构 gate。

如果 gate 失败：

```text
paper_score = 0
```

Gate 检查内容包括：

```text
顶层 section 是否存在
section 是否为 list
sample_id 是否唯一
alloy_id/process_id/sample_id 引用是否断裂
下游 sample_id 是否指向已存在 sample
```

---

## 6. Skip 与 Force 机制

### 6.1 Verify skip

如果以下两个文件都存在，且没有传 `--force`，则跳过该 paper：

```text
outputs_dataset/<paper_id>/verify/text_extraction_fixed.json
outputs_dataset/<paper_id>/verify/verify_report.json
```

强制重跑：

```bash
python3 run_verify.py --paper-ids A1 --force
```

### 6.2 Verify Eval skip

如果以下文件存在，且没有传 `--force`，则跳过该 paper：

```text
outputs_dataset/<paper_id>/verify_eval/quality_report.json
```

强制重跑：

```bash
python3 run_verify_eval.py --paper-ids A1 --force
```

---

## 7. 运行命令

进入项目根目录：

```bash
cd /Users/mac/Desktop/SteelDig/SteelDig_multimodal
```

运行单篇 verify：

```bash
python3 run_verify.py --paper-ids A1 --workers 1
```

运行单篇 verify_eval：

```bash
python3 run_verify_eval.py --paper-ids A1 --workers 1
```

运行单篇 verify 前后对比：

```bash
python3 run_verify_eval.py --paper-ids A1 --compare-verify --workers 1
```

强制重跑：

```bash
python3 run_verify.py --paper-ids A1 --force --workers 1
python3 run_verify_eval.py --paper-ids A1 --force --workers 1
```

运行多篇：

```bash
python3 run_verify.py --paper-ids A0,A1,A2,A3,A4 --workers 2
python3 run_verify_eval.py --paper-ids A0,A1,A2,A3,A4 --workers 2
```

只做离线结构检查，不调用 LLM：

```bash
python3 run_verify.py --paper-ids A1 --no-llm --force
python3 run_verify_eval.py --paper-ids A1 --no-llm --force
```

---

## 8. 回溯检查方式

### 8.1 查看 paper 总分

```text
outputs_dataset/<paper_id>/verify_eval/quality_report.json
```

关键字段：

```json
{
  "paper_score": 83.32757078986587,
  "score_formula": {},
  "sample_reports": []
}
```

### 8.2 查看 sample 分数

在 `quality_report.json` 中：

```json
{
  "sample_id": "sample_austenitic",
  "sample_score": 81.64,
  "field_count": 51
}
```

### 8.3 查看字段分数

在 sample 的 `fields` 中：

```json
{
  "field_id": "F00005",
  "path": "papers.A1.keywords[0]",
  "value": "Low density steels",
  "is_correct": "yes",
  "evidence_confidence": 1.0,
  "evidence_refs": ["b0013"],
  "reason": "关键词列表中明确包含 Low density steels。",
  "field_score": 100.0
}
```

### 8.4 查看证据文本

打开：

```text
outputs_dataset/<paper_id>/verify_eval/evidence_blocks.json
```

根据 `evidence_refs` 查找对应 `block_id`。

### 8.5 查看 LLM 输入输出

输入：

```text
outputs_dataset/<paper_id>/verify_eval/sample_inputs/<sample_id>.json
```

原始输出：

```text
outputs_dataset/<paper_id>/verify_eval/sample_raw_outputs/<sample_id>.json
```

解析后输出：

```text
outputs_dataset/<paper_id>/verify_eval/sample_outputs/<sample_id>.json
```

---

## 9. 当前 A1 验证结果示例

使用完整 evidence blocks 重跑 A1 后：

```text
A1: score=83.33 fields=278 target=verify_fixed gate_ok=True
```

确认：

```text
outputs_dataset/A1/verify_eval/sample_inputs/paper_level.json
```

包含完整 evidence blocks：

```text
blocks = 567
```

并且 paper-level keywords 可正确回溯到对应 block：

```text
papers.A1.keywords[0]
value = Low density steels
evidence_refs = ["b0013"]
field_score = 100
```

---

## 10. 设计边界

`verify` 不做：

```text
不重新抽取整篇论文
不让 LLM 输出完整 fixed JSON
不无校验应用 LLM patch
不默认开启 append_record
不凭外部知识补事实
```

`verify_eval` 不做：

```text
不修改目标 JSON
不输出 LLM 自定义总分
不每个字段单独请求 LLM
不使用人工 truth JSON
不评估 prompt 中未列出的字段
```

这两个模块的目标不是复杂框架，而是一个可运行、可回溯、能真实发现问题的后处理闭环。
