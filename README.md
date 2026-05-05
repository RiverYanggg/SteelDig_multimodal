# Paper Extractor Workflow

一个只面向本地部署模型的论文提取项目，当前默认按 `Qwen/Qwen3.5-9B` 的 OpenAI 兼容接口运行。

## 当前结构

```text
.
├── dataset/
├── prompt/
├── paper_extractor/
│   ├── client.py       # 本地 OpenAI 兼容客户端
│   ├── common.py       # 公共工具
│   ├── config.py       # 本地模型与工作流配置数据结构
│   ├── postprocess.py  # txt -> json 后处理
│   ├── preprocess/     # 预处理：markdown 清洗、参考文献抽取、图片分组
│   └── workflow.py     # 主工作流实现
├── extract_image_info.py
├── run_paper_workflow.py  # 命令行入口
├── run_workflow.py        # 直接改 Python 配置的入口
├── run_workflow.sh        # 最薄 shell 包装
├── requirements.txt
└── pyproject.toml
```

## 运行方式

推荐直接修改配置文件 [config/workflow.json](/Users/mac/Desktop/LLM_project/SteelDig_multimodal/config/workflow.json)，然后运行：

```bash
python3 run_workflow.py
```

或使用命令行入口：

```bash
python3 run_paper_workflow.py \
  --config config/workflow.json
```

如果文本和多模态都走同一个本地模型，不需要额外配置 `multimodal_model`。命令行参数也可以覆盖配置文件中的模型设置。

## 模型配置

当前项目使用正式配置文件管理模型信息，位置是：

- [config/workflow.json](/Users/mac/Desktop/LLM_project/SteelDig_multimodal/config/workflow.json)

其中和大模型相关的主要字段是：

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

含义：

- `model`：模型名
- `base_url`：OpenAI 兼容服务地址
- `api_key`：接口密钥；本地 vLLM / OpenAI-compatible 服务通常可用 `EMPTY`

## 预处理说明

工作流现在会先对每篇论文执行预处理，再进入文本抽取和多模态抽取。

预处理输出位于每篇论文结果目录下的 `preprocess/`：

- `cleaned_input.md`：清洗后的 markdown，作为后续文本抽取输入
- `references.json`：从原文中分离出的参考文献
- `image_groups.json`：基于清洗后 markdown 生成的图片分组结果
- `summary.json`：预处理摘要，包括是否使用 `*_content_list.json`、移除类别统计等

如果同目录下存在 `*_content_list.json`，预处理会优先利用其中的分类信息清除噪音块，尤其是 `ref_text` 参考文献类内容；如果该文件不存在或为空，则退化为基于 markdown 规则的清洗。

## 输出目录

现在每篇论文对应一个独立结果目录，内部按职责分层：

- `preprocess/`
  - `cleaned_input.md`
  - `references.json`
  - `image_groups.json`
  - `summary.json`
- `intermediate/`
  - `text/text_extraction.txt`：文本模型原始输出，保留 thinking
  - `multimodal/figure_XXX.txt`：每个 Figure 的多模态原始输出
  - `multimodal/image_groups.json`
- `final/`
  - `text_extraction.json`
  - `figure_XXX.json`
  - `multimodal_figures.json`
- `logs/`
  - `text.log.jsonl`
  - `multimodal.log.jsonl`
  - `post_parse.log.jsonl`

## 后处理策略

后处理优先使用规则解析：

- 先尝试从原始 txt 中提取合法 JSON
- 会处理常见噪音，如 `<think>...</think>`、Markdown 代码块、正文前后夹带说明文字、多段 JSON 片段等
- 对文本抽取优先选择最像顶层 schema 的 JSON 对象
- 对图片抽取会统一归一化为 Figure 级 JSON 结果

只有当规则解析失败时，才会调用一个托底解析 Agent，把原始 txt 修复成合法 JSON。

## 组图多模态策略

多模态请求以 Figure 组图为单位：

- 同一张 Figure 下的全部子图打包为一个请求
- 模型输出一个 Figure 级 JSON 对象，而不是每张子图一条记录
- 最终结果格式示例：

```json
{
  "paper_id": "10.1002_srin.201900665",
  "figure_id": "Figure 6",
  "image_paths": [
    "images/1.jpg",
    "images/2.jpg",
    "images/3.jpg",
    "images/4.jpg",
    "images/5.jpg",
    "images/6.jpg"
  ],
  "image_count": 6,
  "image_type": "microscopy_tem",
  "description": "该组图展示了xxx",
  "confidence": 0.92
}
```

## 配置说明

核心配置只有两层：

- `LocalModelConfig`：`model`、`base_url`、`api_key`
- `WorkflowSettings`：输入输出路径、并行度、是否跳过多模态、文本模型配置、多模态模型配置

默认值在 [paper_extractor/config.py](/Users/mac/Desktop/paper_extractor/0421_paper_extractor/paper_extractor/config.py:1)。

## 多模态说明

项目当前支持把图片编码为 `image_url` 发送给本地 OpenAI 兼容服务。如果你的 `Qwen3.5-9B` 服务支持多模态，保持 [run_workflow.py](/Users/mac/Desktop/paper_extractor/0421_paper_extractor/run_workflow.py:16) 中的 `skip_multimodal=False` 即可。

如果某次只想跑文本抽取，可以将 `skip_multimodal=True`。

## 安装

```bash
pip install -r requirements.txt
```
