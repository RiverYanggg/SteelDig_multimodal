# SteelDig Multimodal

SteelDig Multimodal 是一个面向材料科学论文的本地多阶段抽取项目。它以 MinerU 等工具解析出的论文 Markdown 为输入，完成论文清洗、结构化 JSON 抽取、图像组图理解、单位统一、证据校验、无真值质量评估、知识 Markdown 生成，以及 Neo4j 知识图谱构建。

本项目的核心目标不是简单摘要论文，而是把材料论文中的材料体系、成分、工艺、样品、组织、相、界面、性能、表征和机理等事实，整理成可审计、可复跑、可评估、可进入数据库或图谱的结构化产物。

## 目录

- [1. 项目能做什么](#1-项目能做什么)
- [2. 推荐处理流程](#2-推荐处理流程)
- [3. 安装环境](#3-安装环境)
- [4. 准备输入文件](#4-准备输入文件)
- [5. 配置文件怎么准备](#5-配置文件怎么准备)
- [6. 最推荐的运行方式](#6-最推荐的运行方式)
- [7. 每个模块的功能](#7-每个模块的功能)
- [8. 输出目录和文件说明](#8-输出目录和文件说明)
- [9. 常用命令全集](#9-常用命令全集)
- [10. 单位统一应该什么时候运行](#10-单位统一应该什么时候运行)
- [11. Verify 和 Verify Eval 怎么用](#11-verify-和-verify-eval-怎么用)
- [12. Truth/Prediction 评估怎么用](#12-truthprediction-评估怎么用)
- [13. Neo4j 知识图谱怎么用](#13-neo4j-知识图谱怎么用)
- [14. 配置字段详解](#14-配置字段详解)
- [15. 调试和排错](#15-调试和排错)
- [16. 开发与测试](#16-开发与测试)
- [17. GitHub 提交建议](#17-github-提交建议)

## 1. 项目能做什么

对每篇论文，项目可以生成以下产物：

- `preprocess/cleaned_input.md`：清洗后的论文 Markdown，是后续抽取和 knowledge 阶段的统一文本输入。
- `preprocess/image_groups.json`：按 Figure 组织的图片组、caption 和正文引用句。
- `intermediate/text/text_extraction.txt`：文本模型原始输出，保留用于追溯。
- `intermediate/multimodal/figure_001.txt`：每个 Figure 组图的多模态模型原始输出。
- `final/text_extraction.json`：按照 `prompt/json_schema.json` 组织的结构化抽取结果。
- `final/multimodal_figures.json`：图像组图级别的结构化总结。
- `normalized/text_extraction_units.json`：单位统一后的完整结构化 JSON。
- `normalized/unit_normalization_report.json`：单位转换报告，记录 converted / unchanged / skipped / ambiguous。
- `verify/text_extraction_fixed.json`：经过证据校验和保守 patch 修复后的完整 JSON。
- `verify/verify_report.json`：verify 的修复报告。
- `verify_eval/quality_report.md`：无真值质量评估报告。
- `final/text_claims.jsonl`：knowledge workflow 生成的 claim 级事实。
- `final/text_knowledge.md`：面向阅读、训练或 RAG 的高密度知识 Markdown。
- Neo4j 图谱节点和关系，或 dry-run 导出的 graph payload。

## 2. 推荐处理流程

正式批处理时，推荐按下面的顺序理解整个项目：

```text
MinerU Markdown / images / content_list
        |
        v
preprocess
        |
        v
text extraction + multimodal extraction
        |
        v
postprocess
        |
        v
final/text_extraction.json
        |
        v
unit normalization
        |
        v
normalized/text_extraction_units.json
        |
        v
verify
        |
        v
verify/text_extraction_fixed.json
        |
        v
verify_eval / knowledge Markdown / Neo4j / benchmark evaluation
```

最推荐的完整运行入口是：

```bash
python3 steeldig.py pipeline -- \
  --config config/workflow.json \
  --input dataset \
  --output-root outputs_dataset \
  --recursive \
  --workers 4 \
  --resume-mode resume_partial \
  --knowledge-mode fused
```

这个入口会保证：

- 不同论文之间可以并行。
- 同一篇论文内部严格按阶段顺序运行。
- 中断后可以用 `resume_partial` 补跑缺失阶段。
- `fused` knowledge 一定读取同一篇论文自己的 `final/multimodal_figures.json`。

## 3. 安装环境

建议 Python 版本：

```text
Python >= 3.10
```

创建虚拟环境并安装依赖：

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

当前主要依赖：

- `openai`：调用 OpenAI-compatible chat completion 接口。
- `httpx`：底层 HTTP 客户端。
- `neo4j`：写入 Neo4j 图数据库。

本项目默认使用 OpenAI 兼容接口，只要服务支持 `/v1/chat/completions` 即可，例如：

- 本地 vLLM
- DeepSeek API
- Moonshot / Kimi API
- 其他 OpenAI-compatible 网关

## 4. 准备输入文件

### 4.1 推荐目录结构

最推荐使用 MinerU 解析后的目录结构：

```text
dataset/
└── <paper_id>/
    └── hybrid_auto/
        ├── <paper_id>.md
        ├── <paper_id>_content_list.json
        └── images/
            ├── image_001.jpg
            ├── image_002.jpg
            └── ...
```

其中：

- `<paper_id>.md` 是必须的。
- `<paper_id>_content_list.json` 是可选但强烈推荐的，预处理会用它更精确地删除 header、footer、copyright、references 等噪声。
- `images/` 是多模态抽取需要的图片目录。

### 4.2 paper_id 如何确定

项目用 Markdown 文件名去掉 `.md` 后缀作为 `paper_id`。

例如：

```text
dataset/10.1002_srin.202200207/hybrid_auto/10.1002_srin.202200207.md
```

对应：

```text
paper_id = 10.1002_srin.202200207
```

注意：同一次运行中，所有 Markdown 文件名的 stem 必须唯一。如果两个文件都叫 `paper.md`，它们都会写入 `outputs_dataset/paper/`，项目会在运行前报错并拒绝继续。

### 4.3 Markdown 中图片路径要求

图片路径最好相对 Markdown 所在目录，例如：

```markdown
![Figure 1](images/image_001.jpg)

Figure 1. SEM image of the alloy after annealing.
```

多模态阶段会根据 Markdown 图片链接找到实际图片文件。如果图片链接失效，会导致对应 Figure 请求失败。

### 4.4 可以只输入单个 Markdown 吗

可以。

```bash
python3 steeldig.py pipeline -- \
  --config config/workflow.json \
  --input dataset/A0/hybrid_auto/A0.md \
  --output-root outputs_dataset \
  --knowledge-mode text
```

如果没有图片或不想跑多模态，可以加：

```bash
--skip-multimodal
```

## 5. 配置文件怎么准备

项目约定：提交到 Git 的配置文件只放 `*.example.json`，真实运行配置由用户本地复制生成，并填入自己的路径、模型名和 key。

### 5.1 主工作流配置

复制：

```bash
cp config/workflow.example.json config/workflow.json
```

然后编辑：

```text
config/workflow.json
```

这个文件用于：

- `pipeline`
- `extract`
- `knowledge`

### 5.2 Verify 配置

复制：

```bash
cp config/verify_config.example.json config/verify_config.json
```

然后编辑：

```text
config/verify_config.json
```

这个文件用于：

- `verify`
- `verify-eval`

### 5.3 Truth/Prediction 评估配置

如果不启用 LLM bridge：

```bash
cp config/eval_config.example.json config/eval_config.json
```

如果要启用 LLM bridge：

```bash
cp config/eval_config_llm.example.json config/eval_config.json
```

然后编辑：

```text
config/eval_config.json
```

这个文件用于：

- `evaluate`

### 5.4 字段规则配置

复制：

```bash
cp config/field_rules.example.json config/field_rules.json
```

然后编辑：

```text
config/field_rules.json
```

`field_rules` 是字段匹配和评估规则，不是私钥配置，但为了保持 `config/` 目录统一，本仓库也只提交 example 文件。

它用于：

- truth/pred 字段匹配
- numeric tolerance
- ID 字段过滤
- sample/process 对齐辅助规则

如果你要针对新 schema 调整评估逻辑，可以直接修改它，或复制成自己的 rules 文件并在命令中传入。

### 5.5 一次性初始化全部本地配置

如果你第一次 clone 项目，可以直接执行：

```bash
cp config/workflow.example.json config/workflow.json
cp config/verify_config.example.json config/verify_config.json
cp config/eval_config.example.json config/eval_config.json
cp config/field_rules.example.json config/field_rules.json
```

如果评估时要启用 LLM bridge，则用下面这条替代第三条：

```bash
cp config/eval_config_llm.example.json config/eval_config.json
```

之后再编辑这些本地文件，填入自己的模型名、base_url、api_key 和路径。

### 5.6 为什么真实配置不提交

真实配置可能包含：

- API key
- 私有 base_url
- 本地绝对路径
- 实验输出目录

这些文件已在 `.gitignore` 中忽略：

```text
config/workflow.json
config/verify_config.json
config/eval_config.json
config/eval_config_llm.json
config/field_rules.json
config/*.local.json
```

## 6. 最推荐的运行方式

### 6.1 第一次跑通最小流程

准备配置：

```bash
cp config/workflow.example.json config/workflow.json
cp config/verify_config.example.json config/verify_config.json
cp config/eval_config.example.json config/eval_config.json
cp config/field_rules.example.json config/field_rules.json
```

编辑 `config/workflow.json`，至少确认：

- `input_path`
- `output_root`
- `text_model.model`
- `text_model.base_url`
- `text_model.api_key`
- `multimodal_model.model`
- `multimodal_model.base_url`
- `multimodal_model.api_key`

跑一篇或少量论文：

```bash
python3 steeldig.py pipeline -- \
  --config config/workflow.json \
  --input dataset \
  --output-root outputs_dataset \
  --recursive \
  --workers 1 \
  --limit-papers 1 \
  --resume-mode resume_partial \
  --knowledge-mode fused
```

如果没有图片模型或只想先验证文本链路：

```bash
python3 steeldig.py pipeline -- \
  --config config/workflow.json \
  --input dataset \
  --output-root outputs_dataset \
  --recursive \
  --workers 1 \
  --limit-papers 1 \
  --skip-multimodal \
  --knowledge-mode text
```

### 6.2 批量正式运行

```bash
python3 steeldig.py pipeline -- \
  --config config/workflow.json \
  --input dataset \
  --output-root outputs_dataset \
  --recursive \
  --workers 4 \
  --resume-mode resume_partial \
  --knowledge-mode fused
```

### 6.3 中断后继续

直接重跑同一条命令，并保留：

```bash
--resume-mode resume_partial
```

该模式会检查每篇论文是否已有：

- `intermediate/text/text_extraction.txt`
- `final/text_extraction.json`
- `normalized/text_extraction_units.json`
- `final/text_knowledge.md`
- `final/text_claims.jsonl`

然后只补跑缺失阶段。

## 7. 每个模块的功能

### 7.1 `paper_extractor.preprocess`

路径：

```text
paper_extractor/preprocess/
```

职责：

- 读取原始 Markdown。
- 尝试读取 MinerU 的 `*_content_list.json`。
- 删除参考文献、页眉页脚、版权、关键词等噪声。
- 提取 references。
- 解析 Figure 组图。
- 写出 `cleaned_input.md` 和 `image_groups.json`。

主要输出：

```text
preprocess/cleaned_input.md
preprocess/image_groups.json
preprocess/references.json
preprocess/summary.json
```

### 7.2 `paper_extractor.workflow`

路径：

```text
paper_extractor/workflow.py
```

职责：

- 枚举 Markdown 文件。
- 校验 `paper_id` 是否重复。
- 调用 preprocess。
- 调用文本模型。
- 调用多模态模型。
- 写出所有 raw intermediate 文件。
- 在 extraction-only 模式下统一触发 postprocess。

### 7.3 `paper_extractor.postprocess`

路径：

```text
paper_extractor/postprocess.py
```

职责：

- 从模型原始 `.txt` 中提取 JSON。
- 去掉 markdown code fence。
- 处理 `<think>...</think>` 等模型额外输出。
- 解析 text extraction JSON。
- 解析 figure JSON。
- 汇总 `multimodal_figures.json`。

postprocess 之后才会有稳定的：

```text
final/text_extraction.json
final/multimodal_figures.json
```

### 7.4 `paper_extractor.unit_normalization`

路径：

```text
paper_extractor/unit_normalization/
```

职责：

- 遍历 `final/text_extraction.json`。
- 识别显式 `{value, unit}`、`temperature + unit` 等结构。
- 将可安全转换的单位统一为项目 canonical units。
- 不修改原始 `final/text_extraction.json`。
- 生成完整 normalized JSON 和转换报告。

推荐运行位置：

```text
postprocess 之后，verify 之前
```

### 7.5 `paper_extractor.knowledge`

路径：

```text
paper_extractor/knowledge/
```

职责：

- 将 `cleaned_input.md` 分块。
- 生成 `paper_map`。
- 对每个 chunk 抽取 claims。
- 做 claim 去重、证据对齐和置信度修正。
- 构造 synthesis payload。
- 生成 `text_claims.jsonl` 和 `text_knowledge.md`。

两种模式：

- `text`：只用文本。
- `fused`：文本 + `final/multimodal_figures.json`。

### 7.6 `verify`

路径：

```text
verify/
```

职责：

- 对结构化 JSON 做确定性结构检查。
- 基于 `cleaned_input.md` 构造 evidence blocks。
- 按 sample 组织局部验证输入。
- 可调用 LLM 生成受限 patch。
- 由代码校验 patch，只应用安全修复。
- 写出完整 `verify/text_extraction_fixed.json`。

它不是重新抽取器，不会让模型重写整篇论文 JSON。

### 7.7 `verify_eval`

路径：

```text
verify_eval/
```

职责：

- 不依赖 ground truth。
- 不修改 JSON。
- 判断字段是否有论文 evidence 支持。
- 输出 paper-level、sample-level、field-level 质量报告。

输入优先级：

```text
verify/text_extraction_fixed.json
normalized/text_extraction_units.json
final/text_extraction.json
```

### 7.8 `evaluation_json2json`

路径：

```text
evaluation_json2json/
```

职责：

- 比较两套模型输出的 `text_extraction.json`。
- 支持 truth/pred 模型目录。
- 对 alloy/process/sample 做对象对齐。
- 将对象映射到 canonical ID。
- 展开字段事实。
- 做数值、单位、文本语义匹配。
- 计算 Precision / Recall / F1。

适合做模型之间的 benchmark。

### 7.9 `paper_extractor.knowledge_graph`

路径：

```text
paper_extractor/knowledge_graph/
```

职责：

- 读取结构化抽取结果。
- 构建 Paper / Alloy / Process / Sample / Phase / Figure / Finding 等节点。
- 构建样品、工艺、组织、性能和证据关系。
- dry-run 导出 JSON payload。
- 写入 Neo4j。

## 8. 输出目录和文件说明

典型输出目录：

```text
outputs_dataset/<paper_id>/
├── preprocess/
│   ├── cleaned_input.md
│   ├── image_groups.json
│   ├── references.json
│   └── summary.json
├── intermediate/
│   ├── text/
│   │   └── text_extraction.txt
│   ├── multimodal/
│   │   ├── image_groups.json
│   │   └── figure_001.txt
│   └── knowledge/
│       ├── chunks_index.json
│       ├── paper_map.json
│       ├── chunk_0001.raw.txt
│       ├── synthesis_payload.json
│       └── validation_warnings.json
├── final/
│   ├── text_extraction.json
│   ├── figure_001.json
│   ├── multimodal_figures.json
│   ├── text_claims.jsonl
│   ├── text_knowledge.md
│   └── text_knowledge.meta.json
├── normalized/
│   ├── text_extraction_units.json
│   └── unit_normalization_report.json
├── verify/
│   ├── text_extraction_fixed.json
│   ├── verify_report.json
│   ├── deterministic_report.json
│   ├── deterministic_report_after.json
│   ├── evidence_blocks.json
│   ├── sample_bundles/
│   ├── sample_inputs/
│   ├── sample_raw_outputs/
│   └── patches/
├── verify_eval/
│   ├── quality_report.json
│   ├── quality_report.md
│   ├── field_facts.json
│   ├── gate_report.json
│   └── evidence_blocks.json
└── logs/
    ├── text.log.jsonl
    ├── multimodal.log.jsonl
    ├── post_parse.log.jsonl
    └── knowledge.log.jsonl
```

最常看的文件：

- 抽取结果：`final/text_extraction.json`
- 单位统一结果：`normalized/text_extraction_units.json`
- verify 修复结果：`verify/text_extraction_fixed.json`
- verify 质量报告：`verify/verify_report.json`
- 无真值评估报告：`verify_eval/quality_report.md`
- knowledge 成品：`final/text_knowledge.md`
- 原始模型输出：`intermediate/**/*.txt`
- 模型调用日志：`logs/*.jsonl`

## 9. 常用命令全集

### 9.1 查看统一入口

```bash
python3 steeldig.py --help
```

支持的子命令：

```text
extract
pipeline
knowledge
units
verify
verify-eval
evaluate
graph
```

### 9.2 只跑主抽取

```bash
python3 steeldig.py extract -- \
  --config config/workflow.json \
  --input dataset \
  --output-root outputs_dataset \
  --recursive \
  --workers 4
```

只跑文本，不跑图片：

```bash
python3 steeldig.py extract -- \
  --config config/workflow.json \
  --input dataset \
  --output-root outputs_dataset \
  --recursive \
  --skip-multimodal
```

跳过已完成论文：

```bash
python3 steeldig.py extract -- \
  --config config/workflow.json \
  --input dataset \
  --output-root outputs_dataset \
  --recursive \
  --skip-existing
```

### 9.3 跑完整 pipeline

```bash
python3 steeldig.py pipeline -- \
  --config config/workflow.json \
  --input dataset \
  --output-root outputs_dataset \
  --recursive \
  --workers 4 \
  --resume-mode resume_partial \
  --knowledge-mode fused
```

### 9.4 只补跑 knowledge

```bash
python3 steeldig.py knowledge -- \
  --config config/workflow.json \
  --run-dir outputs_dataset/A0 \
  --mode fused
```

如果没有多模态结果：

```bash
python3 steeldig.py knowledge -- \
  --config config/workflow.json \
  --run-dir outputs_dataset/A0 \
  --mode text
```

### 9.5 只补跑单位统一

```bash
python3 steeldig.py units -- \
  --dataset-root outputs_dataset \
  --paper-ids A0,A1 \
  --force
```

跑全部已有论文：

```bash
python3 steeldig.py units -- \
  --dataset-root outputs_dataset \
  --workers 4
```

### 9.6 跑 verify

先准备配置：

```bash
cp config/verify_config.example.json config/verify_config.json
```

运行：

```bash
python3 steeldig.py verify -- \
  --config config/verify_config.json \
  --dataset-root outputs_dataset \
  --paper-ids A0,A1 \
  --force
```

不调用 LLM，只做确定性 smoke test：

```bash
python3 steeldig.py verify -- \
  --config config/verify_config.json \
  --dataset-root outputs_dataset \
  --paper-ids A0 \
  --no-llm \
  --force
```

### 9.7 跑 verify_eval

```bash
python3 steeldig.py verify-eval -- \
  --config config/verify_config.json \
  --dataset-root outputs_dataset \
  --paper-ids A0,A1 \
  --force
```

比较 verify 前后质量：

```bash
python3 steeldig.py verify-eval -- \
  --config config/verify_config.json \
  --dataset-root outputs_dataset \
  --paper-ids A0 \
  --compare-verify \
  --force
```

### 9.8 跑 truth/prediction 评估

准备配置：

```bash
cp config/eval_config.example.json config/eval_config.json
```

运行：

```bash
python3 steeldig.py evaluate -- \
  --config config/eval_config.json \
  --truth deepseek \
  --pred doubao \
  --force
```

### 9.9 构建 Neo4j 图谱

dry-run：

```bash
python3 steeldig.py graph -- \
  --dataset-root outputs_dataset \
  --dry-run \
  --export-json outputs_dataset/graph_payload.json
```

写入 Neo4j：

```bash
python3 steeldig.py graph -- \
  --dataset-root outputs_dataset \
  --uri bolt://127.0.0.1:7687 \
  --username neo4j \
  --password '<your-password>' \
  --database neo4j
```

## 10. 单位统一应该什么时候运行

单位统一最适合放在：

```text
postprocess 之后，verify 之前
```

也就是：

```text
final/text_extraction.json
        |
        v
normalized/text_extraction_units.json
        |
        v
verify/text_extraction_fixed.json
```

原因：

- postprocess 之前只有模型原始文本，还没有稳定 JSON。
- verify 之前先统一单位，可以让验证模块在一致的数值空间中工作。
- verify_eval 之后再统一太晚，因为评估已经读取了未统一的结果。
- 不建议在 prompt 中完全依赖模型做单位换算，因为模型换算不可审计。

当前 canonical units 采用材料领域常用工程单位：

```text
temperature: °C
duration: h
stress / strength / modulus: MPa
length / grain size / precipitate size: μm
composition / percent / elongation / reduction ratio: %
hardness: HV
density: g/cm^3
mass gain: mg/cm^2
energy density: mJ/m^2
fracture toughness: MPa·m^0.5
rate: s^-1
```

示例：

```text
0.855 GPa -> 855 MPa
500 nm -> 0.5 μm
30 min -> 0.5 h
1073.15 K -> 800 °C
```

## 11. Verify 和 Verify Eval 怎么用

### 11.1 Verify 的定位

`verify` 是保守修复模块。

它做的是：

- 读取已有结构化 JSON。
- 读取 `preprocess/cleaned_input.md`。
- 做确定性结构检查。
- 找到 sample 级证据块。
- 让 LLM 提出受限 patch。
- 由代码校验 patch。
- 只应用安全 patch。

它不做的是：

- 不重新抽取整篇论文。
- 不让 LLM 重写完整 JSON。
- 不直接相信 LLM patch。

### 11.2 Verify 的输入优先级

```text
normalized/text_extraction_units.json
final/text_extraction.json
```

`run_verify.py` 默认会先补跑 unit normalization。若你明确要验证原始 JSON，可传：

```bash
--skip-unit-normalization
```

### 11.3 Verify Eval 的定位

`verify_eval` 是无真值质量评估模块。

它不修改 JSON，只输出质量报告。

输入优先级：

```text
verify/text_extraction_fixed.json
normalized/text_extraction_units.json
final/text_extraction.json
```

因此最推荐顺序是：

```bash
python3 steeldig.py units -- --dataset-root outputs_dataset
python3 steeldig.py verify -- --config config/verify_config.json --dataset-root outputs_dataset
python3 steeldig.py verify-eval -- --config config/verify_config.json --dataset-root outputs_dataset
```

## 12. Truth/Prediction 评估怎么用

这个模块用于比较两套模型输出，不用于修复单篇论文。

### 12.1 输入目录

评估模块默认读取：

```text
evaluation_json2json/outputs_exp/<model_name>/<paper_id>/final/text_extraction.json
```

例如：

```text
evaluation_json2json/outputs_exp/deepseek/A0/final/text_extraction.json
evaluation_json2json/outputs_exp/doubao/A0/final/text_extraction.json
```

### 12.2 运行

```bash
cp config/eval_config.example.json config/eval_config.json
```

```bash
python3 steeldig.py evaluate -- \
  --config config/eval_config.json \
  --truth deepseek \
  --pred doubao \
  --workers 4 \
  --force
```

### 12.3 输出

```text
evaluation_json2json/output/eval_truth_<truth>_pred_<pred>/
├── evaluation_report.json
├── papers/
├── canonical/
├── diagnostics/
└── field_judge/
```

主要指标：

- precision
- recall
- f1
- section-level TP / FP / FN
- paper-level diagnostics

## 13. Neo4j 知识图谱怎么用

### 13.1 图谱构建原则

知识图谱不是把 JSON 每个字段都拆成节点，而是围绕材料论文的核心结构建图：

```text
Paper
  -> Alloy
  -> Process
  -> Sample
  -> ProcessingStep
  -> Structure
  -> PhaseOccurrence
  -> PropertySet / PropertyMeasurement
  -> Characterization
  -> Figure
  -> Finding
```

`Sample` 是核心桥接节点，连接材料、工艺、组织、性能和证据。

### 13.2 dry-run

```bash
python3 steeldig.py graph -- \
  --dataset-root outputs_dataset \
  --paper-id A0 \
  --dry-run
```

导出 payload：

```bash
python3 steeldig.py graph -- \
  --dataset-root outputs_dataset \
  --paper-id A0 \
  --dry-run \
  --export-json outputs_dataset/A0_graph_payload.json
```

### 13.3 写入 Neo4j

先确保 Neo4j 启动：

```bash
neo4j status
```

写入：

```bash
python3 steeldig.py graph -- \
  --dataset-root outputs_dataset \
  --uri bolt://127.0.0.1:7687 \
  --username neo4j \
  --password '<your-password>' \
  --database neo4j
```

常用查询见：

```text
docs/neo4j_queries.md
```

## 14. 配置字段详解

### 14.1 `config/workflow.example.json`

用途：

- 主抽取
- 多模态抽取
- postprocess
- knowledge workflow

字段：

- `input_path`：输入 Markdown 文件或目录。
- `output_root`：输出根目录。
- `recursive`：目录输入时是否递归扫描 `.md`。
- `workers`：论文级并行数量。
- `limit_papers`：限制处理论文数，`0` 表示不限制。
- `skip_post_parse`：是否跳过 raw text 到 JSON 的后处理。
- `skip_multimodal`：是否跳过图片分析。
- `text_model.model`：文本模型名称。
- `text_model.base_url`：文本模型 OpenAI-compatible endpoint。
- `text_model.api_key`：文本模型 key。
- `text_model.max_tokens`：文本模型最大输出 token。
- `multimodal_model.*`：多模态模型配置。

### 14.2 `config/verify_config.example.json`

用途：

- verify
- verify_eval

字段：

- `dataset_root`：包含 `<paper_id>/final/text_extraction.json` 的根目录。
- `schema_path`：通常是 `../prompt/json_schema.json`。
- `output_summary_path`：verify_eval 数据集级 summary 文件名。
- `force`：已有输出时是否强制重跑。
- `workers`：论文级并行数量。
- `max_evidence_chars`：证据文本最大长度。
- `append_record_enabled`：verify 是否允许追加记录。
- `llm_enabled`：是否启用 LLM。
- `llm.model`：verify/eval 使用的模型。
- `llm.base_url`：LLM endpoint。
- `llm.api_key`：LLM key。
- `llm.temperature`：建议保持 `0.0`。
- `llm.verify_ssl`：是否校验证书。
- `llm.max_retries`：最大重试次数。

### 14.3 `config/eval_config.example.json`

用途：

- truth/prediction benchmark

字段：

- `outputs_exp_root`：模型输出根目录。
- `truth_model`：作为真值的模型目录名。
- `pred_model`：作为预测的模型目录名。
- `output_root`：评估输出目录。
- `field_rules_path`：字段匹配规则。
- `force`：是否强制重评。
- `workers`：并行线程数。
- `llm_bridge.enabled`：是否启用 LLM 对齐和语义判断。
- `llm_bridge.model/base_url/api_key`：LLM bridge 配置。
- `llm_bridge.prompt_path`：sample bridge prompt 路径。

### 14.4 `config/field_rules.example.json`

用途：

- truth/prediction 评估字段规则。
- verify_eval 字段展开和字段规则。
- 数值容差、ID 字段、sample/process 对齐辅助规则。

字段：

- `id_fields`：评估时跳过的纯 ID 字段。
- `sample_id_stopwords`：从 sample id 中剔除的通用词。
- `sample_context_stopwords`：sample 上下文匹配时的停用词。
- `process_stopwords`：process 对齐时的停用词。
- `numeric_tolerances.default`：默认数值容差。
- `numeric_tolerances.<field_path>`：特定字段的绝对/相对容差。

### 14.5 环境变量注入 key

verify 和 evaluation 支持以下环境变量兜底：

```bash
export EVAL_LLM_MODEL="deepseek-v4-flash"
export EVAL_LLM_BASE_URL="https://api.deepseek.com"
export EVAL_LLM_API_KEY="..."
```

也支持：

```bash
export DEEPSEEK_MODEL="deepseek-v4-flash"
export DEEPSEEK_BASE_URL="https://api.deepseek.com"
export DEEPSEEK_API_KEY="..."
```

主抽取工作流也可以通过命令行覆盖 key：

```bash
python3 steeldig.py pipeline -- \
  --config config/workflow.json \
  --text-api-key "$TEXT_API_KEY" \
  --mm-api-key "$MM_API_KEY"
```

## 15. 调试和排错

### 15.1 找不到 Markdown

报错：

```text
No markdown files found.
```

检查：

- `--input` 是否正确。
- 是否真的有 `.md` 文件。
- 如果目录很深，是否传了 `--recursive`。

### 15.2 paper_id 冲突

报错中会出现：

```text
Duplicate paper_id detected
```

原因：

- 多个 Markdown 文件名相同。

解决：

- 把 Markdown 文件改成唯一名称，建议使用 DOI、A0、A1 或项目内部唯一编号。

### 15.3 图片找不到

多模态阶段可能报：

```text
Image not found
```

检查：

- Markdown 图片路径是否相对 Markdown 文件目录。
- `images/` 是否存在。
- 文件名大小写是否一致。

### 15.4 LLM 接口报错

检查：

- `base_url` 是否包含 `/v1`。
- `api_key` 是否正确。
- 模型名是否是服务端支持的模型名。
- 本地服务是否启动。
- 代理是否干扰本地 `127.0.0.1` 请求。

项目的 `paper_extractor/client.py` 对 OpenAI 客户端设置了 `trust_env=False`，用于降低系统代理对本地接口的影响。

### 15.5 postprocess 失败

优先看：

```text
outputs_dataset/<paper_id>/logs/post_parse.log.jsonl
outputs_dataset/<paper_id>/intermediate/text/text_extraction.txt
```

常见原因：

- 模型没有输出 JSON。
- JSON 被截断。
- 输出里混入太多解释文本。
- schema 字段不完整。

### 15.6 knowledge 结果太少

优先看：

```text
intermediate/knowledge/paper_map.json
intermediate/knowledge/chunk_*.raw.txt
intermediate/knowledge/validation_warnings.json
intermediate/knowledge/synthesis_payload.json
```

常见原因：

- `cleaned_input.md` 清洗过度。
- chunk 证据无法回贴。
- claim 被 normalizer 判为低可信。
- synthesis payload 过滤过严。

### 15.7 verify_eval 分数低

优先看：

```text
verify_eval/quality_report.md
verify_eval/field_facts.json
verify_eval/evidence_blocks.json
```

常见原因：

- 抽取字段没有原文证据。
- sample_id / process_id 关联错误。
- 单位或数值不统一。
- verify 还没跑，评估的是原始 final JSON。

## 16. 开发与测试

运行全部测试：

```bash
python3 -m unittest discover tests
```

编译关键入口：

```bash
python3 -m py_compile \
  steeldig.py \
  run_paper_workflow.py \
  run_paper_then_knowledge_workflow.py \
  run_unit_normalization.py \
  run_verify.py \
  run_verify_eval.py \
  run_evaluation.py \
  run_knowledge_graph.py
```

安装为可执行命令：

```bash
.venv/bin/python -m pip install -e .
steeldig --help
```

代码阅读建议：

1. `steeldig.py`
2. `run_paper_then_knowledge_workflow.py`
3. `paper_extractor/workflow.py`
4. `paper_extractor/postprocess.py`
5. `paper_extractor/unit_normalization/core.py`
6. `verify/core.py`
7. `verify_eval/core.py`
8. `paper_extractor/knowledge/workflow.py`
9. `paper_extractor/knowledge_graph/builder.py`

## 17. GitHub 提交建议

应该提交：

- 源码：`paper_extractor/`、`verify/`、`verify_eval/`、`evaluation_json2json/`
- 提示词：`prompt/`
- 示例配置：`config/*.example.json`
- 字段规则示例：`config/field_rules.example.json`
- 文档：`README.md`、`docs/`、`input/README.md`
- 测试：`tests/`
- 入口：`steeldig.py`、`run_*.py`

不应该提交：

- `config/workflow.json`
- `config/verify_config.json`
- `config/eval_config.json`
- `config/field_rules.json`
- `dataset/`
- `outputs_dataset/`
- `workflow_runs/`
- `evaluation_json2json/output/`
- `evaluation_json2json/outputs_exp/`
- API key、私有模型地址、私有论文数据

提交前建议检查：

```bash
git status --short
python3 -m unittest discover tests
rg -n "sk-[A-Za-z0-9]|/Users/" README.md docs config paper_extractor verify verify_eval
```

如果 `rg` 命中了真实 key 或本机绝对路径，先清理再提交。
