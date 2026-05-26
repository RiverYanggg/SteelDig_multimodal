# Inferred Layer And Corpus Relation Layer Schema

这份文档定义在当前事实图谱之上新增的两层：

- `Inferred Layer`
- `Corpus Relation Layer`

目标不是替换已有 `Paper / Sample / Alloy / Process / PhaseOccurrence / Figure / Finding` 事实层，而是在其上增加：

- 面向单篇论文内部的隐式推理表达
- 面向多篇论文之间的关系建模
- 面向 GraphRAG / 检索问答的高阶 claim、topic、evidence 组织

---

## 1. 设计原则

### 1.1 分层而不是混写

图谱分为三层：

1. `Fact Layer`
2. `Inferred Layer`
3. `Corpus Relation Layer`

其中：

- `Fact Layer` 只存原文直接支持的结构化事实
- `Inferred Layer` 只存单篇论文内部由模型综合得到的推理结论
- `Corpus Relation Layer` 只存跨论文关系、共识、冲突、主题簇与研究空白

### 1.2 推理层必须可审计

所有推理节点都必须带 provenance：

- `source_type = "inferred"`
- `inference_scope = "paper_internal" | "cross_paper"`
- `generator`
- `prompt_version`
- `created_at`
- `confidence`
- `evidence_node_keys`
- `human_verified`

### 1.3 不污染事实层

以下内容不要直接覆盖事实层节点属性：

- 主导机制判断
- 因果链归纳
- 跨论文一致/冲突判断
- 研究 gap

它们必须作为新节点或新关系存在。

### 1.4 优先支持检索与问答

新增层的主要用途：

- 支持 GraphRAG 中的 query planning
- 支持 evidence-grounded answer synthesis
- 支持 paper-level / corpus-level 比较问答

不是为了追求最大图谱复杂度。

---

## 2. 与现有事实层的边界

当前已有事实层主链：

- `Paper -> Sample -> Alloy / Process / Structure / PropertySet`
- `Sample -> PhaseOccurrence -> Phase`
- `Sample -> Characterization -> Technique`
- `Figure -> Finding -> Sample / PhaseOccurrence / Element`

新增两层只允许：

- 引用事实层节点
- 聚合事实层节点
- 对事实层节点之间的高阶关系做显式表达

新增两层不负责：

- 改写 `text_extraction.json` 中的原始事实字段
- 替换 `Figure.description` 或 `Finding.text`
- 把所有自然语言总结都建成图节点

---

## 3. Inferred Layer

`Inferred Layer` 用于表达单篇论文内部的隐式结论。

建议第一阶段只引入 5 类节点：

- `InferredClaim`
- `Mechanism`
- `CausalRelation`
- `ComparativeClaim`
- `EvidenceCluster`

### 3.1 InferredClaim

#### 语义

单篇论文内部的高阶推理结论，是最核心的推理节点。

#### 典型内容

- 主导 strengthening mechanism
- process -> microstructure -> property 的归纳结论
- 多条 finding / figure 共同支持的总结性判断
- 论文作者未明确写成单句、但可由证据归纳的结论

#### 推荐属性

```json
{
  "claim_id": "A23::inferred_claim::001",
  "paper_id": "A23",
  "title": "Cold rolling drives a two-stage hardening pathway",
  "statement": "Increasing cold rolling reduction first refines planar slip bands and then activates twinning and shear banding, jointly raising strength.",
  "claim_type": "mechanism_summary",
  "scope_text": "Fe-30Mn-11Al-1.2C under cold rolling",
  "novelty": "paper_specific",
  "confidence": 0.81,
  "source_type": "inferred",
  "inference_scope": "paper_internal",
  "generator": "gpt-5",
  "prompt_version": "inferred_claims_v1",
  "created_at": "2026-05-21T00:00:00Z",
  "evidence_node_keys": [
    "A23::figure_005",
    "A23::figure_006",
    "A23::finding::003"
  ],
  "human_verified": false
}
```

#### 推荐关系

- `Paper-[:HAS_INFERRED_CLAIM]->InferredClaim`
- `InferredClaim-[:ABOUT]->Sample`
- `InferredClaim-[:INVOLVES_PHASE]->PhaseOccurrence`
- `InferredClaim-[:INVOLVES_ELEMENT]->Element`
- `InferredClaim-[:SUPPORTED_BY]->Figure`
- `InferredClaim-[:SUPPORTED_BY]->Finding`
- `InferredClaim-[:PROPOSES_MECHANISM]->Mechanism`
- `InferredClaim-[:HAS_EVIDENCE_CLUSTER]->EvidenceCluster`

### 3.2 Mechanism

#### 语义

机制概念节点，用于跨 claim 和跨论文复用。

#### 典型内容

- twinning-induced strengthening
- precipitation strengthening
- planar slip stabilization
- Hall-Petch-like grain refinement strengthening
- shear-band-assisted hardening

#### 推荐属性

```json
{
  "mechanism_key": "twinning_induced_strengthening",
  "name": "Twinning-induced strengthening",
  "aliases": ["TWIP strengthening", "deformation twinning strengthening"],
  "category": "strengthening",
  "description": "Strength increase attributed to the activation of deformation twinning and related barriers to dislocation motion."
}
```

#### 推荐关系

- `InferredClaim-[:PROPOSES_MECHANISM]->Mechanism`
- `Paper-[:DISCUSSES_MECHANISM]->Mechanism`
- `PaperRelation-[:ON_MECHANISM]->Mechanism`

`Mechanism` 建议作为全库共享节点，不按 `paper_id` 作用域重复建。

### 3.3 CausalRelation

#### 语义

表达显式建模的因果链，适用于 `cause -> mediator -> effect`。

#### 推荐属性

```json
{
  "causal_id": "A23::causal::001",
  "paper_id": "A23",
  "cause_text": "cold rolling reduction increase",
  "mediator_text": "slip band refinement and deformation twinning",
  "effect_text": "yield strength increase",
  "condition_text": "from solution-treated to 90% reduction state",
  "direction": "positive",
  "confidence": 0.76,
  "source_type": "inferred",
  "inference_scope": "paper_internal",
  "generator": "gpt-5",
  "prompt_version": "causal_relations_v1",
  "created_at": "2026-05-21T00:00:00Z",
  "evidence_node_keys": [
    "A23::figure_002",
    "A23::figure_005",
    "A23::figure_006"
  ],
  "human_verified": false
}
```

#### 推荐关系

- `InferredClaim-[:HAS_CAUSAL_LINK]->CausalRelation`
- `CausalRelation-[:CAUSES_CHANGE_IN]->PropertyMeasurement`
- `CausalRelation-[:MEDIATED_BY]->Mechanism`
- `CausalRelation-[:AFFECTS]->PhaseOccurrence`
- `CausalRelation-[:ABOUT]->Sample`

第一阶段允许 `cause_text / mediator_text / effect_text` 作为属性存储，避免过度节点化。

### 3.4 ComparativeClaim

#### 语义

表达单篇论文内部样品之间的比较判断。

#### 典型内容

- `sample_cr90` stronger than `sample_st`
- long annealed sample has lower ductility than short annealed sample
- higher Al content correlates with stronger planar slip tendency

#### 推荐属性

```json
{
  "comparison_id": "A31::comparison::002",
  "paper_id": "A31",
  "dimension": "uniform_elongation",
  "comparison": "lower_than",
  "statement": "The long-annealed 2Al sample shows lower uniform elongation than the short-annealed 2Al sample.",
  "condition_text": "tensile loading at room temperature",
  "confidence": 0.88,
  "source_type": "inferred",
  "inference_scope": "paper_internal",
  "generator": "gpt-5",
  "prompt_version": "comparative_claims_v1",
  "created_at": "2026-05-21T00:00:00Z",
  "evidence_node_keys": [
    "A31::finding::004",
    "A31::figure_002"
  ],
  "human_verified": false
}
```

#### 推荐关系

- `Paper-[:HAS_COMPARATIVE_CLAIM]->ComparativeClaim`
- `ComparativeClaim-[:COMPARES_SUBJECT]->Sample`
- `ComparativeClaim-[:SUPPORTED_BY]->Figure`
- `ComparativeClaim-[:SUPPORTED_BY]->Finding`

为了避免关系丢失，建议在属性中同时存：

- `subject_a_key`
- `subject_b_key`

### 3.5 EvidenceCluster

#### 语义

把多个 `Figure`、`Finding`、`Characterization` 聚合成一个支持某个推理结论的证据簇。

#### 推荐属性

```json
{
  "cluster_id": "A23::evidence_cluster::001",
  "paper_id": "A23",
  "summary": "TEM and mechanical-property figures jointly support the two-stage hardening mechanism.",
  "evidence_strength": "strong",
  "evidence_count": 5,
  "confidence": 0.84,
  "source_type": "inferred",
  "inference_scope": "paper_internal",
  "generator": "gpt-5",
  "prompt_version": "evidence_clusters_v1",
  "created_at": "2026-05-21T00:00:00Z",
  "evidence_node_keys": [
    "A23::figure_002",
    "A23::figure_005",
    "A23::figure_006",
    "A23::figure_007",
    "A23::finding::002"
  ],
  "human_verified": false
}
```

#### 推荐关系

- `InferredClaim-[:HAS_EVIDENCE_CLUSTER]->EvidenceCluster`
- `EvidenceCluster-[:INCLUDES_EVIDENCE]->Figure`
- `EvidenceCluster-[:INCLUDES_EVIDENCE]->Finding`
- `EvidenceCluster-[:INCLUDES_EVIDENCE]->Characterization`

---

## 4. Corpus Relation Layer

`Corpus Relation Layer` 用于表达多篇论文之间的关系。

建议第一阶段只引入 4 类节点：

- `Topic`
- `PaperRelation`
- `ConsensusGroup`
- `ResearchGap`

### 4.1 Topic

#### 语义

跨论文共享的检索与归纳主题节点。

#### 典型内容

- `kappa_carbide_strengthening`
- `cold_rolling_texture_transition`
- `deformation_twinning`
- `planar_slip_stabilization`

#### 推荐属性

```json
{
  "topic_key": "kappa_carbide_strengthening",
  "name": "Kappa-carbide strengthening",
  "aliases": ["κ-carbide strengthening", "kappa carbide hardening"],
  "category": "mechanism_topic",
  "description": "Claims and evidence concerning the strengthening contribution of kappa carbides."
}
```

#### 推荐关系

- `Paper-[:HAS_TOPIC]->Topic`
- `InferredClaim-[:ON_TOPIC]->Topic`
- `PaperRelation-[:ON_TOPIC]->Topic`
- `ConsensusGroup-[:ON_TOPIC]->Topic`
- `ResearchGap-[:ON_TOPIC]->Topic`

### 4.2 PaperRelation

#### 语义

跨论文关系的主节点，推荐使用节点而不是直接边，以便挂载说明、证据和 provenance。

#### 关系类型建议

- `supports_same_mechanism`
- `consistent_with`
- `complements`
- `extends`
- `narrows_scope_of`
- `conflicts_with`
- `uses_similar_system`
- `uses_similar_process`

#### 推荐属性

```json
{
  "relation_id": "A23__A31__paper_relation__001",
  "source_paper_id": "A23",
  "target_paper_id": "A31",
  "relation_type": "complements",
  "statement": "A23 and A31 jointly support deformation-substructure-mediated strengthening, but in different alloy/process contexts.",
  "comparison_basis": "mechanism",
  "agreement_level": "partial",
  "confidence": 0.74,
  "evidence_summary": "Both papers report strengthening associated with deformation substructures, though one emphasizes twinning/shear bands and the other precipitation-assisted planar slip.",
  "source_type": "inferred",
  "inference_scope": "cross_paper",
  "generator": "gpt-5",
  "prompt_version": "cross_paper_relations_v1",
  "created_at": "2026-05-21T00:00:00Z",
  "evidence_node_keys": [
    "A23::inferred_claim::001",
    "A31::inferred_claim::002"
  ],
  "human_verified": false
}
```

#### 推荐关系

- `PaperRelation-[:SOURCE_PAPER]->Paper`
- `PaperRelation-[:TARGET_PAPER]->Paper`
- `PaperRelation-[:ON_TOPIC]->Topic`
- `PaperRelation-[:ON_MECHANISM]->Mechanism`
- `PaperRelation-[:SUPPORTED_BY]->InferredClaim`
- `PaperRelation-[:SUPPORTED_BY]->Finding`

不推荐第一阶段直接创建：

- `(:Paper)-[:CONFLICTS_WITH]->(:Paper)`
- `(:Paper)-[:EXTENDS]->(:Paper)`

因为这会让 provenance 挂不住，也不利于后期人审。

### 4.3 ConsensusGroup

#### 语义

表达多篇论文在某 topic 上形成的共识簇。

#### 推荐属性

```json
{
  "consensus_id": "consensus::kappa_carbide_strengthening::001",
  "topic_key": "kappa_carbide_strengthening",
  "statement": "Across several papers, nanoscale kappa carbides are repeatedly associated with strengthening, but ductility trade-offs vary by distribution and shearability.",
  "consensus_type": "qualified_consensus",
  "paper_count": 6,
  "confidence": 0.79,
  "source_type": "inferred",
  "inference_scope": "cross_paper",
  "generator": "gpt-5",
  "prompt_version": "consensus_groups_v1",
  "created_at": "2026-05-21T00:00:00Z",
  "evidence_node_keys": [
    "A31::inferred_claim::002",
    "A66::inferred_claim::001",
    "A5::inferred_claim::003"
  ],
  "human_verified": false
}
```

#### 推荐关系

- `ConsensusGroup-[:ON_TOPIC]->Topic`
- `ConsensusGroup-[:INCLUDES_PAPER]->Paper`
- `ConsensusGroup-[:SUPPORTED_BY]->InferredClaim`
- `ConsensusGroup-[:SUPPORTED_BY]->PaperRelation`

### 4.4 ResearchGap

#### 语义

表达跨论文归纳出来的研究空白、争议点或未解决问题。

#### 推荐属性

```json
{
  "gap_id": "gap::kappa_carbide_shearability::001",
  "topic_key": "kappa_carbide_strengthening",
  "statement": "The role of kappa-carbide shearability in sustaining ductility under different precipitation morphologies remains unresolved.",
  "gap_type": "mechanism_uncertainty",
  "priority": "high",
  "confidence": 0.72,
  "source_type": "inferred",
  "inference_scope": "cross_paper",
  "generator": "gpt-5",
  "prompt_version": "research_gaps_v1",
  "created_at": "2026-05-21T00:00:00Z",
  "evidence_node_keys": [
    "A31__A66__paper_relation__001",
    "A31::inferred_claim::004"
  ],
  "human_verified": false
}
```

#### 推荐关系

- `ResearchGap-[:ON_TOPIC]->Topic`
- `ResearchGap-[:IDENTIFIED_FROM]->Paper`
- `ResearchGap-[:SUPPORTED_BY]->PaperRelation`
- `ResearchGap-[:SUPPORTED_BY]->InferredClaim`

---

## 5. 建模准则

### 5.1 哪些内容值得进 Inferred Layer

只有同时满足以下条件的内容才推荐入图：

- 由多个事实节点支持
- 具有复用价值
- 对检索问答有帮助
- 可以提供 evidence list
- 可以接受置信度和后续修订

### 5.2 哪些内容不要进图

以下内容优先留在 Markdown 或离线分析文件中：

- 泛泛的论文摘要
- 低价值语气判断
- 缺乏证据支持的模型猜测
- 一次性展示文案

### 5.3 节点复用规则

- `Mechanism` 和 `Topic` 为全库共享节点
- `InferredClaim`、`CausalRelation`、`ComparativeClaim`、`EvidenceCluster` 为 `paper_id` scoped 节点
- `PaperRelation` 为论文对 scoped 节点
- `ConsensusGroup` 与 `ResearchGap` 为 corpus scoped 节点

---

## 6. JSON 落盘设计

建议在每篇论文的 `final/` 下新增：

- `inferred_claims.json`
- `mechanism_graph.json`

在全库级别新增目录：

- `corpus_outputs/`

其中保存：

- `cross_paper_relations.json`
- `consensus_groups.json`
- `research_gaps.json`

### 6.1 `inferred_claims.json`

建议格式：

```json
{
  "paper_id": "A23",
  "inferred_claims": [],
  "comparative_claims": [],
  "causal_relations": [],
  "evidence_clusters": []
}
```

### 6.2 `mechanism_graph.json`

建议格式：

```json
{
  "paper_id": "A23",
  "mechanisms": [],
  "claim_mechanism_links": [],
  "topic_links": []
}
```

### 6.3 `cross_paper_relations.json`

建议格式：

```json
{
  "corpus_id": "outputs_dataset",
  "paper_relations": []
}
```

### 6.4 `consensus_groups.json`

建议格式：

```json
{
  "corpus_id": "outputs_dataset",
  "consensus_groups": []
}
```

### 6.5 `research_gaps.json`

建议格式：

```json
{
  "corpus_id": "outputs_dataset",
  "research_gaps": []
}
```

---

## 7. Neo4j 落库建议

### 7.1 新增标签

- `InferredClaim`
- `Mechanism`
- `CausalRelation`
- `ComparativeClaim`
- `EvidenceCluster`
- `Topic`
- `PaperRelation`
- `ConsensusGroup`
- `ResearchGap`

### 7.2 新增约束

建议补充唯一键约束：

```cypher
CREATE CONSTRAINT inferred_claim_node_key IF NOT EXISTS FOR (n:InferredClaim) REQUIRE n.node_key IS UNIQUE;
CREATE CONSTRAINT mechanism_node_key IF NOT EXISTS FOR (n:Mechanism) REQUIRE n.node_key IS UNIQUE;
CREATE CONSTRAINT causal_relation_node_key IF NOT EXISTS FOR (n:CausalRelation) REQUIRE n.node_key IS UNIQUE;
CREATE CONSTRAINT comparative_claim_node_key IF NOT EXISTS FOR (n:ComparativeClaim) REQUIRE n.node_key IS UNIQUE;
CREATE CONSTRAINT evidence_cluster_node_key IF NOT EXISTS FOR (n:EvidenceCluster) REQUIRE n.node_key IS UNIQUE;
CREATE CONSTRAINT topic_node_key IF NOT EXISTS FOR (n:Topic) REQUIRE n.node_key IS UNIQUE;
CREATE CONSTRAINT paper_relation_node_key IF NOT EXISTS FOR (n:PaperRelation) REQUIRE n.node_key IS UNIQUE;
CREATE CONSTRAINT consensus_group_node_key IF NOT EXISTS FOR (n:ConsensusGroup) REQUIRE n.node_key IS UNIQUE;
CREATE CONSTRAINT research_gap_node_key IF NOT EXISTS FOR (n:ResearchGap) REQUIRE n.node_key IS UNIQUE;
```

### 7.3 关系命名建议

建议统一使用可读且稳定的关系类型：

- `HAS_INFERRED_CLAIM`
- `HAS_COMPARATIVE_CLAIM`
- `PROPOSES_MECHANISM`
- `HAS_CAUSAL_LINK`
- `HAS_EVIDENCE_CLUSTER`
- `SUPPORTED_BY`
- `ON_TOPIC`
- `SOURCE_PAPER`
- `TARGET_PAPER`
- `ON_MECHANISM`
- `INCLUDES_PAPER`
- `IDENTIFIED_FROM`

---

## 8. 与 GraphRAG 的对接建议

新增两层后，GraphRAG 检索顺序建议改为：

1. `Topic / Mechanism / Phase / Process` 级别 query grounding
2. `PaperRelation / InferredClaim` 级别图检索
3. `Finding / Figure.description / text chunk` 级别语义检索
4. 基于 `SUPPORTED_BY` 与 `evidence_node_keys` 拼装证据包

这样能回答：

- 哪些论文支持某机制
- 哪些论文在某议题上结论冲突
- 这个跨论文结论是由哪些 figure / finding 支持的

---

## 9. 第一阶段实现优先级

建议实现顺序：

1. `InferredClaim`
2. `Mechanism`
3. `PaperRelation`
4. `Topic`
5. `ComparativeClaim`
6. `CausalRelation`
7. `ConsensusGroup`
8. `ResearchGap`

理由：

- `InferredClaim + Mechanism + PaperRelation + Topic` 已经能支撑大多数检索问答
- `ConsensusGroup` 与 `ResearchGap` 更适合第二阶段做 corpus synthesis

---

## 10. 推荐最小查询样式

### 10.1 查某机制有哪些论文支持

```cypher
MATCH (m:Mechanism {name: "Twinning-induced strengthening"})<-[:PROPOSES_MECHANISM]-(c:InferredClaim)<-[:HAS_INFERRED_CLAIM]-(p:Paper)
RETURN p.paper_id, c.statement, c.confidence
ORDER BY c.confidence DESC;
```

### 10.2 查两篇论文的关系说明

```cypher
MATCH (r:PaperRelation)-[:SOURCE_PAPER]->(p1:Paper {paper_id: "A23"})
MATCH (r)-[:TARGET_PAPER]->(p2:Paper {paper_id: "A31"})
RETURN r.relation_type, r.statement, r.confidence;
```

### 10.3 查某 topic 的共识与争议

```cypher
MATCH (t:Topic {topic_key: "kappa_carbide_strengthening"})
OPTIONAL MATCH (cg:ConsensusGroup)-[:ON_TOPIC]->(t)
OPTIONAL MATCH (gap:ResearchGap)-[:ON_TOPIC]->(t)
RETURN cg.statement, gap.statement;
```

---

## 11. 总结

新增两层后的总体结构是：

- `Fact Layer` 负责可验证事实
- `Inferred Layer` 负责单篇论文内部的高阶推理
- `Corpus Relation Layer` 负责跨论文关系、共识、冲突与研究空白

最重要的约束是：

- 不混淆事实与推理
- 每个推理结论都能追溯证据
- 每个跨论文关系都要有 topic、statement、confidence 与 provenance

这样后续无论做 Neo4j 浏览、GraphRAG、证据式问答还是人工审核，都会稳很多。
