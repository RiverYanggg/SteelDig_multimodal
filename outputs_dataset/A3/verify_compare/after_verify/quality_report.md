# Verify Eval Report: A3

- target_kind: verify_fixed
- paper_score: 94.13
- field_count: 262
- gate_ok: True

## Scoring Formula

- yes=1.0, partial=0.6, unknown=0.3, no=0.0
- field_score = correctness_score * evidence_confidence * 100
- sample_score = sum(field_score * field_weight) / sum(field_weight)
- paper_score = sum(sample_score * sample_weight) / sum(sample_weight)
- if structure gate fails, paper_score = 0

## Samples
- paper_level: 95.72 (104 fields)
- sample_28mn0ni_hr: 96.67 (6 fields)
- sample_28mn0ni_hr_cr: 79.52 (31 fields)
- sample_28mn0ni_hr_cr_973: 92.08 (50 fields)
- sample_15mn5ni_hr_cr_1023: 100.00 (9 fields)
- sample_15mn5ni_hr_cr: 100.00 (8 fields)
- sample_15mn5ni_hr_cr_1173: 100.00 (9 fields)
- sample_28mn0ni_hr_cr_1023: 100.00 (6 fields)
- sample_28mn0ni_hr_cr_1173: 100.00 (9 fields)
- sample_28mn5ni_hr_cr: 100.00 (8 fields)
- sample_28mn5ni_hr_cr_1023: 100.00 (5 fields)
- sample_28mn5ni_hr_cr_1173: 100.00 (9 fields)
- sample_28mn5ni_hr_cr_973: 100.00 (8 fields)

## Field-Level Trace

### paper_level
- F00001 `papers.A3.authors[0]`: score=100.00, judge=yes, conf=1.00, refs=b0003
- F00002 `papers.A3.authors[1]`: score=100.00, judge=yes, conf=1.00, refs=b0003
- F00003 `papers.A3.authors[2]`: score=100.00, judge=yes, conf=1.00, refs=b0003
- F00004 `papers.A3.authors[3]`: score=100.00, judge=yes, conf=1.00, refs=b0003
- F00005 `papers.A3.authors[4]`: score=100.00, judge=yes, conf=1.00, refs=b0003
- F00006 `papers.A3.authors[5]`: score=100.00, judge=yes, conf=1.00, refs=b0003
- F00007 `papers.A3.authors[6]`: score=100.00, judge=yes, conf=1.00, refs=b0003
- F00008 `papers.A3.keywords[0]`: score=100.00, judge=yes, conf=1.00, refs=b0007
- F00009 `papers.A3.keywords[1]`: score=100.00, judge=yes, conf=1.00, refs=b0008
- F00010 `papers.A3.keywords[2]`: score=100.00, judge=yes, conf=1.00, refs=b0009
- F00011 `papers.A3.keywords[3]`: score=100.00, judge=yes, conf=1.00, refs=b0010
- F00012 `papers.A3.keywords[4]`: score=100.00, judge=yes, conf=1.00, refs=b0011
- F00013 `papers.A3.paper_scope`: score=95.00, judge=yes, conf=0.95, refs=b0013
- F00014 `papers.A3.research_type`: score=90.00, judge=yes, conf=0.90, refs=b0013,b0021
- F00015 `papers.A3.title`: score=100.00, judge=yes, conf=1.00, refs=b0001
- F00016 `alloys.alloy_15mn5ni.aliases[0]`: score=100.00, judge=yes, conf=1.00, refs=b0018
- F00017 `alloys.alloy_15mn5ni.aliases[1]`: score=100.00, judge=yes, conf=1.00, refs=b0013
- F00018 `alloys.alloy_15mn5ni.alloy_name`: score=100.00, judge=yes, conf=1.00, refs=b0018
- F00019 `alloys.alloy_15mn5ni.alloying_elements[0]`: score=100.00, judge=yes, conf=1.00, refs=b0023
- F00020 `alloys.alloy_15mn5ni.alloying_elements[1]`: score=100.00, judge=yes, conf=1.00, refs=b0023
- F00021 `alloys.alloy_15mn5ni.alloying_elements[2]`: score=100.00, judge=yes, conf=1.00, refs=b0023
- F00022 `alloys.alloy_15mn5ni.alloying_elements[3]`: score=100.00, judge=yes, conf=1.00, refs=b0023
- F00023 `alloys.alloy_15mn5ni.alloys_notes`: score=70.00, judge=yes, conf=0.70, refs=b0018
- F00024 `alloys.alloy_15mn5ni.base_element`: score=100.00, judge=yes, conf=1.00, refs=b0023
- F00025 `alloys.alloy_15mn5ni.nominal_composition[al].element`: score=100.00, judge=yes, conf=1.00, refs=b0023
- F00026 `alloys.alloy_15mn5ni.nominal_composition[al].weight_percent`: score=100.00, judge=yes, conf=1.00, refs=b0023
- F00027 `alloys.alloy_15mn5ni.nominal_composition[c].element`: score=100.00, judge=yes, conf=1.00, refs=b0023
- F00028 `alloys.alloy_15mn5ni.nominal_composition[c].weight_percent`: score=100.00, judge=yes, conf=1.00, refs=b0023
- F00029 `alloys.alloy_15mn5ni.nominal_composition[fe].element`: score=100.00, judge=yes, conf=1.00, refs=b0023
- F00030 `alloys.alloy_15mn5ni.nominal_composition[fe].weight_percent`: score=100.00, judge=yes, conf=1.00, refs=b0023
- F00031 `alloys.alloy_15mn5ni.nominal_composition[mn].element`: score=100.00, judge=yes, conf=1.00, refs=b0023
- F00032 `alloys.alloy_15mn5ni.nominal_composition[mn].weight_percent`: score=100.00, judge=yes, conf=1.00, refs=b0023
- F00033 `alloys.alloy_15mn5ni.nominal_composition[ni].element`: score=100.00, judge=yes, conf=1.00, refs=b0023
- F00034 `alloys.alloy_15mn5ni.nominal_composition[ni].weight_percent`: score=100.00, judge=yes, conf=1.00, refs=b0023
- F00035 `alloys.alloy_28mn0ni.aliases[0]`: score=100.00, judge=yes, conf=1.00, refs=b0018
- F00036 `alloys.alloy_28mn0ni.aliases[1]`: score=100.00, judge=yes, conf=1.00, refs=b0013
- F00037 `alloys.alloy_28mn0ni.alloy_name`: score=100.00, judge=yes, conf=1.00, refs=b0018
- F00038 `alloys.alloy_28mn0ni.alloying_elements[0]`: score=100.00, judge=yes, conf=1.00, refs=b0023
- F00039 `alloys.alloy_28mn0ni.alloying_elements[1]`: score=100.00, judge=yes, conf=1.00, refs=b0023
- F00040 `alloys.alloy_28mn0ni.alloying_elements[2]`: score=100.00, judge=yes, conf=1.00, refs=b0023
- F00041 `alloys.alloy_28mn0ni.alloys_notes`: score=90.00, judge=yes, conf=0.90, refs=b0013
- F00042 `alloys.alloy_28mn0ni.base_element`: score=100.00, judge=yes, conf=1.00, refs=b0023
- F00043 `alloys.alloy_28mn0ni.nominal_composition[al].element`: score=100.00, judge=yes, conf=1.00, refs=b0023
- F00044 `alloys.alloy_28mn0ni.nominal_composition[al].weight_percent`: score=100.00, judge=yes, conf=1.00, refs=b0023
- F00045 `alloys.alloy_28mn0ni.nominal_composition[c].element`: score=100.00, judge=yes, conf=1.00, refs=b0023
- F00046 `alloys.alloy_28mn0ni.nominal_composition[c].weight_percent`: score=100.00, judge=yes, conf=1.00, refs=b0023
- F00047 `alloys.alloy_28mn0ni.nominal_composition[fe].element`: score=100.00, judge=yes, conf=1.00, refs=b0023
- F00048 `alloys.alloy_28mn0ni.nominal_composition[fe].weight_percent`: score=100.00, judge=yes, conf=1.00, refs=b0023
- F00049 `alloys.alloy_28mn0ni.nominal_composition[mn].element`: score=100.00, judge=yes, conf=1.00, refs=b0023
- F00050 `alloys.alloy_28mn0ni.nominal_composition[mn].weight_percent`: score=100.00, judge=yes, conf=1.00, refs=b0023
- F00051 `alloys.alloy_28mn5ni.aliases[0]`: score=100.00, judge=yes, conf=1.00, refs=b0018
- F00052 `alloys.alloy_28mn5ni.aliases[1]`: score=100.00, judge=yes, conf=1.00, refs=b0013
- F00053 `alloys.alloy_28mn5ni.alloy_name`: score=100.00, judge=yes, conf=1.00, refs=b0018
- F00054 `alloys.alloy_28mn5ni.alloying_elements[0]`: score=100.00, judge=yes, conf=1.00, refs=b0023
- F00055 `alloys.alloy_28mn5ni.alloying_elements[1]`: score=100.00, judge=yes, conf=1.00, refs=b0023
- F00056 `alloys.alloy_28mn5ni.alloying_elements[2]`: score=100.00, judge=yes, conf=1.00, refs=b0023
- F00057 `alloys.alloy_28mn5ni.alloying_elements[3]`: score=100.00, judge=yes, conf=1.00, refs=b0023
- F00058 `alloys.alloy_28mn5ni.alloys_notes`: score=70.00, judge=yes, conf=0.70, refs=b0018,b0023
- F00059 `alloys.alloy_28mn5ni.base_element`: score=100.00, judge=yes, conf=1.00, refs=b0023
- F00060 `alloys.alloy_28mn5ni.nominal_composition[al].element`: score=100.00, judge=yes, conf=1.00, refs=b0023
- F00061 `alloys.alloy_28mn5ni.nominal_composition[al].weight_percent`: score=100.00, judge=yes, conf=1.00, refs=b0023
- F00062 `alloys.alloy_28mn5ni.nominal_composition[c].element`: score=100.00, judge=yes, conf=1.00, refs=b0023
- F00063 `alloys.alloy_28mn5ni.nominal_composition[c].weight_percent`: score=100.00, judge=yes, conf=1.00, refs=b0023
- F00064 `alloys.alloy_28mn5ni.nominal_composition[fe].element`: score=100.00, judge=yes, conf=1.00, refs=b0023
- F00065 `alloys.alloy_28mn5ni.nominal_composition[fe].weight_percent`: score=100.00, judge=yes, conf=1.00, refs=b0023
- F00066 `alloys.alloy_28mn5ni.nominal_composition[mn].element`: score=100.00, judge=yes, conf=1.00, refs=b0023
- F00067 `alloys.alloy_28mn5ni.nominal_composition[mn].weight_percent`: score=100.00, judge=yes, conf=1.00, refs=b0023
- F00068 `alloys.alloy_28mn5ni.nominal_composition[ni].element`: score=100.00, judge=yes, conf=1.00, refs=b0023
- F00069 `alloys.alloy_28mn5ni.nominal_composition[ni].weight_percent`: score=100.00, judge=yes, conf=1.00, refs=b0023
- F00070 `processes.proc_15mn5ni_hr.description`: score=90.00, judge=yes, conf=0.90, refs=b0021
- F00071 `processes.proc_15mn5ni_hr.processes_notes`: score=95.00, judge=yes, conf=0.95, refs=b0032
- F00072 `processes.proc_15mn5ni_hr_cr.description`: score=90.00, judge=yes, conf=0.90, refs=b0021
- F00073 `processes.proc_15mn5ni_hr_cr.processes_notes`: score=100.00, judge=yes, conf=1.00, refs=b0021
- F00074 `processes.proc_15mn5ni_hr_cr_1023.description`: score=85.00, judge=yes, conf=0.85, refs=b0021,b0138
- F00075 `processes.proc_15mn5ni_hr_cr_1073.description`: score=85.00, judge=yes, conf=0.85, refs=b0021,b0138
- F00076 `processes.proc_15mn5ni_hr_cr_1173.description`: score=85.00, judge=yes, conf=0.85, refs=b0021,b0138
- F00077 `processes.proc_15mn5ni_hr_cr_1273.description`: score=85.00, judge=yes, conf=0.85, refs=b0021,b0121
- F00078 `processes.proc_15mn5ni_hr_cr_873.description`: score=85.00, judge=yes, conf=0.85, refs=b0021,b0121
- F00079 `processes.proc_15mn5ni_hr_cr_973.description`: score=85.00, judge=yes, conf=0.85, refs=b0021,b0138
- F00080 `processes.proc_28mn0ni_hr.description`: score=90.00, judge=yes, conf=0.90, refs=b0021

### sample_28mn0ni_hr
- F00100 `processing_steps.sample_28mn0ni_hr.duration`: score=100.00, judge=yes, conf=1.00, refs=b0021
- F00101 `processing_steps.sample_28mn0ni_hr.method`: score=100.00, judge=yes, conf=1.00, refs=b0021
- F00102 `processing_steps.sample_28mn0ni_hr.processing_steps_notes`: score=100.00, judge=yes, conf=1.00, refs=b0021
- F00103 `processing_steps.sample_28mn0ni_hr.sequence`: score=90.00, judge=yes, conf=0.90, refs=b0021
- F00104 `processing_steps.sample_28mn0ni_hr.temperature_with_unit`: score=100.00, judge=yes, conf=1.00, refs=b0021
- F00105 `processing_steps.sample_28mn0ni_hr.type`: score=90.00, judge=yes, conf=0.90, refs=b0021

### sample_28mn0ni_hr_cr
- F00106 `processing_steps.sample_28mn0ni_hr_cr.duration`: score=100.00, judge=yes, conf=1.00, refs=b0021
- F00107 `processing_steps.sample_28mn0ni_hr_cr.method`: score=100.00, judge=yes, conf=1.00, refs=b0021,b0013
- F00108 `processing_steps.sample_28mn0ni_hr_cr.processing_steps_notes`: score=100.00, judge=yes, conf=1.00, refs=b0021
- F00109 `processing_steps.sample_28mn0ni_hr_cr.reduction_ratio`: score=100.00, judge=yes, conf=1.00, refs=b0021,b0013
- F00110 `processing_steps.sample_28mn0ni_hr_cr.sequence`: score=90.00, judge=yes, conf=0.90, refs=b0021
- F00111 `processing_steps.sample_28mn0ni_hr_cr.temperature_with_unit`: score=48.00, judge=partial, conf=0.80, refs=b0013,b0021
- F00112 `processing_steps.sample_28mn0ni_hr_cr.type`: score=100.00, judge=yes, conf=1.00, refs=b0021,b0013
- F00120 `structures.sample_28mn0ni_hr_cr.microstructure_list[3].defects[planar_slip_bands].dislocation_density`: score=36.00, judge=partial, conf=0.60, refs=b0152
- F00121 `structures.sample_28mn0ni_hr_cr.microstructure_list[3].defects[planar_slip_bands].type`: score=100.00, judge=yes, conf=1.00, refs=b0033
- F00122 `structures.sample_28mn0ni_hr_cr.microstructure_list[3].grain_structure.average_grain_size.value_with_unit`: score=0.00, judge=unknown, conf=0.00, refs=-
- F00123 `structures.sample_28mn0ni_hr_cr.microstructure_list[3].grain_structure.texture`: score=0.00, judge=unknown, conf=0.00, refs=-
- F00124 `structures.sample_28mn0ni_hr_cr.microstructure_list[3].phases_present[austenite].crystal_structure`: score=90.00, judge=yes, conf=0.90, refs=b0033
- F00125 `structures.sample_28mn0ni_hr_cr.microstructure_list[3].phases_present[austenite].grain_size`: score=30.00, judge=partial, conf=0.50, refs=b0032
- F00126 `structures.sample_28mn0ni_hr_cr.microstructure_list[3].phases_present[austenite].morphology`: score=100.00, judge=yes, conf=1.00, refs=b0033
- F00127 `structures.sample_28mn0ni_hr_cr.microstructure_list[3].phases_present[austenite].phase_name`: score=100.00, judge=yes, conf=1.00, refs=b0033
- F00128 `structures.sample_28mn0ni_hr_cr.microstructure_list[3].phases_present[austenite].texture`: score=0.00, judge=unknown, conf=0.00, refs=-
- F00129 `structures.sample_28mn0ni_hr_cr.microstructure_list[3].phases_present[austenite].volume_fraction`: score=100.00, judge=yes, conf=1.00, refs=b0033
- F00130 `structures.sample_28mn0ni_hr_cr.microstructure_list[3].related_sequence`: score=42.00, judge=partial, conf=0.70, refs=b0021
- F00131 `structures.sample_28mn0ni_hr_cr.number_of_phases`: score=100.00, judge=yes, conf=1.00, refs=b0033
- F00132 `structures.sample_28mn0ni_hr_cr.overall_structure`: score=100.00, judge=yes, conf=1.00, refs=b0033
- F00187 `properties.sample_28mn0ni_hr_cr.mechanical.hardness[bulk].region`: score=100.00, judge=yes, conf=1.00, refs=b0028,b0073
- F00188 `properties.sample_28mn0ni_hr_cr.mechanical.hardness[bulk].scale`: score=100.00, judge=yes, conf=1.00, refs=b0028
- F00189 `properties.sample_28mn0ni_hr_cr.mechanical.hardness[bulk].value_with_unit`: score=95.00, judge=yes, conf=0.95, refs=b0118
- F00190 `properties.sample_28mn0ni_hr_cr.mechanical.tensile_properties.elongation[0].value_with_unit`: score=100.00, judge=yes, conf=1.00, refs=b0138
- F00191 `properties.sample_28mn0ni_hr_cr.mechanical.tensile_properties.ultimate_tensile_strength[0].others.uncertainty`: score=100.00, judge=yes, conf=1.00, refs=b0138
- F00192 `properties.sample_28mn0ni_hr_cr.mechanical.tensile_properties.ultimate_tensile_strength[0].value_with_unit`: score=100.00, judge=yes, conf=1.00, refs=b0138
- F00193 `properties.sample_28mn0ni_hr_cr.mechanical.tensile_properties.yield_strength[0].others.uncertainty`: score=100.00, judge=yes, conf=1.00, refs=b0138
- F00194 `properties.sample_28mn0ni_hr_cr.mechanical.tensile_properties.yield_strength[0].value_with_unit`: score=100.00, judge=yes, conf=1.00, refs=b0138
- F00252 `characterization_methods.sample_28mn0ni_hr_cr.key_findings`: score=48.00, judge=partial, conf=0.80, refs=b0073,b0118
- F00253 `characterization_methods.sample_28mn0ni_hr_cr.purpose`: score=100.00, judge=yes, conf=1.00, refs=b0028
- F00254 `characterization_methods.sample_28mn0ni_hr_cr.technique`: score=100.00, judge=yes, conf=1.00, refs=b0028

### sample_28mn0ni_hr_cr_973
- F00113 `processing_steps.sample_28mn0ni_hr_cr_973.cooling_medium`: score=100.00, judge=yes, conf=1.00, refs=b0021
- F00114 `processing_steps.sample_28mn0ni_hr_cr_973.duration`: score=100.00, judge=yes, conf=1.00, refs=b0021
- F00115 `processing_steps.sample_28mn0ni_hr_cr_973.method`: score=100.00, judge=yes, conf=1.00, refs=b0069
- F00116 `processing_steps.sample_28mn0ni_hr_cr_973.reduction_ratio`: score=100.00, judge=yes, conf=1.00, refs=b0021
- F00117 `processing_steps.sample_28mn0ni_hr_cr_973.sequence`: score=30.00, judge=partial, conf=0.50, refs=b0021
- F00118 `processing_steps.sample_28mn0ni_hr_cr_973.temperature_with_unit`: score=100.00, judge=yes, conf=1.00, refs=b0069
- F00119 `processing_steps.sample_28mn0ni_hr_cr_973.type`: score=100.00, judge=yes, conf=1.00, refs=b0021
- F00133 `structures.sample_28mn0ni_hr_cr_973.microstructure_counts`: score=100.00, judge=yes, conf=1.00, refs=b0058,b0064,b0067
- F00134 `structures.sample_28mn0ni_hr_cr_973.microstructure_list[4].grain_structure.average_grain_size.value_with_unit`: score=100.00, judge=yes, conf=1.00, refs=b0061
- F00135 `structures.sample_28mn0ni_hr_cr_973.microstructure_list[4].phases_present[b2_intergranular].crystal_structure`: score=42.00, judge=partial, conf=0.70, refs=b0037
- F00136 `structures.sample_28mn0ni_hr_cr_973.microstructure_list[4].phases_present[b2_intergranular].grain_size`: score=100.00, judge=yes, conf=1.00, refs=b0037
- F00137 `structures.sample_28mn0ni_hr_cr_973.microstructure_list[4].phases_present[b2_intergranular].morphology`: score=100.00, judge=yes, conf=1.00, refs=b0037
- F00138 `structures.sample_28mn0ni_hr_cr_973.microstructure_list[4].phases_present[b2_intergranular].phase_name`: score=100.00, judge=yes, conf=1.00, refs=b0037
- F00139 `structures.sample_28mn0ni_hr_cr_973.microstructure_list[4].phases_present[b2_intergranular].volume_fraction`: score=100.00, judge=yes, conf=1.00, refs=b0067
- F00140 `structures.sample_28mn0ni_hr_cr_973.microstructure_list[4].phases_present[carbide_coarser].morphology`: score=100.00, judge=yes, conf=1.00, refs=b0069
- F00141 `structures.sample_28mn0ni_hr_cr_973.microstructure_list[4].phases_present[carbide_coarser].phase_name`: score=100.00, judge=yes, conf=1.00, refs=b0069
- F00142 `structures.sample_28mn0ni_hr_cr_973.microstructure_list[4].phases_present[carbide_coarser].volume_fraction`: score=100.00, judge=yes, conf=1.00, refs=b0069
- F00143 `structures.sample_28mn0ni_hr_cr_973.microstructure_list[4].phases_present[carbide_intragranular].morphology`: score=100.00, judge=yes, conf=1.00, refs=b0069
- F00144 `structures.sample_28mn0ni_hr_cr_973.microstructure_list[4].phases_present[carbide_intragranular].phase_name`: score=100.00, judge=yes, conf=1.00, refs=b0069
- F00145 `structures.sample_28mn0ni_hr_cr_973.microstructure_list[4].phases_present[carbide_intragranular].volume_fraction`: score=100.00, judge=yes, conf=1.00, refs=b0069
- F00146 `structures.sample_28mn0ni_hr_cr_973.microstructure_list[4].phases_present[deformed].crystal_structure`: score=30.00, judge=partial, conf=0.50, refs=b0032
- F00147 `structures.sample_28mn0ni_hr_cr_973.microstructure_list[4].phases_present[deformed].morphology`: score=100.00, judge=yes, conf=1.00, refs=b0069
- F00148 `structures.sample_28mn0ni_hr_cr_973.microstructure_list[4].phases_present[deformed].phase_name`: score=100.00, judge=yes, conf=1.00, refs=b0050
- F00149 `structures.sample_28mn0ni_hr_cr_973.microstructure_list[4].phases_present[deformed].volume_fraction`: score=48.00, judge=partial, conf=0.80, refs=b0058
- F00150 `structures.sample_28mn0ni_hr_cr_973.microstructure_list[4].phases_present[recrystallized].crystal_structure`: score=30.00, judge=partial, conf=0.50, refs=b0032
- F00151 `structures.sample_28mn0ni_hr_cr_973.microstructure_list[4].phases_present[recrystallized].grain_size`: score=100.00, judge=yes, conf=1.00, refs=b0061
- F00152 `structures.sample_28mn0ni_hr_cr_973.microstructure_list[4].phases_present[recrystallized].morphology`: score=100.00, judge=yes, conf=1.00, refs=b0037
- F00153 `structures.sample_28mn0ni_hr_cr_973.microstructure_list[4].phases_present[recrystallized].phase_name`: score=100.00, judge=yes, conf=1.00, refs=b0037
- F00154 `structures.sample_28mn0ni_hr_cr_973.microstructure_list[4].phases_present[recrystallized].volume_fraction`: score=100.00, judge=yes, conf=1.00, refs=b0058
- F00155 `structures.sample_28mn0ni_hr_cr_973.microstructure_list[4].precipitates[b2].distribution`: score=100.00, judge=yes, conf=1.00, refs=b0069
- F00156 `structures.sample_28mn0ni_hr_cr_973.microstructure_list[4].precipitates[b2].size.value_with_unit`: score=100.00, judge=yes, conf=1.00, refs=b0037
- F00157 `structures.sample_28mn0ni_hr_cr_973.microstructure_list[4].precipitates[b2].type`: score=100.00, judge=yes, conf=1.00, refs=b0037
- F00158 `structures.sample_28mn0ni_hr_cr_973.microstructure_list[4].precipitates[carbide].distribution`: score=100.00, judge=yes, conf=1.00, refs=b0069
- F00159 `structures.sample_28mn0ni_hr_cr_973.microstructure_list[4].precipitates[carbide].size.value_with_unit`: score=100.00, judge=yes, conf=1.00, refs=b0069
- F00160 `structures.sample_28mn0ni_hr_cr_973.microstructure_list[4].precipitates[carbide].type`: score=100.00, judge=yes, conf=1.00, refs=b0069
- F00161 `structures.sample_28mn0ni_hr_cr_973.microstructure_list[4].related_sequence`: score=30.00, judge=partial, conf=0.50, refs=b0021
- F00162 `structures.sample_28mn0ni_hr_cr_973.number_of_phases`: score=100.00, judge=yes, conf=1.00, refs=b0036
- F00163 `structures.sample_28mn0ni_hr_cr_973.overall_structure`: score=100.00, judge=yes, conf=1.00, refs=b0058,b0069
- F00210 `properties.sample_28mn0ni_hr_cr_973.mechanical.hardness[bulk].region`: score=100.00, judge=yes, conf=1.00, refs=b0028
- F00211 `properties.sample_28mn0ni_hr_cr_973.mechanical.hardness[bulk].scale`: score=100.00, judge=yes, conf=1.00, refs=b0028
- F00212 `properties.sample_28mn0ni_hr_cr_973.mechanical.hardness[bulk].value_with_unit`: score=100.00, judge=yes, conf=1.00, refs=b0121
- F00213 `properties.sample_28mn0ni_hr_cr_973.mechanical.tensile_properties.elongation[0].value_with_unit`: score=100.00, judge=yes, conf=1.00, refs=b0138
- F00214 `properties.sample_28mn0ni_hr_cr_973.mechanical.tensile_properties.strain_hardening_rate[0].value_with_unit`: score=100.00, judge=yes, conf=1.00, refs=b0138
- F00215 `properties.sample_28mn0ni_hr_cr_973.mechanical.tensile_properties.ultimate_tensile_strength[0].others.uncertainty`: score=100.00, judge=yes, conf=1.00, refs=b0138
- F00216 `properties.sample_28mn0ni_hr_cr_973.mechanical.tensile_properties.ultimate_tensile_strength[0].value_with_unit`: score=100.00, judge=yes, conf=1.00, refs=b0138
- F00217 `properties.sample_28mn0ni_hr_cr_973.mechanical.tensile_properties.yield_strength[0].others.uncertainty`: score=100.00, judge=yes, conf=1.00, refs=b0138
- F00218 `properties.sample_28mn0ni_hr_cr_973.mechanical.tensile_properties.yield_strength[0].value_with_unit`: score=100.00, judge=yes, conf=1.00, refs=b0138
- F00255 `characterization_methods.sample_28mn0ni_hr_cr_973.key_findings`: score=100.00, judge=yes, conf=1.00, refs=b0138
- F00256 `characterization_methods.sample_28mn0ni_hr_cr_973.purpose`: score=100.00, judge=yes, conf=1.00, refs=b0028
- F00257 `characterization_methods.sample_28mn0ni_hr_cr_973.technique`: score=100.00, judge=yes, conf=1.00, refs=b0028

### sample_15mn5ni_hr_cr_1023
- F00164 `interfaces.sample_15mn5ni_hr_cr_1023.defect_interaction[0].interaction_type`: score=100.00, judge=yes, conf=1.00, refs=b0142
- F00165 `interfaces.sample_15mn5ni_hr_cr_1023.defect_interaction[0].quality_description`: score=100.00, judge=yes, conf=1.00, refs=b0142
- F00166 `interfaces.sample_15mn5ni_hr_cr_1023.interface_notes[0].stress_strain_distribution`: score=100.00, judge=yes, conf=1.00, refs=b0142
- F00167 `interfaces.sample_15mn5ni_hr_cr_1023.phase_evolution`: score=100.00, judge=yes, conf=1.00, refs=b0142,b0167
- F00168 `interfaces.sample_15mn5ni_hr_cr_1023.phases[austenite].phase_1_name`: score=100.00, judge=yes, conf=1.00, refs=b0142
- F00169 `interfaces.sample_15mn5ni_hr_cr_1023.phases[austenite].phase_2_name`: score=100.00, judge=yes, conf=1.00, refs=b0142
- F00249 `characterization_methods.sample_15mn5ni_hr_cr_1023.key_findings`: score=100.00, judge=yes, conf=1.00, refs=b0142
- F00250 `characterization_methods.sample_15mn5ni_hr_cr_1023.purpose`: score=100.00, judge=yes, conf=1.00, refs=b0142,b0026
- F00251 `characterization_methods.sample_15mn5ni_hr_cr_1023.technique`: score=100.00, judge=yes, conf=1.00, refs=b0142,b0026

### sample_15mn5ni_hr_cr
- F00170 `properties.sample_15mn5ni_hr_cr.mechanical.hardness[bulk].region`: score=100.00, judge=yes, conf=1.00, refs=b0073
- F00171 `properties.sample_15mn5ni_hr_cr.mechanical.hardness[bulk].scale`: score=100.00, judge=yes, conf=1.00, refs=b0073
- F00172 `properties.sample_15mn5ni_hr_cr.mechanical.hardness[bulk].value_with_unit`: score=100.00, judge=yes, conf=1.00, refs=b0118
- F00173 `properties.sample_15mn5ni_hr_cr.mechanical.tensile_properties.elongation[0].value_with_unit`: score=100.00, judge=yes, conf=1.00, refs=b0138
- F00174 `properties.sample_15mn5ni_hr_cr.mechanical.tensile_properties.ultimate_tensile_strength[0].others.uncertainty`: score=100.00, judge=yes, conf=1.00, refs=b0138
- F00175 `properties.sample_15mn5ni_hr_cr.mechanical.tensile_properties.ultimate_tensile_strength[0].value_with_unit`: score=100.00, judge=yes, conf=1.00, refs=b0138
- F00176 `properties.sample_15mn5ni_hr_cr.mechanical.tensile_properties.yield_strength[0].others.uncertainty`: score=100.00, judge=yes, conf=1.00, refs=b0138
- F00177 `properties.sample_15mn5ni_hr_cr.mechanical.tensile_properties.yield_strength[0].value_with_unit`: score=100.00, judge=yes, conf=1.00, refs=b0138

### sample_15mn5ni_hr_cr_1173
- F00178 `properties.sample_15mn5ni_hr_cr_1173.mechanical.hardness[bulk].region`: score=100.00, judge=yes, conf=1.00, refs=b0028
- F00179 `properties.sample_15mn5ni_hr_cr_1173.mechanical.hardness[bulk].scale`: score=100.00, judge=yes, conf=1.00, refs=b0028
- F00180 `properties.sample_15mn5ni_hr_cr_1173.mechanical.hardness[bulk].value_with_unit`: score=100.00, judge=yes, conf=1.00, refs=b0121
- F00181 `properties.sample_15mn5ni_hr_cr_1173.mechanical.tensile_properties.elongation[0].value_with_unit`: score=100.00, judge=yes, conf=1.00, refs=b0138
- F00182 `properties.sample_15mn5ni_hr_cr_1173.mechanical.tensile_properties.strain_hardening_rate[0].value_with_unit`: score=100.00, judge=yes, conf=1.00, refs=b0138
- F00183 `properties.sample_15mn5ni_hr_cr_1173.mechanical.tensile_properties.ultimate_tensile_strength[0].others.uncertainty`: score=100.00, judge=yes, conf=1.00, refs=b0138
- F00184 `properties.sample_15mn5ni_hr_cr_1173.mechanical.tensile_properties.ultimate_tensile_strength[0].value_with_unit`: score=100.00, judge=yes, conf=1.00, refs=b0138
- F00185 `properties.sample_15mn5ni_hr_cr_1173.mechanical.tensile_properties.yield_strength[0].others.uncertainty`: score=100.00, judge=yes, conf=1.00, refs=b0138
- F00186 `properties.sample_15mn5ni_hr_cr_1173.mechanical.tensile_properties.yield_strength[0].value_with_unit`: score=100.00, judge=yes, conf=1.00, refs=b0138

### sample_28mn0ni_hr_cr_1023
- F00195 `properties.sample_28mn0ni_hr_cr_1023.mechanical.tensile_properties.elongation[0].value_with_unit`: score=100.00, judge=yes, conf=1.00, refs=b0138
- F00196 `properties.sample_28mn0ni_hr_cr_1023.mechanical.tensile_properties.strain_hardening_rate[0].value_with_unit`: score=100.00, judge=yes, conf=1.00, refs=b0138
- F00197 `properties.sample_28mn0ni_hr_cr_1023.mechanical.tensile_properties.ultimate_tensile_strength[0].others.uncertainty`: score=100.00, judge=yes, conf=1.00, refs=b0138
- F00198 `properties.sample_28mn0ni_hr_cr_1023.mechanical.tensile_properties.ultimate_tensile_strength[0].value_with_unit`: score=100.00, judge=yes, conf=1.00, refs=b0138
- F00199 `properties.sample_28mn0ni_hr_cr_1023.mechanical.tensile_properties.yield_strength[0].others.uncertainty`: score=100.00, judge=yes, conf=1.00, refs=b0138
- F00200 `properties.sample_28mn0ni_hr_cr_1023.mechanical.tensile_properties.yield_strength[0].value_with_unit`: score=100.00, judge=yes, conf=1.00, refs=b0138

### sample_28mn0ni_hr_cr_1173
- F00201 `properties.sample_28mn0ni_hr_cr_1173.mechanical.hardness[bulk].region`: score=100.00, judge=yes, conf=1.00, refs=b0028
- F00202 `properties.sample_28mn0ni_hr_cr_1173.mechanical.hardness[bulk].scale`: score=100.00, judge=yes, conf=1.00, refs=b0073,b0121
- F00203 `properties.sample_28mn0ni_hr_cr_1173.mechanical.hardness[bulk].value_with_unit`: score=100.00, judge=yes, conf=1.00, refs=b0121
- F00204 `properties.sample_28mn0ni_hr_cr_1173.mechanical.tensile_properties.elongation[0].value_with_unit`: score=100.00, judge=yes, conf=1.00, refs=b0138
- F00205 `properties.sample_28mn0ni_hr_cr_1173.mechanical.tensile_properties.strain_hardening_rate[0].value_with_unit`: score=100.00, judge=yes, conf=1.00, refs=b0138
- F00206 `properties.sample_28mn0ni_hr_cr_1173.mechanical.tensile_properties.ultimate_tensile_strength[0].others.uncertainty`: score=100.00, judge=yes, conf=1.00, refs=b0138
- F00207 `properties.sample_28mn0ni_hr_cr_1173.mechanical.tensile_properties.ultimate_tensile_strength[0].value_with_unit`: score=100.00, judge=yes, conf=1.00, refs=b0138
- F00208 `properties.sample_28mn0ni_hr_cr_1173.mechanical.tensile_properties.yield_strength[0].others.uncertainty`: score=100.00, judge=yes, conf=1.00, refs=b0138
- F00209 `properties.sample_28mn0ni_hr_cr_1173.mechanical.tensile_properties.yield_strength[0].value_with_unit`: score=100.00, judge=yes, conf=1.00, refs=b0138

### sample_28mn5ni_hr_cr
- F00219 `properties.sample_28mn5ni_hr_cr.mechanical.hardness[bulk].region`: score=100.00, judge=yes, conf=1.00, refs=b0028
- F00220 `properties.sample_28mn5ni_hr_cr.mechanical.hardness[bulk].scale`: score=100.00, judge=yes, conf=1.00, refs=b0028
- F00221 `properties.sample_28mn5ni_hr_cr.mechanical.hardness[bulk].value_with_unit`: score=100.00, judge=yes, conf=1.00, refs=b0118
- F00222 `properties.sample_28mn5ni_hr_cr.mechanical.tensile_properties.elongation[0].value_with_unit`: score=100.00, judge=yes, conf=1.00, refs=b0138
- F00223 `properties.sample_28mn5ni_hr_cr.mechanical.tensile_properties.ultimate_tensile_strength[0].others.uncertainty`: score=100.00, judge=yes, conf=1.00, refs=b0138
- F00224 `properties.sample_28mn5ni_hr_cr.mechanical.tensile_properties.ultimate_tensile_strength[0].value_with_unit`: score=100.00, judge=yes, conf=1.00, refs=b0138
- F00225 `properties.sample_28mn5ni_hr_cr.mechanical.tensile_properties.yield_strength[0].others.uncertainty`: score=100.00, judge=yes, conf=1.00, refs=b0138
- F00226 `properties.sample_28mn5ni_hr_cr.mechanical.tensile_properties.yield_strength[0].value_with_unit`: score=100.00, judge=yes, conf=1.00, refs=b0138

### sample_28mn5ni_hr_cr_1023
- F00227 `properties.sample_28mn5ni_hr_cr_1023.mechanical.tensile_properties.elongation[0].value_with_unit`: score=100.00, judge=yes, conf=1.00, refs=b0138
- F00228 `properties.sample_28mn5ni_hr_cr_1023.mechanical.tensile_properties.ultimate_tensile_strength[0].others.uncertainty`: score=100.00, judge=yes, conf=1.00, refs=b0138
- F00229 `properties.sample_28mn5ni_hr_cr_1023.mechanical.tensile_properties.ultimate_tensile_strength[0].value_with_unit`: score=100.00, judge=yes, conf=1.00, refs=b0138
- F00230 `properties.sample_28mn5ni_hr_cr_1023.mechanical.tensile_properties.yield_strength[0].others.uncertainty`: score=100.00, judge=yes, conf=1.00, refs=b0138
- F00231 `properties.sample_28mn5ni_hr_cr_1023.mechanical.tensile_properties.yield_strength[0].value_with_unit`: score=100.00, judge=yes, conf=1.00, refs=b0138

### sample_28mn5ni_hr_cr_1173
- F00232 `properties.sample_28mn5ni_hr_cr_1173.mechanical.hardness[bulk].region`: score=100.00, judge=yes, conf=1.00, refs=b0121
- F00233 `properties.sample_28mn5ni_hr_cr_1173.mechanical.hardness[bulk].scale`: score=100.00, judge=yes, conf=1.00, refs=b0121
- F00234 `properties.sample_28mn5ni_hr_cr_1173.mechanical.hardness[bulk].value_with_unit`: score=100.00, judge=yes, conf=1.00, refs=b0121
- F00235 `properties.sample_28mn5ni_hr_cr_1173.mechanical.tensile_properties.elongation[0].value_with_unit`: score=100.00, judge=yes, conf=1.00, refs=b0138
- F00236 `properties.sample_28mn5ni_hr_cr_1173.mechanical.tensile_properties.strain_hardening_rate[0].value_with_unit`: score=100.00, judge=yes, conf=1.00, refs=b0138
- F00237 `properties.sample_28mn5ni_hr_cr_1173.mechanical.tensile_properties.ultimate_tensile_strength[0].others.uncertainty`: score=100.00, judge=yes, conf=1.00, refs=b0138
- F00238 `properties.sample_28mn5ni_hr_cr_1173.mechanical.tensile_properties.ultimate_tensile_strength[0].value_with_unit`: score=100.00, judge=yes, conf=1.00, refs=b0138
- F00239 `properties.sample_28mn5ni_hr_cr_1173.mechanical.tensile_properties.yield_strength[0].others.uncertainty`: score=100.00, judge=yes, conf=1.00, refs=b0138
- F00240 `properties.sample_28mn5ni_hr_cr_1173.mechanical.tensile_properties.yield_strength[0].value_with_unit`: score=100.00, judge=yes, conf=1.00, refs=b0138

### sample_28mn5ni_hr_cr_973
- F00241 `properties.sample_28mn5ni_hr_cr_973.mechanical.hardness[bulk].region`: score=100.00, judge=yes, conf=1.00, refs=b0073,b0121
- F00242 `properties.sample_28mn5ni_hr_cr_973.mechanical.hardness[bulk].scale`: score=100.00, judge=yes, conf=1.00, refs=b0073
- F00243 `properties.sample_28mn5ni_hr_cr_973.mechanical.hardness[bulk].value_with_unit`: score=100.00, judge=yes, conf=1.00, refs=b0121
- F00244 `properties.sample_28mn5ni_hr_cr_973.mechanical.tensile_properties.elongation[0].value_with_unit`: score=100.00, judge=yes, conf=1.00, refs=b0138
- F00245 `properties.sample_28mn5ni_hr_cr_973.mechanical.tensile_properties.ultimate_tensile_strength[0].others.uncertainty`: score=100.00, judge=yes, conf=1.00, refs=b0138
- F00246 `properties.sample_28mn5ni_hr_cr_973.mechanical.tensile_properties.ultimate_tensile_strength[0].value_with_unit`: score=100.00, judge=yes, conf=1.00, refs=b0138
- F00247 `properties.sample_28mn5ni_hr_cr_973.mechanical.tensile_properties.yield_strength[0].others.uncertainty`: score=100.00, judge=yes, conf=1.00, refs=b0138
- F00248 `properties.sample_28mn5ni_hr_cr_973.mechanical.tensile_properties.yield_strength[0].value_with_unit`: score=100.00, judge=yes, conf=1.00, refs=b0138
