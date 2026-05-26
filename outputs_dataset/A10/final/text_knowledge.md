# Fe-C-Cr-Mn-Si Steel Design via Extreme High Accuracy Machine Learning

## Material System
- **Alloy family:** Fe-C-Cr-Mn-Si multi-component steel for cladding coatings.
- **Base alloying set:** C, Si, Mn, Cr, S, Ni, P, Fe, Mo, V, W (mass percentages).
- **Experimental validation samples (arc-cladded on ASTM A36 steel substrate):**
  - **Sample 1:** Fe-C-Cr-Mn-Si alloy without Ni, Mo, V, W additions. Composition: 14 wt% Cr, 0.45 wt% C. Single-phase Fe-Cr solid solution with face-centered cubic (FCC) lattice.
  - **Sample 2:** Fe-C-Cr-Mn-Si alloy with Ni (1.13 wt%), V (0.25 wt%), and W (1.19 wt%) additions. Composition: 5.3 wt% Cr, 0.53 wt% C. Identified as Fe-Cr-Ni FCC phase.
  - **Sample 3:** Fe-C-Cr-Mn-Si alloy with Ni (1.2 wt%), Mo (1.5 wt%), and V (0.25 wt%) additions. Composition: 5.2 wt% Cr, 0.15 wt% C. Identified as Fe-Cr-Ni FCC phase.
- **Phase constitution dependence:** The presence or absence of Ni determines whether the matrix phase is binary Fe-Cr solid solution (Sample 1) or ternary Fe-Cr-Ni solid solution (Samples 2 and 3).
- **Data sources for model training:** Initially 173 data points from MatWeb database, augmented to 192 data points via conditional generative adversarial networks (CGANs).

## Processing Route and Variables
- **Overall framework:** Data-driven inverse design pipeline integrating CGAN for data augmentation, Support Vector Regression (SVR) modeling, feature engineering based on modified solid solution strengthening theory, Firefly Algorithm (FA) for inverse design optimization, and arc cladding for experimental validation.
- **Synthetic data generation:** CGAN used to expand the training dataset.
- **Feature inputs to ML model (final optimal set of 3):**
  1. `G` – shear modulus.
  2. `δ_Ec` – difference in cohesive energy.
  3. `D_Ec` – local cohesive energy mismatch.
  These three parameters derive from a modified solid solution strengthening theory description. Initial screening considered variables including atomic radius difference (lattice distortion), valence electron concentration (`e/a`), second ionization energy, and others; the three-feature set was selected via recursive feature elimination (RFE) voting and exhaustive cross-validation.
- **Model selection:** Among nine evaluated machine learning algorithms (SVR, Extra Trees, MLP, Ridge, LightGBM, XGBoost, Random Forest, Linear Regression, Decision Tree), SVR achieved the highest performance. Model training used 10-fold cross-validation.
- **Inverse design optimization:** Four heuristic algorithms compared for maximizing predicted microhardness:
  - Firefly Algorithm (FA): predicted optimum **733.59 HV**.
  - Particle Swarm Optimization (PSO): predicted optimum **730.04 HV**.
  - Grey Wolf Optimizer (GWO): predicted optimum **708.60 HV**.
  - Simulated Annealing (SA): predicted optimum **700.37 HV**.
- **Experimental fabrication (cladding):** Three compositions selected from inverse design were deposited by arc cladding on ASTM A36 steel substrates for property validation.
- **Characterization techniques:**
  - X-ray diffraction (XRD) for phase identification and lattice distortion (peak shift relative to standard Fe peak).
  - Vickers microhardness testing under 1 kg load with 20 s dwell time.

## Microstructure and Phase Evolution
- **Phase constitution (XRD evidence):**
  - **Sample 1 (no Ni, high Cr 14 wt%):** Single-phase Fe-Cr solid solution (FCC), with diffraction peaks indexed as (110), (200), (211).
  - **Sample 2 (1.13 wt% Ni, 5.3 wt% Cr) and Sample 3 (1.2 wt% Ni, 5.2 wt% Cr):** Fe-Cr-Ni ternary solid solution (FCC) with identical peak indices (110), (200), (211).
  - The phase change from Fe-Cr to Fe-Cr-Ni is triggered by Ni addition; Ni content as low as ~1.1–1.2 wt% changes the phase identity.
- **Lattice distortion and solid solution evidence:**
  - XRD peak shift: All alloy diffraction peaks are systematically shifted to higher 2θ angles relative to the standard Fe peak position (vertical dashed line near 44° for the (110) peak). This rightward shift indicates lattice contraction or distortion attributed to atomic radius mismatch between solute atoms (Cr, Ni, Mn, Si, etc.) and the Fe matrix.
  - The lattice distortion serves as direct microstructural evidence of solid solution strengthening operating in these alloys; it reflects the elastic strain field around solute atoms.

## Processing-Structure-Property Chain
1. **Composition selection (inverse design):** The Firefly Algorithm identified a compositional window in the Fe-C-Cr-Mn-Si system predicted to maximize microhardness (733.59 HV) based on three physics-informed features (G, δ_Ec, D_Ec).
2. **Training data augmentation (CGAN):** Expanding the dataset from 173 to 192 points via CGAN reduced data scarcity and improved model generalization before feature selection and model training.
3. **Feature engineering (modified solid solution strengthening theory):** Out of the full set of candidate features, recursive feature elimination, Pearson correlation, and exhaustive cross-validation converged on three dominant features—**shear modulus (G), difference in cohesive energy (δ_Ec), and local cohesive energy mismatch (D_Ec)** —achieving cross-validation score stabilization at exactly 3 features with no gain from adding 4 or 5 variables. This directly links the solid solution strengthening physical mechanism to the predictive model.
4. **Model training (SVR with 10-fold cross-validation):** The SVR trained on these 3 features achieved **R² = 0.89** and **RMSE = 0.31** for predicting solid solution strengthening stress (Δσ_SSS) across the dataset (including eventually the validation samples). Before incorporating the modified solid solution theory, SVR performance was lower (R² = 0.85, RMSE = 0.39, as shown in the nine-model screening with standard features).
5. **Cladding deposition:** Three alloy compositions—representing distinct combinations of Cr content, C content, and the presence of Ni/Mo/W/V—were arc-cladded onto ASTM A36 steel to produce coating samples.
6. **Microstructure formation (XRD):** The deposited coatings develop either Fe-Cr (Sample 1) or Fe-Cr-Ni (Samples 2, 3) FCC solid solutions, all exhibiting lattice distortion (peak shifts) indicating atomic misfit and solid solution strengthening.
7. **Property outcome (microhardness):**
   - **Sample 1** (Fe-Cr, 14 wt% Cr, 0.45 wt% C): Predicted 521 HV, Experimental 515 HV (error **1.17%**).
   - **Sample 2** (Fe-Cr-Ni, 5.3 wt% Cr, 0.53 wt% C with Ni, V, W): Predicted 490 HV, Experimental 500 HV (error **2.00%**).
   - **Sample 3** (Fe-Cr-Ni, 5.2 wt% Cr, 0.15 wt% C with Ni, Mo, V): Predicted 415 HV, Experimental 424 HV (error **2.09%**).
   - The maximum relative prediction error among the three validation samples is 2.09%, validating the "extreme high accuracy" claim of the ML pipeline under practical fabrication conditions.
   - Hardness levels correlate with Cr content and carbon level; C content also directly affects the carbide population potential and lattice strain, though the dominant enhancement mechanism is solid solution strengthening as modeled by the three cohesive-energy- and shear-modulus-based features.

## Mechanistic Interpretation
- **Solid solution strengthening as core mechanism:** The entire model is built on a modified solid solution strengthening theory. Unlike empirical composition-to-hardness regression, the model maps three physically interpretable parameters—**difference in cohesive energy (δ_Ec), local cohesive energy mismatch (D_Ec), and shear modulus (G)** —to the strengthening increment (Δσ_SSS) and thus to microhardness.
- **Physical meaning of the selected features:**
  - **δ_Ec (cohesive energy difference):** Quantifies the change in bond strength between the solute and solvent atoms. A larger cohesive energy mismatch increases the local elastic resistance to dislocation motion, directly enhancing solid solution strengthening.
  - **D_Ec (local cohesive energy mismatch):** Captures the variation of cohesive energy in the local chemical environment around a solute, influencing the local obstacle strength for dislocations.
  - **G (shear modulus):** Represents the resistance to shear deformation; solutes that modify the local shear modulus create elastic interactions with dislocations, contributing to strengthening via the modulus misfit component of solid solution hardening.
- **Connection to lattice distortion:** The XRD peak shifts experimentally confirm that solute atoms (Cr, Ni, in particular) generate substantial lattice distortion in the Fe-based FCC matrix. This distortion is a direct manifestation of atomic size misfit and elastic strain, which are coupled with the cohesive energy landscape that the SVR model captures through the three theoretical descriptors. The model thus provides a quantitative bridge from electronic/atomic-scale energy descriptors to macro-scale hardness via solid solution hardening.
- **Cr importance:** Feature importance ranking shows Cr as the most influential alloying element for microhardness among the full element set (C, Si, Mn, Cr, S, Ni, P, Fe, Mo, V, W), consistent with the strong solid solution strengthening it imparts via atomic size misfit and cohesive energy modification.
- **Model improvement mechanism:** Incorporating solid solution strengthening theory (δ_Ec, D_Ec, G) into the feature set increases R² from 0.85 to 0.89 and reduces RMSE from 0.39 to 0.31, because these features directly encode the underlying physics of dislocation-solute interaction rather than treating composition as a black-box variable.
- **Inverse design rationale:** FA outperforms PSO, GWO, and SA in maximizing predicted hardness because of its superior local attraction capacity. The theoretical descriptors then guide the selection of specific Cr, C, and subordinate element (Ni, Mo, V, W) levels to achieve the predicted maximum of 733.59 HV in the composition space.

## Key Quantitative Findings
- **Data scale:** 173 original data points from MatWeb, augmented to 192 via CGAN.
- **Model performance before theoretical feature injection (SVR with standard features):** R² = 0.85, RMSE = 0.39.
- **Model performance after injecting modified solid solution strengthening features (3 features: G, δ_Ec, D_Ec):** R² = 0.89, RMSE = 0.31 (for Δσ_SSS prediction, all sample data).
- **Optimal feature count:** Exhaustive screening shows cross-validation scores stabilize at 3 features; adding a 4th or 5th feature yields no improvement.
- **Inverse design maximum predicted microhardness:** FA achieves 733.59 HV; PSO 730.04 HV; GWO 708.60 HV; SA 700.37 HV.
- **Experimental validation results (Vickers microhardness under 1 kg/20 s):**
  - Sample 1: predicted 521 HV / experimental 515 HV → **1.17% error**.
  - Sample 2: predicted 490 HV / experimental 500 HV → **2.00% error**.
  - Sample 3: predicted 415 HV / experimental 424 HV → **2.09% error**.
  - All three samples: relative prediction error ≤ 2.09%.
- **Element importance hierarchy:** Cr > Ni > Mo (from feature importance ranking funnel chart); Mn, V, W show weaker individual correlation with microhardness in the analyzed dataset.
- **Δσ_SSS parity plot (SVR):** RMSE = 0.31, R² = 0.89; the majority of prediction errors are below 15 MPa across the experimental range ~1200–1800 MPa.
- **Multicollinearity among features:** During feature selection, Pearson correlation identified six pairs with |PCC| ≥ 0.95 among nine candidate features, leading to removal of redundant variables (ηB, ω, δ_EI-2nd, γ) in favor of the final set of e/a, G, EI-2nd, δ_Ec, and D_Ec, with only G, δ_Ec, and D_Ec used as final model inputs.

## Visual Evidence
- **Figure 1 (figure_012):** XRD patterns of the three cladded samples. Panel (a): full 2θ range 20–100° showing Sample 1 as Fe-Cr phase and Samples 2–3 as Fe-Cr-Ni phase. Panel (b): enlarged (110) peak region 40–50° where all alloy peaks shift rightward relative to a standard Fe peak dashed line, providing direct diffraction evidence of lattice distortion due to solute atomic radius mismatch—this supports the solid solution strengthening mechanism.
- **Figure 2 (figure_008):** Exhaustive screening scatter plot of cross-validation score vs. feature count (1–5). With 1 feature, scores are highly variable (0.3–1.3); at 2 features, the range narrows; at 3 features, scores concentrate in the narrow 0.25–0.35 range and stabilize, showing 3 is the optimal number. Supports the final selection of G, δ_Ec, D_Ec as sufficient for high-accuracy modeling.
- **Figure 3 (figure_003):** Composite feature engineering display: (a) RFE voting heatmap; (b) Pearson correlation circle heatmap; (c) feature importance bar chart showing shear modulus (G), cohesive energy difference (δ_Ec), and local cohesive energy mismatch (D_Ec) as dominant predictors; (d) cross-validation score vs. feature number confirming stabilization at 3 features. Directly establishes the physical metallurgy basis of the SVR model.
- **Figure 4 (figure_004 / figure_010):** SVR parity plot for Δσ_SSS prediction (predicted vs. experimental, all samples). Data points cluster tightly along the y=x guideline; color bar shows errors 0.60–29.90 MPa; annotation gives RMSE = 0.31 and R² = 0.89. Demonstrates the high accuracy achieved by the theory-informed model.
- **Figure 5 (figure_005 / figure_013):** Bar chart comparing predicted (blue) and experimental (pink) microhardness for three validation samples, with error bars. Numerical labels confirm prediction errors of 1.17% (Sample 1), 2.00% (Sample 2), and 2.09% (Sample 3). Constitutes the primary experimental validation evidence.
- **Figure 6 (figure_006):** Pairwise correlation scatter matrix among 11 composition variables and microhardness. Diagonal shows probability density distributions; off-diagonal reveals strong negative Fe-content correlations with other solutes, and positive correlations of microhardness with Cr, Mo, W, and C—supporting solid solution strengthening trends and guiding feature selection.
- **Figure 7 (figure_002):** Feature importance analysis: left panel shows dataset scatter grid; right panel presents an importance ranking funnel with Cr at top, then Ni and Mo, confirming the dominant role of Cr in determining microhardness.
- **Figure 8 (figure_007):** Feature selection workflow panels: (a) RFE voting heatmap; (b) PCC heatmap of nine candidate features revealing high multicollinearity; (c) importance scores ranking. Provides detailed evidence that e/a, G, EI-2nd, δ_Ec, and D_Ec are the definitive key features, with ηB, ω, δ_EI-2nd, and γ removed due to redundancy.
- **Figure 9 (figure_009):** Nine-panel scatter plot comparing nine ML models (SVR, ET, MLP, Ridge, LightGBM, XGBoost, RF, LR, DT) with training (blue) and testing (orange) data. SVR achieves the highest R² (0.85) and RMSE (0.39) among all baseline models using the three theoretical features before the final optimization step, justifying the choice of SVR as the core algorithm.
- **Figure 10 (figure_011):** Bar chart comparing four optimization algorithms for inverse design: FA (733.59 HV) > PSO (730.04 HV) > GWO (708.60 HV) > SA (700.37 HV). Justifies the selection of FA for finding maximum-hardness compositions.
