# Quickstart

这份文档只讲最短路径，不讲实现细节。

---

## 1. 安装

```bash
pip install -r requirements.txt
```

确保本地模型服务已经启动，并且 `config/workflow.json` 中的：

- `text_model.base_url`
- `multimodal_model.base_url`

能正确访问。

---

## 2. 最推荐的运行方式

如果你希望一批论文按“每篇论文内部顺序正确、不同论文之间并行”的方式处理，直接运行：

```bash
python3 run_paper_then_knowledge_workflow.py \
  --config config/workflow.json \
  --input dataset \
  --recursive \
  --workers 4 \
  --resume-mode resume_partial \
  --knowledge-mode fused
```

这会对每篇论文依次执行：

1. 主抽取
2. post-parse
3. knowledge

并且不同论文之间并行。

---

## 3. 如果只想跑主抽取

```bash
python3 run_paper_workflow.py \
  --config config/workflow.json \
  --input dataset \
  --recursive \
  --workers 4
```

如果已经跑过一部分，想自动跳过已完成论文：

```bash
python3 run_paper_workflow.py \
  --config config/workflow.json \
  --input dataset \
  --recursive \
  --workers 4 \
  --skip-existing
```

---

## 4. 如果只想对已有结果补跑 knowledge

```bash
python3 run_knowledge_workflow.py \
  --config config/workflow.json \
  --run-dir workflow_runs/10.1002_srin.202200207 \
  --mode fused
```

---

## 5. 输出看哪里

每篇论文输出目录：

```text
workflow_runs/<paper_id>/
```

最重要的文件：

- `final/text_extraction.json`
- `final/multimodal_figures.json`
- `final/text_claims.jsonl`
- `final/text_knowledge.md`

调试优先看：

- `logs/*.jsonl`
- `intermediate/**/*.txt`

---

## 6. 最常见错误

### 依赖没装

如果报：

```text
ModuleNotFoundError: No module named 'httpx'
```

重新执行：

```bash
pip install -r requirements.txt
```

### 文件名冲突

项目现在会检查重复 `paper_id`。

因为：

- `paper_id = Markdown 文件名去掉后缀`

如果两篇论文都叫 `paper.md`，会被拒绝运行。把它们改成唯一文件名，例如 DOI 或唯一编号即可。

### 中途断了如何继续

推荐直接重跑原命令，并保留：

```bash
--resume-mode resume_partial
```

该模式会按论文检查：

- extraction 是否已存在
- post-parse 是否已存在
- knowledge 是否已存在

然后只补跑缺失阶段。
