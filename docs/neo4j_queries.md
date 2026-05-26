# Neo4j Query Cookbook

以下查询默认基于本项目的知识图谱模型。

## 使用原则

- 在 Neo4j Browser 里想看到“边”，不要只 `RETURN` 节点，优先 `RETURN path`
- 全库不要直接一次性展开，先看单篇论文子图，再看单个样品局部图
- 推荐先浏览 `A0`，确认 `Paper -> Sample -> Alloy/Process -> PhaseOccurrence -> Figure/Finding` 这条主链

## 0. 先确认是否有数据

```cypher
MATCH (n)
RETURN count(n) AS total_nodes;
```

## 0.1 查看当前有哪些关系类型

```cypher
MATCH ()-[r]->()
RETURN DISTINCT type(r) AS relationship_type
ORDER BY relationship_type;
```

## 1. 查看数据库里有哪些论文

```cypher
MATCH (p:Paper)
RETURN p.paper_id AS paper_id, p.title AS title
ORDER BY paper_id;
```

## 2. 查看 A0 的论文骨架

这是最适合最先看的图，能直接看到 `Paper`、`Sample`、`Alloy`、`Process` 以及关系边。

```cypher
MATCH p1 = (p:Paper {paper_id: "A0"})-[:HAS_SAMPLE]->(s:Sample)
OPTIONAL MATCH p2 = (s)-[:OF_ALLOY]->(a:Alloy)
OPTIONAL MATCH p3 = (s)-[:PROCESSED_BY]->(proc:Process)
RETURN p1, p2, p3;
```

## 3. 查看某篇论文的样品桥接结构

```cypher
MATCH (p:Paper {paper_id: "A0"})-[:HAS_SAMPLE]->(s:Sample)
OPTIONAL MATCH (s)-[:OF_ALLOY]->(a:Alloy)
OPTIONAL MATCH (s)-[:PROCESSED_BY]->(proc:Process)
RETURN p.paper_id, s.sample_id, a.alloy_name, proc.description
ORDER BY s.sample_id;
```

## 4. 查看某个样品观察到的相

这条会展示 `Sample -> PhaseOccurrence -> Phase` 的组织链。

```cypher
MATCH path =
  (s:Sample {sample_id: "sample_3cu"})-[:EXHIBITS_PHASE]->(po:PhaseOccurrence)-[:INSTANTIATES]->(ph:Phase)
RETURN path;
```

## 5. 查看某个样品的完整局部图

如果你想看一张比较完整、但还不至于失控的图，推荐从单个样品开始。

```cypher
MATCH p1 = (s:Sample {sample_id: "sample_3cu"})-[:OF_ALLOY]->(a:Alloy)
OPTIONAL MATCH p2 = (s)-[:PROCESSED_BY]->(proc:Process)
OPTIONAL MATCH p3 = (s)-[:HAS_STEP]->(step:ProcessingStep)
OPTIONAL MATCH p4 = (s)-[:EXHIBITS_PHASE]->(po:PhaseOccurrence)-[:INSTANTIATES]->(ph:Phase)
OPTIONAL MATCH p5 = (s)-[:CHARACTERIZED_BY]->(c:Characterization)-[:USES_TECHNIQUE]->(t:Technique)
OPTIONAL MATCH p6 = (fig:Figure)-[:EVIDENCE_FOR]->(s)
OPTIONAL MATCH p7 = (f:Finding)-[:ABOUT]->(s)
RETURN p1, p2, p3, p4, p5, p6, p7;
```

## 6. 查看某个样品观察到的相

```cypher
MATCH (s:Sample {sample_id: "sample_3cu"})-[:EXHIBITS_PHASE]->(po:PhaseOccurrence)-[:INSTANTIATES]->(ph:Phase)
RETURN s.sample_id, po.microstructure_uuid, ph.name, po.morphologies, po.lattice_parameters
ORDER BY ph.name;
```

## 7. 查看 A0 的图像证据层

这条图最适合解释 figure/finding 为什么被纳入图谱。

```cypher
MATCH p1 = (p:Paper {paper_id: "A0"})-[:HAS_FIGURE]->(fig:Figure)
OPTIONAL MATCH p2 = (fig)-[:SUMMARIZED_AS]->(summary:Finding)
OPTIONAL MATCH p3 = (fig)-[:SUPPORTS]->(supported:Finding)
RETURN p1, p2, p3;
```

## 8. 查看 A0 的完整展示图

这条查询会返回一张“有实体，也有关系”的论文子图，适合展示，但不要直接用于全库。

```cypher
MATCH p1 = (p:Paper {paper_id: "A0"})-[:HAS_SAMPLE]->(s:Sample)
OPTIONAL MATCH p2 = (s)-[:OF_ALLOY]->(a:Alloy)
OPTIONAL MATCH p3 = (s)-[:PROCESSED_BY]->(proc:Process)
OPTIONAL MATCH p4 = (s)-[:EXHIBITS_PHASE]->(po:PhaseOccurrence)-[:INSTANTIATES]->(ph:Phase)
OPTIONAL MATCH p5 = (s)-[:CHARACTERIZED_BY]->(c:Characterization)-[:USES_TECHNIQUE]->(t:Technique)
OPTIONAL MATCH p6 = (p)-[:HAS_FIGURE]->(fig:Figure)
OPTIONAL MATCH p7 = (p)-[:HAS_FINDING]->(f:Finding)
RETURN p1, p2, p3, p4, p5, p6, p7
LIMIT 300;
```

## 9. 查找所有涉及 κ-carbide 的论文

```cypher
MATCH (p:Paper)-[:HAS_SAMPLE]->(:Sample)-[:EXHIBITS_PHASE]->(:PhaseOccurrence)-[:INSTANTIATES]->(ph:Phase)
WHERE toLower(ph.name) CONTAINS "kappa" OR ph.name CONTAINS "κ"
RETURN DISTINCT p.paper_id, p.title
ORDER BY p.paper_id;
```

## 10. 查找涉及 Cu-rich phase 的图像证据

```cypher
MATCH (f:Figure)-[:SUMMARIZED_AS|SUPPORTS]->(finding:Finding)-[:INVOLVES]->(:PhaseOccurrence)-[:INSTANTIATES]->(ph:Phase)
WHERE toLower(ph.name) CONTAINS "cu-rich"
RETURN DISTINCT f.figure_id, f.paper_id, f.image_type, f.image_paths
ORDER BY f.paper_id, f.figure_id;
```

## 11. 查找所有使用 TEM 的样品

```cypher
MATCH (s:Sample)-[:CHARACTERIZED_BY]->(c:Characterization)-[:USES_TECHNIQUE]->(t:Technique)
WHERE toLower(t.name) CONTAINS "tem"
RETURN DISTINCT s.sample_id, c.characterization_id, t.name, c.key_findings
ORDER BY s.sample_id;
```

## 12. 查找哪些 finding 同时涉及 Cu 和 κ-carbide

```cypher
MATCH (f:Finding)-[:INVOLVES_ELEMENT]->(e:Element {symbol: "Cu"})
MATCH (f)-[:INVOLVES]->(:PhaseOccurrence)-[:INSTANTIATES]->(ph:Phase)
WHERE toLower(ph.name) CONTAINS "kappa" OR ph.name CONTAINS "κ"
RETURN f.finding_id, f.paper_id, f.text
ORDER BY f.paper_id, f.finding_id;
```

## 13. 查看某篇论文的证据层

```cypher
MATCH (p:Paper {paper_id: "A0"})-[:HAS_FIGURE]->(fig:Figure)
OPTIONAL MATCH (fig)-[:SUMMARIZED_AS]->(summary:Finding)
OPTIONAL MATCH (fig)-[:SUPPORTS]->(supported:Finding)
RETURN fig.figure_id, summary.text, collect(DISTINCT supported.finding_id) AS supports_findings
ORDER BY fig.figure_id;
```

## 14. 不建议直接运行的全图查询

下面这种查询虽然能返回全图，但在 82 篇数据上几乎一定会非常乱：

```cypher
MATCH (n)-[r]->(m)
RETURN n, r, m;
```

更好的做法是：

- 先限定 `paper_id`
- 或先限定 `sample_id`
- 优先返回 `path`
