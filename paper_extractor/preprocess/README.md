# `paper_extractor/preprocess/` 模块说明

这个目录负责把原始 Markdown 清洗成适合模型消费的输入，并从中提取 figure 分组、参考文献等辅助信息。

---

## 1. 为什么需要预处理

原始论文 Markdown 往往存在很多噪声：

- 参考文献
- 页眉页脚
- 版权声明
- DOI、收稿日期、修回日期
- 关键词区块
- 多余的换行和排版噪音

如果不先清洗，后续文本模型会：

- 上下文浪费在无关内容上
- 更容易输出错误字段
- 对图片 caption 和正文引用的对应关系理解变差

所以预处理的目标是：

- 尽量保留正文和 figure 语义
- 尽量去掉对抽取无用的版面噪声

---

## 2. 文件职责

### `pipeline.py`

预处理总入口。

关键函数：

- `preprocess_paper`
- `write_preprocess_outputs`

职责：

- 读取 Markdown
- 尝试加载 `*_content_list.json`
- 选择清洗策略
- 提取 references
- 解析 image groups
- 写出 `preprocess/` 产物

### `markdown_cleaner.py`

正文清洗逻辑。

分两类路径：

1. 有 `content_list`
2. 没有 `content_list`

有 `content_list` 时更精细，因为可以按 category 删除块。

### `image_groups.py`

Figure 分组解析逻辑。

负责：

- 找 Markdown 中的图片链接
- 找图片后面的 Figure caption
- 收集该 Figure 在正文中的引用句子
- 输出 Figure 级条目

### `content_list.py`

对 `*_content_list.json` 的辅助读取函数。

### `models.py`

定义 `PreprocessArtifacts` 数据结构，用来承接预处理产物。

---

## 3. Figure 分组怎么做

核心逻辑在 [image_groups.py](/Users/mac/Desktop/LLM_project/SteelDig_multimodal/paper_extractor/preprocess/image_groups.py:1)。

大致规则：

1. 遇到 Markdown 图片语法，先把图片路径放进 `pending_images`
2. 如果后面紧跟 `Figure N ...`，则把这些图片和该 caption 合并成一个组
3. 同时扫描正文里对 `Figure N` / `Fig. N` 的引用句
4. 最后输出：
   - `image_paths`
   - `caption`
   - `paper_abstract`
   - `paper_title`
   - `citation_sentences`

这意味着多模态阶段天然就是 Figure 级别，而不是单图级别。

---

## 4. `content_list` 的作用

如果论文目录下存在：

- `<paper_stem>_content_list.json`

预处理会优先使用它。

好处：

- 能基于 category 删除更可靠的噪声块
- 例如 `ref_text`、`header`、`footer`、`copyright`
- 比单纯正则规则更稳定

如果没有这个文件：

- 系统退回到 `clean_markdown_without_content_list`
- 通过规则识别参考文献和常见噪声段

---

## 5. 预处理输出

每篇论文会得到：

```text
preprocess/
├── cleaned_input.md
├── image_groups.json
├── references.json
└── summary.json
```

### `cleaned_input.md`

这是最重要的文件。

它既用于：

- 主文本抽取
- knowledge 工作流

### `image_groups.json`

供：

- 主工作流多模态阶段
- 调试 figure 分组质量

### `references.json`

保存被剥离的参考文献信息，方便之后单独使用或检查。

### `summary.json`

记录预处理过程元信息，例如：

- `paper_id`
- `source_md_path`
- `source_json_path`
- `used_content_list`
- `removed_categories`
- `removed_blocks`
- `reference_count`
- `image_group_count`

---

## 6. 你最应该先看什么

如果你想调预处理效果，建议依次看：

1. 原始 Markdown
2. `preprocess/cleaned_input.md`
3. `preprocess/image_groups.json`
4. `preprocess/summary.json`

最典型的迭代方式是：

- 如果正文清洗过度，改 `markdown_cleaner.py`
- 如果 figure/caption 对齐不好，改 `image_groups.py`

---

## 7. 常见问题

### 为什么图分组有时会丢 caption？

因为 Markdown 结构并不总是规整，`image_groups.py` 依赖一些启发式规则：

- 图片后是否紧跟 `Figure ...`
- 中间夹杂的是噪声还是正文

所以格式异常的论文可能会出现空 caption。

### 为什么 abstract 要在 image group 中重复保存？

因为多模态 prompt 需要：

- title
- abstract
- caption
- citation sentences

把这些局部打包后，多模态阶段不需要回头再重新读整篇清洗后的 Markdown。
