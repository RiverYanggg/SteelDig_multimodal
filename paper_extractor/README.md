# `paper_extractor/` 模块说明

这个目录是项目核心实现所在位置。

如果把整个仓库看成一个多阶段流水线，那么 `paper_extractor/` 提供了四层能力：

1. 配置与基础工具
2. 主抽取工作流
3. 预处理
4. knowledge 工作流

---

## 1. 模块结构

```text
paper_extractor/
├── client.py
├── common.py
├── config.py
├── postprocess.py
├── workflow.py
├── preprocess/
└── knowledge/
```

### `config.py`

定义全局配置对象：

- `LocalModelConfig`
- `WorkflowSettings`

并负责：

- 从 JSON 文件加载配置
- 解析相对路径
- 写出默认配置

### `client.py`

封装模型客户端初始化。

特点：

- 使用 `OpenAI` Python SDK
- 底层 HTTP 客户端使用 `httpx`
- `trust_env=False`
  防止本地 `127.0.0.1` 请求被代理变量劫持

### `common.py`

放了一批所有工作流都会用到的工具函数，例如：

- 读取 prompt 文件
- JSON 候选提取
- 截断长文本用于日志
- 文本清洗
- 从 caption 中提取 `Figure N`

### `workflow.py`

主抽取工作流实现，职责是：

- 枚举输入 Markdown
- 调预处理
- 调文本模型
- 调多模态模型
- 输出中间产物
- 在批处理结束后统一做 post-parse

### `postprocess.py`

把模型原始输出转为最终稳定 JSON。

这是主工作流和 knowledge fused 链接起来的关键模块之一。

### `preprocess/`

负责“把原始 Markdown 变成适合模型消费的干净输入”。

详细说明见：

- [preprocess/README.md](/Users/mac/Desktop/LLM_project/SteelDig_multimodal/paper_extractor/preprocess/README.md)

### `knowledge/`

负责 chunk-level claim 抽取和知识 Markdown 合成。

详细说明见：

- [knowledge/README.md](/Users/mac/Desktop/LLM_project/SteelDig_multimodal/paper_extractor/knowledge/README.md)

---

## 2. 主抽取链的数据流

核心函数：

- [paper_extractor/workflow.py](/Users/mac/Desktop/LLM_project/SteelDig_multimodal/paper_extractor/workflow.py:107) `run_one_paper`
- [paper_extractor/workflow.py](/Users/mac/Desktop/LLM_project/SteelDig_multimodal/paper_extractor/workflow.py:312) `run_workflow`

单篇论文数据流：

1. `md_path -> preprocess_paper`
2. 产出 `preprocess/cleaned_input.md`
3. `cleaned_input.md -> text prompt`
4. 文本模型输出 `intermediate/text/text_extraction.txt`
5. `image_groups -> figure-level multimodal requests`
6. 图像模型输出 `intermediate/multimodal/figure_XXX.txt`
7. `postprocess.py` 把原始输出变成 `final/*.json`

---

## 3. post-parse 为什么单独拆一层

因为模型输出往往并不稳定，常见问题包括：

- 带 `<think>...</think>`
- 带 Markdown 代码块
- 多段 JSON 混在一起
- 前后夹带解释文字
- 原始 JSON 字段不完整

所以项目没有直接相信模型输出，而是先把原文落盘，再由 `postprocess.py` 做解析与修复。

这有几个好处：

- 失败时可回溯
- prompt 可独立调优
- 解析策略可逐步升级
- 后期更容易做 fallback agent 或规则增强

---

## 4. 并行模型

主工作流里的并行在 `workflow.py` 中通过 `ThreadPoolExecutor` 完成。

并行粒度是：

- 论文级并行

不是：

- 文本请求级并行
- 图像请求级并行
- chunk 级并行

这样做的主要理由是：

- 输出目录天然按论文隔离
- 更容易做错误统计
- 更适合后续 knowledge 链接

---

## 5. 代码阅读建议

建议先读：

1. [config.py](/Users/mac/Desktop/LLM_project/SteelDig_multimodal/paper_extractor/config.py:1)
2. [workflow.py](/Users/mac/Desktop/LLM_project/SteelDig_multimodal/paper_extractor/workflow.py:1)
3. [postprocess.py](/Users/mac/Desktop/LLM_project/SteelDig_multimodal/paper_extractor/postprocess.py:1)
4. [knowledge/workflow.py](/Users/mac/Desktop/LLM_project/SteelDig_multimodal/paper_extractor/knowledge/workflow.py:1)

然后再下钻：

1. `preprocess/`
2. `knowledge/extractor.py`
3. `knowledge/synthesis_payload.py`

---

## 6. 开发时最常改的地方

通常包括：

- `prompt/text_extractor_prompt.md`
- `prompt/image_type_prompt.md`
- `paper_extractor/postprocess.py`
- `paper_extractor/knowledge/prompts.py`
- `paper_extractor/knowledge/synthesis_payload.py`

如果你想提升：

- 文本 schema 稳定性
  优先改 `text_extractor_prompt.md` + `postprocess.py`
- 多模态 Figure 质量
  优先改 `image_type_prompt.md`
- knowledge 事实密度
  优先改 `knowledge/prompts.py` + `knowledge/synthesis_payload.py`
