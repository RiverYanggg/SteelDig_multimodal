# Material System

The investigated material is a fully austenitic Fe-Mn-Al-C low-density steel with the following composition:

- **Nominal composition**: Fe-31Mn-9Al-1C-0.45Nb-0.45Mo-0.45W (wt%)
- **Actual composition**: Fe-30.9Mn-8.7Al-0.9C-0.45Nb-0.45Mo-0.43W (wt%)

Three hot-rolled samples are designated according to their thickness reduction ratio:
- **HR45**: 45% hot-rolling reduction (final thickness 60 mm)
- **HR68**: 68% hot-rolling reduction (final thickness 35 mm)
- **HR82**: 82% hot-rolling reduction (final thickness 20 mm)

# Processing Route and Variables

- **Starting billet thickness**: 110 mm
- **Reheating temperature before rolling**: 1150 °C
- **Hot-rolling passes**: 4 passes (HR45), 6 passes (HR68), 9 passes (HR82), producing reductions of 45%, 68%, and 82%, respectively
- **Cooling after rolling**: water quenching to room temperature

# Microstructure and Phase Evolution

**Matrix phase**: The steel maintains a fully austenitic (FCC) microstructure across all hot-rolling reductions. EBSD band contrast maps reveal equiaxed FCC austenite grains with abundant annealing twins (figure_002). Phase maps confirm essentially single-phase FCC austenite.

**Grain structure evolution with increasing reduction** (figure_002, figure_009 panel a):
- HR45: mean grain size (excluding twins) ~45 μm, effective grain size (including twin boundaries) 21.82 μm
- HR68: effective grain size 11.55 μm
- HR82: mean grain size (excluding twins) ~19 μm, effective grain size 7.02 μm
- Twin boundary fraction decreases from 67% (HR45) to 52% (HR82), but the effective grain size still refines substantially due to increased high-angle grain boundary density

**Dislocation density** (figure_002 KAM maps, figure_009 panel a):
- HR45: 2.71 × 10¹³ m⁻² (geometrically necessary dislocation density)
- HR82: 9.87 × 10¹³ m⁻²
- Increasing hot-rolling reduction progressively elevates local strain concentrations and geometrically necessary dislocation density, as shown by Kernel Average Misorientation maps

**Precipitate phases**:
- **(Nb,Mo,W)C carbides** (figures 003, 004): Micron-sized polygonal particles (1–25 μm) aligned along rolling direction, and submicron-sized (~260 nm) particles homogeneously distributed within the austenite matrix. TEM-EDS confirms strong Nb enrichment and Mo/W presence; SAED along [110] zone axis confirms FCC MC-type carbide structure with lattice parameter 4.36 Å. Volume fraction ~0.2%, independent of rolling reduction.
- **κ-carbides** (figure_005): Nano-sized ordered L′1₂-type κ-carbides formed via spinodal decomposition during water quenching, revealed by faint (001) and (010) superlattice reflections in SAED along [100] zone axis. Dark-field imaging shows homogeneous distribution. Mean sizes: HR45: 0.81 ± 0.26 nm; HR68: 0.78 ± 0.17 nm; HR82: 0.83 ± 0.23 nm. Volume fractions: HR45: 3.5 ± 0.33%; HR68: 3.3 ± 0.52%; HR82: 3.9 ± 0.39%. Neither size nor volume fraction of κ-carbides changes significantly with increasing rolling reduction (figure_009 panel b).

# Processing-Structure-Property Chain

**Processing → Structure**: Increasing hot-rolling reduction from 45% to 82% (through increased number of rolling passes from 4 to 9, at the same reheating temperature of 1150 °C followed by water quenching) promotes dynamic recrystallization and progressive grain refinement (effective grain size decreases from 21.82 μm to 7.02 μm), while simultaneously accumulating geometrically necessary dislocations (from 2.71 × 10¹³ to 9.87 × 10¹³ m⁻²). The (Nb,Mo,W)C particles serve as preferential nucleation sites for particle-stimulated nucleation during dynamic recrystallization. Both κ-carbide and (Nb,Mo,W)C precipitate populations remain essentially invariant with reduction ratio.

**Structure → Properties** (figure_006, figure_008):
- HR45 (effective grain size 21.82 μm): yield strength ~480 MPa, ultimate tensile strength ~861 MPa, total elongation ~60%, uniform elongation ~52%, Charpy impact energy 133 ± 2.5 J/m²
- HR68 (effective grain size 11.55 μm): intermediate values linking HR45 and HR82
- HR82 (effective grain size 7.02 μm): yield strength ~648 MPa, ultimate tensile strength ~976 MPa, total elongation ~50%, uniform elongation ~39%, Charpy impact energy 105 ± 1.2 J/m²
- Increase in yield strength: ~170 MPa; increase in UTS: ~110 MPa from HR45 to HR82
- Ductility decreases modestly: total elongation from ~60% to ~50%, uniform elongation from ~52% to ~39%
- All samples retain reduction of area exceeding 60% and toughness above 100 J/m²

**Fracture behavior** (figure_007): All samples exhibit ductile fracture with dimples and microvoids. Microvoids nucleate via debonding of intragranular (Nb,Mo,W)C particles. Dimple size in HR45 is visibly larger than in HR68 and HR82, correlating with larger grain size.

**Comparison to benchmarks** (figure_008): The investigated Fe-Mn-Al-C steel with hot-rolling grain refinement achieves superior strength–ductility–toughness combinations compared to solution-treated austenitic stainless steels and conventional age-hardened Fe-Mn-Al-C steels, which show comparable strength but markedly inferior ductility (~21%) and toughness at equivalent yield strength levels.

**Strain-hardening behavior** (figure_011): All samples exhibit a characteristic three-stage strain-hardening response: Stage I (sharp drop after yielding), Stage II (gradual increase to peak values), Stage III (continuous decrease until fracture). Increasing hot-rolling reduction raises strain-hardening rates across the entire plastic strain range, which contributes to excellent ductility despite higher strength.

# Mechanistic Interpretation

**Strengthening mechanisms** (figure_010): Quantitative analysis decomposes the measured yield strength into contributions from:
- Friction stress σ₀ = 203.1 MPa (from Hall-Petch fitting)
- Precipitate strengthening: shearable κ-carbide contribution (σp-shearing) and Orowan bypass contribution from (Nb,Mo,W)C (σp-Orowan), both unchanged across reductions
- Dislocation strengthening σds, increasing with rolling reduction
- Grain boundary strengthening σgb, dominating the strength increment

The Hall-Petch coefficient is determined as 733.4 MPa·μm^(1/2). Grain boundary strengthening (including both high-angle grain boundaries and annealing twin boundaries) is the dominant strengthening contributor, while dislocation strengthening provides a substantial secondary contribution. The calculated total yield strengths show good agreement with experimental values, confirming that the strength improvement with increasing hot-rolling reduction is primarily attributable to grain boundary and dislocation strengthening, with precipitate strengthening remaining constant.

**Ductility and strain-hardening rationalization** (figures 012, 013):
- At low strains (εe ≈ 0.1), homogeneous planar slip bands and Taylor lattices form via intersecting non-coplanar {111} slip traces
- Slip band spacing decreases with increasing plastic strain in all samples, eventually saturating at approximately 50 nm
- HR82 (finer initial grains) starts with smaller slip band spacing (68.05 ± 8.91 nm at strain 0.1) vs. HR45 (296.40 ± 50.06 nm); the finer-grained samples exhibit faster slip band refinement kinetics and earlier saturation
- At intermediate strains (εe ≈ 0.2), slip bands become more closely spaced; microbands begin to form earlier in HR68 and HR82 than in HR45
- At higher strains (εe ≈ 0.4), well-developed microbands with distinct boundaries dominate the microstructure
- The earlier saturation of slip band refinement and earlier microband formation in finer-grained samples reduces the duration of Stage II strain hardening, providing the mechanistic explanation for the minor decrease in uniform elongation from 52% to 39% with increasing rolling reduction
- Higher accumulated back stress on dislocation sources in smaller grains accelerates the evolution of deformation substructure

# Key Quantitative Findings

- **Grain size** (effective, including twins): 21.82 μm (HR45) → 11.55 μm (HR68) → 7.02 μm (HR82)
- **Dislocation density**: 2.71 × 10¹³ m⁻² (HR45) → 9.87 × 10¹³ m⁻² (HR82)
- **κ-carbide**: size ~0.8 nm, volume fraction ~3.5%, invariant with reduction
- **(Nb,Mo,W)C**: size ~260 nm (submicron) and 1–25 μm (micron-sized), volume fraction ~0.2%, invariant with reduction
- **Yield strength**: ~480 MPa (HR45) → ~648 MPa (HR82), Δ ≈ 170 MPa
- **Ultimate tensile strength**: ~861 MPa (HR45) → ~976 MPa (HR82), Δ ≈ 110 MPa
- **Total elongation**: ~60% (HR45) → ~50% (HR82)
- **Uniform elongation**: ~52% (HR45) → ~39% (HR82)
- **Charpy impact energy**: 133 ± 2.5 J/m² (HR45) → 105 ± 1.2 J/m² (HR82)
- **Friction stress σ₀**: 203.1 MPa
- **Hall-Petch coefficient**: 733.4 MPa·μm^(1/2)
- **Slip band spacing saturation**: ~50 nm across all samples
- **Slip band spacing at εe ≈ 0.1**: 296.40 ± 50.06 nm (HR45) vs. 68.05 ± 8.91 nm (HR82)

# Visual Evidence

**figure_002 (EBSD characterization):** Band contrast maps (a–c) show equiaxed FCC austenite grains with annealing twins, demonstrating progressive grain refinement from HR45 to HR82. Phase maps with grain boundary networks (d–f) reveal decreasing twin boundary fraction (67% to 52%) but reduced effective grain sizes (21.82 μm to 7.02 μm). KAM maps (g–i) display elevated local strain concentrations and higher geometrically necessary dislocation densities in HR82, supporting the increase in measured dislocation density from 2.71 × 10¹³ to 9.87 × 10¹³ m⁻².

**figure_003 (SEM of second-phase particles):** BSE images at low magnification (a–c) show micron-sized polygonal (Nb,Mo,W)C aligned along rolling direction; high-magnification images (d–f) reveal submicron-sized (~260 nm) particles homogeneously distributed in the austenite matrix. The particle distributions are comparable across HR45, HR68, and HR82.

**figure_004 (TEM of submicron precipitate):** Bright-field image (a) shows ~200–300 nm particle; EDS mapping (b–h) confirms Nb enrichment and Mo/W presence with Fe/Mn/Al depletion, identifying it as (Nb,Mo,W)C; SAED (i) along [110] zone axis confirms FCC MC-type carbide with lattice parameter 4.36 Å.

**figure_005 (TEM of κ-carbides):** SAED patterns (a–c) along [100] zone axis show faint (001) and (010) superlattice reflections marking L′1₂-type ordered κ-carbides in all three samples. Dark-field images (d–f) reveal nano-sized precipitates (~0.8 nm) with uniform distribution and comparable sizes/volume fractions independent of rolling reduction.

**figure_006 (Mechanical properties):** Engineering stress-strain curves (a) show HR82 achieving the highest strength (YS ~648 MPa, UTS ~976 MPa) with total elongation ~50%, while HR45 shows lowest strength but highest ductility (~60%). Charpy impact energy (b) decreases linearly from 133 to 105 J/m² with increasing reduction.

**figure_007 (Fractography):** All samples exhibit ductile dimple fracture with microvoids nucleated at (Nb,Mo,W)C particles. HR45 shows visibly larger dimples than HR68 and HR82, correlating with its larger grain size. Ductile fracture characteristics are retained across all conditions.

**figure_008 (S–E–T trade-off):** Scatter plot demonstrates the strength–elongation–toughness balance for HR45, HR68, and HR82. The investigated steel maintains 50–60% total elongation and >100 J/cm² Charpy energy as yield strength increases from ~480 to ~648 MPa, outperforming solution-treated austenitic stainless steels and conventional age-hardened Fe-Mn-Al-C alloys at comparable strength levels.

**figure_009 (Microstructural evolution trends):** Panel (a) quantifies grain size reduction (mean: ~45 to ~19 μm; effective: ~22 to ~7 μm) and dislocation density increase (2.7 × 10¹³ to 9.9 × 10¹³ m⁻²) with increasing reduction. Panel (b) confirms κ-carbide (~3.5 vol%, ~0.8 nm) and (Nb,Mo,W)C (~0.2 vol%, ~260 nm) remain essentially constant.

**figure_010 (Strengthening mechanism quantification):** Hall-Petch plot (a) extracts σ₀ = 203.1 MPa and k = 733.4 MPa·μm^(1/2). Stacked bar chart (b) decomposes yield strength contributions, showing grain boundary strengthening dominates and increases most significantly from HR45 to HR82, with dislocation strengthening as the secondary contributor. Calculated values agree with experimental yield strengths.

**figure_011 (Strain-hardening curves):** True stress–strain curves with strain-hardening rate plots reveal characteristic three-stage behavior. Strain-hardening rates increase with rolling reduction and maintain ~2000 MPa over a wide plastic strain range.

**figure_012 (Deformation substructure TEM):** BF images at εe = 0.1, 0.2, and 0.4 document evolution from planar slip bands and Taylor lattices (εe = 0.1) to closely spaced slip bands with incipient microbands at εe = 0.2 (earlier in HR68 and HR82), to well-developed microbands at εe = 0.4. Finer initial grains accelerate deformation substructure evolution.

**figure_013 (Slip band spacing evolution):** Slip band spacing decreases with strain and saturates at ~50 nm for all samples. HR82 starts with smallest spacing (68.05 nm at εe = 0.1 vs. 296.40 nm for HR45) and saturates earliest, supporting faster slip band refinement kinetics and earlier microband formation in finer-grained samples.
