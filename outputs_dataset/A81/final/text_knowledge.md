# Strong yet ductile low-density steel via multiphase heterogeneous microstructure

## Material System
- **Alloy**: Fe-0.25C-3Mn-2Al-0.4Si (low-density steel, nominal composition in wt.%)
- **Phases present**: ferrite (F), bainite (B), tempered martensite (TM), fresh martensite (FM), retained austenite (RA), deformation-induced martensite (DIM)
- **Critical transformation temperatures**: Ac1 = 705 °C, Ac3 = 950 °C, Bf = 380 °C, Ms = 346 °C

## Processing Route and Variables

### Primary Processing
- Vacuum induction melting and hot forging
- Homogenization at 1200 °C for 60 min
- Multi-pass hot rolling: 6 passes from ~1100 °C to 880 °C, 90% total reduction, air cooling
- Cold rolling: 60% reduction to 1.6 mm final sheet thickness

### Heat Treatment — Intercritical Annealing + Low Bainite Aging
Six sample conditions generated from the same cold-rolled stock:

| Sample ID | Intercritical Annealing | Low Bainite Aging |
|-----------|--------------------------|-------------------|
| AN750  | 750 °C / 30 min, air cool | None |
| AN800  | 800 °C / 30 min, air cool | None |
| AN850  | 850 °C / 30 min, air cool | None |
| AN750-T | 750 °C / 30 min, air cool | 400 °C / 30 min |
| AN800-T | 800 °C / 30 min, air cool | 400 °C / 30 min |
| AN850-T | 850 °C / 30 min, air cool | 400 °C / 30 min |

All intercritical annealing temperatures lie between Ac1 (705 °C) and Ac3 (950 °C).

### Tensile Specimen Geometry
Machined from 1.6 mm thick sheet: gauge length 14 mm, width 5 mm, thickness 1 mm, total length 58 mm, grip width 10 mm.

## Microstructure and Phase Evolution

### Hot-Rolled and Cold-Rolled Precursors
- Hot-rolled (HR) state: lath-like fresh martensite (FM) and bainite (B); EBSD shows 100% BCC phase with zero retained austenite fraction
- Cold-rolled state: elongated lamellar structure containing FM and B

### Annealed-Only Series (AN750, AN800, AN850)
- Intercritical annealing produces polygonal ferrite (F), bainite (B), fresh martensite (FM), and retained austenite (RA)
- RA volume fraction decreases with increasing annealing temperature: 3.0 vol% (AN750) → 1.1 vol% (AN800) → 0.2 vol% (AN850)
- RA average diameter increases with temperature: 0.59 μm (AN750) → 0.72 μm (AN800) → 0.83 μm (AN850)

### Annealed + Aged Series (AN750-T, AN800-T, AN850-T)
After 400 °C low bainite aging, the microstructure comprises F + B/TM + FM + RA. Quantitative phase fractions for the T-series:

| Phase | AN750-T | AN800-T | AN850-T |
|-------|---------|---------|---------|
| Ferrite (F) | 49.3% | 46.8% | 54.7% |
| Bainite / Tempered Martensite (B/TM) | — | — | — |
| Fresh Martensite (FM) | 8.3% | — | 3.3% |
| Retained Austenite (RA) | 7.4% | 2.4% | 0.6% |

- Ferrite average grain size coarsens from 4.53 μm (AN750-T) → 5.35 μm (AN850-T)
- B/TM refines significantly to 0.86 μm at 850 °C
- RA content decreases monotonically with increasing annealing temperature: 7.4% → 2.4% → 0.6%
- FM fraction also decreases: 8.3% → … → 3.3%

### Phase Discrimination via EBSD IQ Histograms
- IQ histograms exhibit bimodal distributions
- Peak I (~4–5×10⁴): bainite/tempered martensite (B/TM)
- Peak II (~7–9×10⁴): fresh martensite (FM)
- Peak separation arises from carbon concentration and dislocation density differences

### TEM-Based Distinction of B vs. TM
- Carbides in bainite: align at approximately 60° to lath boundaries
- Carbides in tempered martensite: randomly distributed

### Deformation-Induced Martensite (DIM)
- Average DIM equivalent circle diameter: 0.12 μm (AN750-T) → 0.15 μm (AN800-T) → 0.19 μm (AN850-T)
- Increasing annealing temperature promotes coarser DIM sizes

### Elemental Partitioning (EPMA)
- Carbon is primarily enriched in harder phases (B/TM, FM, RA) and depleted in ferrite
- At higher annealing temperatures (750 → 850 °C), carbon distribution becomes progressively more uniform
- Mn, Al, and Si show relatively homogeneous distributions across all conditions

## Processing-Structure-Property Chain

### Processing → Microstructure
Intercritical annealing temperature controls the volume fraction, size, and stability of RA, as well as the relative proportions of F, B/TM, and FM:
- **750 °C** maximizes RA fraction (7.4% after aging) with fine RA diameter (~0.59 μm in AN750)
- **850 °C** minimizes RA (0.6% after aging) while coarsening ferrite and refining B/TM; carbon distribution becomes more uniform
- Low bainite aging at 400 °C tempers part of the martensite into TM and stabilizes RA via carbon partitioning

### Microstructure → Mechanical Properties
Engineering stress–strain data for T-series:

| Sample | Yield Strength | Tensile Strength | Elongation | PSE |
|--------|---------------|------------------|------------|-----|
| AN750-T | — | 1068 MPa | 34.0% | — |
| AN800-T | — | 1295 MPa | 18.7% | — |
| AN850-T | — | 1269 MPa | 13.9% | — |

Reported property ranges across all conditions: yield strength 697–991 MPa, tensile strength 1068–1295 MPa, elongation 13.9–34.0%. Product of strength and elongation (PSE) exceeds 30 GPa·%, positioning this steel above conventional QP, DP, TRIP, and TBF steels.

### Microstructure → Deformation Mechanisms
- **AN750-T**: uniform strain distribution, effective stress partitioning between soft F and hard B/TM/FM domains during uniform plastic deformation; highest elongation (34.0%)
- **AN800-T**: two local strain concentration points expand at 45° and coalesce, leading to necking; highest tensile strength (1295 MPa)
- **AN850-T**: strain concentration localizes in hard domains; lowest elongation (13.9%)

## Mechanistic Interpretation

### Back Stress Strengthening
- Strain gradients arising from mechanical incompatibility between soft ferrite and hard B/TM/FM domains generate geometrically necessary dislocations (GNDs) at heterophase interfaces
- Back stress (σ_B) values measured at necking: 217 MPa (AN750-T), 300 MPa (AN800-T), 278 MPa (AN850-T); range reaches up to ~300 MPa
- Back stress contributes 236–300 MPa to the overall flow stress, providing significant hetero-deformation-induced hardening

### TRIP Effect
- Retained austenite transforms progressively to deformation-induced martensite during straining
- Olson-Cohen kinetic model parameters: α=5, β=1.28, n=0.55
- Final DIM fractions at fracture: 4.74% (AN750-T, from 7.4% initial RA), 1.16% (AN800-T, from 2.4% initial RA), 0.28% (AN850-T, from 0.6% initial RA)
- TRIP effect diminishes at higher annealing temperatures due to reduced RA content and stability

### Strain Partitioning and Stress Concentration Mitigation
- KAM analysis confirms strain localization at F/B/TM interfaces; point-to-origin misorientation peaks at boundaries then gradually decays
- AN800-T exhibits highest average KAM (0.69°) compared to AN750-T (0.53°) and AN850-T (0.62°), attributed to elevated B/TM content
- Post-fracture EBSD in necking region: RA volume fraction decreases to 0.018 (AN750-T), 0.004 (AN800-T), 0.002 (AN850-T)
- Sharp P-T-P misorientation spikes (up to ~55°) coincide with pattern quality minima at phase interfaces, evidencing GND pile-up and stress partitioning

### Fracture Behavior
- Microvoids nucleate predominantly at soft/hard domain interfaces
- AN750-T and AN800-T: crack tips blunt at hard domain interfaces, generating secondary cracks
- AN850-T: hard domains are severed due to increased brittleness from local carbon and manganese enrichment
- Dimple size decreases with annealing temperature: average 1.54 μm (AN750-T) → 1.44 μm (AN800-T) → 1.31 μm (AN850-T)
- AN750-T: deep equiaxed dimples (ductile fracture); AN800-T and AN850-T: mixed-mode with quasi-cleavage facets from FM

## Key Quantitative Findings
1. **RA optimization**: Intercritical annealing at 750 °C + aging yields 7.4 vol% RA, the highest among all conditions.
2. **Strength–ductility synergy**: AN750-T achieves 1068 MPa tensile strength with 34.0% elongation; AN800-T achieves 1295 MPa with 18.7% elongation.
3. **Back stress magnitude**: 217–300 MPa at necking, representing a major strengthening contribution.
4. **TRIP kinetics**: DIM fraction evolves from 0 to 4.74% (AN750-T) during deformation.
5. **KAM strain metric**: AN800-T average KAM reaches 0.69°, highest among T-series.
6. **PSE benchmark**: Exceeds 30 GPa·%, outperforming QP, DP, TRIP, and TBF steels.

## Visual Evidence

### Figure 1 (chart_schematic): Multiphase Design and Property Overview
Provides an integrated schematic of SEM/EBSD/TEM/DIC/XRD evidence linking the hierarchical multiphase microstructure (F+B/TM+FM+RA) to mechanical performance. Supports the core claim that back stress (236–300 MPa), TRIP effect, and coordinated deformation mitigate stress concentration and yield superior strength–ductility combination.

### Figure 2 (fabrication_synthesis): Processing Route and Specimen Preparation
Documents the complete T–t profile: 1200 °C/60 min homogenization, 1100→880 °C hot rolling (90% reduction), 60% cold rolling to 1.6 mm, intercritical annealing at 750/800/850 °C for 30 min, and optional 400 °C/30 min aging. Microstructural evolution schematics and tensile specimen geometry are provided, establishing the processing-structure-property linkage framework.

### Figure 3 (microscopy_sem): Microstructure Evolution — SEM
Eight SEM subfigures comparing HR, cold-rolled, AN750/800/850, and AN750/800/850-T conditions. Documents the transition from lath FM+B to multiphase F+B+FM+RA mixtures with systematic variation with annealing temperature. Red arrows specifically mark RA locations.

### Figure 4 (diffraction_ebsd): Retained Austenite Evolution — EBSD + XRD
EBSD phase maps (BCC red, FCC green) quantify RA content: 0% (HR) → 3.0% (AN750) → 1.1% (AN800) → 0.2% (AN850). Line chart and XRD patterns confirm RA peaks at 750 °C and BCC+FCC coexistence. Establishes the process window for RA stabilization.

### Figure 5 (microscopy_tem): Phase Identification — TEM
12 TEM images (bright-field, dark-field, SAED) differentiating B from TM via carbide orientation (60° to boundary in B, random in TM). Confirms RA films between laths and decreasing RA content (7.4% → 0.6%) with temperature. Fills the EBSD phase-discrimination gap.

### Figure 6 (diffraction_ebsd): Phase Separation and Interfacial Strain — EBSD
IQ+phase maps for AN750/800/850-T quantify FCC fractions (0.074/0.024/0.006). Bimodal IQ histograms enable B/TM vs. FM separation. KAM maps and point-to-origin profiles show peak misorientation at F/B/TM interfaces, with AN800-T exhibiting the highest average KAM (0.69°), supporting the hetero-deformation-induced strengthening mechanism.

### Figure 7 (chart_plot): Phase Fractions and Mechanical Properties
Quantitative bar charts of F, B/TM, FM, RA volume fractions and grain sizes versus annealing temperature. Engineering stress–strain curves and PSE benchmark plot demonstrate AN800-T (1295 MPa, 18.7%) and AN750-T (1068 MPa, 34.0%) outperform conventional AHSS grades.

### Figure 8 (chart_plot): TRIP Kinetics — Olson-Cohen Model
Three dual-axis plots showing DIM increase and RA decrease with true strain. Initial RA of 7.4%/2.4%/0.6% yields final DIM of 4.74%/1.16%/0.28%. Quantitatively confirms TRIP effect weakens at higher annealing temperatures.

### Figure 9 (spectroscopy_eds): Elemental Partitioning — EPMA
2D elemental maps (Fe, C, Mn, Al, Si) and quantitative line scans across B/TM, RA, and FM phases. Carbon enrichment in hard phases confirmed; carbon homogenization increases with annealing temperature. Mn, Al, Si remain relatively uniform.

### Figure 10 (property_mechanical): Back Stress and DIC Strain Fields
True stress–strain curves with iso-work model decomposition and DIC strain maps. Back stress σ_B = 217 MPa (AN750-T), 300 MPa (AN800-T), 278 MPa (AN850-T). DIC reveals uniform strain in AN750-T, 45° strain concentration coalescence in AN800-T, and hard-domain localization in AN850-T.

### Figure 11 (microscopy_tem): Heterostructure GND Accumulation
Bright-field and dark-field TEM showing GND pile-ups at soft/hard domain interfaces. Defines heterostructure parameters (R, Δh). Stress decomposition plot partitions flow stress into σ_B, f_Fσ_F, f_BTMσ_BTM, f_DIMσ_DIM, f_RAσ_RA, f_FMσ_FM contributions.

### Figure 12 (microscopy_sem): Fracture Surfaces and Dimple Statistics
Crack path SEM: microvoid nucleation at interfaces; crack blunting in AN750/800-T vs. hard-domain severing in AN850-T. Dimple statistics: average size 1.54 → 1.44 → 1.31 μm with increasing temperature; quasi-cleavage emerges at higher temperatures.

### Figure 13 (diffraction_ebsd): Post-Fracture Necking Region — EBSD
KAM and phase maps in necking zone. RA post-fracture: 0.018 → 0.004 → 0.002. P-T-P misorientation line profiles show sharp spikes (up to ~55°) at phase boundaries coinciding with pattern quality minima, confirming GND accumulation and strain partitioning.

### Figure 14 (property_thermal): Dilatometry — Transformation Temperatures
Dilatometry curve (ΔL vs. T) with 10 °C/s heating to 200 °C, 0.01 °C/s to 980 °C, −30 °C/s cooling. Determines Ac1 = 705 °C, Ac3 = 950 °C, Bf = 380 °C, Ms = 346 °C, defining the intercritical annealing window for microstructure design.

### Figure 15 (diffraction_ebsd): DIM Size Distribution
IPF maps pre- and post-parent grain reconstruction, plus DIM equivalent circle diameter distributions. Average DIM size increases from 0.12 μm (AN750-T) to 0.19 μm (AN850-T), correlating with reduced RA content and altered strain partitioning.
