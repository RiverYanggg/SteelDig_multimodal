# Material System

The analysis covers three distinct steel classes: martensitic and ferritic steels (53 batches), pure ferritic steels, and austenitic steels (24 batches). The material systems include the matrix phases α‑iron (ferrite) and γ‑iron (austenite), as well as equilibrium precipitate phases obtained from thermodynamic calculations—cementite (Fe₃C), niobium carbide (NbC), titanium carbide (TiC), and chromium‑rich M₂₃C₆ carbide.

# Processing Route and Variables

The primary “processing” variables are the chemical composition and the resulting equilibrium phase constitution. Elemental concentrations (in mass percent) of Cr, Mo, Si, Mn, Cu, Ni, C, N, Nb, and Ti are considered. For the ferritic and austenitic steel groups, the equilibrium phase fractions and the chemical composition of the individual phases are computed using Thermo‑Calc. Temperature is noted as a variable (room temperature up to 400 °C); however, quantitative temperature‑dependent modulus data are not reported in the core facts.

# Microstructure and Phase Evolution

The study explicitly differentiates between analysis strategies:
- **Martensitic and ferritic steels (Figure 1):** Phase composition and microstructure are neglected; the elastic modulus is correlated directly with the bulk chemical composition.
- **Ferritic steels (Figure 2):** The equilibrium constitution is resolved into the element content within the ferrite phase and the fraction of cementite, both calculated by Thermo‑Calc.
- **Austenitic steels (Figure 3):** The phase constitution includes the austenite matrix and the carbide precipitates NbC, TiC, and M₂₃C₆, with their volume fractions and composition determined via Thermo‑Calc.

This hierarchical distinction allows the isolation of the role of each phase constituent in determining the elastic modulus.

# Processing–Structure–Property Chain

The causal chain begins with the controlled chemical composition of the steel (processing input). Through thermodynamic phase formation (or alternatively, by ignoring phase partitioning), the constitution of the microstructure is established. The macroscopic elastic modulus (property) is then modeled as a linear summation of the contributions of each element or phase, quantified by regression coefficients rᵢ (units: GPa per mass percent or per unit phase fraction).

**For martensitic and ferritic steels (bulk composition, phase neglected):**
- Elements that increase the modulus: Si (r ≈ 4.6 GPa), Cr (≈ 2.7 GPa), Mo (≈ 2.6 GPa), Cu (≈ 2.4 GPa). Mn and Fe show modest positive contributions.
- Elements that decrease the modulus: C (r ≈ –0.5 GPa). Ni exhibits a negligible to slightly negative effect.
- Model quality: R² = 0.96, standard error = 1.2 GPa.

**For ferritic steels (composition in ferrite + cementite content):**
- Elements in ferrite that increase the modulus: Si (r ≈ 5.5 GPa), Mn (≈ 5.4 GPa), Mo (≈ 3.9 GPa), Cr (≈ 2.2 GPa), Cu (≈ 2.7 GPa). Cu is statistically insignificant due to large error bars.
- Cementite (Fe₃C) shows a regression coefficient essentially identical to that of pure Fe (≈ 2.1 GPa), implying that cementite content does not affect the modulus.

**For austenitic steels (phase constitution):**
- Strong positive effects: TiC (r ≈ 7.3 GPa) and NbC (≈ 6.5 GPa) significantly raise the modulus.
- Chromium contributes positively (≈ 2.5 GPa).
- Nitrogen exhibits the highest coefficient (≈ 15 GPa) but with extremely large uncertainty due to limited data (only four steels with appreciable N).
- Nickel and molybdenum show lower coefficients (≈ 2 GPa and ≈ 0.5 GPa, respectively), consistent with a modulus‑reducing tendency.
- M₂₃C₆ carbide has a coefficient similar to the Fe baseline (≈ 2 GPa), indicating a negligible effect despite statistical significance.
- Model quality: R² = 0.83, standard error = 2.9 GPa.

In all cases, the measured modulus is captured as the sum over all components of the product of the component fraction (mass percent or phase fraction) and the component’s regression coefficient.

# Mechanistic Interpretation

- **Solid‑solution strengthening vs. modulus:** The regression coefficients reflect electronic and bonding modifications in the iron lattice caused by solute atoms. Silicon, chromium, molybdenum, and manganese, which have a high rᵢ, increase the bonding stiffness of the α‑Fe lattice, while carbon in solution (in the martensitic/ferritic group) reduces it, likely due to the distortion and softening of the lattice or measurement averaging over carbon‑enriched regions.
- **Role of cementite:** In the ferritic steel model that accounts for phase constitution, cementite exhibits a coefficient equal to that of pure iron, indicating that this carbide does not alter the composite modulus beyond the rule‑of‑mixtures contribution of its iron content. This is mechanistically explained by the similar elastic stiffness of cementite and ferrite in the loading regime measured, or by the fact that cementite particles are not continuous and thus do not contribute additional stiffening.
- **Austenitic steel stiffening by fine carbides:** The high coefficients of TiC and NbC arise from the intrinsically high stiffness of these interstitial carbides and their dispersal in the austenitic matrix, providing a composite strengthening effect. The similar baseline of Cr₂₃C₆ to Fe suggests that, despite being a carbide, its modulus contribution per unit phase fraction is not markedly greater than that of the matrix, possibly due to its coarser distribution or lower intrinsic modulus.
- **Data‑limited nitrogen effect:** The extremely high but uncertain coefficient for N in austenite is noted; without sufficient data points, the regression cannot robustly resolve its true effect, but the sign is positive, hinting at a strong interstitial hardening effect on the lattice modulus.
- **Statistical significance:** The chart rankings by (rᵢ/σᵢ) emphasize that elements with small error bars (Si, Cr, Mo, Mn, NbC, TiC) have the most reliable influence, while elements with large variability (Cu in ferritic steels, N in austenitic steels) cannot be considered predictive with the current dataset.

# Key Quantitative Findings

- **Martensitic/ferritic steels (53 batches):** Bulk composition model yields R² = 0.96, residual standard error = 1.2 GPa. Si gives the largest positive per‑weight‑percent increment (~4.6 GPa), C gives a negative contribution (~–0.5 GPa).
- **Ferritic steels (Thermo‑Calc‑informed):** Si (~5.5 GPa) and Mn (~5.4 GPa) have the highest reliable coefficients. Cementite’s coefficient (≈ 2.1 GPa) equals that of Fe, so cementite fraction does not change the predicted modulus.
- **Austenitic steels (24 batches, Thermo‑Calc‑informed):** R² = 0.83, standard error = 2.9 GPa. TiC (≈ 7.3 GPa) and NbC (≈ 6.5 GPa) produce strong stiffening. N has the largest coefficient (~15 GPa) but with large uncertainty (only 4 steels). M₂₃C₆ and Fe have similar coefficients (~2 GPa).
- All regression models are restricted to the composition ranges present in the collected datasets.

# Visual Evidence

- **Figure 1:** Regression coefficients for martensitic and ferritic steels (phase neglected). The bar chart with error bars shows the magnitude and reliability of rᵢ for Si (~4.6 GPa), Cr (~2.7 GPa), Mo (~2.6 GPa), Cu (~2.4 GPa), C (≈ –0.5 GPa), and others. Open circles are literature points; black squares are this study. The high R² (0.96) and low standard error (1.2 GPa) support the compositional dependence.
- **Figure 2:** Regression coefficients for ferritic steels with Thermo‑Calc‑resolved ferrite composition and cementite fraction. Si (~5.5 GPa) and Mn (~5.4 GPa) show the strongest positive influence. Cementite’s bar is indistinguishable from Fe’s bar (~2.1 GPa), providing direct evidence that cementite does not affect the modulus. Cu shows a positive mean but with large error bars.
- **Figure 3:** Regression coefficients for austenitic steels, resolving NbC, TiC, M₂₃C₆, and dissolved elements. TiC (~7.3 GPa) and NbC (~6.5 GPa) have clearly positive, moderately precise coefficients. Cr (~2.5 GPa) is positive. N appears very high (~15 GPa) but with error bars spanning a much wider range. M₂₃C₆ nearly coincides with the Fe baseline (~2 GPa), indicating negligible practical stiffening. The model captures 83% of variance (R²) with a standard error of 2.9 GPa.
