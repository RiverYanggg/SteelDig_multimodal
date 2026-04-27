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
│   └── workflow.py     # 主工作流实现
├── extract_image_info.py
├── run_paper_workflow.py  # 命令行入口
├── run_workflow.py        # 直接改 Python 配置的入口
├── run_workflow.sh        # 最薄 shell 包装
├── requirements.txt
└── pyproject.toml
```

## 运行方式

直接改 [run_workflow.py](/Users/mac/Desktop/paper_extractor/0421_paper_extractor/run_workflow.py:1) 里的 `SETTINGS`，然后运行：

```bash
python3 run_workflow.py
```

或使用命令行入口：

```bash
python3 run_paper_workflow.py \
  --input dataset \
  --recursive \
  --text-model Qwen/Qwen3.5-9B \
  --text-base-url http://127.0.0.1:8000/v1
```

如果文本和多模态都走同一个本地模型，不需要额外配置 `--mm-*` 参数。

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
