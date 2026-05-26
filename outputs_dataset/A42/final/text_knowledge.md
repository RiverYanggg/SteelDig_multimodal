# Material System
Fe-30Mn-9Al-0.8C low-density austenitic steel, solution-treated initial state (MAF-0) with coarse grains (~50 μm).

# Processing Route and Variables
**Process:** Warm multiaxial forging (MAF) at 250 °C.  
**Sample designations and cumulative strain:** MAF-0 (0 pass, reference undeformed), MAF-1 (1 pass, equivalent strain ~0.47), MAF-3 (3 passes, equivalent strain ~1.4), MAF-5 (5 passes, equivalent strain ~2.34).  
**Per-pass conditions:** Normal strain per pass 33%; sequential compression along three orthogonal directions with 90° sample rotations between compressions.  
**Blank dimensions (pre-forging):** 20 × 20 × 30 mm; tensile specimens were machined from forged billets with gauge length 16 mm, gauge diameter 4 mm.  
**Note:** The billet fractured during a sixth pass attempt.

# Microstructure and Phase Evolution
**Phase constitution:** Austenitic γ-phase throughout deformation; κ-carbide peaks persist in XRD patterns of all conditions (MAF-0 through MAF-5), indicating unchanged carbide phases during MAF at 250 °C.  
**Grain size (EBSD):** Mean grain size refines from ~50 μm (MAF-0, solutionized) to ~13 μm after 5 passes (MAF-5). Grain size as a function of equivalent plastic strain follows an exponential decay relation d = 50 × exp(−0.64ε) with R² = 0.991.  
**Dislocation density (XRD):**  
- MAF-0: 0.79 × 10¹⁵ m⁻²  
- MAF-1: increases relative to MAF-0  
- MAF-3: further increase  
- MAF-5: 8.98 × 10¹⁵ m⁻²  
Dislocation density evolution with equivalent plastic strain fits ρ = ρ₀ + k₁(1−exp(−k₂ε)), with ρ₀ = 7.96 × 10¹⁴ m⁻², k₁ = (7.91 ± 0.53) × 10¹⁵ m⁻², k₂ = 1.81 ± 0.42, R² = 0.986.  
**Grain boundary character (EBSD):** High-angle boundary fraction first drops from 0.62 (MAF-0) to 0.29 (MAF-1) and 0.24 (MAF-3), then rises to 0.69 after 5 passes, indicating conversion of low-angle boundaries to high-angle boundaries at higher strains.  
**Texture evolution (EBSD IPF maps, normal/pressing direction):** Strong initial [101] texture in MAF-0 becomes progressively randomized with increasing MAF passes.  
**Kernel Average Misorientation (KAM) from EBSD:** Average KAM increases from 0.34° (MAF-0) → 0.72° (MAF-1) → 0.87° (MAF-3) → 1.07° (MAF-5), consistent with geometrically necessary dislocation accumulation.

# Processing-Structure-Property Chain
- **MAF-0 → 0 pass, ε_eq ≈ 0:** Coarse austenite grains ~50 μm; lowest dislocation density; sharp XRD peaks; yield strength ~380 MPa; UTS 762 MPa; total elongation ~75%; large work hardening (UTS − YS ≈ 382 MPa).  
- **MAF-1 → 1 pass, ε_eq ≈ 0.47:** Grain refinement begins; dislocation density rises; yield strength reaches 1040 MPa; UTS 1368 MPa; elongation drops to ~30%.  
- **MAF-3 → 3 passes, ε_eq ≈ 1.4:** Grain size further reduced; dislocation density continues to increase; yield strength 1279 MPa; UTS 1415 MPa; elongation ~13.7%.  
- **MAF-5 → 5 passes, ε_eq ≈ 2.34:** Grain size refined to ~13 μm; dislocation density reaches 8.98 × 10¹⁵ m⁻²; yield strength 1528 MPa; UTS 1548 MPa; work hardening capacity nearly exhausted (only ~20 MPa); uniform elongation decreases to ~0.8%, total elongation ~8%.  
**Causal link:** The progressive increase in MAF passes at 250 °C produces rising equivalent strain, which drives grain refinement and dislocations accumulation. These microstructural changes cause monotonic yield/ultimate strength increase while drastically reducing ductility and work hardening capacity. Grain refinement and dislocation density evolution are captured quantitatively and incorporated into the modified J-C model.

# Mechanistic Interpretation
**Dominant strengthening mechanisms (as passes increase):**  
- Dislocation strengthening: dislocation density rises from 0.79 to 8.98 × 10¹⁵ m⁻², contributing to elevated flow stress.  
- Grain boundary strengthening: grain refinement from ~50 to ~13 μm increases Hall-Petch-type contribution.  
- The κ-carbide precipitation contribution is regarded as unchanged because the phase persists unchanged.  
**Ductility loss with increasing passes:** Diminishing work-hardening rate is linked to the exhaustion of dislocation storage capacity and the conversion of low-angle boundaries to high-angle boundaries at high strains were grain boundary strengthening becomes increasingly important.  
**Modified Johnson-Cook model:** The constitutive law incorporates strain-dependent dislocation density (Eq. 7) and grain size (Eq. 8). FE simulations (ABAQUS VUMAT) predict yield strength close to experiment up to 3 passes. At 5 passes, the simulation under-predicts yield strength (simulated ~1450 MPa vs. experimental ~1528 MPa), which the authors attribute to the model omission of texture effects, and at this stage grain boundary strengthening is proposed to contribute more than previously.

# Key Quantitative Findings
- Tensile yield strength increases from ~380 MPa (MAF-0) to 1528 MPa (MAF-5); UTS from 762 MPa to 1548 MPa.  
- Total elongation decreases from ~75% (MAF-0) to ~8% (MAF-5); uniform elongation to ~0.8% at MAF-5.  
- Dislocation density rises from 0.79 × 10¹⁵ m⁻² (MAF-0) to 8.98 × 10¹⁵ m⁻² (MAF-5) (XRD).  
- Grain size refines from ~50 μm (MAF-0) to ~13 μm (MAF-5), following d = 50 exp(−0.64ε) with R² = 0.991.  
- Dislocation density evolution fit: ρ = ρ₀ + k₁(1−exp(−k₂ε)), R² = 0.986, with ρ₀ = 7.96 × 10¹⁴ m⁻², k₁ = (7.91 ± 0.53) × 10¹⁵ m⁻², k₂ = 1.81 ± 0.42.  
- High-angle grain boundary fraction: 0.62 (MAF-0) → 0.29 (MAF-1) → 0.24 (MAF-3) → 0.69 (MAF-5).  
- KAM average: 0.34° (MAF-0) → 0.72° (MAF-1) → 0.87° (MAF-3) → 1.07° (MAF-5).  

# Visual Evidence
- **figure_001** (property_mechanical, engineering stress–strain curves): Demonstrates the strength–ductility trade-off across MAF-0/1/3/5. Yield strength ~380 → 1040 → 1279 → 1528 MPa; UTS 762 → 1368 → 1415 → 1548 MPa; elongation ~75% → ~30% → ~13.7% → ~8%. Work hardening capacity drops from ~382 MPa to ~20 MPa.  
- **figure_002** (schematic of MAF processing): Defines the 3-stage compression sequence with 90° rotations, per-pass strain, and coordinate system, linking the processing route directly to the sample history used for all microstructural and property data.  
- **figure_003** (sample photographs): Shows forged billets and machined miniature tensile specimens for MAF-1/3/5, confirming successful processing to equivalent strains up to ~2.34 at 250 °C before the sixth-pass fracture.  
- **figure_004** (sample geometry schematics): Standardizes specimen extraction and tensile geometry (gauge length 16 mm, diameter 4 mm), locating the analysis area at the core of MAF samples.  
- **figure_005** (FE mesh): Supports the ABAQUS model setup (C3D8R elements, 0.6 mm mesh, 0.15 friction coefficient) used to simulate plastic flow with the modified J-C model.  
- **figure_006** (XRD patterns): Confirms austenitic γ-phase and persistent κ-carbide peaks; demonstrates peak broadening with increasing MAF passes, consistent with grain refinement and dislocation density increase from 0.79 to 8.98 × 10¹⁵ m⁻².  
- **figure_007** (dislocation density vs. equivalent strain): Provides the experimentally measured dislocation density points (MAF-0/1/3/5) and the nonlinear fit (Eq. 7) with R² = 0.986, directly underpinning the dislocation term in the constitutive model.  
- **figure_008** (EBSD image quality + IPF maps): Visually traces grain refinement, boundary misorientation evolution (HAB fraction 0.62 → 0.29 → 0.24 → 0.69), and texture randomization from MAF-0 through MAF-5.  
- **figure_009** (grain size distribution + size vs. strain): Quantitatively validates grain size evolution, confirming d = 50 exp(−0.64ε) with R² = 0.991, used as Eq. 8 in the constitutive model.  
- **figure_010** (KAM maps from EBSD): Maps geometrically necessary dislocation accumulation (KAM_avg from 0.34° to 1.07°) with increasing MAF passes, providing independent support for dislocation strengthening.  
- **figure_011** (engineering stress–strain curves, separate figure instance): Reiterates the full set of strength–elongation values and the complete loss of work hardening in MAF-5.  
- **figure_012** (VUMAT flow chart): Documents the FE implementation strategy for the modified J-C model including SDV tracking of equivalent strain, dislocation density, grain size, and flow stress.  
- **figure_013** (FE contour maps of strain, dislocation density, grain size, flow stress): Validates the spatial heterogeneity predicted by the model: highest strain/dislocation density/flow stress and finest grains concentrate in the central region.  
- **figure_014** (experimental vs. simulated yield strength): Directly compares experiment and FE simulation across MAF passes: strong agreement up to 3 passes, with underprediction at 5 passes (~1450 vs. 1528 MPa) attributed to texture effects not included in the model.  
- **figure_015** (FE yield strength distribution maps): Shows increasing yield strength magnitude and center-to-surface gradient with MAF passes, predicted from the coupled microstructure-based constitutive model.
