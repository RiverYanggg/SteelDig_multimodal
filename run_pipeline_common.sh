#!/usr/bin/env bash

set -euo pipefail

# 切换到脚本所在目录，避免从别的目录启动时找不到相对路径。
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# =========================
# 常用可编辑参数
# =========================

# 配置文件路径。通常保持默认即可。
CONFIG_PATH="config/workflow.json"

# 输入路径：
# - 可以是单个 .md 文件
# - 也可以是包含多个 .md 的目录
INPUT_PATH="dataset"

# 输出根目录。每篇论文会输出到 OUTPUT_ROOT/<paper_id>/ 下。
OUTPUT_ROOT="workflow_runs"

# 并行处理的论文数。建议按本地模型服务吞吐能力调整。
WORKERS=4

# 是否递归扫描 INPUT_PATH 下的子目录：
# - true: 递归查找 .md 文件
# - false: 只扫描当前目录
RECURSIVE=true

# 是否跳过 post-parse：
# - false: 正常执行 txt -> json 后处理
# - true: 跳过后处理
# 注意：如果 KNOWLEDGE_MODE="fused"，通常不要设为 true。
SKIP_POST_PARSE=false

# 是否跳过多模态图像分析阶段：
# - false: 执行图像分析
# - true: 只跑文本相关流程
SKIP_MULTIMODAL=false

# 是否让 knowledge 流程使用 mock model：
# - false: 使用真实模型
# - true: 用于离线调试 / smoke test
KNOWLEDGE_MOCK_MODEL=false

# 续跑模式：
# - none: 每次都从头跑
# - skip_completed: 完整跑完的论文直接跳过
# - resume_partial: 自动补跑缺失阶段，最常用
RESUME_MODE="resume_partial"

# knowledge 模式：
# - text: 只基于文本抽取结果构建 knowledge
# - fused: 融合文本和图像信息，正式场景更常用
KNOWLEDGE_MODE="fused"

# knowledge 动态分块参数：
# - TARGET_CHUNKS: 期望每篇论文切成几块，默认约 5 块
# - MAX_CHUNKS: 软上限，能合并时尽量不超过该数量
# - MAX_CHUNK_CHARS: 单个 chunk 的硬字符上限
# - MIN_CHUNK_CHARS: 小于该长度的相邻 chunk 会优先合并
KNOWLEDGE_TARGET_CHUNKS=5
KNOWLEDGE_MAX_CHUNKS=8
KNOWLEDGE_MAX_CHUNK_CHARS=24000
KNOWLEDGE_MIN_CHUNK_CHARS=6000

# 限制处理论文数量：
# - 0: 不限制，处理全部论文
# - >0: 只处理前 N 篇，适合抽样测试
LIMIT_PAPERS=0

# 可选模型覆盖参数：
# 留空时使用 config/workflow.json 里的配置；
# 填写后会覆盖配置文件中的对应字段。
TEXT_MODEL=""
TEXT_BASE_URL=""
TEXT_API_KEY=""
MM_MODEL=""
MM_BASE_URL=""
MM_API_KEY=""

# 组装最终启动命令。上面的变量改完后，这里无需手动修改。
CMD=(
  python3 run_paper_then_knowledge_workflow.py
  --config "$CONFIG_PATH"
  --input "$INPUT_PATH"
  --output-root "$OUTPUT_ROOT"
  --workers "$WORKERS"
  --resume-mode "$RESUME_MODE"
  --knowledge-mode "$KNOWLEDGE_MODE"
  --knowledge-max-chunk-chars "$KNOWLEDGE_MAX_CHUNK_CHARS"
  --knowledge-target-chunks "$KNOWLEDGE_TARGET_CHUNKS"
  --knowledge-max-chunks "$KNOWLEDGE_MAX_CHUNKS"
  --knowledge-min-chunk-chars "$KNOWLEDGE_MIN_CHUNK_CHARS"
)

# 下面这些判断用于按需追加布尔 / 可选参数。
if [[ "$RECURSIVE" == "true" ]]; then
  CMD+=(--recursive)
fi

if [[ "$SKIP_POST_PARSE" == "true" ]]; then
  CMD+=(--skip-post-parse)
fi

if [[ "$SKIP_MULTIMODAL" == "true" ]]; then
  CMD+=(--skip-multimodal)
fi

if [[ "$KNOWLEDGE_MOCK_MODEL" == "true" ]]; then
  CMD+=(--knowledge-mock-model)
fi

if [[ "$LIMIT_PAPERS" -gt 0 ]]; then
  CMD+=(--limit-papers "$LIMIT_PAPERS")
fi

if [[ -n "$TEXT_MODEL" ]]; then
  CMD+=(--text-model "$TEXT_MODEL")
fi

if [[ -n "$TEXT_BASE_URL" ]]; then
  CMD+=(--text-base-url "$TEXT_BASE_URL")
fi

if [[ -n "$TEXT_API_KEY" ]]; then
  CMD+=(--text-api-key "$TEXT_API_KEY")
fi

if [[ -n "$MM_MODEL" ]]; then
  CMD+=(--mm-model "$MM_MODEL")
fi

if [[ -n "$MM_BASE_URL" ]]; then
  CMD+=(--mm-base-url "$MM_BASE_URL")
fi

if [[ -n "$MM_API_KEY" ]]; then
  CMD+=(--mm-api-key "$MM_API_KEY")
fi

# 打印最终执行命令，便于确认实际传入了哪些参数。
printf 'Running command:\n'
printf '  %q' "${CMD[@]}"
printf '\n'

# 正式执行工作流。
"${CMD[@]}"
