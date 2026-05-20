from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict


DEFAULT_FIELD_RULES: Dict[str, Any] = {
    "id_fields": [
        "paper_id",
        "alloy_id",
        "process_id",
        "sample_id",
        "structure_id",
        "interface_set_id",
        "interface_id",
        "interaction_id",
        "property_set_id",
        "property_id",
        "performance_id",
        "characterization_id",
        "computation_id",
        "uuid",
        "microstructure_uuid",
        "precipitate_id",
    ],
    "anchor_key_priority": [
        "element",
        "direction",
        "region",
        "type",
        "phase_name",
        "phase_1_name",
        "phase_2_name",
        "method",
        "related_sequence",
        "coherence",
    ],
    "text_fields": [
        "papers.title",
        "papers.journal",
        "papers.keywords[*]",
        "alloys.alloy_name",
        "alloys.aliases[*]",
        "alloys.alloys_notes",
        "processes.description",
        "processes.processes_notes",
        "processing_steps.type",
        "processing_steps.method",
        "processing_steps.cooling_medium",
        "processing_steps.processing_steps_notes",
        "structures.overall_structure",
        "structures.microstructure_list[*].phases_present[*].phase_name",
        "structures.microstructure_list[*].phases_present[*].morphology",
        "structures.microstructure_list[*].defects[*].type",
        "structures.microstructure_list[*].grain_structure.texture",
        "interfaces.phases[*].phase_1_name",
        "interfaces.phases[*].phase_2_name",
        "interfaces.defect_interaction[*].interaction_type",
        "interfaces.phase_evolution",
        "properties.mechanical.tensile_properties.youngs_modulus",
        "properties.chemical.corrosion_resistance.passivation_behavior",
        "properties.chemical.oxidation_resistance.protective_scale",
        "performance.application_relevance",
        "characterization_methods.method_name",
        "characterization_methods.purpose",
        "computational_details.method",
        "computational_details.software",
        "unmapped_findings[*]",
    ],
    "numeric_tolerances": {
        "default": {"abs": 0.0, "rel": 0.02},
        "alloys.nominal_composition[*].weight_percent": {"abs": 0.05, "rel": 0.02},
        "alloys.nominal_composition[*].atomic_percent": {"abs": 0.05, "rel": 0.02},
        "processing_steps.temperature": {"abs": 5.0, "rel": 0.0},
        "processing_steps.duration": {"abs": 0.25, "rel": 0.05},
        "properties.*.value": {"abs": 0.1, "rel": 0.03},
        "properties.*.uncertainty": {"abs": 0.1, "rel": 0.05},
    },
    "sample_id_stopwords": [
        "sample",
        "specimen",
        "specimens",
        "test",
        "tests",
        "property",
        "properties",
        "microstructure",
        "mechanical",
        "characterization",
    ],
    "sample_context_stopwords": [
        "tensile",
        "impact",
        "charpy",
        "hardness",
        "fracture",
        "strength",
        "elongation",
        "density",
        "phase",
        "structure",
    ],
    "process_stopwords": [
        "process",
        "condition",
        "sample",
        "steel",
        "alloy",
        "specimen",
    ],
}


@dataclass(frozen=True)
class MatchingSettings:
    alloy_threshold: float = 0.55
    process_threshold: float = 0.50
    loose_section_threshold: float = 0.35
    sample_strong_threshold: float = 0.72
    sample_soft_threshold: float = 0.45
    unique_margin: float = 0.08


@dataclass(frozen=True)
class LLMBridgeSettings:
    enabled: bool = False
    model: str = "deepseek-v4-pro"
    base_url: str = "https://api.deepseek.com"
    api_key: str = "EMPTY"
    temperature: float = 0.0
    max_component_records: int = 12
    prompt_path: str = "evaluation/prompts/sample_bridge_prompt.md"


@dataclass(frozen=True)
class EvaluationSettings:
    truth_dir: str = "dataset/json_truth"
    prediction_root: str = "dataset/output"
    output_path: str = "evaluation/output/evaluation_report.json"
    per_paper_output_dir: str = "evaluation/output/papers"
    field_rules_path: str = "evaluation/config/field_rules.json"
    paper_ids: tuple[str, ...] = ()
    matching: MatchingSettings = field(default_factory=MatchingSettings)
    llm_bridge: LLMBridgeSettings = field(default_factory=LLMBridgeSettings)


def load_evaluation_settings(config_path: str | Path) -> EvaluationSettings:
    path = Path(config_path).expanduser().resolve()
    data = json.loads(path.read_text(encoding="utf-8"))
    return evaluation_settings_from_dict(data, base_dir=path.parent)


def evaluation_settings_from_dict(data: Dict[str, Any], base_dir: Path | None = None) -> EvaluationSettings:
    base_dir = base_dir or Path.cwd()
    matching_data = dict(data.get("matching", {}))
    llm_data = dict(data.get("llm_bridge", {}))
    workflow_model_defaults = _load_workflow_text_model_defaults(base_dir)

    return EvaluationSettings(
        truth_dir=_resolve_path(str(data.get("truth_dir", "dataset/json_truth")), base_dir),
        prediction_root=_resolve_path(str(data.get("prediction_root", "dataset/output")), base_dir),
        output_path=_resolve_path(str(data.get("output_path", "evaluation/output/evaluation_report.json")), base_dir),
        per_paper_output_dir=_resolve_path(
            str(data.get("per_paper_output_dir", "evaluation/output/papers")),
            base_dir,
        ),
        field_rules_path=_resolve_path(
            str(data.get("field_rules_path", "evaluation/config/field_rules.json")),
            base_dir,
        ),
        paper_ids=tuple(str(item) for item in data.get("paper_ids", []) if str(item).strip()),
        matching=MatchingSettings(
            alloy_threshold=float(matching_data.get("alloy_threshold", 0.55)),
            process_threshold=float(matching_data.get("process_threshold", 0.50)),
            loose_section_threshold=float(matching_data.get("loose_section_threshold", 0.35)),
            sample_strong_threshold=float(matching_data.get("sample_strong_threshold", 0.72)),
            sample_soft_threshold=float(matching_data.get("sample_soft_threshold", 0.45)),
            unique_margin=float(matching_data.get("unique_margin", 0.08)),
        ),
        llm_bridge=LLMBridgeSettings(
            enabled=bool(llm_data.get("enabled", False)),
            model=str(
                _prefer_config_or_env(
                    llm_data.get("model"),
                    "EVAL_LLM_MODEL",
                    "DEEPSEEK_MODEL",
                    workflow_model_defaults.get("model", "deepseek-v4-pro"),
                )
            ),
            base_url=str(
                _prefer_config_or_env(
                    llm_data.get("base_url"),
                    "EVAL_LLM_BASE_URL",
                    "DEEPSEEK_BASE_URL",
                    workflow_model_defaults.get("base_url", "https://api.deepseek.com"),
                )
            ),
            api_key=str(
                _prefer_config_or_env(
                    llm_data.get("api_key"),
                    "EVAL_LLM_API_KEY",
                    "DEEPSEEK_API_KEY",
                    workflow_model_defaults.get("api_key", "EMPTY"),
                )
            ),
            temperature=float(llm_data.get("temperature", 0.0)),
            max_component_records=int(llm_data.get("max_component_records", 12)),
            prompt_path=_resolve_path(
                str(llm_data.get("prompt_path", "evaluation/prompts/sample_bridge_prompt.md")),
                base_dir,
            ),
        ),
    )


def dump_evaluation_settings(settings: EvaluationSettings, config_path: str | Path) -> None:
    path = Path(config_path).expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(asdict(settings), ensure_ascii=False, indent=2), encoding="utf-8")


def default_evaluation_settings(project_root: Path) -> EvaluationSettings:
    return EvaluationSettings(
        truth_dir=str((project_root / "dataset" / "json_truth").resolve()),
        prediction_root=str((project_root / "dataset" / "output").resolve()),
        output_path=str((project_root / "evaluation" / "output" / "evaluation_report.json").resolve()),
        per_paper_output_dir=str((project_root / "evaluation" / "output" / "papers").resolve()),
        field_rules_path=str((project_root / "evaluation" / "config" / "field_rules.json").resolve()),
    )


def load_field_rules(path: str | Path) -> Dict[str, Any]:
    rules_path = Path(path).expanduser().resolve()
    if not rules_path.exists():
        return DEFAULT_FIELD_RULES
    data = json.loads(rules_path.read_text(encoding="utf-8"))
    merged = dict(DEFAULT_FIELD_RULES)
    for key, value in data.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = {**merged[key], **value}
        else:
            merged[key] = value
    return merged


def sanitize_settings(settings: EvaluationSettings) -> Dict[str, Any]:
    payload = asdict(settings)
    api_key = payload.get("llm_bridge", {}).get("api_key")
    if api_key and api_key != "EMPTY":
        payload["llm_bridge"]["api_key"] = "***"
    return payload


def _resolve_path(value: str, base_dir: Path) -> str:
    path = Path(value).expanduser()
    if path.is_absolute():
        return str(path.resolve())
    return str((base_dir / path).resolve())


def _prefer_config_or_env(config_value: Any, primary_env: str, secondary_env: str, default: str) -> str:
    if config_value is not None:
        text = str(config_value).strip()
        if text and text.upper() != "EMPTY":
            return text
    return os.getenv(primary_env) or os.getenv(secondary_env) or default


def _load_workflow_text_model_defaults(base_dir: Path) -> Dict[str, str]:
    candidates = [
        base_dir / "workflow.json",
        base_dir.parent / "config" / "workflow.json",
        Path.cwd() / "config" / "workflow.json",
    ]
    for candidate in candidates:
        path = candidate.expanduser().resolve()
        if not path.exists():
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        text_model = data.get("text_model")
        if isinstance(text_model, dict):
            return {
                "model": str(text_model.get("model", "") or ""),
                "base_url": str(text_model.get("base_url", "") or ""),
                "api_key": str(text_model.get("api_key", "") or ""),
            }
    return {}
