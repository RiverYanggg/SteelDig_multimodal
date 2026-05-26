## Material System
- **Base alloy**: Fe–20Mn–9Al–1.5C (wt%) austenitic low-density steel
- **Alloyed variants studied**:
  - 3Cr: Fe–20Mn–9Al–1.5C–3Cr
  - 2Ni: Fe–20Mn–9Al–1.5C–2Ni
  - 2Ni3Cr: Fe–20Mn–9Al–1.5C–2Ni–3Cr
  - 2Ni5Cr: Fe–20Mn–9Al–1.5C–2Ni–5Cr
- **Matrix phase**: γ-austenite (FCC, single-phase confirmed by XRD and EBSD)
- **Precipitate phases observed**:
  - κ-carbides: E2₁ perovskite structure, ideal stoichiometry (Fe,Mn)₃AlC, cuboidal morphology
  - Ni-rich κ-carbide variant: AlNi₃C type
  - Long-range ordered (LRO) domains: L1₂ structure with ellipsoidal morphology
  - κ′-carbides / L′1₂ metastable phase
- **Density target**: Below 6.8 g/cm³
- **No B2 (BCC) phase detected** in any alloy by XRD

## Processing Route and Variables
- **Homogenization**: 1200°C for 2 h
- **Hot rolling**: 95% reduction to 4 mm thickness
- **Cooling**: Ultra-fast cooling at ~40°C/s following hot rolling
- **Post-processing state**: Fully recrystallized, equiaxed austenitic grains with high fractions of Σ3 twin boundaries
- **Deformation**: Room-temperature tensile testing to various cumulative engineering strains (3%, 5%, 10%, and near-fracture large deformation LD)

## Microstructure and Phase Evolution
- **Grain structure** (EBSD IPF maps, figure_002): Equiaxed fully-recrystallized single-phase FCC austenite; average grain sizes ranging from 3.51 μm to 8.95 μm across the four alloys
- **Phase constitution** (XRD, figure_003): All alloys exhibit only γ(111), γ(200), γ(220), γ(311), γ(222) austenite peaks; no B2 or other secondary intermetallic peaks detected
- **Nanoscale precipitates** (TEM, Figure 2 dark-field images from {110} LRO or {110} κ reflections):
  - **3Cr steel**: Homogeneously distributed LRO domains, average size ~1.75 nm, no κ-carbides
  - **2Ni steel**: Orthorhombic κ-carbides with cuboidal morphology, average size ~10.69 nm (largest among all alloys)
  - **2Ni3Cr steel**: κ-carbides, average size ~5.46 nm
  - **2Ni5Cr steel**: Mixed LRO domains, average size ~2.14 nm; Cr addition suppresses κ-carbide size
- **Ordering evidence** (SAED along [011]γ zone axis, Figure 2): Faint superlattice spots at 1/2{200}γ positions for LRO-containing steels; distinct κ-carbide superlattice reflections for Ni-rich steels
- **Atomic-resolution imaging** (HRTEM + IFFT, figure_004): LRO domains exhibit ellipsoidal morphology; κ-carbides exhibit cuboidal shapes; IFFT images reconstructed using {011} and {100} superlattice reflections

## Processing-Structure-Property Chain
- **Cr effect on precipitation**: Cr addition increases formation energy of κ-carbide → suppresses κ-carbide nucleation → promotes nanoscale LRO domains (~1.75–2.14 nm) instead
- **Ni effect on precipitation**: Ni addition reduces formation energy (AlNi₃C: –0.181 eV/atom by DFT) → promotes κ-carbide precipitation → larger coherent κ-carbides (up to ~10.69 nm in 2Ni steel)
- **Ni–Cr synergy**: 2Ni3Cr yields intermediate precipitate size (~5.46 nm κ-carbides); 2Ni5Cr yields fine LRO domains (~2.14 nm)
- **Strength hierarchy**: 2Ni (YS 1202 MPa, UTS 1283 MPa) > 2Ni3Cr (YS ~1110 MPa, UTS ~1206 MPa) > 2Ni5Cr > 3Cr (YS 969 MPa, UTS 1141 MPa)
- **Ductility hierarchy**: 3Cr (TEL ~54.4%) > 2Ni5Cr > 2Ni3Cr (TEL ~45.9%) > 2Ni (TEL ~34.1%)
- **Strength–ductility product**: 2Ni3Cr achieves balanced performance with TS×TEL reaching ~62.07 GPa·%, placing it in the superior strength–ductility synergy region compared to literature data for Fe–Al, Fe–Mn, Fe–Mn–C, Fe–Mn–Al–C, and stainless steels (Figure 4d)
- **Deformation substructure evolution** (TEM, figures 5-8):
  - **3Cr steel**: Initial planar dislocation slip on {111} slip bands with Schmid factor 0.52 at 3% strain → high-density dislocation arrays (HDDA) with narrower slip band spacing and multiple slip systems (1-11) and (11-1) activated at 10% strain → deformation twins (~dozen nm width) and stacking faults (~dozen nm width) appear only at very high strain near fracture (54% LD)
  - **2Ni steel**: (111) planar slip bands at 5% strain → multiplication and reduced spacing of slip bands at 10% strain → high dislocation densities, very fine slip bands, and occasional stacking faults near final failure; no deformation twins observed
- **Fracture mode** (SEM, figure_006): All alloys exhibit ductile dimple fracture; 2Ni shows finer and shallower dimples; 3Cr, 2Ni3Cr, and 2Ni5Cr show deeper, more developed dimples consistent with higher ductility

## Mechanistic Interpretation
- **Precipitation threshold control**: Ni alloying lowers E2₁ κ-carbide formation energy, promoting precipitation; Cr alloying raises formation energy, suppressing κ-carbide nucleation and favoring LRO nanodomains below a critical transition radius (approximately 1.1 nm for 3Cr, 0.9 nm for 2Ni5Cr)
- **Strengthening mechanism decomposition** (stacked bar chart, Figure 11): Four contributions evaluated:
  - Lattice friction stress (σ₀): Minor contribution
  - Grain boundary strengthening (σ_gb): Moderate contribution, grain sizes 3.51–8.95 μm
  - Solid solution strengthening (σ_ss): Dominant contribution across all alloys
  - Precipitation strengthening (σ_prep): Peaks in 2Ni, varies significantly between alloys
  - Calculated sum agrees well with experimental yield strength
- **Precipitation hardening mechanisms** (Figure 10): Below critical transition radius, ordering strengthening (σ_order) operates; above critical radius, coherency + modulus mismatch strengthening (σ_coh + σ_mod) dominates; 2Ni steel shows highest σ_coh+σ_mod (~39 MPa at ~4.7 nm radius)
- **Work hardening behavior** (strain hardening rate curves, Figure 4c and 12):
  - Three stages identified: Stage I (sharp decrease), Stage II (increasing trend, prolonged with increasing Cr), Stage III (final decrease)
  - 3Cr steel: Higher plateau (~2000 MPa) sustained to higher true strain (~0.4); HDDA densification + dynamic slip band refinement (DSBR) provide sustained strain hardening
  - 2Ni steel: Lower plateau (~1400 MPa) with earlier failure at ~0.25 strain; planar slip mediated deformation
  - 2Ni5Cr maintains higher work hardening rates than 2Ni and 2Ni3Cr in Stage III
- **DSBR and HDDA effects** (Cr-promoted): Cr alloying promotes dynamic slip band refinement, activates secondary slip systems, and generates high-density dislocation arrays → delays necking instability → enhances uniform elongation and overall ductility

## Key Quantitative Findings
- **Grain sizes**: 3.51–8.95 μm (fully recrystallized equiaxed grains)
- **Precipitate sizes**: 3Cr LRO ~1.75 nm; 2Ni κ-carbide ~10.69 nm; 2Ni3Cr κ-carbide ~5.46 nm; 2Ni5Cr LRO ~2.14 nm
- **Critical transition radius for strengthening mechanism shift**: ~1.1 nm (3Cr), ~0.9 nm (2Ni5Cr)
- **Tensile properties**:
  - 3Cr: YS 969 MPa, UTS 1141 MPa, TEL ~54.4%
  - 2Ni: YS 1202 MPa, UTS 1283 MPa, TEL ~34.1%
  - 2Ni3Cr: YS ~1110 MPa, UTS ~1206 MPa, TEL ~45.9%
  - 2Ni5Cr: Intermediate strength and ductility (exact values from stress-strain curves in Figure 4a)
- **Strength–ductility product**: TS×TEL up to ~62.07 GPa·% for 2Ni3Cr
- **DFT formation energy** for Ni-rich κ-carbide (AlNi₃C): –0.181 eV/atom
- **Work hardening plateaus**: 3Cr ~2000 MPa sustained to ε_true ~0.4; 2Ni ~1400 MPa to ε_true ~0.25
- **Precipitation hardening contribution**: σ_coh+σ_mod peaks at ~39 MPa (2Ni at ~4.7 nm radius); σ_order contributes only at small precipitate radii
- **Density**: Below 6.8 g/cm³ (design target)
- **Deformation twins in 3Cr**: Width ~dozen nanometers, appear only near final failure at 54% strain
- **Stacking faults in 3Cr**: Width ~dozen nanometers, near final failure

## Visual Evidence
- **Figure 2 (EBSD + TEM microstructure)**: IPF maps (a1-d1) and phase maps (a2-d2) confirm equiaxed fully-recrystallized single-phase austenite for all four alloys, with grain sizes 3.51–8.95 μm. TEM bright-field (e-h) confirms single-phase γ; dark-field images (i-l) from {110} LRO or {110} κ reflections reveal homogeneously distributed LRO nanodomains (3Cr, 2Ni5Cr) versus cuboidal κ-carbides (2Ni, 2Ni3Cr). SAED patterns (m-p) along [011]γ show faint superlattice spots at 1/2{200}γ for LRO-containing steels and distinct κ-carbide reflections for Ni-rich steels, confirming atomic ordering differences.
- **Figure 3 (XRD)**: All four alloys show only γ(111), γ(200), γ(220), γ(311), γ(222) peaks; no B2 phase detected; similar peak positions across compositions confirm single-phase FCC structure regardless of alloying.
- **Figure 4 (HRTEM + IFFT + size chart)**: Atomic-resolution images along [011]γ zone axis with FFT insets showing superlattice reflections; IFFT images (b,d,f,h) highlight ellipsoidal LRO domains (yellow ellipses, 3Cr, 2Ni5Cr) and cuboidal κ-carbides (2Ni, 2Ni3Cr); bar chart (i) quantifies average sizes: 10.69 nm (2Ni), 5.46 nm (2Ni3Cr), 2.14 nm (2Ni5Cr), 1.75 nm (3Cr).
- **Figure 5 (Tensile properties)**: Engineering stress-strain curves (a) show strength-ductility trade-off across alloys; true stress-strain curves (b); strain hardening rate curves (c) identify Stages I-III with prolonged Stage II for Cr-rich alloys; YS vs TS×TEL comparison (d) shows Ni&Cr-alloyed steels (red stars) achieve superior trade-off up to ~62.07 GPa·% and enhanced YS compared to literature data.
- **Figure 6 (Fracture SEM)**: All alloys exhibit ductile dimple fracture; 2Ni shows finer/shallower dimples; 3Cr, 2Ni3Cr, 2Ni5Cr show deeper dimples correlating with higher elongation (45.9–54.4%).
- **Figure 7 (TEM, 3Cr deformation)**: At 3% strain: planar dislocation multipoles in {111} slip bands, Schmid factor 0.52; at 10% strain: HDDA in (1-11) and (11-1) slip bands with reduced spacing; near failure (54% LD): deformation twins and stacking faults (~dozen nm) appear; SAED patterns confirm austenite matrix.
- **Figure 8 (TEM, 2Ni deformation)**: At 5% strain: (111) planar slip bands; at 10% strain: multiplied and refined slip bands; near failure: high dislocation densities and occasional stacking faults, no deformation twins.
- **Figure 9 (TEM, 2Ni κ-carbides near failure)**: Dark-field image (a) shows cuboidal κ-carbide distribution (~10.69 nm); HRTEM (b) confirms atomic-scale crystallography; precipitates remain stable near fracture.
- **Figure 10 (DFT crystal structures)**: Disordered γ (FCC, Fe/Mn and Al random), ordered γ (Al at vertices), κ-carbide E2₁ perovskite with C at octahedral interstitials, and AlNi₃C variant with Ni substituting Fe/Mn; formation energies from Materials Project DFT (GGA-PBE).
- **Figure 11 (Precipitation hardening histograms)**: σ_order (green) dominates at small radii below critical transition (~1.1 nm 3Cr, ~0.9 nm 2Ni5Cr); σ_coh+σ_mod (orange) dominates above critical size, peaking at ~39 MPa for 2Ni at ~4.7 nm.
- **Figure 12 (Yield strength decomposition)**: Stacked bar chart showing σ₀, σ_gb, σ_ss, σ_prep contributions; σ_ss is dominant; σ_prep peaks in 2Ni; calculated sum matches experimental values (brown circles).
- **Figure 13 (Strain hardening + microstructure schematic)**: 3Cr shows higher plateau (~2000 MPa) with HDDA, twins, and stacking faults; 2Ni shows lower plateau (~1400 MPa) with planar slip and limited stacking faults; schematic insets illustrate microstructural evolution at low, medium, and high strains.
