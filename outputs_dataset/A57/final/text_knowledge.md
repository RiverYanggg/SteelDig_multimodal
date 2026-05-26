# Ultrastrong and Ductile Duplex Lightweight Steel Fe-30Mn-9Al-1C-1V-5Ni (wt.%)

## Material System
- **Alloy composition**: Fe-30Mn-9Al-1C-1V-5Ni (wt.%)
- **Phases present after processing**:
  - Austenite (γ, FCC): ~80 vol%, average grain size 1.31 μm (Gaussian-fitted unimodal distribution)
  - B2 (ordered BCC, NiAl-type): ~20 vol%, bimodal grain size distribution with band-like grains averaging 1.02 μm and particle-like grains averaging 3.38 μm
  - VC carbides: volume fraction 0.26%, particle size 19.9±6.2 nm, coherent with austenite matrix; orientation relationship [011]γ // [011]VC
  - L'1₂-type long-range ordered (LRO) domains within austenite: size 1.0±0.3 nm, volume fraction 11.10%
- **Phase constitution rationale**: Processing temperature of 900 °C selected based on Thermo-Calc 2021b equilibrium calculations; at this temperature κ-carbide is fully dissolved (dissolution above 750 °C), VC maintained at low fractions, and the alloy consists of ~78 vol% austenite and ~20 vol% B2

## Processing Route and Variables
1. **Homogenization**: 1050 °C for 1 h
2. **Hot rolling**: 85% thickness reduction, followed by immediate water quenching; final thickness 3 mm
3. **Cold rolling**: 50% total reduction (single-pass reduction ≤5%) to final thickness 1.5 mm
4. **Solution treatment**: 900 °C for 15 min, followed by water quenching (terminal heat treatment that establishes the dual-nanoprecipitation duplex microstructure)

## Microstructure and Phase Evolution
- **As-processed microstructure (after solution treatment)**:
  - Ultrafine-grained duplex structure: equiaxed austenite grains and B2 phase distributed as both elongated strip-like grains and fine particles at austenite grain boundaries
  - VC nanoprecipitates coherent with γ matrix; size 19.9±6.2 nm; volume fraction 0.26%
  - L'1₂ ordered nanodomains within austenite; size 1.0±0.3 nm; volume fraction 11.10%; visualized by dark-field TEM from superlattice reflections and confirmed by inverse FFT
  - B2/γ interface: semi-coherent with orientation relationship [011]γ // [111]B2, confirmed by HRTEM and FFT patterns
- **Deformation microstructure evolution**:
  - At 6% engineering strain (TEM observations): nonplanar slip bands form; dislocation pile-ups at B2/γ phase boundaries; weakening and volume fraction reduction of L'1₂ ordered domains within slip bands, evidenced by attenuated superlattice reflections in SAED; VC nanoprecipitates impede dislocation motion
  - At 12% engineering strain (TEM observations): increased dislocation density in both phases; dislocation bowing-out configurations; progressive LRO domain dissolution via dislocation shearing; enhanced dislocation hindrance by VC carbides; sustained dislocation accumulation at phase boundaries
  - GND density evolution (in-situ EBSD, Figure 6):
    - Austenite (γ): 5.36×10¹³ m⁻² (0% strain) → 2.64×10¹⁴ m⁻² (6% strain)
    - B2 phase: 1.04×10¹⁴ m⁻² (0% strain) → 2.51×10¹⁴ m⁻² (6% strain)
    - B2 initially has higher GND density (attributed to smaller grain size), but austenite accumulates GNDs more rapidly, surpassing B2 at 6% strain
    - Heterogeneous GND distributions among individual grains observed

## Processing-Structure-Property Chain
- **Processing → Structure**: Solution treatment at 900 °C for 15 min dissolves κ-carbide, stabilizes austenite (~80%) + B2 (~20%) duplex structure, and enables dual nanoprecipitation (coherent VC carbides + L'1₂ ordered domains within austenite); ultrafine grain size inherited from prior cold rolling (50% reduction) and recrystallization
- **Structure → Strength**:
  - Yield strength: 1316 ± 16 MPa
  - Ultimate tensile strength: 1458 ± 11 MPa
  - Total elongation: 11.7% (~12%)
  - Ductile fracture confirmed by dimpled fracture surface (SEM, 5 μm scale bar)
- **Structure → Work-hardening behavior** (three distinct stages):
  - **Stage I** (0–1% true strain): sharp decrease in work-hardening rate, dropping below zero due to large dislocation mean free paths
  - **Stage II** (1–4.3% true strain): rapid increase to peak ~3.7 GPa at ~4.3% strain; driven by rapid dislocation storage in austenite and B2 grains and accumulation at phase boundaries
  - **Stage III** (4.3–12% true strain): gradual decrease but sustained high work-hardening rate >2.7 GPa; dynamic recovery and LRO domain dissolution reduce dislocation storage capacity, compensated by interfacial dislocation pile-up and HDI hardening

## Mechanistic Interpretation
- **Multiple strengthening mechanisms contributing to yield strength** (quantitative decomposition, Figure 9):
  - Hetero-deformation induced (HDI) strengthening: 597 MPa (dominant contribution, ~45% of total YS)
  - Lattice friction stress of austenite (weighted by f_γ): σ₀,γ·f_γ = 78 MPa
  - Solid solution strengthening in austenite: σ_ss,γ·f_γ = 182 MPa
  - Dislocation strengthening in austenite: σ_dis,γ·f_γ = 85 MPa
  - VC precipitation strengthening (Orowan-type): σ_VC·f_γ = 74 MPa
  - L'1₂ ordered domain strengthening: σ_LRO·f_γ = 119 MPa
  - Lattice friction stress of B2 phase: σ₀,B₂·f_B₂ = 135 MPa
  - Dislocation strengthening in B2: σ_dis,B₂·f_B₂ = 46 MPa
  - Experimental YS (≈1316 MPa) matches sum of individual contributions
- **HDI strengthening mechanism**: Heterogeneous plastic deformation between softer austenite and harder B2 phase generates geometrically necessary dislocations (GNDs) at phase boundaries, producing long-range back stresses in soft domains and forward stresses in hard domains
  - HDI stress measured by loading-unloading-reloading (LUR) tests: increases from ~620 MPa at 1% true strain to ~845 MPa at 10.4% true strain
  - Hysteresis loop area increases from ~70 to ~205 MPa·% and yield drop Δσ_y increases from ~2 to ~23 MPa with increasing strain
- **Strain hardening mechanisms for ductility**:
  - Significant dislocation accumulation capacity in both austenite and B2 phases
  - HDI hardening at austenite/B2 interfaces provides sustained work-hardening
  - GND accumulation at phase boundaries compensates for dynamic recovery and LRO domain dissolution at higher strains
- **Deformation coordination**: EBSD Schmid factor maps (Figure 7) show heterogeneous deformation among individual grains; distinct Schmid factor evolution between γ and B2 phases reflects strain partitioning and coordinated co-deformation; Schmid factor variations explain differences in GND densities among grains
- **Dual-nanoprecipitation roles**: Shearable L'1₂ ordered domains provide dynamic precipitation strengthening but progressively dissolve via dislocation shearing; non-shearable coherent VC nanoprecipitates provide stable Orowan-type strengthening throughout deformation

## Key Quantitative Findings
| Property/Parameter | Value | Condition |
|-------------------|-------|-----------|
| Yield strength | 1316 ± 16 MPa | Room temperature tensile test |
| Ultimate tensile strength | 1458 ± 11 MPa | Room temperature tensile test |
| Total elongation | 11.7% | Room temperature tensile test |
| Austenite volume fraction | ~80% (f_B2 = 20%) | After 900 °C/15 min solution treatment |
| Austenite average grain size | 1.31 μm | Gaussian-fitted, EBSD |
| B2 grain sizes | 1.02 μm (band-like), 3.38 μm (particle-like) | Bimodal distribution, EBSD |
| VC particle size | 19.9 ± 6.2 nm | TEM |
| VC volume fraction | 0.26% | — |
| L'1₂ ordered domain size | 1.0 ± 0.3 nm | TEM |
| L'1₂ ordered domain volume fraction | 11.10% | — |
| Peak work-hardening rate | ~3.7 GPa | ~4.3% true strain (Stage II) |
| Sustained work-hardening rate | >2.7 GPa | Stage III (4.3–12% true strain) |
| HDI stress | 620 MPa → 845 MPa | 1% → 10.4% true strain (LUR) |
| HDI strengthening contribution to YS | 597 MPa | ~45% of total YS |
| GND density (γ, 0% → 6% strain) | 5.36×10¹³ → 2.64×10¹⁴ m⁻² | In-situ EBSD |
| GND density (B2, 0% → 6% strain) | 1.04×10¹⁴ → 2.51×10¹⁴ m⁻² | In-situ EBSD |
| Hysteresis loop area | ~70 → ~205 MPa·% | 1% → 10.4% true strain |
| Yield drop Δσ_y | ~2 → ~23 MPa | 1% → 10.4% true strain |

## Visual Evidence
- **Figure 1**: Processing route and thermodynamic foundation. Panel (a) establishes the complete TMP schedule (1050 °C/1 h homogenization, hot rolling with 85% reduction + water quench, cold rolling 50% reduction with ≤5% per pass, 900 °C/15 min solution treatment + water quench). Panel (b) provides Thermo-Calc equilibrium phase diagram (500–1100 °C) confirming the rationale for 900 °C treatment: κ-carbide dissolution above 750 °C, austenite ~78 vol%, B2 ~20 vol%, low VC fraction.
- **Figure 2**: XRD and EBSD phase/grain characterization. Confirms three-phase constitution (γ, B2, VC). EBSD phase map (green austenite, red B2) shows f_B2 = 20% with B2 existing as strip-like grains and fine boundary particles. IPF maps reveal grain morphologies. Grain size histograms quantify unimodal austenite distribution (1.31 μm) and bimodal B2 distribution (1.02 μm and 3.38 μm).
- **Figure 3**: (S)TEM characterization of dual-nanoprecipitation architecture. STEM-EDS maps confirm elemental distributions and V/Ni enrichment. HRTEM + FFT reveals semi-coherent B2/γ interface ([011]γ // [111]B2). VC nanoprecipitate (19.9±6.2 nm) imaged with coherent [011]γ // [011]VC relationship. Dark-field TEM and inverse FFT visualize L'1₂ ordered nanodomains (1.0±0.3 nm, 11.10 vol%) within austenite.
- **Figure 4**: Tensile mechanical properties. Engineering stress-strain curve yields YS ~1316 MPa, UTS ~1458 MPa, total elongation ~12%. Inset SEM shows ductile dimpled fracture. True stress–strain and work-hardening rate curves delineate three stages: Stage I (sharp drop, 0–1%), Stage II (rapid rise to peak ~3.7 GPa, 1–4.3%), Stage III (gradual decline but maintained >2.7 GPa, 4.3–12%).
- **Figure 5**: LUR test results quantifying HDI strengthening. Six successive hysteresis loops (1–11% engineering strain). HDI stress (σ_HDI) increases from ~620 MPa to ~845 MPa. Hysteresis loop area and yield drop Δσ_y increase monotonically with strain, confirming progressive GND accumulation and long-range back stress development at γ/B2 interfaces.
- **Figure 6**: In-situ EBSD GND density maps (0%, 1%, 3%, 6% strain). GND density in austenite increases from 5.36×10¹³ to 2.64×10¹⁴ m⁻²; B2 from 1.04×10¹⁴ to 2.51×10¹⁴ m⁻². Austenite accumulation rate exceeds B2, overtaking at 6% strain. Heterogeneous GND distributions among grains support HDI strengthening mechanism.
- **Figure 7**: EBSD Schmid factor maps for γ (upper row, scale 0–0.5) and B2 (lower row, scale 0–0.2) at 0%, 1%, 3%, 6% strain. Distinct Schmid factor evolution between phases reflects strain partitioning and coordinated deformation. Observations link Schmid factor variations to GND density differences.
- **Figure 8**: TEM deformation microstructure at 6% and 12% strain. Bright-field images show nonplanar slip bands, dislocation pile-ups at phase boundaries, and bowing-out at 12%. Dark-field + SAED reveal progressive weakening of L'1₂ superlattice reflections. Inverse FFT confirms LRO domain dissolution. VC nanoprecipitates shown impeding dislocation motion at both strain levels.
- **Figure 9**: Stacked bar chart of calculated yield strength contributions. HDI strengthening dominates (597 MPa, red). Other contributions: σ₀,γ·f_γ = 78 MPa, σ_ss,γ·f_γ = 182 MPa, σ_dis,γ·f_γ = 85 MPa, σ_VC·f_γ = 74 MPa, σ_LRO·f_γ = 119 MPa, σ₀,B₂·f_B₂ = 135 MPa, σ_dis,B₂·f_B₂ = 46 MPa. Sum matches experimental YS ≈ 1316 MPa.
