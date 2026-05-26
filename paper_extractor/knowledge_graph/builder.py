import json
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class GraphBuildResult:
    nodes: List[Dict[str, Any]]
    relationships: List[Dict[str, Any]]
    source_papers: List[str]

    def summary(self) -> Dict[str, Any]:
        node_counts = Counter(node["label"] for node in self.nodes)
        relationship_counts = Counter(rel["type"] for rel in self.relationships)
        return {
            "papers": len(self.source_papers),
            "node_count": len(self.nodes),
            "relationship_count": len(self.relationships),
            "node_labels": dict(sorted(node_counts.items())),
            "relationship_types": dict(sorted(relationship_counts.items())),
        }


class KnowledgeGraphBuilder:
    def __init__(self) -> None:
        self._reset()

    def _reset(self) -> None:
        self._nodes: Dict[tuple[str, str], Dict[str, Any]] = {}
        self._relationships: Dict[tuple[str, str, str, str, str], Dict[str, Any]] = {}
        self._source_papers: List[str] = []

    def build_from_dataset(
        self,
        dataset_root: Path,
        paper_ids: Optional[Iterable[str]] = None,
        limit: Optional[int] = None,
    ) -> GraphBuildResult:
        self._reset()
        dataset_root = dataset_root.expanduser().resolve()
        selected_ids = set(paper_ids or [])
        paper_dirs = sorted(path for path in dataset_root.iterdir() if path.is_dir())
        if selected_ids:
            paper_dirs = [path for path in paper_dirs if path.name in selected_ids]
        if limit is not None:
            paper_dirs = paper_dirs[:limit]

        for paper_dir in paper_dirs:
            final_dir = paper_dir / "final"
            text_path = final_dir / "text_extraction.json"
            if not text_path.exists():
                continue
            figure_path = final_dir / "multimodal_figures.json"
            text_data = json.loads(text_path.read_text(encoding="utf-8"))
            figure_data = []
            if figure_path.exists():
                figure_data = json.loads(figure_path.read_text(encoding="utf-8"))
            self._ingest_paper(
                paper_id=paper_dir.name,
                text_data=text_data,
                figure_data=figure_data,
                source_dir=final_dir,
            )

        return GraphBuildResult(
            nodes=list(self._nodes.values()),
            relationships=list(self._relationships.values()),
            source_papers=self._source_papers,
        )

    def _ingest_paper(
        self,
        paper_id: str,
        text_data: Dict[str, Any],
        figure_data: List[Dict[str, Any]],
        source_dir: Path,
    ) -> None:
        self._source_papers.append(paper_id)
        papers = text_data.get("papers", [])
        paper = papers[0] if papers else {"paper_id": paper_id}
        paper_key = paper.get("paper_id") or paper_id
        alloy_key_map: Dict[str, str] = {}
        process_key_map: Dict[str, str] = {}
        sample_key_map: Dict[str, str] = {}
        self._merge_node(
            "Paper",
            paper_key,
            {
                "paper_id": paper_key,
                "title": paper.get("title"),
                "doi": paper.get("doi"),
                "publication_year": paper.get("publication_year"),
                "journal": paper.get("journal"),
                "research_type": paper.get("research_type"),
                "paper_scope": paper.get("paper_scope"),
                "keywords": paper.get("keywords", []),
                "authors": paper.get("authors", []),
                "source_dir": str(source_dir),
            },
        )
        alloy_set_key = f"{paper_key}::alloy_set"
        process_set_key = f"{paper_key}::process_set"
        sample_set_key = f"{paper_key}::sample_set"
        self._merge_node(
            "AlloySet",
            alloy_set_key,
            {
                "alloy_set_id": alloy_set_key,
                "paper_id": paper_key,
            },
        )
        self._merge_node(
            "ProcessSet",
            process_set_key,
            {
                "process_set_id": process_set_key,
                "paper_id": paper_key,
            },
        )
        self._merge_node(
            "SampleSet",
            sample_set_key,
            {
                "sample_set_id": sample_set_key,
                "paper_id": paper_key,
            },
        )
        self._merge_relationship("Paper", paper_key, "HAS_ALLOY_SET", "AlloySet", alloy_set_key, {})
        self._merge_relationship("Paper", paper_key, "HAS_PROCESS_SET", "ProcessSet", process_set_key, {})
        self._merge_relationship("Paper", paper_key, "HAS_SAMPLE_SET", "SampleSet", sample_set_key, {})

        alloys = {item.get("alloy_id"): item for item in text_data.get("alloys", []) if item.get("alloy_id")}
        processes = {item.get("process_id"): item for item in text_data.get("processes", []) if item.get("process_id")}
        samples = {item.get("sample_id"): item for item in text_data.get("samples", []) if item.get("sample_id")}
        structures = {item.get("structure_id"): item for item in text_data.get("structures", []) if item.get("structure_id")}
        property_sets = {
            item.get("property_set_id"): item for item in text_data.get("properties", []) if item.get("property_set_id")
        }
        interfaces = [item for item in text_data.get("interfaces", []) if item.get("interface_set_id")]
        characterizations = [
            item for item in text_data.get("characterization_methods", []) if item.get("characterization_id")
        ]
        computations = [item for item in text_data.get("computational_details", []) if item.get("computation_id")]

        phase_occurrence_lookup: Dict[str, Dict[str, Any]] = {}
        step_records_by_sample: Dict[str, List[Dict[str, Any]]] = {}
        phase_occurrence_keys_by_sample: Dict[str, List[str]] = {}
        characterization_keys_by_sample: Dict[str, List[str]] = {}

        for alloy in alloys.values():
            alloy_key = _paper_scoped_key(paper_key, alloy["alloy_id"])
            alloy_key_map[alloy["alloy_id"]] = alloy_key
            self._merge_node(
                "Alloy",
                alloy_key,
                {
                    "alloy_id": alloy.get("alloy_id"),
                    "paper_id": paper_key,
                    "alloy_name": alloy.get("alloy_name"),
                    "aliases": alloy.get("aliases", []),
                    "base_element": alloy.get("base_element"),
                    "alloying_elements": alloy.get("alloying_elements", []),
                    "nominal_composition_json": _to_json(alloy.get("nominal_composition")),
                    "notes": alloy.get("alloys_notes"),
                },
            )
            self._merge_relationship("Paper", paper_key, "HAS_ALLOY", "Alloy", alloy_key, {})
            self._merge_relationship("AlloySet", alloy_set_key, "HAS_ALLOY_ITEM", "Alloy", alloy_key, {})
            for composition in alloy.get("nominal_composition", []) or []:
                symbol = composition.get("element")
                if not symbol:
                    continue
                self._merge_node("Element", symbol, {"symbol": symbol})
                self._merge_relationship(
                    "Alloy",
                    alloy_key,
                    "CONTAINS_ELEMENT",
                    "Element",
                    symbol,
                    {
                        "weight_percent": composition.get("weight_percent"),
                        "atomic_percent": composition.get("atomic_percent"),
                    },
                )

        for process in processes.values():
            process_key = _paper_scoped_key(paper_key, process["process_id"])
            process_key_map[process["process_id"]] = process_key
            self._merge_node(
                "Process",
                process_key,
                {
                    "process_id": process.get("process_id"),
                    "paper_id": paper_key,
                    "alloy_id": process.get("alloy_id"),
                    "description": process.get("description"),
                    "notes": process.get("processes_notes"),
                },
            )
            self._merge_relationship("Paper", paper_key, "HAS_PROCESS", "Process", process_key, {})
            self._merge_relationship("ProcessSet", process_set_key, "HAS_PROCESS_ITEM", "Process", process_key, {})
            alloy_id = process.get("alloy_id")
            alloy_key = alloy_key_map.get(alloy_id) if alloy_id else None
            if alloy_key:
                self._merge_relationship("Alloy", alloy_key, "HAS_PROCESS", "Process", process_key, {})

        for sample in samples.values():
            sample_key = _paper_scoped_key(paper_key, sample["sample_id"])
            sample_key_map[sample["sample_id"]] = sample_key
            self._merge_node(
                "Sample",
                sample_key,
                {
                    "sample_id": sample.get("sample_id"),
                    "paper_id": paper_key,
                    "alloy_id": sample.get("alloy_id"),
                    "process_id": sample.get("process_id"),
                },
            )
            self._merge_relationship("Paper", paper_key, "HAS_SAMPLE", "Sample", sample_key, {})
            self._merge_relationship("SampleSet", sample_set_key, "HAS_SAMPLE_ITEM", "Sample", sample_key, {})
            alloy_key = alloy_key_map.get(sample.get("alloy_id"))
            process_key = process_key_map.get(sample.get("process_id"))
            if alloy_key:
                self._merge_relationship("Sample", sample_key, "OF_ALLOY", "Alloy", alloy_key, {})
            if process_key:
                self._merge_relationship("Sample", sample_key, "PROCESSED_BY", "Process", process_key, {})

        for step in text_data.get("processing_steps", []):
            sample_id = step.get("sample_id")
            sequence = step.get("sequence")
            if not sample_id or not sequence:
                continue
            sample_key = sample_key_map.get(sample_id)
            if not sample_key:
                continue
            step_key = f"{sample_key}::{sequence}"
            self._merge_node(
                "ProcessingStep",
                step_key,
                {
                    "step_id": step_key,
                    "paper_id": paper_key,
                    "sample_id": sample_id,
                    "sequence": sequence,
                    "type": step.get("type"),
                    "method": step.get("method"),
                    "temperature": step.get("temperature"),
                    "temperature_unit": step.get("unit"),
                    "duration": step.get("duration"),
                    "cooling_medium": step.get("cooling_medium"),
                    "reduction_ratio": step.get("reduction_ratio"),
                    "notes": step.get("processing_steps_notes"),
                },
            )
            step_records_by_sample.setdefault(sample_key, []).append(
                {
                    "step_key": step_key,
                    "sequence": sequence,
                }
            )

        for sample_key, step_records in step_records_by_sample.items():
            step_set_key = f"{sample_key}::processing_step_set"
            ordered_steps = sorted(step_records, key=lambda item: _sequence_sort_key(item["sequence"]))
            self._merge_node(
                "ProcessingStepSet",
                step_set_key,
                {
                    "processing_step_set_id": step_set_key,
                    "paper_id": paper_key,
                    "sample_id": sample_key.split("::", 1)[1],
                    "sequence_count": str(len(ordered_steps)),
                    "sequence_ids": [item["sequence"] for item in ordered_steps],
                },
            )
            self._merge_relationship("Sample", sample_key, "HAS_PROCESSING_STEP_SET", "ProcessingStepSet", step_set_key, {})
            for index, item in enumerate(ordered_steps):
                self._merge_relationship("ProcessingStepSet", step_set_key, "HAS_SEQUENCE_STEP", "ProcessingStep", item["step_key"], {})
                if index > 0:
                    previous = ordered_steps[index - 1]["step_key"]
                    self._merge_relationship("ProcessingStep", previous, "NEXT_STEP", "ProcessingStep", item["step_key"], {})

        for structure in structures.values():
            structure_key = _paper_scoped_key(paper_key, structure["structure_id"])
            sample_id = structure.get("sample_id")
            sample_key = sample_key_map.get(sample_id) if sample_id else None
            self._merge_node(
                "Structure",
                structure_key,
                {
                    "structure_id": structure.get("structure_id"),
                    "sample_id": sample_id,
                    "overall_structure": structure.get("overall_structure"),
                    "number_of_phases": structure.get("number_of_phases"),
                    "microstructure_counts": structure.get("microstructure_counts"),
                },
            )
            if sample_key:
                self._merge_relationship("Sample", sample_key, "HAS_STRUCTURE", "Structure", structure_key, {})

            for micro in structure.get("microstructure_list", []) or []:
                uuid = micro.get("uuid")
                if not uuid:
                    continue
                occurrence_key = f"{sample_key or sample_id}::{uuid}"
                phase_names = []
                morphologies = []
                lattice_parameters = []
                for phase in micro.get("phases_present", []) or []:
                    phase_name = phase.get("phase_name")
                    if phase_name:
                        phase_names.append(phase_name)
                    if phase.get("morphology"):
                        morphologies.append(phase.get("morphology"))
                    if phase.get("lattice_parameter"):
                        lattice_parameters.append(f"{phase_name}: {phase.get('lattice_parameter')}")
                self._merge_node(
                    "PhaseOccurrence",
                    occurrence_key,
                    {
                        "occurrence_id": occurrence_key,
                        "sample_id": sample_id,
                        "structure_id": structure_key,
                        "microstructure_uuid": uuid,
                        "related_sequence": micro.get("related_sequence"),
                        "phase_names": phase_names,
                        "morphologies": morphologies,
                        "lattice_parameters": lattice_parameters,
                        "grain_structure_json": _to_json(micro.get("grain_structure")),
                        "defects_json": _to_json(micro.get("defects")),
                        "precipitates_json": _to_json(micro.get("precipitates")),
                    },
                )
                phase_occurrence_lookup[uuid] = {
                    "node_key": occurrence_key,
                    "sample_id": sample_id,
                    "phase_names": phase_names,
                }
                self._merge_relationship("Structure", structure_key, "HAS_PHASE_OCCURRENCE", "PhaseOccurrence", occurrence_key, {})
                if sample_key:
                    phase_occurrence_keys_by_sample.setdefault(sample_key, []).append(occurrence_key)
                if micro.get("related_sequence"):
                    step_key = f"{sample_key}::{micro.get('related_sequence')}"
                    self._merge_relationship("PhaseOccurrence", occurrence_key, "EMERGED_AFTER", "ProcessingStep", step_key, {})

                for phase in micro.get("phases_present", []) or []:
                    phase_name = phase.get("phase_name")
                    if not phase_name:
                        continue
                    phase_key = _slugify(phase_name)
                    self._merge_node(
                        "Phase",
                        phase_key,
                        {
                            "phase_key": phase_key,
                            "name": phase_name,
                            "crystal_structure": phase.get("crystal_structure"),
                        },
                    )
                    self._merge_relationship("PhaseOccurrence", occurrence_key, "INSTANTIATES", "Phase", phase_key, {})

        for sample_key, occurrence_keys in phase_occurrence_keys_by_sample.items():
            phase_set_key = f"{sample_key}::phase_occurrence_set"
            self._merge_node(
                "PhaseOccurrenceSet",
                phase_set_key,
                {
                    "phase_occurrence_set_id": phase_set_key,
                    "paper_id": paper_key,
                    "sample_id": sample_key.split("::", 1)[1],
                    "phase_occurrence_count": str(len(occurrence_keys)),
                },
            )
            self._merge_relationship("Sample", sample_key, "HAS_PHASE_OCCURRENCE_SET", "PhaseOccurrenceSet", phase_set_key, {})
            for occurrence_key in sorted(set(occurrence_keys)):
                self._merge_relationship("PhaseOccurrenceSet", phase_set_key, "HAS_PHASE_OCCURRENCE_ITEM", "PhaseOccurrence", occurrence_key, {})

        for interface_set in interfaces:
            sample_id = interface_set.get("sample_id")
            sample_key = sample_key_map.get(sample_id) if sample_id else None
            interface_set_key = _paper_scoped_key(paper_key, interface_set["interface_set_id"])
            self._merge_node(
                "InterfaceSet",
                interface_set_key,
                {
                    "interface_set_id": interface_set.get("interface_set_id"),
                    "sample_id": sample_id,
                    "phase_evolution": interface_set.get("phase_evolution"),
                    "interface_notes_json": _to_json(interface_set.get("interface_notes")),
                },
            )
            if sample_key:
                self._merge_relationship("Sample", sample_key, "HAS_INTERFACE_SET", "InterfaceSet", interface_set_key, {})

            for interface in interface_set.get("phases", []) or []:
                interface_key = f"{sample_key or sample_id}::{interface.get('interface_id')}"
                phase_1_name = interface.get("phase_1_name")
                phase_2_name = interface.get("phase_2_name")
                self._merge_node(
                    "Interface",
                    interface_key,
                    {
                        "interface_id": interface_key,
                        "sample_id": sample_id,
                        "coherence": interface.get("coherence"),
                        "orientation_relationship": interface.get("orientation_relationship"),
                        "phase_1_name": phase_1_name,
                        "phase_2_name": phase_2_name,
                    },
                )
                self._merge_relationship("InterfaceSet", interface_set_key, "HAS_INTERFACE", "Interface", interface_key, {})
                for phase_name in [phase_1_name, phase_2_name]:
                    if not phase_name:
                        continue
                    phase_key = _slugify(phase_name)
                    self._merge_node("Phase", phase_key, {"phase_key": phase_key, "name": phase_name})
                    self._merge_relationship("Interface", interface_key, "BETWEEN_PHASE", "Phase", phase_key, {})

        for prop_set in property_sets.values():
            sample_id = prop_set.get("sample_id")
            sample_key = sample_key_map.get(sample_id) if sample_id else None
            prop_key = _paper_scoped_key(paper_key, prop_set["property_set_id"])
            self._merge_node(
                "PropertySet",
                prop_key,
                {
                    "property_set_id": prop_set.get("property_set_id"),
                    "sample_id": sample_id,
                    "mechanical_json": _to_json(prop_set.get("mechanical")),
                    "physical_json": _to_json(prop_set.get("physical")),
                    "chemical_json": _to_json(prop_set.get("chemical")),
                    "radiation_json": _to_json(prop_set.get("radiation_properties")),
                },
            )
            if sample_key:
                self._merge_relationship("Sample", sample_key, "HAS_PROPERTY_SET", "PropertySet", prop_key, {})
            self._add_property_measurements(prop_key, prop_set)

        for characterization in characterizations:
            char_key = _paper_scoped_key(paper_key, characterization["characterization_id"])
            sample_id = characterization.get("sample_id")
            sample_key = sample_key_map.get(sample_id) if sample_id else None
            technique = characterization.get("technique")
            technique_key = _slugify(technique) if technique else None
            self._merge_node(
                "Characterization",
                char_key,
                {
                    "characterization_id": characterization.get("characterization_id"),
                    "sample_id": sample_id,
                    "microstructure_uuid": characterization.get("microstructure_uuid"),
                    "technique": technique,
                    "purpose": characterization.get("purpose"),
                    "key_findings": characterization.get("key_findings"),
                },
            )
            if sample_key:
                characterization_keys_by_sample.setdefault(sample_key, []).append(char_key)
            if technique_key:
                self._merge_node("Technique", technique_key, {"technique_key": technique_key, "name": technique})
                self._merge_relationship("Characterization", char_key, "USES_TECHNIQUE", "Technique", technique_key, {})
            micro_uuid = characterization.get("microstructure_uuid")
            if micro_uuid and micro_uuid in phase_occurrence_lookup:
                self._merge_relationship(
                    "Characterization",
                    char_key,
                    "OBSERVED",
                    "PhaseOccurrence",
                    phase_occurrence_lookup[micro_uuid]["node_key"],
                    {},
                )

        for sample_key, char_keys in characterization_keys_by_sample.items():
            char_set_key = f"{sample_key}::characterization_set"
            self._merge_node(
                "CharacterizationSet",
                char_set_key,
                {
                    "characterization_set_id": char_set_key,
                    "paper_id": paper_key,
                    "sample_id": sample_key.split("::", 1)[1],
                    "characterization_count": str(len(char_keys)),
                },
            )
            self._merge_relationship("Sample", sample_key, "HAS_CHARACTERIZATION_SET", "CharacterizationSet", char_set_key, {})
            for char_key in sorted(set(char_keys)):
                self._merge_relationship("CharacterizationSet", char_set_key, "HAS_CHARACTERIZATION", "Characterization", char_key, {})

        for computation in computations:
            comp_key = _paper_scoped_key(paper_key, computation["computation_id"])
            sample_id = computation.get("sample_id")
            sample_key = sample_key_map.get(sample_id) if sample_id else None
            self._merge_node(
                "Computation",
                comp_key,
                {
                    "computation_id": computation.get("computation_id"),
                    "sample_id": sample_id,
                    "simulation_method": computation.get("simulation_method"),
                    "software_used": computation.get("software_used"),
                    "potential_model": computation.get("potential_model"),
                    "validation_against_experiment": computation.get("validation_against_experiment"),
                    "analytical_model_json": _to_json(computation.get("analytical_model")),
                },
            )
            if sample_key:
                self._merge_relationship("Sample", sample_key, "HAS_COMPUTATION", "Computation", comp_key, {})

        findings_by_text: Dict[str, str] = {}
        for idx, finding_text in enumerate(text_data.get("unmapped_findings", []) or [], start=1):
            finding_key = f"{paper_key}::finding::{idx:03d}"
            findings_by_text[finding_text] = finding_key
            self._merge_node(
                "Finding",
                finding_key,
                {
                    "finding_id": finding_key,
                    "paper_id": paper_key,
                    "text": finding_text,
                    "source_type": "unmapped_finding",
                },
            )
            self._link_finding_mentions(
                finding_key,
                finding_text,
                samples,
                phase_occurrence_lookup,
                alloys,
                sample_key_map,
            )

        if findings_by_text:
            finding_set_key = f"{paper_key}::finding_set"
            self._merge_node(
                "FindingSet",
                finding_set_key,
                {
                    "finding_set_id": finding_set_key,
                    "paper_id": paper_key,
                    "finding_count": str(len(findings_by_text)),
                },
            )
            self._merge_relationship("Paper", paper_key, "HAS_FINDING_SET", "FindingSet", finding_set_key, {})
            for finding_key in sorted(findings_by_text.values()):
                self._merge_relationship("FindingSet", finding_set_key, "HAS_FINDING_ITEM", "Finding", finding_key, {})

        for interface_set in interfaces:
            text = interface_set.get("phase_evolution")
            if not text:
                continue
            finding_key = f"{paper_key}::phase_evolution::{interface_set['interface_set_id']}"
            self._merge_node(
                "Finding",
                finding_key,
                {
                    "finding_id": finding_key,
                    "paper_id": paper_key,
                    "text": text,
                    "source_type": "phase_evolution",
                },
            )
            sample_id = interface_set.get("sample_id")
            sample_key = sample_key_map.get(sample_id) if sample_id else None
            self._link_finding_mentions(
                finding_key,
                text,
                samples,
                phase_occurrence_lookup,
                alloys,
                sample_key_map,
            )

        for figure in figure_data:
            raw_figure_key = figure.get("figure_id")
            if not raw_figure_key:
                continue
            figure_key = _paper_scoped_key(paper_key, raw_figure_key)
            self._merge_node(
                "Figure",
                figure_key,
                {
                    "figure_id": raw_figure_key,
                    "paper_id": paper_key,
                    "image_type": figure.get("image_type"),
                    "image_count": _stringify(figure.get("image_count")),
                    "image_paths": figure.get("image_paths", []),
                    "description": figure.get("description"),
                    "confidence": _stringify(figure.get("confidence")),
                },
            )
            description = figure.get("description") or ""
            for finding_text, finding_key in findings_by_text.items():
                if _text_overlap(description, finding_text):
                    self._merge_relationship("Figure", figure_key, "SUPPORTS", "Finding", finding_key, {})

            figure_finding_key = f"{paper_key}::figure_summary::{figure_key}"
            self._merge_node(
                "Finding",
                figure_finding_key,
                {
                    "finding_id": figure_finding_key,
                    "paper_id": paper_key,
                    "text": description,
                    "source_type": "multimodal_figure_summary",
                },
            )
            self._merge_relationship("Figure", figure_key, "SUMMARIZED_AS", "Finding", figure_finding_key, {})
            self._link_finding_mentions(
                figure_finding_key,
                description,
                samples,
                phase_occurrence_lookup,
                alloys,
                sample_key_map,
            )

        if figure_data:
            figure_set_key = f"{paper_key}::figure_set"
            self._merge_node(
                "FigureSet",
                figure_set_key,
                {
                    "figure_set_id": figure_set_key,
                    "paper_id": paper_key,
                    "figure_count": str(len([figure for figure in figure_data if figure.get('figure_id')])),
                },
            )
            self._merge_relationship("Paper", paper_key, "HAS_FIGURE_SET", "FigureSet", figure_set_key, {})
            for figure in figure_data:
                raw_figure_key = figure.get("figure_id")
                if not raw_figure_key:
                    continue
                figure_key = _paper_scoped_key(paper_key, raw_figure_key)
                self._merge_relationship("FigureSet", figure_set_key, "HAS_FIGURE_ITEM", "Figure", figure_key, {})

    def _add_property_measurements(self, prop_key: str, prop_set: Dict[str, Any]) -> None:
        mechanical = (prop_set.get("mechanical") or {}).get("tensile_properties") or {}
        measurement_groups = [
            ("yield_strength", mechanical.get("yield_strength", [])),
            ("ultimate_tensile_strength", mechanical.get("ultimate_tensile_strength", [])),
            ("elongation", mechanical.get("elongation", [])),
            ("strain_hardening_rate", mechanical.get("strain_hardening_rate", [])),
            ("hardness", (prop_set.get("mechanical") or {}).get("hardness", [])),
        ]
        for metric_name, items in measurement_groups:
            for index, item in enumerate(items or [], start=1):
                metric_key = f"{prop_key}::{metric_name}::{index:03d}"
                self._merge_node(
                    "PropertyMeasurement",
                    metric_key,
                    {
                        "measurement_id": metric_key,
                        "property_type": metric_name,
                        "direction": item.get("direction"),
                        "region": item.get("region"),
                        "value": item.get("value"),
                        "unit": item.get("unit"),
                        "scale": item.get("scale"),
                        "uncertainty": (item.get("others") or {}).get("uncertainty"),
                    },
                )
                self._merge_relationship("PropertySet", prop_key, "HAS_MEASUREMENT", "PropertyMeasurement", metric_key, {})

    def _link_finding_mentions(
        self,
        finding_key: str,
        text: str,
        samples: Dict[str, Dict[str, Any]],
        phase_occurrences: Dict[str, Dict[str, Any]],
        alloys: Dict[str, Dict[str, Any]],
        sample_key_map: Dict[str, str],
    ) -> None:
        if not text:
            return
        lowered = text.lower()

        for phase_occurrence in phase_occurrences.values():
            phase_names = phase_occurrence.get("phase_names", [])
            if any(phase_name and phase_name.lower() in lowered for phase_name in phase_names):
                self._merge_relationship(
                    "Finding",
                    finding_key,
                    "INVOLVES",
                    "PhaseOccurrence",
                    phase_occurrence["node_key"],
                    {},
                )

        element_mentions = {symbol for symbol in ["Fe", "Mn", "Al", "C", "Cu", "Ni", "Cr", "Si"] if _mentions_element(text, symbol)}
        for symbol in sorted(element_mentions):
            self._merge_node("Element", symbol, {"symbol": symbol})
            self._merge_relationship("Finding", finding_key, "INVOLVES_ELEMENT", "Element", symbol, {})

    def _merge_node(self, label: str, key: str, properties: Dict[str, Any]) -> None:
        node_key = (label, key)
        cleaned = {k: v for k, v in properties.items() if v not in (None, [], "")}
        cleaned["node_key"] = key
        cleaned["label"] = label
        if node_key in self._nodes:
            self._nodes[node_key]["properties"].update(cleaned)
            return
        self._nodes[node_key] = {"label": label, "key": key, "properties": cleaned}

    def _merge_relationship(
        self,
        start_label: str,
        start_key: str,
        rel_type: str,
        end_label: str,
        end_key: str,
        properties: Dict[str, Any],
    ) -> None:
        rel_key = (start_label, start_key, rel_type, end_label, end_key)
        cleaned = {k: v for k, v in properties.items() if v not in (None, [], "")}
        if rel_key in self._relationships:
            self._relationships[rel_key]["properties"].update(cleaned)
            return
        self._relationships[rel_key] = {
            "start_label": start_label,
            "start_key": start_key,
            "type": rel_type,
            "end_label": end_label,
            "end_key": end_key,
            "properties": cleaned,
        }


def _slugify(text: Optional[str]) -> str:
    if not text:
        return "unknown"
    value = text.lower()
    value = value.replace("κ", "kappa").replace("γ", "gamma")
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_") or "unknown"


def _to_json(value: Any) -> Optional[str]:
    if value in (None, [], {}):
        return None
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def _stringify(value: Any) -> Optional[str]:
    if value is None:
        return None
    return str(value)


def _text_overlap(text_a: str, text_b: str) -> bool:
    if not text_a or not text_b:
        return False
    tokens_a = set(_tokenize(text_a))
    tokens_b = set(_tokenize(text_b))
    if not tokens_a or not tokens_b:
        return False
    overlap = len(tokens_a & tokens_b)
    return overlap >= min(4, max(2, min(len(tokens_a), len(tokens_b)) // 4))


def _tokenize(text: str) -> List[str]:
    return re.findall(r"[a-zA-Z0-9_+\-]+", text.lower())


def _mentions_element(text: str, symbol: str) -> bool:
    if not text or not symbol:
        return False
    if symbol == "C":
        patterns = [
            r"\bfe[- ]?\d+mn[- ]?\d+al[- ]?\d+c\b",
            r"\bfe[- ]?\d+mn[- ]?\d+al[- ]?\d+c[- ]?\d+cu\b",
            r"\bfe[- ]?mn[- ]?al[- ]?c\b",
            r"\bcu-rich\b",
        ]
        return any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in patterns)
    boundary_pattern = rf"(?<![A-Za-z]){re.escape(symbol)}(?![a-z])"
    return re.search(boundary_pattern, text) is not None


def _paper_scoped_key(paper_id: str, local_id: str) -> str:
    return f"{paper_id}::{local_id}"


def _sequence_sort_key(sequence: Optional[str]) -> tuple[int, tuple[Any, ...], str]:
    if not sequence:
        return (1, (), "")
    parts = re.split(r"([0-9]+)", sequence)
    normalized: List[Any] = []
    for part in parts:
        if not part:
            continue
        if part.isdigit():
            normalized.append(int(part))
        else:
            normalized.append(part.lower())
    return (0, tuple(normalized), sequence)
