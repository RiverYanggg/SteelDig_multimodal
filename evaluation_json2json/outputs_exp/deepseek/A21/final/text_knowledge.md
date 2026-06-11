# Material System
- **Alloy family**: Fe-Mn-Al-C austenitic low-density steels.
- **Nominal composition range**: 18–30 wt% Mn, 8–12 wt% Al, 0.6–1.8 wt% C, balance Fe.
- **Experimental validation alloy**: Fe‑30Mn‑8Al‑1C (nominal); measured composition Fe‑30.4Mn‑7.9Al‑1.1C (wt%).
- **Key phases investigated**: γ austenite (FCC), κ‑carbide (L′1₂-type nanoprecipitate), α‑ferrite, β‑Mn, B2/DO₃ intermetallics.

# Processing Route and Variables
- **Alloy preparation**: Induction melting under Ar atmosphere; homogenization at 1200 °C for 2 h; forging to 60×60 mm billet; secondary homogenization at 1050 °C for 100 min; hot rolling to 12 mm plate; air cooling.
- **Cold deformation**: Cold rolling with 75% thickness reduction.
- **Solution annealing**: 1000 °C for 15 min followed by water quenching (single‑phase γ state prior to aging).
- **Aging treatment**: 550 °C for 2 h (within the 500–600 °C window) followed by water cooling. This aging step induces κ‑carbide precipitation in the γ matrix.
- **Machine learning feature descriptors** (composition and thermodynamic parameters): Mn, Al, C, Fe, valence electron concentration (VEC), melting temperature (Tm), mixing entropy (ΔSmix), mixing enthalpy (ΔHmix), electronegativity difference (Δχ), atomic size difference (δ). Δχ and δ were removed before modeling due to high Pearson correlation (>0.95) with other descriptors.

# Microstructure and Phase Evolution
- **Post‑aging microstructure of Fe‑30Mn‑8Al‑1C**: Fully recrystallized single‑phase γ‑austenite matrix with equiaxed grains of average size **17 μm** (EBSD, optical microscopy).
- **κ‑carbide precipitation**: Nanoscale coherent κ‑carbides (L′1₂) homogeneously distributed within the γ matrix, verified by bright‑field/dark‑field TEM and SAED along the [011̄] zone axis.
- **Phase‑prediction models**:
  - Random Forest (RF) classifier achieves cross‑validation accuracy of **0.98** for existence of κ phase (Y1), **0.98** for (γ+κ) dual‑phase region at 500–600 °C (Y2), and **0.96** for single γ region (Y3).
  - SVM regression for κ‑phase volume fraction (Y₄) yields RMSE <1% and R = 0.99.
- **Composition‑microstructure maps** at fixed 30 wt% Mn:
  - κ phase exists when Al > ~5 wt% (Fig. 7a).
  - (γ+κ) dual‑phase region at 500–600 °C is confined to Al ≈ 4.5–9.3 wt% and C ≈ 0.4–1.1 wt% (Fig. 7b).
  - Single γ‑phase region extends up to Al ≈ 11.6 wt% (Fig. 7c).
  - Triple‑condition satisfaction (κ exists, single γ at equilibrium, and γ+κ duplex at 500–600 °C) is achieved in a narrow Al–C window (Fig. 7e).

# Processing–Structure–Property Chain
1. **Composition → Phase stability**: High Al (>5 wt%) enables κ‑carbide; C controls the temperature window of the γ+κ duplex region. In Fe‑30Mn‑8Al‑1C, Al (7.9 wt%) and C (1.1 wt%) fall inside the required window, ensuring a single γ matrix at solution temperature and the formation of κ during aging.
2. **Solution annealing (1000 °C, 15 min) + water quench → Single‑phase γ, 17 μm grains**: This provides a clean, supersaturated matrix for subsequent precipitation.
3. **Aging (550 °C, 2 h) → γ + nanoscale κ‑carbides**: The uniform precipitation of coherent κ particles occurs without formation of detrimental phases (α, β‑Mn, B2/DO₃), as predicted.
4. **Microstructure → Tensile properties**:
   - The resulting γ + κ microstructure delivers **yield strength 953 MPa, ultimate tensile strength 1109 MPa, and total elongation 42%** (Fig. 9b).
   - The high strength is attributed to precipitation hardening from nanoscale κ‑carbides, while the fully recrystallized austenitic matrix with moderate grain size sustains large ductility.
5. **ML‑guided design chain**: From 78,477 possible compositions → two‑step screening (κ exists, single γ, γ+κ at 500–600 °C, κ fraction ≥10%, density ≤7 g/cm³) → 150 optimal candidates → experimental validation of Fe‑30Mn‑8Al‑1C confirms predicted microstructure and properties.

# Mechanistic Interpretation
- **Dominant elements**: Feature importance analysis (mean decrease accuracy) identifies **Al** as the most critical element for both single γ region and κ‑phase existence (MDA >40–50%), because Al expands the austenite phase field while simultaneously providing the thermodynamic driving force for κ‑carbide ordering. **C** consistently shows the lowest impact in classification but becomes important for the (γ+κ) dual‑phase temperature range and κ fraction.
- **κ‑carbide strengthening**: The coherent, nanoscale κ precipitates impede dislocation motion, leading to a substantial yield strength increment over the solution‑treated state, while the cubic‑to‑cubic orientation relationship with the γ matrix preserves ductility.
- **Avoidance of deleterious phases**: The composition screening (particularly Y3 = single γ) ensures that brittle phases such as α‑ferrite, β‑Mn, and B2/DO₃ are suppressed, which would otherwise degrade ductility and toughness.
- **Density optimization**: Increasing Al reduces density (from 7.234 to 6.812 g/cm³ in the screened region) by replacing heavier Fe atoms, while C helps maintain austenite stability. The ML screening balanced low density (<7 g/cm³) with high κ fraction (≥10%), yielding lightweight yet strong alloys.

# Key Quantitative Findings
- **Classification accuracy** (RF): Y1 (κ exists) = 0.98; Y2 (γ+κ at 500–600 °C) = 0.98; Y3 (single γ) = 0.96.
- **Regression performance** (SVM): RMSE <1%, R = 0.99 for κ fraction.
- **Feature correlations**: C‑δ (0.98), C‑Δχ (0.97), Fe‑Mn (−0.9), Al‑VEC (−0.94), C‑ΔHmix (−0.93). Δχ and δ removed for modeling.
- **Optimal screening yield**: 78,477 → 1,320 (first step) → 150 candidates (second step; κ ≥10%, density ≤7 g/cm³).
- **Fe‑30Mn‑8Al‑1C (validated)**:
  - Measured composition: Mn 30.4, Al 7.9, C 1.1 (wt%).
  - Grain size: 17 μm (recrystallized equiaxed γ).
  - Tensile properties: YS 953 MPa, UTS 1109 MPa, Elongation 42%.
  - Density (predicted from ML contour): ~6.9 g/cm³.

# Visual Evidence
- **Figure 1** (figure_001): Not directly readable; described as containing a “Check for updates” icon. No scientific data extracted.
- **Figure 2** (figure_002): Flowchart of the ML‑based alloy design framework, showing sequential filters (κ exists?, single γ?, γ+κ at 500–600 °C?, high κ fraction?, low density?) culminating in experimental validation loop.
- **Figure 3** (figure_003): Pearson correlation matrix heatmap of ten descriptors. Strong positive C‑δ (0.98) and C‑Δχ (0.97) led to removal of δ and Δχ. Strong negative correlations (Fe‑Mn −0.9, Al‑VEC −0.94) confirm descriptor independence after reduction.
- **Figure 4** (figure_004): Algorithm selection (panel a): RF gives highest CVA (0.96–0.98). MDA importance (panels b–d): Al dominates for Y1 (κ) and Y3 (single γ), while Mn and Fe dominate for Y2 (γ+κ region). C has the least impact.
- **Figure 5** (figure_005): Regression algorithm evaluation (panel a): SVM shows RMSE <1%. Descriptor importance (panel b): Al removal causes largest RMSE increase. Parity plot (panel c): R = 0.99, confirming predictive accuracy for κ fraction.
- **Figure 6** (figure_006): Two‑step screening schema reducing design space from 78,477 to 1,320 to 150 candidates based on phase and property constraints.
- **Figure 7** (figure_007): Composition–structure maps at 30 wt% Mn in Al–C space:
  - (a) κ exists (red) when Al > ~5 wt%.
  - (b) γ+κ at 500–600 °C within intermediate Al (4.5–9.3) and C (0.4–1.1).
  - (c) Single γ region (red) up to ~11.6 wt% Al.
  - (d) Overlap of Y1 and Y3: single γ + κ phase.
  - (e) Triple intersection (Y1∩Y2∩Y3) pinpointing optimal compositions.
- **Figure 8** (figure_009): Microstructural validation of Fe‑30Mn‑8Al‑1C after aging at 550 °C/2 h:
  - (a) XRD: single‑phase γ peaks.
  - (b,c) EBSD IPF and phase map: fully recrystallized γ grains, average 17 μm.
  - (d,e) TEM BF/DF: nanoscale κ precipitates in γ matrix.
  - (f) SAED [011̄]: FCC structure with κ superlattice spots.
- **Figure 9** (figure_010): Property validation:
  - (a) EPMA maps: uniform distribution of Mn, Al, C; no macroscopic segregation.
  - (b) Engineering stress–strain curve: YS 953 MPa, UTS 1109 MPa, elongation 42%.
  - (c) Optical micrograph: equiaxed grains ~17 μm.
- **Figure 10** (figure_008): Second‑step performance screening:
  - (a) Contour of κ fraction (0.45–13.15%) vs Al and C.
  - (c) Density contour (7.234 to 6.812 g/cm³).
  - (b) Pareto‑optimal selection: 30 candidates satisfying κ ≥11% and density ≤6.9 g/cm³; red star marks the validated Fe‑30Mn‑8Al‑1C.
