# Verify Eval Report: A0

- target_kind: verify_fixed
- paper_score: 89.87
- field_count: 108
- gate_ok: True

## Scoring Formula

- yes=1.0, partial=0.6, unknown=0.3, no=0.0
- field_score = correctness_score * evidence_confidence * 100
- sample_score = sum(field_score * field_weight) / sum(field_weight)
- paper_score = sum(sample_score * sample_weight) / sum(sample_weight)
- if structure gate fails, paper_score = 0

## Samples
- paper_level: 95.20 (52 fields)
- sample_0cu: 65.49 (16 fields)
- sample_3cu: 95.07 (40 fields)

## Field-Level Trace

### paper_level
- F00001 `papers.A0.authors[0]`: score=100.00, judge=yes, conf=1.00, refs=b0003
- F00002 `papers.A0.authors[1]`: score=100.00, judge=yes, conf=1.00, refs=b0003
- F00003 `papers.A0.authors[2]`: score=100.00, judge=yes, conf=1.00, refs=b0003
- F00004 `papers.A0.authors[3]`: score=100.00, judge=yes, conf=1.00, refs=b0003
- F00005 `papers.A0.authors[4]`: score=100.00, judge=yes, conf=1.00, refs=b0003
- F00006 `papers.A0.keywords[0]`: score=100.00, judge=yes, conf=1.00, refs=b0007
- F00007 `papers.A0.keywords[1]`: score=100.00, judge=yes, conf=1.00, refs=b0008
- F00008 `papers.A0.keywords[2]`: score=100.00, judge=yes, conf=1.00, refs=b0009
- F00009 `papers.A0.keywords[3]`: score=100.00, judge=yes, conf=1.00, refs=b0010
- F00010 `papers.A0.keywords[4]`: score=100.00, judge=yes, conf=1.00, refs=b0011
- F00011 `papers.A0.paper_scope`: score=90.00, judge=yes, conf=0.90, refs=b0013,b0015
- F00012 `papers.A0.research_type`: score=100.00, judge=yes, conf=1.00, refs=b0017
- F00013 `papers.A0.title`: score=100.00, judge=yes, conf=1.00, refs=b0001
- F00014 `alloys.alloy_0cu.aliases[0]`: score=100.00, judge=yes, conf=1.00, refs=b0017
- F00015 `alloys.alloy_0cu.alloy_name`: score=100.00, judge=yes, conf=1.00, refs=b0017,b0048
- F00016 `alloys.alloy_0cu.alloying_elements[0]`: score=90.00, judge=yes, conf=0.90, refs=b0017
- F00017 `alloys.alloy_0cu.alloying_elements[1]`: score=90.00, judge=yes, conf=0.90, refs=b0017
- F00018 `alloys.alloy_0cu.alloying_elements[2]`: score=90.00, judge=yes, conf=0.90, refs=b0017
- F00019 `alloys.alloy_0cu.base_element`: score=90.00, judge=yes, conf=0.90, refs=b0017
- F00020 `alloys.alloy_0cu.nominal_composition[al].element`: score=100.00, judge=yes, conf=1.00, refs=b0017
- F00021 `alloys.alloy_0cu.nominal_composition[al].weight_percent`: score=100.00, judge=yes, conf=1.00, refs=b0017
- F00022 `alloys.alloy_0cu.nominal_composition[c].element`: score=100.00, judge=yes, conf=1.00, refs=b0017
- F00023 `alloys.alloy_0cu.nominal_composition[c].weight_percent`: score=100.00, judge=yes, conf=1.00, refs=b0017
- F00024 `alloys.alloy_0cu.nominal_composition[fe].element`: score=100.00, judge=yes, conf=1.00, refs=b0017
- F00025 `alloys.alloy_0cu.nominal_composition[fe].weight_percent`: score=80.00, judge=yes, conf=0.80, refs=b0017
- F00026 `alloys.alloy_0cu.nominal_composition[mn].element`: score=100.00, judge=yes, conf=1.00, refs=b0017
- F00027 `alloys.alloy_0cu.nominal_composition[mn].weight_percent`: score=100.00, judge=yes, conf=1.00, refs=b0017
- F00028 `alloys.alloy_3cu.aliases[0]`: score=100.00, judge=yes, conf=1.00, refs=b0017
- F00029 `alloys.alloy_3cu.alloy_name`: score=100.00, judge=yes, conf=1.00, refs=b0017,b0013
- F00030 `alloys.alloy_3cu.alloying_elements[0]`: score=90.00, judge=yes, conf=0.90, refs=b0017
- F00031 `alloys.alloy_3cu.alloying_elements[1]`: score=90.00, judge=yes, conf=0.90, refs=b0017
- F00032 `alloys.alloy_3cu.alloying_elements[2]`: score=90.00, judge=yes, conf=0.90, refs=b0017
- F00033 `alloys.alloy_3cu.alloying_elements[3]`: score=90.00, judge=yes, conf=0.90, refs=b0017
- F00034 `alloys.alloy_3cu.base_element`: score=90.00, judge=yes, conf=0.90, refs=b0017
- F00035 `alloys.alloy_3cu.nominal_composition[al].element`: score=100.00, judge=yes, conf=1.00, refs=b0017
- F00036 `alloys.alloy_3cu.nominal_composition[al].weight_percent`: score=100.00, judge=yes, conf=1.00, refs=b0017
- F00037 `alloys.alloy_3cu.nominal_composition[c].element`: score=100.00, judge=yes, conf=1.00, refs=b0017
- F00038 `alloys.alloy_3cu.nominal_composition[c].weight_percent`: score=100.00, judge=yes, conf=1.00, refs=b0017
- F00039 `alloys.alloy_3cu.nominal_composition[cu].element`: score=100.00, judge=yes, conf=1.00, refs=b0017
- F00040 `alloys.alloy_3cu.nominal_composition[cu].weight_percent`: score=100.00, judge=yes, conf=1.00, refs=b0017
- F00041 `alloys.alloy_3cu.nominal_composition[fe].element`: score=100.00, judge=yes, conf=1.00, refs=b0017
- F00042 `alloys.alloy_3cu.nominal_composition[fe].weight_percent`: score=80.00, judge=yes, conf=0.80, refs=b0017
- F00043 `alloys.alloy_3cu.nominal_composition[mn].element`: score=100.00, judge=yes, conf=1.00, refs=b0017
- F00044 `alloys.alloy_3cu.nominal_composition[mn].weight_percent`: score=100.00, judge=yes, conf=1.00, refs=b0017
- F00045 `processes.proc_0cu_sol_age.description`: score=100.00, judge=yes, conf=1.00, refs=b0017
- F00046 `processes.proc_3cu_sol_age.description`: score=100.00, judge=yes, conf=1.00, refs=b0017
- F00103 `unmapped_findings.idx_0.value`: score=100.00, judge=yes, conf=1.00, refs=b0048
- F00104 `unmapped_findings.idx_1.value`: score=100.00, judge=yes, conf=1.00, refs=b0047
- F00105 `unmapped_findings.idx_2.value`: score=100.00, judge=yes, conf=1.00, refs=b0048
- F00106 `unmapped_findings.idx_3.value`: score=100.00, judge=yes, conf=1.00, refs=b0015
- F00107 `unmapped_findings.idx_4.value`: score=48.00, judge=partial, conf=0.80, refs=b0019,b0020
- F00108 `unmapped_findings.idx_5.value`: score=30.00, judge=partial, conf=0.50, refs=b0020,b0043,b0047

### sample_0cu
- F00047 `processing_steps.sample_0cu.duration`: score=100.00, judge=yes, conf=1.00, refs=b0017
- F00048 `processing_steps.sample_0cu.method`: score=100.00, judge=yes, conf=1.00, refs=b0017
- F00049 `processing_steps.sample_0cu.sequence`: score=90.00, judge=yes, conf=0.90, refs=b0017
- F00050 `processing_steps.sample_0cu.temperature_with_unit`: score=100.00, judge=yes, conf=1.00, refs=b0017
- F00051 `processing_steps.sample_0cu.type`: score=95.00, judge=yes, conf=0.95, refs=b0017
- F00057 `structures.sample_0cu.microstructure_counts`: score=30.00, judge=partial, conf=0.50, refs=b0048
- F00058 `structures.sample_0cu.microstructure_list[0].phases_present[austenite].crystal_structure`: score=9.00, judge=unknown, conf=0.30, refs=-
- F00059 `structures.sample_0cu.microstructure_list[0].phases_present[austenite].lattice_parameter`: score=100.00, judge=yes, conf=1.00, refs=b0048
- F00060 `structures.sample_0cu.microstructure_list[0].phases_present[austenite].morphology`: score=90.00, judge=yes, conf=0.90, refs=b0013,b0017,b0048
- F00061 `structures.sample_0cu.microstructure_list[0].phases_present[austenite].phase_name`: score=90.00, judge=yes, conf=0.90, refs=b0013,b0017
- F00062 `structures.sample_0cu.microstructure_list[0].phases_present[austenite].volume_fraction`: score=6.00, judge=unknown, conf=0.20, refs=-
- F00063 `structures.sample_0cu.number_of_phases`: score=6.00, judge=unknown, conf=0.20, refs=-
- F00064 `structures.sample_0cu.overall_structure`: score=30.00, judge=partial, conf=0.50, refs=b0017,b0048
- F00093 `characterization_methods.sample_0cu.key_findings`: score=100.00, judge=yes, conf=1.00, refs=b0048
- F00094 `characterization_methods.sample_0cu.purpose`: score=36.00, judge=partial, conf=0.60, refs=b0048
- F00095 `characterization_methods.sample_0cu.technique`: score=100.00, judge=yes, conf=1.00, refs=b0048

### sample_3cu
- F00052 `processing_steps.sample_3cu.duration`: score=100.00, judge=yes, conf=1.00, refs=b0017
- F00053 `processing_steps.sample_3cu.method`: score=100.00, judge=yes, conf=1.00, refs=b0017
- F00054 `processing_steps.sample_3cu.sequence`: score=100.00, judge=yes, conf=1.00, refs=b0017
- F00055 `processing_steps.sample_3cu.temperature_with_unit`: score=100.00, judge=yes, conf=1.00, refs=b0017
- F00056 `processing_steps.sample_3cu.type`: score=100.00, judge=yes, conf=1.00, refs=b0017
- F00065 `structures.sample_3cu.microstructure_counts`: score=90.00, judge=yes, conf=0.90, refs=b0013,b0047
- F00066 `structures.sample_3cu.microstructure_list[0].phases_present[austenite].crystal_structure`: score=80.00, judge=yes, conf=0.80, refs=b0020,b0013
- F00067 `structures.sample_3cu.microstructure_list[0].phases_present[austenite].lattice_parameter`: score=100.00, judge=yes, conf=1.00, refs=b0020
- F00068 `structures.sample_3cu.microstructure_list[0].phases_present[austenite].morphology`: score=80.00, judge=yes, conf=0.80, refs=b0013
- F00069 `structures.sample_3cu.microstructure_list[0].phases_present[austenite].phase_name`: score=100.00, judge=yes, conf=1.00, refs=b0013
- F00070 `structures.sample_3cu.microstructure_list[2].defects[dislocation].dislocation_density`: score=90.00, judge=yes, conf=0.90, refs=b0020
- F00071 `structures.sample_3cu.microstructure_list[2].defects[dislocation].type`: score=90.00, judge=yes, conf=0.90, refs=b0020
- F00072 `structures.sample_3cu.microstructure_list[2].phases_present[carbide].lattice_parameter`: score=100.00, judge=yes, conf=1.00, refs=b0020
- F00073 `structures.sample_3cu.microstructure_list[2].phases_present[carbide].morphology`: score=100.00, judge=yes, conf=1.00, refs=b0047
- F00074 `structures.sample_3cu.microstructure_list[2].phases_present[carbide].phase_name`: score=100.00, judge=yes, conf=1.00, refs=b0013,b0020
- F00075 `structures.sample_3cu.microstructure_list[2].phases_present[cu_rich_phase].crystal_structure`: score=100.00, judge=yes, conf=1.00, refs=b0020
- F00076 `structures.sample_3cu.microstructure_list[2].phases_present[cu_rich_phase].lattice_parameter`: score=100.00, judge=yes, conf=1.00, refs=b0020
- F00077 `structures.sample_3cu.microstructure_list[2].phases_present[cu_rich_phase].morphology`: score=100.00, judge=yes, conf=1.00, refs=b0020
- F00078 `structures.sample_3cu.microstructure_list[2].phases_present[cu_rich_phase].phase_name`: score=100.00, judge=yes, conf=1.00, refs=b0013
- F00079 `structures.sample_3cu.microstructure_list[2].phases_present[cu_rich_phase].plane_spacing_002`: score=100.00, judge=yes, conf=1.00, refs=b0020
- F00080 `structures.sample_3cu.microstructure_list[2].related_sequence`: score=36.00, judge=partial, conf=0.60, refs=b0017,b0047
- F00081 `structures.sample_3cu.number_of_phases`: score=90.00, judge=yes, conf=0.90, refs=b0013,b0020
- F00082 `structures.sample_3cu.overall_structure`: score=90.00, judge=yes, conf=0.90, refs=b0013,b0044
- F00083 `interfaces.sample_3cu.interface_notes[0].stress_strain_distribution`: score=100.00, judge=yes, conf=1.00, refs=b0044
- F00084 `interfaces.sample_3cu.phase_evolution`: score=90.00, judge=yes, conf=0.90, refs=b0047,b0048
- F00085 `interfaces.sample_3cu.phases[austenite].coherence`: score=100.00, judge=yes, conf=1.00, refs=b0019,b0044
- F00086 `interfaces.sample_3cu.phases[austenite].orientation_relationship`: score=100.00, judge=yes, conf=1.00, refs=b0013
- F00087 `interfaces.sample_3cu.phases[austenite].phase_1_name`: score=100.00, judge=yes, conf=1.00, refs=b0013
- F00088 `interfaces.sample_3cu.phases[austenite].phase_2_name`: score=100.00, judge=yes, conf=1.00, refs=b0013
- F00089 `interfaces.sample_3cu.phases[carbide].coherence`: score=100.00, judge=yes, conf=1.00, refs=b0019
- F00090 `interfaces.sample_3cu.phases[carbide].orientation_relationship`: score=100.00, judge=yes, conf=1.00, refs=b0013
- F00091 `interfaces.sample_3cu.phases[carbide].phase_1_name`: score=100.00, judge=yes, conf=1.00, refs=b0013
- F00092 `interfaces.sample_3cu.phases[carbide].phase_2_name`: score=100.00, judge=yes, conf=1.00, refs=b0013
- F00096 `characterization_methods.sample_3cu.key_findings`: score=100.00, judge=yes, conf=1.00, refs=b0047
- F00097 `characterization_methods.sample_3cu.purpose`: score=90.00, judge=yes, conf=0.90, refs=b0047
- F00098 `characterization_methods.sample_3cu.technique`: score=100.00, judge=yes, conf=1.00, refs=b0017,b0043
- F00099 `computational_details.sample_3cu.analytical_model[0].equation_role`: score=90.00, judge=yes, conf=0.90, refs=b0044
- F00100 `computational_details.sample_3cu.analytical_model[0].model_name`: score=100.00, judge=yes, conf=1.00, refs=b0045
- F00101 `computational_details.sample_3cu.analytical_model[0].model_note`: score=100.00, judge=yes, conf=1.00, refs=b0044
- F00102 `computational_details.sample_3cu.analytical_model[0].parameters`: score=100.00, judge=yes, conf=1.00, refs=b0045
