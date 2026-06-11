# Material System
- Alloy designation: Fe–30Mn–9Al–C–3Ni low-density steel (weight percent; also referred to as Fe30Mn9AlC3Ni0.6Cr in some imaging captions indicating minor Cr).
- Phases of interest: γ-austenite (FCC), κ-carbide (nano-scale precipitates).
- Feedstock: gas-atomized powder produced by plasma rotating electrode process (PREP), particle size D10–D90 ~ 15–53 µm, D50 = 35.69 µm; spherical morphology, excellent flowability (Hall flow 14 s/50 g).
- Reference material: as-cast Fe–30Mn–9Al–C–3Ni steel (UTS 879.0 MPa, elongation 20.53%).

# Processing Route and Variables
- Additive manufacturing technique: selective laser melting (SLM) using SLM Solutions SLM280 printer.
- Feedstock powder: PREP spherical powder, size 15–53 µm.
- Fixed SLM parameters:
  - Scanning speed: 750 mm s⁻¹
  - Layer thickness: 0.02 mm
  - Hatch spacing: 0.08 mm
  - Laser spot diameter: 0.1 mm
  - Substrate preheating: 200 °C
  - Atmosphere: Ar with O₂ < 300 ppm
  - Scanning strategy: 67° rotation between successive layers
- Main variable: laser power (and thus volumetric energy density):
  - P-70: 70 W → 58.33 J mm⁻³
  - P-90: 90 W → 75.00 J mm⁻³
  - P-110: 110 W → 91.67 J mm⁻³
  - P-130: 130 W → 108.33 J mm⁻³
  - P-150: 150 W → 125.00 J mm⁻³

# Microstructure and Phase Evolution
- **Powder (before SLM)**: XRD shows two-phase mixture of γ-austenite (dominant) and α-ferrite (minor). SEM cross-sections reveal dendritic solidification pattern inside particles.
- **As-built SLM samples (all powers)**: XRD patterns contain only γ-austenite peaks (FCC); no residual α-ferrite is detected, indicating complete transformation to austenite during rapid solidification.
  - FWHM of (111) γ peak decreases from 0.289° (P-70) to 0.237° (P-150), reflecting progressive grain coarsening with increasing energy input.
- **Porosity and defects (OM, transverse section)**:
  - P-70: 4.75 % porosity – many irregular lack-of-fusion pores.
  - P-90: 0.25 %
  - P-110: 0.13 % (minimum, near-full densification)
  - P-130: 0.28 %
  - P-150: 0.35 % – visible microcracks added.
- **Grain structure (EBSD IPF maps)**:
  - Transverse (x–y) plane: fine equiaxed austenite grains with random crystallographic orientation (color dispersion in IPF), consequence of 67° layer rotation minimizing texture.
  - Longitudinal (x–z, build direction) plane: dominant columnar grains growing along the thermal gradient, with some equiaxed grains at melt-pool boundaries.
  - Mean grain size (transverse, EBSD statistics):
    - P-70: 8.1 µm
    - P-90: 10.6 µm
    - P-110: 11.0 µm
    - P-130: 13.9 µm
    - P-150: 14.3 µm
  - P-110 longitudinal: 14.9 µm (larger than transverse counterpart).
- **Nanoscale precipitates and dislocations (TEM, P-110)**:
  - Bright-field images show dislocation tangles and high-density dislocation regions.
  - SAED patterns confirm coexistence of γ-austenite and κ-carbide with orientation relationship [011]γ // [011]κ.
  - Dark-field image (using (010)κ reflection) reveals uniformly distributed nano-scale κ-carbide particles.
  - HRTEM and FFT confirm [011] zone axis of austenite.
- **Surface topography (AFM/laser confocal)**:
  - Sa (arithmetic mean roughness) decreases monotonically: 20.71 µm (P-70) → 4.19 µm (P-150). Higher power yields smoother surfaces owing to more complete melting and better consolidation.
- **Surface morphology (SEM)**:
  - P-70: abundant lack-of-fusion defects, unmelted powder particles, holes.
  - P-90: defects significantly reduced.
  - P-110: minimal defects, isolated balling (optimum).
  - P-130, P-150: pronounced balling effects (fluid instability) indicated by arrow-marked spherical particles.

# Processing-Structure-Property Chain
- **P-70 (58.33 J mm⁻³)**: insufficient energy → incomplete powder melting → high porosity (4.75 %), lack-of-fusion voids → tensile specimen fails early at ~20 % strain with elongation only 23.10 %; hardness ~278–279 HV; low strength.
- **Increasing power to 90–110 W**: higher energy density → more complete melting → porosity drops to 0.25–0.13 % → density and load-bearing area increase. Rapid cooling refines grains (11.0 µm) and precipitates nano-κ carbides; high dislocation density accumulates. Work hardening capacity is excellent (continuous yielding, extensive strain hardening).
  - **P-110 (91.67 J mm⁻³) optimizes the balance:**
    - Highest relative density ~99.87 % → minimizes stress concentration from pores.
    - Moderate grain size (~11 µm transverse) → good Hall-Petch strengthening without excessive grain-boundary embrittlement.
    - κ-carbide dispersion and dislocation tangles → precipitation strengthening and dislocation hardening.
    - Resulting mechanical properties: YS 887.1 MPa, UTS 1076.8 MPa, elongation 40.80 %, hardness 294 HV (longitudinal) / 292 HV (transverse).
- **P-130, P-150 (108.33–125.00 J mm⁻³)**: excessive energy input → coarser grains (13.9–14.3 µm), porosity slightly rises to 0.28–0.35 %, balling and microcracks appear. Strength and ductility deteriorate: P-150 elongation drops to 28.28 %; hardness decreases to ~283 HV (longitudinal) / 281 HV (transverse). Fracture surfaces show mixed dimple/cleavage features.
- **Compared to as-cast reference**: All SLM samples show superior strength and ductility, e.g., as-cast UTS 879.0 MPa, elongation 20.53 % vs P-110 UTS 1076.8 MPa, elongation 40.80 %. This superiority originates from the fine, defect-lean austenite + κ-carbide SLM microstructure, in contrast to the coarse cast structure.

# Mechanistic Interpretation
- Low power induces lack-of-fusion pores that act as stress concentrators, triggering premature fracture and limiting ductility.
- Optimum power (110 W) ensures full melting and minimal porosity, while the fast cooling intrinsic to SLM produces fine equiaxed austenite, high dislocation density, and uniformly dispersed nano-κ carbides. The combination of grain refinement, precipitation hardening, and dislocation strengthening elevates yield and ultimate tensile strengths, and the stable austenite provides excellent work hardening, leading to the observed 40.80 % elongation.
- Excessively high power increases the melt-pool lifetime and reduces cooling rate, causing grain coarsening, thermal-stress-induced cracks, and melt-pool instability (balling). These defects and coarser microstructure weaken the material and reduce ductility.

# Key Quantitative Findings
- Optimal SLM parameters: 110 W, energy density 91.67 J mm⁻³.
- Corresponding porosity: 0.13 % (relative density ~99.87 %).
- Grain size: transverse 11.0 µm, longitudinal 14.9 µm (P-110).
- Vickers hardness (P-110): longitudinal 294 HV, transverse 292 HV.
- Tensile properties (P-110): YS = 887.1 MPa, UTS = 1076.8 MPa, elongation = 40.80 %.
- Property span across laser powers:
  - Porosity range: 0.13 % (P-110) to 4.75 % (P-70).
  - Grain size range: 8.1 µm (P-70) to 14.3 µm (P-150) in transverse section.
  - Elongation: 23.10 % (P-70) to 40.80 % (P-110).
  - Hardness: 279 HV (P-70) to 294 HV (P-110).
- Surface roughness (Sa): 20.71 µm (P-70) → 4.19 µm (P-150).
- As-cast reference: UTS 879.0 MPa, elongation 20.53 %.
- Phase after SLM: exclusively γ-austenite; κ-carbide precipitates detected in P-110.

# Visual Evidence
- **Figure 2 (SEM + EDS of powder)**: Confirms highly spherical PREP powder, uniform element distribution (Fe, Mn, Al, Ni), and dense internal structure with dendritic solidification.
- **Figure 3 (Powder size distribution)**: Shows narrow size range 15–53 µm, D50 = 35.69 µm, and superior flowability (14 s/50 g), supporting suitability for SLM.
- **Figure 4 (XRD of powder)**: Indicates coexistence of γ-austenite and α-ferrite in the starting powder, providing the baseline phase constitution before SLM.
- **Figure 5 (XRD of SLM samples)**: Demonstrates exclusive γ-austenite phase after SLM and FWHM decrease with increasing laser power, evidencing grain coarsening.
- **Figure 6 (OM porosity)**: Visualizes the porosity trend – highest at 70 W, minimum at 110 W, slight increase with cracks at 150 W – directly correlating defect fraction with laser power.
- **Figure 7 (EBSD IPF + longitudinal)**: Reveals equiaxed random grains in transverse plane and columnar grains along build direction; grain size increases with power.
- **Figure 8 (Grain size histograms)**: Quantifies average grain sizes: 8.1 µm (70 W) → 14.3 µm (150 W) transverse; P-110 longitudinal 14.9 µm, establishing the microstructure–property link.
- **Figure 9 (TEM)**: Provides direct evidence of nanoscale κ-carbide precipitation, dislocation tangles, and orientation relationship in the highest-performing P-110 sample.
- **Figure 10 (AFM roughness)**: Documents progressive surface smoothing with increasing power, consistent with improved melting and densification.
- **Figure 11 (SEM surface morphology)**: Shows transition from lack-of-fusion defects (low power) to balling-induced defects (high power), with 110 W giving the best surface integrity.
- **Figure 12 (Tensile stress–strain curves)**: Demonstrates the superior strength–ductility combination of P-110 and the substantial improvement over as-cast material; P-70’s early failure and P-150’s reduced elongation are directly observed.
- **Figure 13 (Hardness bar chart)**: Confirms the peak hardness at 110 W for both longitudinal and transverse directions, reflecting the optimal defect and grain structure.
- **Figure 14 (Fractography)**: Fracture surfaces evolve from lack-of-fusion, unmelted particles (P-70) to fine ductile dimples (P-90, P-110), then to mixed dimple–cleavage with cracks (P-130, P-150), explaining the ductility trends.
