# `paper_extractor/knowledge/` 模块说明

这个目录负责把论文文本压缩为更适合训练或知识消费的中间事实与 Markdown 卡片。

它不是主抽取工作流的重复实现，而是一个更强调“证据、归纳、压缩”的第二阶段工作流。

---

## 1. 整体目标

Knowledge 工作流的目标是生成两类产物：

1. `text_claims.jsonl`
   面向程序与训练数据构建的细粒度事实记录
2. `text_knowledge.md`
   面向知识整理与语言模型训练的高密度 Markdown 卡片

相比主抽取：

- 主抽取偏“保留细节”
- knowledge 偏“总结与压缩”

---

## 2. 文件结构

```text
knowledge/
├── __init__.py
├── chunker.py
├── extractor.py
├── markdown_writer.py
├── normalizer.py
├── prompts.py
├── synthesis_payload.py
└── workflow.py
```

### `workflow.py`

总入口，编排整个 knowledge 链。

### `chunker.py`

把长 Markdown 按 section + paragraph 切成块，同时保留字符偏移。

### `extractor.py`

调用模型完成：

- `paper_map` 生成
- chunk claim 抽取
- markdown synthesis

### `prompts.py`

知识工作流各阶段 prompt 构造器。

### `normalizer.py`

对 raw claims 做：

- 去重
- evidence 对齐
- 置信度修正
- warning 生成

### `synthesis_payload.py`

把高价值 claims 压缩成面向 Markdown 合成的 `core_facts` 结构。

### `markdown_writer.py`

把最终产物落盘：

- `text_knowledge.md`
- `text_claims.jsonl`
- `text_knowledge.meta.json`

---

## 3. 工作流分阶段说明

### 3.1 读取输入

有两条路径：

1. 直接从原始 Markdown 跑
2. 从已有 `run_dir` 跑

如果传了 `--run-dir`，它会优先复用：

- `preprocess/cleaned_input.md`

这能确保与主工作流看到的是同一份清洗文本。

### 3.2 chunk 切分

`chunker.py` 做的不是简单固定字数切片，而是：

- 先按段落切
- 尽量保留 section 边界
- 控制最大字符数
- 默认保留少量 overlap 段落

每个 chunk 带有：

- `chunk_id`
- `paper_id`
- `section`
- `paragraph_start/end`
- `char_start/end`
- `token_estimate`
- `text`

这为后续 evidence 对齐提供了基础。

### 3.3 生成 `paper_map`

`paper_map` 是全文级导航信息。

它不是最终事实库，而是给 chunk claim 阶段提供论文主线、术语和样品别名背景。

典型字段：

- `paper_id`
- `title`
- `abstract_summary`
- `research_objective`
- `material_systems`
- `main_process_variables`
- `sample_aliases`
- `expected_information_axis`
- `key_sections`

### 3.4 抽取 chunk claims

对每个 chunk 调一次模型，要求输出：

```json
{"claims":[...]}
```

每条 claim 典型包含：

- `claim_type`
- `subject`
- `claim`
- `values`
- `evidence_text`
- `figures`
- `tables`
- `confidence`

注意：

- `claim` 可以是归纳后的事实表述
- `evidence_text` 必须尽量是 chunk 中连续出现的原文证据

### 3.5 归一化与验证

`normalizer.py` 是 knowledge 质量控制的关键一环。

它做了这些事情：

- 用 fingerprint 去重
- 重新检查 `evidence_text` 是否真的存在于原 chunk 中
- 找到证据在 chunk 中的字符偏移
- 如果 evidence 不存在或不可靠，则：
  - `validation_status` 改为异常状态
  - `confidence` 降为 `low`
  - 写入 `validation_warnings.json`

### 3.6 构建 synthesis payload

所有 normalized claims 不会原样送给 Markdown 合成，而是先压缩成高价值 `core_facts`。

bucket 包括：

- `material_system`
- `processing`
- `structure`
- `properties`
- `mechanisms`
- `characterization`

压缩时会：

- 去重
- 去噪
- 限制每个 bucket 最多保留多少条
- 对更有直接证据、置信度更高、带图表引用的事实给更高分

### 3.7 融合 visual evidence

当 `mode=fused` 时，workflow 会尝试读取：

- `final/multimodal_figures.json`

然后把图像证据压缩到 synthesis payload 中，最终提供给 Markdown 生成阶段。

这意味着 `fused` 模式适用于：

- 图片中承载了对组织、断口、相结构、表征结果的重要补充说明

### 3.8 生成最终 Markdown

最后一步会用：

- `paper_map`
- `compressed_core_facts`
- `visual_evidence`

生成英文 Markdown 知识卡片，强调材料系统、工艺-组织-性能链与机理解释。

---

## 4. 输出文件解读

### `intermediate/knowledge/chunks.jsonl`

用于回看分块质量。

### `intermediate/knowledge/paper_map.json`

用于检查“论文全局理解”是否偏掉。

### `intermediate/knowledge/claims_raw.jsonl`

用于看 chunk 级模型抽取的原始结果。

### `intermediate/knowledge/claims_normalized.jsonl`

用于看最终保留下来的规范 claim。

### `intermediate/knowledge/validation_warnings.json`

如果 claim 证据对齐失败、置信度被降级，通常会在这里体现。

### `final/text_claims.jsonl`

这是最适合做后续程序消费的知识结果。

### `final/text_knowledge.md`

这是最适合人工浏览和训练语料整理的最终摘要。

---

## 5. 如何调质量

如果最终 Markdown 不够好，通常不要直接先改 `markdown_writer.py`，而应该先定位上游问题。

建议排查顺序：

1. `paper_map.json` 是否偏题
2. `claims_raw.jsonl` 是否抽到了正确事实
3. `claims_normalized.jsonl` 是否过度丢失
4. `synthesis_payload.json` 是否压缩得太狠
5. `visual_evidence` 是否有效进入 fused 模式
6. 最后才看 `build_markdown_prompt`

最常见的改动点：

- 调 `prompts.py`
- 调 `synthesis_payload.py`
- 调 `normalizer.py`

---

## 6. 什么时候用 `mock_model`

`mock_model` 适合：

- 不想真的调用远程/本地模型
- 只想验证 workflow、目录写出、文件结构和下游逻辑

它不适合：

- 判断真实抽取质量
- 做 prompt 对比

因为 mock 输出是确定性假数据，只用于 smoke test。
