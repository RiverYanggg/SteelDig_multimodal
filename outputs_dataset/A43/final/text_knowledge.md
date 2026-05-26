# Material System
The study focuses on **medium-manganese low-density steels** in the Fe-C-Mn-Al system with microalloying additions. The primary experimental validation alloy is **Fe-0.25C-3Mn-2Al-0.4Si** (designated ANT steel). Literature validation datasets include **Fe-0.29C-12.14Mn-2.96Al-0.11V-0.063Nb** (three processing conditions with distinct strengthening contributions) and **Fe-9.7Mn-2.04Al-0.99Si-0.52V-0.42C** (three processing conditions). The full data corpus comprises 177 original literature entries spanning medium-manganese low-density steel compositions, augmented to 776 samples via Gaussian Mixture Models.

# Processing Route and Variables
The experimental alloy Fe-0.25C-3Mn-2Al-0.4Si was processed through a thermomechanical sequence: **vacuum induction melting → hot forging → hot rolling (90% reduction) → cold rolling (60% reduction) → annealing at 750°C, 800°C, or 850°C for 30 min → air cooling → tempering at 400°C**. The three resulting conditions are designated **ANT750, ANT800, and ANT850**.

The four process-controlled strengthening mechanism contributions treated as predictive features are:
- **Solid solution strengthening contribution (σ₀)**: friction stress from lattice resistance and solute atoms
- **Grain refinement strengthening contribution (σ_g)**: Hall-Petch type boundary strengthening
- **Dislocation strengthening contribution (σ_d)**: Taylor hardening from geometrically necessary dislocations
- **Orowan strengthening contribution (σ_Orowan)**: precipitation bypass strengthening

The machine learning pipeline involved GMM-based data augmentation (177 → 776 samples, optimal Gaussian components selected via Bayesian Information Criterion with Expectation-Maximization parameter estimation), model selection among seven regressors (Decision Tree, KNN, XGBoost, CatBoost, Extra Trees, LightGBM, AdaBoost), and Genetic Algorithm hyperparameter optimization (population size 30, crossover probability 0.7, mutation probability 0.3) applied to Extra Trees, yielding optimized parameters: n_estimators=1657, max_depth=51, min_samples_split=3.

# Microstructure and Phase Evolution
SEM and EBSD characterization of the Fe-0.25C-3Mn-2Al-0.4Si alloy after annealing and tempering reveals a **dual-phase microstructure of equiaxed ferrite and lath-like bainite**, with retained austenite content below 5 vol% for all conditions. The annealing temperature governs the phase balance and grain dimensions:

- **ANT750 (750°C anneal)**: 52 vol% ferrite (grain size 5.7 μm), 43.0 vol% bainite (lath size 3.0 μm). GND density: 0.61 × 10¹⁴ m⁻², Taylor factor: 3.45.
- **ANT800 (800°C anneal)**: 43 vol% ferrite (5.4 μm), 55.1 vol% bainite (4.1 μm). GND density: 0.84 × 10¹⁴ m⁻², Taylor factor: 3.58.
- **ANT850 (850°C anneal)**: 69 vol% ferrite (6.8 μm), 30.8 vol% bainite (2.6 μm). GND density: 0.72 × 10¹⁴ m⁻², Taylor factor: 3.53.

With increasing annealing temperature, the ferrite volume fraction increases from 52% to 69% and ferrite grain size coarsens from 5.7 to 6.8 μm, while bainite content decreases. The AN800 condition exhibits the highest GND density and Taylor factor, correlating with peak dislocation strengthening contribution. The GND density distributions are consistently right-skewed across all conditions.

# Processing-Structure-Property Chain
The causal chain from annealing temperature to final yield strength operates as follows:

**Annealing temperature** → **Phase constitution and grain dimensions** → **σ_g** (Hall-Petch): Grain refinement strengthening contributions calculated as 264 MPa (ANT750), 256 MPa (ANT800), and 292 MPa (ANT850), reflecting the interplay of ferrite grain size and phase fractions.

**Annealing temperature** → **Dislocation substructure evolution** → **σ_d** (Taylor hardening): AN800 exhibits the highest GND density (0.84 × 10¹⁴ m⁻²) and yield strength (968 MPa), while AN750 shows the lowest GND density (0.61 × 10¹⁴ m⁻²) and yield strength (709 MPa). AN850 with intermediate GND density (0.72 × 10¹⁴ m⁻²) achieves 964 MPa.

**Property outcome**: Room-temperature tensile testing of the three ANT conditions reveals a strength-ductility trade-off governed by microstructural parameters. AN750 exhibits continuous yielding with the lowest strength (yield strength ~709 MPa) but exceptional ductility exceeding 30% total strain. AN800 and AN850 show discontinuous yielding with significantly higher yield strengths (~968 MPa and ~964 MPa), pronounced strain hardening peaks (ultimate tensile strength ~1230 MPa and ~1280 MPa), and reduced elongation to fracture (~14% and ~9%, respectively).

The GA-Extra Trees framework integrates the four strengthening contributions to predict YS with R²=0.997, RMSE=31.60 MPa, MAPE=4.39%. Experimental validation on ANT steels yields prediction errors of 10–19 MPa (12 MPa at 750°C, 10 MPa at 800°C, 19 MPa at 850°C), while literature validation on Fe-0.29C-12.14Mn-2.96Al-0.11V-0.063Nb and Fe-9.7Mn-2.04Al-0.99Si-0.52V-0.42C achieves an average prediction error of 1.84% against measured values.

# Mechanistic Interpretation
SHAP analysis and feature importance ranking (for the Fe-9.7Mn-2.04Al-0.99Si-0.52V-0.42C system) reveal the hierarchical contribution of strengthening mechanisms: **dislocation strengthening dominates with a feature importance of ~0.48 (mean |SHAP| ~560)**, attributed to Taylor hardening from high-density dislocation networks that inhibit slip band propagation. **Orowan strengthening is the second most important mechanism (~0.27, mean |SHAP| ~150)**, attributed to dispersed precipitates such as NbC and VC. **Grain refinement strengthening ranks third (~0.19, mean |SHAP| ~80)**, while **solid solution strengthening contributes minimally (~0.05, mean |SHAP| ~20)**. This hierarchical ordering validates that the data-driven model captures physically meaningful nonlinear synergies beyond linear superposition, with the dominant role of dislocation strengthening confirmed for the ANT800 condition which exhibits both the highest GND density and the highest yield strength.

# Key Quantitative Findings
- **GMM augmentation**: 177 → 776 samples; augmented and original distributions show overlapping peaks and identical truncation points for all four strengthening mechanism features and YS.
- **Model selection (before optimization)**: Extra Trees achieves R²=0.978, RMSE=76.2 MPa, MAPE=9.80% on the GMM-augmented dataset, outperforming CatBoost (R²=0.970, RMSE=89.5 MPa), XGBoost (R²=0.969, RMSE=90.4 MPa), KNN (R²=0.973, RMSE=85.2 MPa), LightGBM (R²=0.959, RMSE=104.8 MPa), DT (R²=0.944, RMSE=123 MPa), and AdaBoost (R²=0.901, RMSE=162.5 MPa).
- **GA optimization vs. alternatives**: GA-Extra Trees achieves RMSE=31.6 MPa, MAPE=4.39%, R²=0.997, compared to Grid Search-ET (RMSE=80.239 MPa, MAPE=11.037%, R²=0.972) and Bayesian-ET (RMSE=80.721 MPa, MAPE=11.423%, R²=0.976). The GA optimization reduces RMSE by approximately 58.5% and MAPE by 55.2% relative to the unoptimized Extra Trees model.
- **GA convergence**: Best RMSE converges rapidly and remains stable over 30 generations; Average RMSE stabilizes after approximately the 26th generation.
- **Experimental ANT validation errors**: Extra Trees prediction errors are 34, 31, and 36 MPa for ANT750, ANT800, and ANT850, respectively; GA-Extra Trees reduces these to 12, 10, and 19 MPa, representing an approximate 65% average error reduction.
- **Literature validation**: Average prediction error of 1.84% for Fe-0.29C-12.14Mn-2.96Al-0.11V-0.063Nb and Fe-9.7Mn-2.04Al-0.99Si-0.52V-0.42C datasets, versus 1.56% for in-house experimental validation.
- **Microstructural – mechanical correlations**: AN800 (0.84 × 10¹⁴ m⁻² GND, 55.1% bainite, 4.1 μm bainite lath size) → YS 968 MPa, UTS ~1230 MPa, elongation ~14%. AN750 (0.61 × 10¹⁴ m⁻² GND, 52% ferrite, 5.7 μm ferrite grain size) → YS 709 MPa, elongation >30%.

# Visual Evidence
**Figure 1 (SEM micrographs + quantitative data, ANT750/800/850)**: Dual-phase microstructures of equiaxed ferrite (5.4–6.8 μm, 43–69 vol%) and lath-like bainite (2.6–4.1 μm, 30.8–55.1 vol%) with minor retained austenite (<5%). EBSD-derived GND densities (0.61–0.84 × 10¹⁴ m⁻²) and Taylor factors (3.45–3.58) correlate with tensile YS (709/968/964 MPa), supporting dislocation strengthening as ~48% of total YS and grain refinement strengthening as ~19%.

**Figure 2 (Framework flowchart)**: Comprehensive workflow from 177 original data entries, GMM augmentation to 776 samples, seven-model evaluation and selection of Extra Trees, GA optimization, to final prediction with R²=0.997, RMSE=31.6 MPa, MAPE=4.39%. Experimental stress-strain curves and predicted-vs-measured bar charts validate GA-ET accuracy.

**Figure 3 (GMM augmentation workflow)**: Three-stage process: original dataset preparation with σ₀, σ_g, σ_d, σ_Orowan features (n=177); training with BIC-based optimal Gaussian component selection; EM algorithm estimation of mean, covariance, and weight parameters, followed by denoising and consolidation to 776 samples, preserving statistical consistency.

**Figure 4 (Kernel density distributions – 5 panels)**: Original vs. GMM-augmented data distributions for (a) Dislocation strengthening, (b) Fine grain strengthening, (c) Solid solution strengthening, (d) Orowan strengthening, (e) Yield Strength. Augmented data reproduces core statistical features of original distributions, with overlapping YS peaks and identical right truncation points, confirming physical law preservation during expansion.

**Figure 5 (Goodness-of-fit scatter plots – 7 models)**: Predicted vs. actual YS for DT, XGBoost, LightGBM, CatBoost, Extra Trees, KNN, AdaBoost. Extra Trees achieves best fit (R²=0.978, RMSE=76.2 MPa, MAPE=9.80%), AdaBoost poorest (R²=0.901, MAPE=33.1%). Data points align along the ideal diagonal across models for YS up to ~3000 MPa.

**Figure 6 (Model performance comparison bar charts)**: RMSE, MAPE, and R² bar charts for all seven models. Extra Trees leads in RMSE (76.2 MPa), MAPE (9.8%), and R² (0.978). CatBoost second (89.5 MPa, 10.2%, 0.970), KNN third (85.2 MPa, 10.4%, 0.973). AdaBoost worst (162.5 MPa, 33.1%, 0.901).

**Figure 7 (Extra Trees ensemble schematic)**: N independent decision trees with hierarchical nodes producing individual predictions, aggregated through majority voting to final prediction. This ensemble structure achieved RMSE=76.2 MPa, MAPE=9.8%, R²=0.978.

**Figure 8 (Genetic Algorithm architecture)**: Parent 1 and Parent 2 chromosome arrays with crossover producing Offspring 1 and Offspring 2. Colored blocks encode hyperparameter genetic information; crossover mechanism explores combinatorial search space. Population size 30, crossover probability 0.7, mutation probability 0.3.

**Figure 9 (Optimization algorithm comparison)**: GA-ET achieves RMSE=31.6 MPa, MAPE=4.39%, R²=0.997 vs. Grid Search-ET (80.239 MPa, 11.037%, 0.972) and Bayesian-ET (80.721 MPa, 11.423%, 0.976). GA significantly outperforms both alternatives.

**Figure 10 (GA-ET optimization results – scatter + convergence)**: (a) Predicted vs. actual YS scatter plot (0–2700 MPa) with tight clustering around the diagonal. (b) GA convergence over 30 generations: Best RMSE converges rapidly, Average RMSE stabilizes after generation 26. Optimized ET hyperparameters: n_estimators=1657, max_depth=51, min_samples_split=3.

**Figure 11 (Model improvement comparison bars)**: GA-ET vs. standard ET: RMSE reduced from 76.2 to 31.6 MPa (~58.5% reduction), MAPE from 9.8% to 4.39% (~55.2% reduction), R² improved from 0.978 to 0.997.

**Figure 12 (Actual vs. predicted YS line plot)**: GA-ET predicted curve (red) closely follows experimentally measured actual YS (gray) across ~120 samples spanning 0–3000 MPa, visually confirming R²=0.997 and RMSE=31.60 MPa.

**Figure 13 (Engineering stress-strain curves – ANT750/800/850)**: AN750 (750°C anneal): continuous yielding, YS ~709 MPa, elongation >30%. AN800 (800°C): discontinuous yielding, YS ~968 MPa, UTS ~1230 MPa, elongation ~14%. AN850 (850°C): discontinuous yielding, YS ~964 MPa, UTS ~1280 MPa, elongation ~9%. Demonstrates annealing-temperature-dependent strength-ductility trade-off governed by ferrite fraction, bainite morphology, and grain size.

**Figure 14 (SEM micrographs – AN750/800/850)**: Dual-phase microstructure evolution with annealing temperature. Quantitative phase analysis: AN750 (52% ferrite, 5.7 μm; 43.0% bainite, 3.0 μm), AN800 (43% ferrite, 5.4 μm; 55.1% bainite, 4.1 μm), AN850 (69% ferrite, 6.8 μm; 30.8% bainite, 2.6 μm). Ferrite volume fraction and grain size increase with temperature.

**Figure 15 (GND density and Taylor factor histograms – 6 panels)**: AN750: GND 0.61 × 10¹⁴ m⁻², Taylor 3.45. AN800: GND 0.84 × 10¹⁴ m⁻², Taylor 3.58. AN850: GND 0.72 × 10¹⁴ m⁻², Taylor 3.53. All distributions right-skewed. AN800 exhibits highest GND density and Taylor factor, correlating with peak YS (968 MPa).

**Figure 16 (Prediction error comparison bar chart)**: Standard ET vs. GA-ET prediction errors for ANT750 (34 vs. 12 MPa), ANT800 (31 vs. 10 MPa), ANT850 (36 vs. 19 MPa). GA optimization provides ~65% average error reduction across all three annealing conditions.

**Figure 17 (Literature validation scatter plot)**: Predicted vs. actual YS for Fe-0.29C-12.14Mn-2.96Al-0.11V-0.063Nb and Fe-9.7Mn-2.04Al-0.99Si-0.52V-0.42C datasets. Data points cluster tightly around the ideal diagonal; average prediction error of 1.84%, comparable to 1.56% experimental error. Confirms generalization capability across compositions and processing conditions.

**Figure 18 (Feature importance and SHAP analysis)**: For Fe-9.7Mn-2.04Al-0.99Si-0.52V-0.42C: (a) Feature importance bar chart shows dislocation strengthening ~0.48, Orowan ~0.27, grain refinement ~0.19, solid solution ~0.05. (b) SHAP mean |SHAP| values: dislocation ~560, Orowan ~150, grain refinement ~80, solid solution ~20. Dislocation strengthening identified as dominant mechanism, consistent with Taylor hardening model; Orowan second due to NbC/VC precipitates.
