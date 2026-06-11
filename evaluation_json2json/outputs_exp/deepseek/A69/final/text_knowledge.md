# Material System
- Fe–Mn–Al ternary alloy series: Fe₁₋ₓMnₓAl with Mn fraction x = 0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1, spanning from FeAl to MnAl.
- Crystal structure: B2 ordered cubic (CsCl-type), space group Pm-3m. Al atoms occupy corner sites (one simple cubic sublattice), while Fe and Mn atoms randomly substitute on the body‑center sublattice, maintaining full solid solubility across the entire composition range.

# Processing Route and Variables
- **Virtual processing variable:** Mn content x in Fe₁₋ₓMnₓAl, i.e., systematic replacement of Fe by Mn on the B2 body‑center sublattice.
- **DFT calculation settings:** CASTEP code, GGA‑PBE exchange‑correlation functional, ultrasoft pseudopotentials, plane‑wave kinetic energy cutoff 450 eV, Brillouin zone integration with 8×8×8 Monkhorst‑Pack k‑point mesh.

# Microstructure and Phase Evolution
- All compositions retain the B2 ordered cubic structure (Pm-3m); no phase transition occurs.
- Increasing x only changes the statistical occupation of the Fe/Mn sublattice, i.e., the local chemical environment evolves from pure Fe–Al pairs to mixed Fe/Mn–Al pairs and finally to pure Mn–Al pairs, without altering lattice symmetry.

# Processing-Structure-Property Chain
**Process → Structure**
- Mn fraction (x) is increased from 0 to 1 → Mn progressively substitutes Fe on the body‑center sublattice of the B2 FeAl lattice while preserving the Pm‑3m space group.

**Structure → Electronic Structure**
- **Electronic density of states:** The total DOS at the Fermi level remains non‑zero for all x, confirming metallic conductivity. The occupied states near the Fermi level derive predominantly from Fe‑d and Mn‑d states mixed with Al‑p states (from −5 eV to 1 eV), indicating a combination of covalent hybridization and metallic delocalization.
- **Electron density maps:** Contours elongated along the Al–Fe/Mn bond axes (Figure 011) directly visualize covalent bonding; difference maps show electron accumulation in the interstitial region (metallic character) and localization around atomic cores.

**Structure → Thermodynamic Stability**
- Formation enthalpy ΔHf and cohesive energy Ecoh become less negative with increasing Mn content.
  - FeAl (x=0): ΔHf = −0.391 eV/atom, Ecoh = −6.947 eV/atom (most stable).
  - MnAl (x=1): ΔHf ≈ −0.22 eV/atom, Ecoh ≈ −6.58 eV/atom (least stable).
- Negative values for all compositions confirm thermodynamic stability of the entire series.

**Structure → Mechanical Properties (Elastic Constants and Moduli)**
- **Bulk modulus B:** Decreases nearly monotonically from ∼187 GPa (FeAl) to ∼170 GPa (MnAl).
- **Shear modulus G and C₄₄:** Exhibit a V‑shaped (non‑monotonic) dependence, both reaching minima at the equiatomic composition Fe₀.₅Mn₀.₅Al.
  - Fe₀.₅Mn₀.₅Al: G ≈ 77 GPa, C₄₄ ≈ 126 GPa (lowest stiffness, highest compressibility).
- **Young’s modulus E and tetragonal shear C₁₁−C₁₂:** Show the same V‑shape trend:
  - FeAl: E ≈ 296 GPa, C₁₁−C₁₂ ≈ 160 GPa.
  - Fe₀.₅Mn₀.₅Al: E ≈ 202 GPa, C₁₁−C₁₂ ≈ 73 GPa.
- **Ductility indicators:**
  - Poisson’s ratio ν and the Pugh ratio B/G increase from FeAl (ν ≈ 0.236, B/G ≈ 1.56, brittle) to a maximum at Fe₀.₅Mn₀.₅Al (ν ≈ 0.309, B/G ≈ 2.28, ductile) and finally rise again for MnAl (ν ≈ 0.324, B/G ≈ 2.52). According to the Pugh criterion (B/G > 1.75 = ductile), all alloys with x ≥ 0.25 become ductile.

**Structure → Elastic Anisotropy**
- Universal anisotropy index Aᵁ and shear anisotropic index AꜬ follow a similar non‑monotonic trend.
  - FeAl (x=0) shows the lowest anisotropy (Aᵁ ≈ 0.56).
  - MnAl (x=1) exhibits the highest anisotropy (Aᵁ ≈ 3.8).
- 3 D Young’s modulus surfaces and planar projections (Figure 016) reveal strongly non‑spherical shape for all compositions, confirming pronounced directional stiffness.

**Structure → Hardness and Debye Temperature**
- Vickers hardness HV and Debye temperature ΘD are strongly correlated and decrease sharply from FeAl to Fe₀.₅Mn₀.₅Al, partially recover around x ≈ 0.75, and then drop toward MnAl.
  - FeAl: HV ≈ 16.5 GPa, ΘD ≈ 652.5 K.
  - Fe₀.₅Mn₀.₅Al: HV ≈ 6.7 GPa, ΘD ≈ 533.3 K (minimum).
  - Fe₀.₂₅Mn₀.₇₅Al: HV ≈ 9.8 GPa, ΘD ≈ 574.2 K (local maximum).
  - MnAl: HV ≈ 5.0 GPa, ΘD ≈ 504.1 K.

# Mechanistic Interpretation
- The B2 FeAl alloy possesses strong Fe–Al covalent bonds together with metallic bonding, resulting in high elastic moduli, high hardness, high Debye temperature, and low anisotropy.
- With increasing Mn substitution up to x = 0.5, the directional covalent bonding network is progressively disrupted, leading to a systematic decrease in shear‑related stiffness (G, C₄₄, C₁₁−C₁₂), a drop in hardness and Debye temperature, and a transition from brittle to ductile behavior.
- The partial recovery of properties between x = 0.5 and x ≈ 0.75 (a local maximum in hardness and ΘD) is attributed to an electronic configuration that momentarily strengthens covalent character, likely due to an optimal Fe/Mn ratio.
- At the Mn‑rich end (x ≥ 0.8), further Mn substitution weakens bonding again, leading to the highest anisotropy and lowest hardness in MnAl.
- The anisotropy evolution directly follows the imbalance among elastic constants; the nearly isotropic FeAl becomes highly anisotropic in the Mn‑rich compositions, which could be exploited for directional property design.

# Key Quantitative Findings
- **Thermodynamic stability:** FeAl ΔHf = −0.391 eV/atom, Ecoh = −6.947 eV/atom; MnAl ΔHf ≈ −0.22 eV/atom, Ecoh ≈ −6.58 eV/atom.
- **Young’s modulus:** FeAl (x=0) ∼296 GPa, Fe₀.₅Mn₀.₅Al (x=0.5) ∼202 GPa.
- **Shear modulus minimum:** Fe₀.₅Mn₀.₅Al ∼77 GPa.
- **B/G and Poisson’s ratio peak:** Fe₀.₅Mn₀.₅Al B/G ≈ 2.28, ν ≈ 0.309; MnAl B/G ≈ 2.52, ν ≈ 0.324.
- **Anisotropy extremes:** Aᵁ (FeAl) ≈ 0.56, Aᵁ (MnAl) ≈ 3.8.
- **Hardness:** FeAl ∼16.5 GPa, Fe₀.₅Mn₀.₅Al ∼6.7 GPa, MnAl ∼5.0 GPa.
- **Debye temperature:** FeAl ∼652.5 K, Fe₀.₅Mn₀.₅Al ∼533.3 K, MnAl ∼504.1 K.

# Visual Evidence
- **Figures 001–008 (crystal structure models):** Display the B2 ordered cubic supercell (Pm‑3m) with color‑coded Fe, Mn, and Al atoms, directly supporting the substitutional solid‑solution model used as input for all DFT calculations.
- **Figure 009 (thermodynamic stability):** Dual‑axis plot of formation enthalpy and cohesive energy vs. Mn content. Both curves increase (become less negative) with x, demonstrating decreasing thermodynamic stability; FeAl is the most stable phase.
- **Figure 010 (electronic density of states):** Spin‑polarized total and partial DOS for the full composition series. Non‑zero DOS at EF proves metallic character; Fe‑d and Mn‑d states dominate near EF and hybridize with Al‑p states, supporting mixed covalent‑metallic bonding.
- **Figure 011 (electron density distribution):** Total electron density and density difference maps on selected planes. Elongation of contours along Al–Fe/Mn bond directions confirms covalent interactions; delocalized electron density in interstitial regions indicates metallic bonding.
- **Figure 012 (Young’s modulus and C₁₁−C₁₂):** Composition‑dependent E and C₁₁−C₁₂. The V‑shaped curves with minima at Fe₀.₅Mn₀.₅Al reflect maximum compressibility and lowest stiffness at the equiatomic composition.
- **Figure 013 (bulk, shear moduli, and C₄₄):** B decreases monotonically, whereas G and C₄₄ show a V‑shaped minimum at Fe₀.₅Mn₀.₅Al, consistent with the highest ductility at this composition.
- **Figure 014 (ductility indices):** Poisson’s ratio and B/G follow the same trend, peaking at Fe₀.₅Mn₀.₅Al and remaining high for MnAl, visualising the brittle‑to‑ductile transition with Mn addition.
- **Figure 015 (anisotropy indices):** Aᵁ and AꜬ vs. x. The strong rise toward MnAl indicates that Mn substitution substantially enhances elastic anisotropy.
- **Figure 016 (Young’s modulus planar projections):** Non‑circular contours on (001) and (110) planes directly reveal directional stiffness for all compositions; Fe₀.₁₂₅Mn₀.₈₇₅Al shows the maximum Young’s modulus along principal axes.
- **Figure 017 (hardness and Debye temperature):** HV and ΘD show parallel non‑monotonic trends, reinforcing that covalent bond weakening (softening) governs both properties, with the minimum at Fe₀.₅Mn₀.₅Al.
