# SteelDig Multimodal

一个面向材料科学论文的本地抽取流水线项目。

项目当前包含两条核心能力链：

1. 主抽取工作流
   从论文 Markdown 中抽取结构化文本信息，并可对图片组图做多模态分析。
2. Knowledge 工作流
   把清洗后的论文文本进一步压缩为适合训练或知识整理的 claim 集与 Markdown 知识卡片。

这两条链既可以独立运行，也可以按单篇论文串行衔接运行。项目已经支持：

- 多篇论文并行处理
- 单篇论文内部严格按阶段顺序执行
- 以 `paper_id` 为目录隔离输出
- `fused` 模式下把多模态图像结论注入 knowledge 汇总

---

## 1. 项目目标

这个仓库的目标不是“把论文原样摘要一下”，而是把材料科学论文中的高价值事实拆成两类产物：

- 面向结构化数据库/后续程序消费的 JSON
- 面向知识训练/知识整理的 Markdown 与 claims

具体来说：

- 主抽取工作流负责“尽可能保留原始细节”
  - 文本模型输出大 JSON
  - 图像模型输出 Figure 级别 JSON
- Knowledge 工作流负责“把细节压缩成更高信息密度的训练材料”
  - paper_map
  - chunk-level claims
  - normalized claims
  - synthesis payload
  - text_knowledge.md

---

## 2. 适用输入

项目当前默认输入是论文转换后的 Markdown 文件，优先使用类似下面的目录形式：

```text
dataset/
  10.1002_srin.202200207/
    hybrid_auto/
      10.1002_srin.202200207.md
      images/
        xxx.jpg
        yyy.jpg
```

如果同目录中存在 `*_content_list.json`，预处理会利用它做更精细的噪声清除；如果不存在，则退化为纯 Markdown 规则清洗。

---

## 3. 项目结构总览

```text
.
├── config/
│   └── workflow.json
├── dataset/
│   └── <paper_id>/hybrid_auto/
├── prompt/
│   ├── json_schema.json
│   ├── text_extractor_prompt.md
│   └── image_type_prompt.md
├── paper_extractor/
│   ├── client.py
│   ├── common.py
│   ├── config.py
│   ├── postprocess.py
│   ├── workflow.py
│   ├── preprocess/
│   │   ├── __init__.py
│   │   ├── content_list.py
│   │   ├── image_groups.py
│   │   ├── markdown_cleaner.py
│   │   ├── models.py
│   │   └── pipeline.py
│   └── knowledge/
│       ├── __init__.py
│       ├── chunker.py
│       ├── extractor.py
│       ├── markdown_writer.py
│       ├── normalizer.py
│       ├── prompts.py
│       ├── synthesis_payload.py
│       └── workflow.py
├── docs/
│   └── quickstart.md
├── run_knowledge_workflow.py
├── run_paper_then_knowledge_workflow.py
├── run_paper_workflow.py
├── requirements.txt
└── pyproject.toml
```

建议同时阅读以下文档：

- [docs/quickstart.md](/Users/mac/Desktop/LLM_project/SteelDig_multimodal/docs/quickstart.md)
- [paper_extractor/README.md](/Users/mac/Desktop/LLM_project/SteelDig_multimodal/paper_extractor/README.md)
- [paper_extractor/preprocess/README.md](/Users/mac/Desktop/LLM_project/SteelDig_multimodal/paper_extractor/preprocess/README.md)
- [paper_extractor/knowledge/README.md](/Users/mac/Desktop/LLM_project/SteelDig_multimodal/paper_extractor/knowledge/README.md)

---

## 4. 安装与环境准备

### 4.1 Python 版本

建议使用 Python 3.11 及以上。

### 4.2 安装依赖

```bash
pip install -r requirements.txt
```

当前 `requirements.txt` 很少，只列了：

- `openai`
- `httpx`

其中：

- `openai` 用于访问 OpenAI-compatible 接口
- `httpx` 被 [paper_extractor/client.py](/Users/mac/Desktop/LLM_project/SteelDig_multimodal/paper_extractor/client.py:1) 显式依赖

如果你没有安装 `httpx`，运行入口时会直接在 import 阶段失败。

### 4.3 本地模型服务

项目默认假设你已经有一个 OpenAI 兼容接口，例如：

- vLLM
- 本地 OpenAI-compatible 服务
- 其他兼容 `/v1/chat/completions` 的服务

默认配置写在 [config/workflow.json](/Users/mac/Desktop/LLM_project/SteelDig_multimodal/config/workflow.json)。

典型默认值类似：

```json
{
  "text_model": {
    "model": "Qwen/Qwen3.5-9B",
    "base_url": "http://127.0.0.1:8000/v1",
    "api_key": "EMPTY"
  },
  "multimodal_model": {
    "model": "Qwen/Qwen3.5-9B",
    "base_url": "http://127.0.0.1:8000/v1",
    "api_key": "EMPTY"
  }
}
```

说明：

- 文本与多模态可以使用同一个模型服务
- 如果本地服务不要求真实 API key，保留 `"EMPTY"` 即可
- `client.py` 会强制 `trust_env=False`，避免本地 `127.0.0.1` 请求被系统代理转发

---

## 5. 最重要的运行方式

这一节只讲“怎么启动”。

### 5.1 方式 A：运行主抽取工作流

适用于你只想做：

- 文本结构化抽取
- 可选图片多模态抽取
- post-parse 生成 `final/*.json`

命令：

```bash
python3 run_paper_workflow.py --config config/workflow.json
```

常用示例：

```bash
python3 run_paper_workflow.py \
  --config config/workflow.json \
  --workers 4 \
  --input dataset \
  --recursive
```

如果已经跑过一部分论文，想自动跳过已完成抽取结果：

```bash
python3 run_paper_workflow.py \
  --config config/workflow.json \
  --workers 4 \
  --input dataset \
  --recursive \
  --skip-existing
```

如果只跑文本，不跑图片：

```bash
python3 run_paper_workflow.py \
  --config config/workflow.json \
  --skip-multimodal
```

如果只想保留模型原始输出，不立即做 txt -> json 后处理：

```bash
python3 run_paper_workflow.py \
  --config config/workflow.json \
  --skip-post-parse
```

### 5.2 方式 B：运行 knowledge 工作流

适用于你只想产出：

- `text_claims.jsonl`
- `text_knowledge.md`

命令：

```bash
python3 run_knowledge_workflow.py --config config/workflow.json
```

只做纯文本 knowledge：

```bash
python3 run_knowledge_workflow.py \
  --config config/workflow.json \
  --mode text
```

如果想复用已经跑过的一篇论文结果目录：

```bash
python3 run_knowledge_workflow.py \
  --config config/workflow.json \
  --run-dir workflow_runs/10.1002_srin.202200207 \
  --mode fused
```

### 5.3 方式 C：推荐方式，按论文串行执行主抽取 -> knowledge

这是当前最完整、最适合正式批量跑的入口。

它的语义是：

- 不同论文之间可并行
- 同一篇论文内部严格按顺序执行：
  1. extraction
  2. post-parse
  3. knowledge

命令：

```bash
python3 run_paper_then_knowledge_workflow.py \
  --config config/workflow.json \
  --workers 4 \
  --resume-mode resume_partial \
  --knowledge-mode fused
```

这是后续大规模处理时最推荐的方式，因为：

- 每篇论文完成主抽取后，立刻进入自己的 post-parse
- post-parse 结束后，立刻进入自己的 knowledge
- `fused` 模式依赖的 `final/multimodal_figures.json` 一定来自同一篇论文
- 不会出现多篇论文结果交叉读取
- 中途中断后可以按阶段自动续跑

推荐批量任务默认使用：

```bash
python3 run_paper_then_knowledge_workflow.py \
  --config config/workflow.json \
  --input dataset \
  --recursive \
  --workers 4 \
  --knowledge-mode fused \
  --resume-mode resume_partial
```

`resume_mode` 说明：

- `none`
  整篇论文完整重跑
- `skip_completed`
  只跳过已经完整完成的论文
- `resume_partial`
  推荐模式。自动检查该论文缺失的阶段，只补跑缺失部分

---

## 6. 配置文件说明

配置定义在 [paper_extractor/config.py](/Users/mac/Desktop/LLM_project/SteelDig_multimodal/paper_extractor/config.py:1)，JSON 配置文件通常是 [config/workflow.json](/Users/mac/Desktop/LLM_project/SteelDig_multimodal/config/workflow.json)。

### 6.1 `WorkflowSettings`

字段说明：

- `input_path`
  输入路径，可以是单个 `.md` 文件，也可以是目录
- `output_root`
  输出根目录，默认 `workflow_runs`
- `recursive`
  是否递归查找 Markdown
- `workers`
  并行处理论文的 worker 数量
- `limit_papers`
  限制处理论文数，`0` 表示不限制
- `skip_existing`
  主抽取工作流可用。跳过已经具备最终抽取结果的论文
- `skip_post_parse`
  是否跳过后处理
- `skip_multimodal`
  是否跳过多模态图片分析
- `text_model`
  文本模型配置
- `multimodal_model`
  多模态模型配置

### 6.2 `LocalModelConfig`

- `model`
- `base_url`
- `api_key`

### 6.3 命令行参数与配置文件的关系

入口脚本会先加载 `config/workflow.json`，然后允许命令行覆盖局部字段。

例如：

```bash
python3 run_paper_workflow.py \
  --config config/workflow.json \
  --workers 8 \
  --skip-multimodal
```

此时：

- 未显式传入的字段仍来自 JSON
- `workers` 和 `skip_multimodal` 以命令行为准

---

## 7. 输出目录说明

项目输出按照 `paper_id` 做目录隔离。

例如：

```text
workflow_runs/
  10.1002_srin.202200207/
    preprocess/
    intermediate/
    final/
    logs/
```

### 7.1 `preprocess/`

- `cleaned_input.md`
  清洗后的 Markdown，是后续文本抽取和 knowledge 的直接输入
- `references.json`
  被分离出来的参考文献条目
- `image_groups.json`
  从 Markdown 中识别出的 Figure 分组结果
- `summary.json`
  预处理摘要

### 7.2 `intermediate/text/`

- `text_extraction.txt`
  文本模型原始输出，可能包含思维链/说明文字/不规范 JSON

### 7.3 `intermediate/multimodal/`

- `image_groups.json`
  主工作流内部使用的清洗后组图列表
- `figure_001.txt`, `figure_002.txt`, ...
  每个 Figure 请求的原始模型输出

### 7.4 `intermediate/knowledge/`

- `chunks.jsonl`
  分块后的 chunk 全量内容
- `chunks_index.json`
  chunk 元信息索引
- `paper_map.json`
  全局论文导航信息
- `paper_map.raw.txt`
  `paper_map` 的原始模型输出
- `claims_raw.jsonl`
  chunk 级原始 claim 结果
- `chunk_0001.raw.txt` 等
  每个 chunk 的原始模型输出
- `claims_normalized.jsonl`
  归一化后的 claims
- `validation_warnings.json`
  证据匹配失败或置信度下调的警告
- `synthesis_payload.json`
  送入 markdown 合成阶段的压缩事实载荷
- `synthesis_prompt.txt`
  最终 knowledge markdown 的提示词快照

### 7.5 `final/`

主抽取产物：

- `text_extraction.json`
- `figure_001.json`, `figure_002.json`, ...
- `multimodal_figures.json`

knowledge 产物：

- `text_knowledge.md`
- `text_claims.jsonl`
- `text_knowledge.meta.json`

### 7.6 `logs/`

- `text.log.jsonl`
- `multimodal.log.jsonl`
- `post_parse.log.jsonl`
- `knowledge.log.jsonl`

这些日志是排查模型输入输出、失败请求和解析问题的第一现场。

---

## 8. 主抽取工作流详解

主抽取工作流的入口逻辑主要在：

- [run_paper_workflow.py](/Users/mac/Desktop/LLM_project/SteelDig_multimodal/run_paper_workflow.py:1)
- [paper_extractor/workflow.py](/Users/mac/Desktop/LLM_project/SteelDig_multimodal/paper_extractor/workflow.py:1)

### 8.1 流程概述

单篇论文的处理顺序是：

1. 预处理 Markdown
2. 用文本模型抽取论文结构化 JSON
3. 按 Figure 组图做多模态抽取
4. 把模型原始输出交给 post-parse
5. 产出 `final/*.json`

### 8.2 预处理做了什么

预处理来自 [paper_extractor/preprocess/pipeline.py](/Users/mac/Desktop/LLM_project/SteelDig_multimodal/paper_extractor/preprocess/pipeline.py:1)。

它会：

- 读取原始 Markdown
- 尝试加载 `*_content_list.json`
- 去掉参考文献、版权、页眉页脚、关键词等噪声
- 保留正文和 figure/caption 信息
- 提取参考文献信息
- 解析图片分组

### 8.3 文本抽取

文本抽取使用：

- `prompt/text_extractor_prompt.md`
- `prompt/json_schema.json`

在 [paper_extractor/workflow.py](/Users/mac/Desktop/LLM_project/SteelDig_multimodal/paper_extractor/workflow.py:31) 中，它会把：

- 基础提示词
- JSON schema
- `paper_id`
- 清洗后的 Markdown 正文

组合成一个完整 prompt，发给文本模型。

模型原始输出先保存到：

- `intermediate/text/text_extraction.txt`

### 8.4 多模态抽取

多模态抽取不是“按单张图片”，而是“按 Figure 组图”。

这点非常重要。

项目会把同一 Figure 下所有子图打包成一个请求，然后要求模型输出一个 Figure 级 JSON：

- `image_type`
- `description`
- `confidence`

后处理再补齐：

- `paper_id`
- `figure_id`
- `image_paths`
- `image_count`

组图抽取提示词来自：

- [prompt/image_type_prompt.md](/Users/mac/Desktop/LLM_project/SteelDig_multimodal/prompt/image_type_prompt.md)

### 8.5 post-parse 的职责

模型输出并不总是规范 JSON，所以 post-parse 要做：

- 规则提取 JSON
- 清除 `<think>...</think>`
- 处理 Markdown 代码块
- 从多段杂乱输出里挑选最像目标结构的 JSON
- 必要时调用 fallback agent 再修复一次

实现见：

- [paper_extractor/postprocess.py](/Users/mac/Desktop/LLM_project/SteelDig_multimodal/paper_extractor/postprocess.py:1)

---

## 9. Knowledge 工作流详解

Knowledge 工作流入口：

- [run_knowledge_workflow.py](/Users/mac/Desktop/LLM_project/SteelDig_multimodal/run_knowledge_workflow.py:1)
- [paper_extractor/knowledge/workflow.py](/Users/mac/Desktop/LLM_project/SteelDig_multimodal/paper_extractor/knowledge/workflow.py:1)

### 9.1 两种模式

- `mode=text`
  只基于文本内容
- `mode=fused`
  除文本外，还读取同一篇论文 `final/multimodal_figures.json` 作为 visual evidence

### 9.2 内部流程

1. 获取 `cleaned_input.md`
2. 按 section + paragraph 分块
3. 先生成全局 `paper_map`
4. 对每个 chunk 抽取 claims
5. 做 claim 归一化和证据校验
6. 压缩出 synthesis payload
7. 生成面向训练的 Markdown 知识卡片

### 9.3 `paper_map` 是什么

`paper_map` 是全文导航信息，不是最终知识输出。

它通常包含：

- title
- abstract_summary
- research_objective
- material_systems
- main_process_variables
- sample_aliases
- expected_information_axis
- key_sections

它的作用是帮助后续 chunk claim 抽取理解论文主线和术语。

### 9.4 claims 是什么

每个 chunk 会抽取一批局部事实，典型字段有：

- `claim_type`
- `subject`
- `claim`
- `values`
- `evidence_text`
- `figures`
- `tables`
- `confidence`

随后 `normalizer.py` 会：

- 去重
- 找回 `evidence_text` 在 chunk 中的位置
- 校验证据是否真的存在于原 chunk
- 对低可信 claim 降级为 `low`
- 输出 warnings

### 9.5 synthesis payload 是什么

`synthesis_payload.py` 会从所有 normalized claims 中选出高价值内容，按主题压缩到几个 bucket：

- `material_system`
- `processing`
- `structure`
- `properties`
- `mechanisms`
- `characterization`

这个阶段是在做“训练数据压缩”，不是简单原样拼接。

### 9.6 knowledge markdown 输出长什么样

最终 `text_knowledge.md` 目标是英文 Markdown，偏“知识卡片”风格，强调：

- Material System
- Processing-Structure-Property Chain
- Mechanistic Interpretation
- Key Quantitative Findings
- Optional Visual Evidence

---

## 10. 三个入口的区别

### `run_paper_workflow.py`

只跑主抽取链：

- preprocess
- text extraction
- multimodal extraction
- post-parse

### `run_knowledge_workflow.py`

只跑 knowledge 链：

- chunk
- paper_map
- chunk claims
- normalize
- synthesize markdown

### `run_paper_then_knowledge_workflow.py`

推荐正式使用：

- 对每篇论文先跑主抽取
- 再跑 post-parse
- 再跑 knowledge
- 多篇论文之间可以并行

---

## 11. 并行与隔离策略

这是当前项目一个很重要的设计点。

### 11.1 并行粒度

并行是在“论文级”进行的，而不是 chunk 级，也不是 figure 级。

也就是说：

- 不同 `paper_id` 之间可以并行
- 同一篇论文内部仍然严格顺序执行

### 11.2 为什么这样设计

因为 `fused` 模式要求：

- 主抽取先生成 `final/multimodal_figures.json`
- knowledge 才能消费这一份图像证据

如果把单篇论文内部也做乱序并发，依赖关系会变得不稳定。

### 11.3 是否会发生“不同论文混乱”

按当前实现，只要输入文件名唯一，就不会。

原因：

- 输出根目录始终是 `output_root / paper_id`
- `paper_id = md_path.stem`
- 每篇论文的 `preprocess/`、`intermediate/`、`final/`、`logs/` 全部在自己的目录下

唯一需要注意的是：

- 如果两篇不同论文的 Markdown 文件名相同，例如都叫 `paper.md`
- 它们的 `paper_id` 都会变成 `paper`
- 就会写进同一个输出目录

现在项目已经在运行前增加了显式检查：

- 如果检测到重复 `paper_id`
- 运行会直接报错并列出冲突文件路径

所以批量跑时，建议保证：

- 每个输入 Markdown 文件名唯一
- 最好直接使用 DOI 或论文唯一标识作为文件名

---

## 12. 常用运行命令清单

### 批量跑主抽取

```bash
python3 run_paper_workflow.py \
  --config config/workflow.json \
  --input dataset \
  --recursive \
  --workers 4
```

### 批量跑“主抽取 + fused knowledge”

```bash
python3 run_paper_then_knowledge_workflow.py \
  --config config/workflow.json \
  --input dataset \
  --recursive \
  --workers 4 \
  --knowledge-mode fused
```

### 跑单篇论文主抽取

```bash
python3 run_paper_workflow.py \
  --config config/workflow.json \
  --input dataset/10.1002_srin.202200207/hybrid_auto/10.1002_srin.202200207.md
```

### 对已有结果目录补跑 knowledge fused

```bash
python3 run_knowledge_workflow.py \
  --config config/workflow.json \
  --run-dir workflow_runs/10.1002_srin.202200207 \
  --mode fused
```

### 离线 smoke test knowledge

```bash
python3 run_knowledge_workflow.py \
  --config config/workflow.json \
  --run-dir workflow_runs/10.1002_srin.202200207 \
  --mode text \
  --mock-model
```

---

## 13. 调试建议

如果你想快速定位问题，建议按下面顺序看文件：

1. `logs/*.jsonl`
2. `intermediate/*.txt`
3. `final/*.json`
4. `intermediate/knowledge/*.raw.txt`
5. `intermediate/knowledge/validation_warnings.json`

常见定位方式：

- 文本抽取不对
  看 `intermediate/text/text_extraction.txt`
- figure 结果不对
  看 `intermediate/multimodal/figure_XXX.txt`
- post-parse 失败
  看 `logs/post_parse.log.jsonl`
- claim 太少/太怪
  看 `intermediate/knowledge/claims_raw.jsonl`
- knowledge 总结偏差大
  看 `paper_map.json` 和 `synthesis_payload.json`

---

## 14. 常见问题

### Q1：为什么 `fused` 模式要求先有 post-parse？

因为 knowledge 读取的是：

- `final/multimodal_figures.json`

而这个文件不是多模态模型直接生成的，是 post-parse 归一化之后得到的。

### Q2：为什么多模态按 Figure 而不是按单图？

因为材料科学论文中很多关键信息依赖组图内部的对照关系，例如：

- 冷却方式对比
- SEM 与 TEM 联合说明
- 相图 + 性能曲线 + 显微组织联动

单图拆开后会丢失语义上下文。

### Q3：为什么 knowledge 还要再跑一遍模型，不能直接复用主抽取 JSON？

因为 knowledge 的目标与主抽取不同：

- 主抽取偏“全面保留”
- knowledge 偏“高价值压缩”

它需要：

- 重新分块
- 做 claim 级证据对齐
- 重新组织 Material-Processing-Structure-Property 链

### Q4：主工作流和 knowledge 工作流是否互相硬依赖？

不是硬依赖。

- 主工作流可以单独跑
- knowledge 工作流也可以从原始 Markdown 单独跑
- 只有当 `mode=fused` 或者你传 `--run-dir` 复用已有结果时，knowledge 才会依赖主工作流产物

---

## 15. 建议阅读顺序

如果你是第一次接手这个项目，建议按这个顺序读代码：

1. [run_paper_then_knowledge_workflow.py](/Users/mac/Desktop/LLM_project/SteelDig_multimodal/run_paper_then_knowledge_workflow.py:1)
2. [paper_extractor/workflow.py](/Users/mac/Desktop/LLM_project/SteelDig_multimodal/paper_extractor/workflow.py:1)
3. [paper_extractor/postprocess.py](/Users/mac/Desktop/LLM_project/SteelDig_multimodal/paper_extractor/postprocess.py:1)
4. [paper_extractor/knowledge/workflow.py](/Users/mac/Desktop/LLM_project/SteelDig_multimodal/paper_extractor/knowledge/workflow.py:1)
5. [paper_extractor/preprocess/pipeline.py](/Users/mac/Desktop/LLM_project/SteelDig_multimodal/paper_extractor/preprocess/pipeline.py:1)
6. [paper_extractor/knowledge/extractor.py](/Users/mac/Desktop/LLM_project/SteelDig_multimodal/paper_extractor/knowledge/extractor.py:1)
7. [paper_extractor/knowledge/synthesis_payload.py](/Users/mac/Desktop/LLM_project/SteelDig_multimodal/paper_extractor/knowledge/synthesis_payload.py:1)

---

## 16. 额外补充的两个实用改进

这次整理额外补了两样更实用的内容：

1. 重复 `paper_id` 检查
   现在主工作流、knowledge 工作流、串联工作流在批量扫描 Markdown 后，都会先检查文件名是否重复。
   如果两个文件会映射到同一个 `paper_id`，程序会直接报错并列出路径，避免结果目录被覆盖或串写。

2. 快速上手文档
   新增 [docs/quickstart.md](/Users/mac/Desktop/LLM_project/SteelDig_multimodal/docs/quickstart.md)，只保留最短安装、启动、输出查看和常见报错说明，适合第一次上手或给同事转交。

3. 断点续跑 / 跳过已完成论文
   推荐入口 `run_paper_then_knowledge_workflow.py` 现在支持根据输出文件判断每篇论文已经完成到哪个阶段，并自动跳过或续跑缺失阶段。
   主抽取入口 `run_paper_workflow.py` 也支持 `--skip-existing`，用于批量补跑剩余论文。

如果你准备继续扩展这个项目，下一批值得优先做的事情通常是：

1. 给主工作流和 knowledge 工作流补单元测试与 smoke test。
2. 把 `paper_map` / claim schema 进一步稳定下来，减少 prompt 漂移。
3. 如果数据规模继续增大，考虑增加失败重试和更细粒度的任务状态索引。

---

## 17. 额外说明

本 README 重点是帮助你快速掌握“项目整体和运行方式”。如果你要理解更深一层的代码细节，请继续看：

- [docs/quickstart.md](/Users/mac/Desktop/LLM_project/SteelDig_multimodal/docs/quickstart.md)
- [paper_extractor/README.md](/Users/mac/Desktop/LLM_project/SteelDig_multimodal/paper_extractor/README.md)
- [paper_extractor/preprocess/README.md](/Users/mac/Desktop/LLM_project/SteelDig_multimodal/paper_extractor/preprocess/README.md)
- [paper_extractor/knowledge/README.md](/Users/mac/Desktop/LLM_project/SteelDig_multimodal/paper_extractor/knowledge/README.md)
