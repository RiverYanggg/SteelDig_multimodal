# Material System
The study covers two broad categories of steels: (i) ferritic and low-alloy steels whose matrix is body-centered cubic (bcc) ferrite, with carbon predominantly present as cementite (Fe₃C); (ii) austenitic steels with a face-centered cubic (fcc) austenite matrix, including Ti-stabilized grades where carbon is bound as TiC. The modeling specifically considers the phases ferrite, austenite, cementite, and TiC. Literature data were screened to retain only entries with complete chemical composition, yielding 244 ferritic and 64 austenitic steel batches, respectively.

# Processing Route and Variables
The “processing” variables in this modeling study are the bulk chemical composition (mass % of C, Cr, Mn, Si, Cu, Mo, V, Ni, Ti, N, Co, Al, etc.) and the choice of the phase-constitution model that translates composition into microstructure. Two approaches are applied to ferritic steels:
- **Simple cementite model**: assumes all carbon forms Fe₃C of fixed stoichiometry and density.
- **Thermodynamic equilibrium model**: calculates the equilibrium partitioning of alloying elements between ferrite and cementite using thermodynamic data; the cementite density is then expressed as a function of its Cr and Mn content (Equations 6 and 7 in the original paper).
For austenitic steels, the matrix is taken as fcc, and for Ti-stabilized grades the amount of TiC is quantified by assuming all Ti not consumed by N forms stoichiometric TiC; residual C is considered dissolved in austenite. No other processing steps (e.g., heat treatment, deformation) are treated as variables; the predicted property is density at room temperature.

# Microstructure and Phase Evolution
The microstructure is implicitly represented by the phase fractions and compositions derived from the chosen model. In ferritic steels, the cementite volume fraction and its alloying content (substitutional Cr and Mn) evolve with bulk composition according to thermodynamic equilibrium. For austenitic steels, Ti-stabilized grades contain TiC precipitates, while carbon not bound as TiC remains in solid solution. The regression analysis treats each element as a contributor to the apparent density of the matrix phase (ferrite or austenite) after accounting for carbide effects. No direct microstructural characterization (grain size, morphology) is presented; the emphasis is on phase constitution and carbide type/amount.

# Processing-Structure-Property Chain
**Composition → Phase constitution → Intrinsic phase density → Macroscopic steel density**
- **Ferritic steels**: Bulk composition determines the equilibrium ferrite/cementite ratio and cementite composition. The apparent density of the steel is modeled as a linear function of the mass fractions of alloying elements dissolved in ferrite. Elements are assigned apparent density coefficients (inverse of regression coefficients) that reflect their effect on the ferrite lattice. Regression on 244 batches gives an equation with R² = 0.994, maximum deviation 4.2 kg/m³, average deviation 1.4 kg/m³.
- **Austenitic steels**: The matrix fcc phase density is regressed against composition. For Ti-stabilized grades, the formation of TiC (density ~4930 kg/m³) is explicitly included, meaning Ti and part of C are removed from the austenite solution. The regression on 64 batches yields R² = 0.975.

# Mechanistic Interpretation
The apparent density coefficients (Figure 1 for ferrite, Figure 3 for austenite) reveal the volumetric effect of solute atoms:
- **Ferritic steels**: Cu (apparent density ~11 800 kg/m³) and Mo (~10 500 kg/m³) increase ferrite density relative to pure bcc Fe, while S (~2500 kg/m³) strongly decreases it. The close agreement between the regression-derived values and literature-reported apparent densities for Cr, Cu, Fe, Mn, Mo, Ni, S, and Si supports the thermodynamic model. The apparent density of V deviates, suggesting that its precipitation as carbides is not fully captured by the simple cementite assumption.
- **Austenitic steels**: Co, Cu, Mo, Ni raise the apparent density of austenite above that of pure fcc Fe (~8000 kg/m³). In contrast, TiC, C, Cr, Mn, N, Si, and Ti reduce the apparent density. The significant error bars on TiC, Ti, C, and N indicate uncertainty in the determination of their coefficients, likely due to the interplay of TiC stoichiometry and possible nitrogen effects.
- The cementite density itself is lowered by alloying: from ~7750 kg/m³ for pure Fe₃C to ~7600 kg/m³ at 0.25 mass fraction Cr, and from ~7700 kg/m³ to ~7080 kg/m³ at 0.9 mass fraction Mn (Figure 2). This composition‑dependent cementite density is an essential input to the thermodynamic model, linking phase constitution to the macroscopic property.

# Key Quantitative Findings
- **Ferritic steel regression model**: R² = 0.994 (244 batches); max deviation 4.2 kg/m³, average deviation 1.4 kg/m³.
- **Austenitic steel regression model**: R² = 0.975 (64 batches).
- **Apparent density in ferrite** (regression, kg/m³): Cu ≈ 11 800, Mo ≈ 10 500, S ≈ 2500; other values align with literature.
- **Apparent density in austenite**: Increasing elements – Co, Cu, Mo, Ni; decreasing elements – TiC, C, Cr, Mn, N, Si, Ti. Reference fcc Fe ≈ 8000 kg/m³.
- **Cementite density variation**: Fe₃C baseline ≈ 7750 kg/m³. With Cr (0–0.25 mass fraction) density decreases to ~7600 kg/m³; with Mn (0–0.9 mass fraction) density decreases to ~7080 kg/m³.

# Visual Evidence
- **Figure 1**: Comparative scatter plot of apparent density (inverse regression coefficients with 95 % error bars) vs. pure elemental density and literature averages for ferritic steel alloying elements. The high R² (0.994) and low deviations (max 4.2, avg 1.4 kg/m³) validate the thermodynamic model. The plot directly shows Cu and Mo as strong density increasers and S as a strong decreaser, while V exhibits poorer agreement, indicating model limitations for that element.
- **Figure 2**: Computed density of cementite as a function of Cr (Pnma) and Mn (Pbnm) substitution. The clear linear decreasing trends illustrate the sensitivity of cementite density to composition, supporting the need for the composition‑dependent cementite density used in the ferritic steel model (Equations 6 and 7).
- **Figure 3**: Regression analysis for austenitic steels showing apparent density coefficients (1/r_i) with error bars compared to theoretical elemental densities. Highlights the distinction between elements that expand (Co, Cu, Mo, Ni) vs. contract (TiC, C, Cr, Mn, N, Si, Ti) the austenite lattice, and quantifies the uncertainty for Ti, C, and N. The R² of 0.975 (64 batches) substantiates the predictive capability for austenitic grades.
