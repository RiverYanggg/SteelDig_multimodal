import json
from typing import Any, Dict, List

from paper_extractor.knowledge.chunker import Chunk


def build_paper_map_prompt(paper_id: str, markdown_text: str, max_chars: int = 24000) -> str:
    excerpt = _build_paper_map_excerpt(markdown_text, max_chars=max_chars)
    return (
        "你是材料科学论文知识抽取规划助手。请根据论文摘录生成高质量 paper_map JSON，用于后续分块事实抽取。\n"
        "只输出一个合法 JSON 对象，不要 Markdown，不要解释，不要代码块。第一个非空白字符必须是 `{`。\n"
        "输出必须能被 json.loads 直接解析；不要使用 NaN、Infinity、注释、尾随逗号或单引号。\n"
        "paper_map 只应包含全局导航信息和术语/样品索引，不要展开所有实验细节，也不要编造摘录中没有的信息。\n"
        "字段必须包含：paper_id, title, abstract_summary, research_objective, material_systems, "
        "main_process_variables, sample_aliases, expected_information_axis, key_sections。\n"
        "abstract_summary 用 2-4 句英文概括研究对象、核心变量、主要表征/性能目标和结论方向。\n"
        "research_objective 用一句英文写清楚本文要解决的材料科学问题。\n"
        "material_systems 保留合金/材料体系、名义成分、样品系列名和关键相名。\n"
        "main_process_variables 保留热处理、变形、冷却、成分变化、测试条件等全局变量。\n"
        "sample_aliases 应记录样品编号、缩写、系列名及其含义，无法确认含义时只记录原样别名。\n"
        "expected_information_axis 应列出后续抽取应重点跟踪的信息轴，例如 composition, processing, microstructure, property, mechanism, figure_evidence。\n"
        "key_sections 应按论文结构列出重要章节及其作用。\n"
        "所有字段值使用字符串、字符串数组或对象；未知填 null 或空数组。\n\n"
        f"paper_id: {paper_id}\n"
        "paper_excerpt:\n"
        f"{excerpt}"
    )


def build_claim_prompt(paper_map: Dict[str, Any], chunk: Chunk, previous_context_summary: str = "") -> str:
    previous_context_summary = previous_context_summary.strip()
    return (
        "你是材料科学论文局部事实抽取与上下文压缩助手。你会收到 paper_map、previous_context_summary 和 current_chunk。\n"
        "paper_map 和 previous_context_summary 仅用于理解研究主线、术语、样品别名和跨章节连续性。\n"
        "claims 必须严格来自 current_chunk，不能把 previous_context_summary 中的事实写成当前 chunk 的 claim。\n"
        "请抽取信息密度高、证据充分、对训练材料科学语言模型有价值的科学事实，尤其是材料成分、工艺参数、样品状态、"
        "相组成、组织形貌、缺陷/析出物、性能数据、Processing-Structure-Property 关系、机理解释、表征方法和图表证据。\n"
        "优先保留带有数值、单位、样品编号、处理条件、相名、图号/表号、趋势对比、因果关系的事实。\n"
        "低价值信息不要抽取：泛泛背景知识、作者单位、版权信息、参考文献列表、仪器型号本身、没有科学结论的实验流程碎片。\n"
        "只输出一个合法 JSON 对象，不要 Markdown，不要解释，不要代码块。\n"
        "输出必须能被 json.loads 直接解析；不要使用 NaN、Infinity、注释、尾随逗号或单引号。\n"
        "输出格式：{\"claims\":[...],\"context_update\":{...}}。\n"
        "每个 claim 字段：claim_type, subject, claim, values, evidence_text, figures, tables, confidence。\n"
        "claim_type 建议使用 composition, processing, microstructure, property, mechanism, characterization, figure_evidence, comparison, finding。\n"
        "claim 应是完整英文事实句，包含必要限定条件；不要只写短语。values 用字符串数组保留所有关键数值/单位/条件。\n"
        "figures/tables 用字符串数组保留 Figure/Table 编号；没有则 []。\n"
        "evidence_text 必须是 current_chunk 中连续出现的短文本，优先 20-80 个词；不要改写 evidence_text，不要从 previous_context_summary 取 evidence。\n"
        "confidence 只能是 high, medium, low。\n\n"
        "context_update 用自然语言和短列表压缩 current_chunk 对后续 chunk 有帮助的信息；它可以概括当前 chunk，但不能编造。\n"
        "context_update 字段必须包含：summary, material_systems, sample_aliases, processing_route, "
        "key_variables, microstructure, properties, mechanisms, figures_or_tables, unresolved_terms。\n"
        "summary 使用英文，控制在 120-180 words，应说明本 chunk 已经处理过哪些信息，以及后续 chunk 需要记住的样品、工艺、组织、性能和图表线索。\n"
        "其他字段都是字符串数组，未知则填空数组。\n\n"
        f"paper_map_json:\n{json.dumps(paper_map, ensure_ascii=False)}\n\n"
        f"previous_context_summary:\n{previous_context_summary or 'None'}\n\n"
        f"chunk_id: {chunk.chunk_id}\nsection: {chunk.section}\ncurrent_chunk:\n{chunk.text}"
    )


def build_markdown_prompt(
    paper_map: Dict[str, Any],
    synthesis_payload: Dict[str, Any],
    visual_evidence: List[Dict[str, Any]] | None = None,
) -> str:
    visual_evidence = visual_evidence or []
    return (
        "你是材料科学论文知识卡片写作助手。请根据 paper_map、compressed_core_facts 和可选 visual_evidence "
        "生成高信息密度、事实饱满、适合语言模型训练的 Markdown。\n"
        "要求：\n"
        "1. 使用英文 Markdown。\n"
        "2. 重点突出 Processing-Structure-Property Chain，确保工艺变量、组织演化、性能结果和机理之间的因果链清晰可追踪。\n"
        "3. 优先保留高信息密度、高保真的科学事实：材料体系、样品编号、成分、工艺窗口、相/组织、缺陷/析出物、性能数值、图表证据和机理解释。\n"
        "4. 不要编造 core_facts 中没有的数值或结论；如果存在 weak support，只能作为低确定性补充，不能写成确定事实。\n"
        "5. 每个重要结论都应尽量带上样品/工艺/组织/性能限定条件；避免空泛表述，例如 'properties improved' 这类句子必须补充比较对象和证据。\n"
        "6. visual_evidence 不为空时，单独写 Visual Evidence，说明每个 figure 支持了什么事实、趋势或机理；若为空，不要写该章节。\n"
        "7. 使用以下结构组织：Material System, Processing Route and Variables, Microstructure and Phase Evolution, Processing-Structure-Property Chain, Mechanistic Interpretation, Key Quantitative Findings, Visual Evidence。\n"
        "8. 只输出 Markdown 正文，不要代码块包裹，不要解释生成过程。\n\n"
        f"paper_map_json:\n{json.dumps(paper_map, ensure_ascii=False)}\n\n"
        f"compressed_core_facts_json:\n{json.dumps(synthesis_payload, ensure_ascii=False)}\n\n"
        f"visual_evidence_json:\n{json.dumps(visual_evidence, ensure_ascii=False)}\n"
    )


def _build_paper_map_excerpt(markdown_text: str, max_chars: int) -> str:
    headings_and_front = []
    for line in markdown_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#") or (stripped and len("".join(headings_and_front)) < max_chars // 3):
            headings_and_front.append(line)
    front = "\n".join(headings_and_front)
    tail = markdown_text[-max_chars // 4:]
    excerpt = f"{front}\n\n--- tail excerpt ---\n\n{tail}"
    return excerpt[:max_chars]
