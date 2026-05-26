# Knowledge Graph

这个模块负责把 `outputs_dataset/<paper_id>/final/` 下的抽取结果转换成可重复导入的 Neo4j 知识图谱。

## 设计原则

- 一个 Neo4j 数据库，包含多篇论文子图
- `Paper` 是论文级锚点
- `Sample` 是主桥接节点，连接 `Alloy`、`Process`、`Structure`、`PropertySet`、`Characterization`
- `Figure` 和 `Finding` 组成证据层
- 数值、单位、描述、方向、sequence 等优先作为属性，不盲目建节点

## 主要节点

- `Paper`
- `Alloy`
- `Element`
- `Process`
- `Sample`
- `ProcessingStep`
- `Structure`
- `PhaseOccurrence`
- `Phase`
- `InterfaceSet`
- `Interface`
- `PropertySet`
- `PropertyMeasurement`
- `Characterization`
- `Technique`
- `Computation`
- `Figure`
- `Finding`

## 主要关系

- `Paper-HAS_ALLOY->Alloy`
- `Paper-HAS_PROCESS->Process`
- `Paper-HAS_SAMPLE->Sample`
- `Paper-HAS_FIGURE->Figure`
- `Paper-HAS_FINDING->Finding`
- `Alloy-CONTAINS_ELEMENT->Element`
- `Alloy-HAS_PROCESS->Process`
- `Sample-OF_ALLOY->Alloy`
- `Sample-PROCESSED_BY->Process`
- `Sample-HAS_STEP->ProcessingStep`
- `Sample-HAS_STRUCTURE->Structure`
- `Sample-EXHIBITS_PHASE->PhaseOccurrence`
- `Structure-HAS_PHASE_OCCURRENCE->PhaseOccurrence`
- `PhaseOccurrence-INSTANTIATES->Phase`
- `PhaseOccurrence-EMERGED_AFTER->ProcessingStep`
- `Sample-HAS_INTERFACE_SET->InterfaceSet`
- `InterfaceSet-HAS_INTERFACE->Interface`
- `Interface-BETWEEN_PHASE->Phase`
- `Sample-HAS_PROPERTY_SET->PropertySet`
- `PropertySet-HAS_MEASUREMENT->PropertyMeasurement`
- `Sample-CHARACTERIZED_BY->Characterization`
- `Characterization-USES_TECHNIQUE->Technique`
- `Characterization-OBSERVED->PhaseOccurrence`
- `Sample-HAS_COMPUTATION->Computation`
- `Figure-EVIDENCE_FOR->Sample`
- `Figure-SUPPORTS->Finding`
- `Figure-SUMMARIZED_AS->Finding`
- `Finding-ABOUT->Sample`
- `Finding-INVOLVES->PhaseOccurrence`
- `Finding-INVOLVES_ELEMENT->Element`

## 为什么不是“全部 JSON 字段都建节点”

因为这会让图谱失真，也会让查询变得很差。图谱应该表达：

- 谁是研究对象
- 谁经历了什么工艺
- 观察到了什么组织与相
- 哪些图和表征手段支持这些结论

而不是把每个温度、单位、说明句都拆成零碎节点。
