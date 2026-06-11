# Unit Normalization

本文档说明单位统一模块的定位、运行时机、输入输出，以及它和 `verify` / `verify_eval` 的关系。

推荐优先使用统一入口：

```bash
python3 steeldig.py units -- --dataset-root outputs_dataset
```

下文保留的 `python3 run_*.py` 命令仍然可用，主要用于兼容旧流程。

---

## 1. 模块定位

单位统一是一个确定性的后处理阶段，目标是把 `text_extraction.json` 中显式带单位的结构化字段统一到项目约定的 canonical units。

它不重新抽取论文，不调用 LLM，不修改原始 `final/text_extraction.json`。

推荐流程：

```text
intermediate/text/text_extraction.txt
        |
        v
final/text_extraction.json
        |
        v
normalized/text_extraction_units.json
        |
        v
verify/text_extraction_fixed.json
        |
        v
verify_eval/quality_report.json
```

也就是说，单位统一最适合放在：

```text
post_parse 之后，verify 之前
```

原因是：

- `post_parse` 之前还没有稳定 JSON，不适合做字段级单位处理。
- `verify` 之前统一单位，可以让 verify 在更一致的数值空间里做证据校验。
- `verify_eval` 之后再统一太晚，评估已经读过未统一的结果。
- 不应在 LLM 抽取 prompt 内强制完成所有换算，因为模型换算不可审计，且容易改坏原文证据。

---

## 2. 输入输出

输入：

```text
outputs_dataset/<paper_id>/final/text_extraction.json
```

输出：

```text
outputs_dataset/<paper_id>/normalized/text_extraction_units.json
outputs_dataset/<paper_id>/normalized/unit_normalization_report.json
```

`text_extraction_units.json` 是统一单位后的完整 JSON。

`unit_normalization_report.json` 记录每个字段的处理结果：

```text
converted: 已换算
unchanged: 已是 canonical unit
skipped: 识别到单位但暂不支持安全换算
ambiguous: 字段或单位不足以安全判断
```

---

## 3. Canonical Units

当前项目采用材料领域更实用的工程基准单位，而不是机械地全部换成纯 SI 基本单位。

```text
temperature: °C
duration: h
stress / strength / modulus / strain_hardening_rate: MPa
length / grain size / precipitate size: μm
percent / composition / elongation / reduction ratio: %
hardness: HV
density: g/cm^3
mass gain: mg/cm^2
energy density: mJ/m^2
fracture toughness: MPa·m^0.5
rate: s^-1
```

例如：

```text
0.855 GPa -> 855 MPa
500 nm -> 0.5 μm
30 min -> 0.5 h
1073.15 K -> 800 °C
```

---

## 4. 推荐运行方式

### 4.1 单独补跑单位统一

对一篇论文：

```bash
python3 run_unit_normalization.py \
  --dataset-root outputs_dataset \
  --paper-ids A2 \
  --force
```

对全部已有结果：

```bash
python3 run_unit_normalization.py \
  --dataset-root outputs_dataset \
  --workers 4
```

### 4.2 跑 verify 时自动统一

`run_verify.py` 默认会先运行单位统一，然后 verify 优先读取：

```text
normalized/text_extraction_units.json
```

命令：

```bash
python3 run_verify.py \
  --dataset-root outputs_dataset \
  --paper-ids A2 \
  --force
```

如果你明确想验证原始 `final/text_extraction.json`，使用：

```bash
python3 run_verify.py \
  --dataset-root outputs_dataset \
  --paper-ids A2 \
  --skip-unit-normalization
```

### 4.3 完整 pipeline 中自动运行

`run_paper_then_knowledge_workflow.py` 已经在 `post_parse` 后自动运行单位统一。

推荐完整命令：

```bash
python3 run_paper_then_knowledge_workflow.py \
  --config config/workflow.json \
  --input dataset \
  --recursive \
  --workers 4 \
  --resume-mode resume_partial \
  --knowledge-mode fused
```

如果要跳过单位统一：

```bash
python3 run_paper_then_knowledge_workflow.py \
  --config config/workflow.json \
  --input dataset \
  --recursive \
  --workers 4 \
  --resume-mode resume_partial \
  --knowledge-mode fused \
  --skip-unit-normalization
```

---

## 5. 与 Verify / Verify Eval 的关系

`verify` 的输入优先级：

```text
normalized/text_extraction_units.json
final/text_extraction.json
```

`verify_eval` 的输入优先级：

```text
verify/text_extraction_fixed.json
normalized/text_extraction_units.json
final/text_extraction.json
```

因此最推荐的顺序是：

```bash
python3 run_unit_normalization.py --dataset-root outputs_dataset
python3 run_verify.py --dataset-root outputs_dataset
python3 run_verify_eval.py --dataset-root outputs_dataset
```

实际使用中，如果直接跑 `run_verify.py`，第一步可以省略，因为 verify 会自动补跑单位统一。

---

## 6. 安全边界

模块只处理结构化字段和显式单位，不改自由文本描述。

不会改写：

```text
processes[].description
*_notes
overall_structure
key_findings
figure description
```

这样可以避免误伤：

```text
Fe-10Mn-6Al
800 °C for 30 min 的自然语言证据
caption 中的坐标轴描述
```

对于没有显式单位的数值，模块默认不补单位。

例如：

```json
{"atomic_percent": "15"}
```

不会被自动改成：

```json
{"atomic_percent": "15 %"}
```

原因是抽取结果可能已经约定字段语义，也可能来自合金名或表格上下文；后处理阶段不应猜测。

---

## 7. 什么时候最合适运行

最合适的时机是每篇论文完成 `post_parse` 后立刻运行。

具体判断：

```text
final/text_extraction.json 已存在
normalized/text_extraction_units.json 不存在，或需要 --force 重跑
verify/text_extraction_fixed.json 尚未生成，或准备 --force 重跑 verify
```

不建议在以下时机运行：

- 主抽取之前：没有 JSON 可处理。
- `intermediate/text/text_extraction.txt` 阶段：模型输出还可能不是合法 JSON。
- verify 之后：verify 已经基于旧单位做过判断，除非同时重跑 verify。
- verify_eval 之后：评估结果已经对应旧输入，除非同时重跑 verify_eval。

如果你修改了单位规则，推荐重跑：

```bash
python3 run_unit_normalization.py --dataset-root outputs_dataset --force
python3 run_verify.py --dataset-root outputs_dataset --force
python3 run_verify_eval.py --dataset-root outputs_dataset --force
```
