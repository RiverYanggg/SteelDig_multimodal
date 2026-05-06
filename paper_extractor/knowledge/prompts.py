import json
from typing import Any, Dict, List

from paper_extractor.knowledge.chunker import Chunk


def build_paper_map_prompt(paper_id: str, markdown_text: str, max_chars: int = 24000) -> str:
    excerpt = _build_paper_map_excerpt(markdown_text, max_chars=max_chars)
    return (
        "你是材料科学论文知识抽取规划助手。请根据论文摘录生成 paper_map JSON，用于后续分块抽取。\n"
        "只输出一个合法 JSON 对象，不要 Markdown，不要解释。\n"
        "paper_map 只应包含全局导航信息，不要展开所有实验细节。\n"
        "字段必须包含：paper_id, title, abstract_summary, research_objective, material_systems, "
        "main_process_variables, sample_aliases, expected_information_axis, key_sections。\n"
        "所有字段值使用字符串、字符串数组或对象；未知填 null 或空数组。\n\n"
        f"paper_id: {paper_id}\n"
        "paper_excerpt:\n"
        f"{excerpt}"
    )


def build_claim_prompt(paper_map: Dict[str, Any], chunk: Chunk) -> str:
    return (
        "你是材料科学论文局部事实抽取助手。你会收到 paper_map 和 current_chunk。\n"
        "paper_map 仅用于理解研究主线、术语和样品别名；claims 必须严格来自 current_chunk。\n"
        "请抽取对训练材料科学语言模型有价值的科学事实，尤其是材料成分、工艺、组织、性能、机理、表征方法、图表证据。\n"
        "不要抽取泛泛背景知识、版权信息、作者单位、参考文献列表。\n"
        "只输出一个合法 JSON 对象，不要 Markdown，不要解释。\n"
        "输出格式：{\"claims\":[...]}。\n"
        "每个 claim 字段：claim_type, subject, claim, values, evidence_text, figures, tables, confidence。\n"
        "evidence_text 必须是 current_chunk 中连续出现的短文本，优先 20-80 个词；不要改写 evidence_text。\n"
        "confidence 只能是 high, medium, low。\n\n"
        f"paper_map_json:\n{json.dumps(paper_map, ensure_ascii=False)}\n\n"
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
        "生成面向语言模型训练的 Markdown。\n"
        "要求：\n"
        "1. 使用英文 Markdown。\n"
        "2. 重点突出 Processing-Structure-Property Chain，确保工艺变量、组织演化、性能结果和机理之间的因果链清晰可追踪。\n"
        "3. 优先保留高信息密度、高保真的科学事实，不要罗列低价值方法学细节。\n"
        "4. 不要编造 core_facts 中没有的数值或结论；如果存在 weak support，只能作为低确定性补充，不能写成确定事实。\n"
        "5. 使用以下结构组织：Material System, Processing-Structure-Property Chain, Mechanistic Interpretation, Key Quantitative Findings, Optional Visual Evidence。\n"
        "6. 如果 visual_evidence 为空，不要写 Visual Evidence 章节。\n"
        "7. 只输出 Markdown 正文，不要代码块包裹。\n\n"
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
