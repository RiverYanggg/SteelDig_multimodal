# Material System

Low-alloy steel with nominal composition 0.398C–0.87Mn–0.31Si (wt%), designed for hot compression deformation studies.

# Processing Route and Variables

Cylindrical specimens (ϕ6 mm × 9 mm) were heated to 1250 °C at 10 °C/s, held for 180 s for austenite homogenization, cooled to the deformation temperature at 10 °C/s, held for 60 s, and uniaxially compressed to a true strain of 0.9, followed by water quenching. Deformation was conducted under two families of conditions:

- **Constant (isothermal, constant strain rate):** temperatures 850–1150 °C, strain rates 0.01–10 s⁻¹.
- **Varying (transient) conditions:**
  - *Strain-rate jumps at 950 °C:* sudden change from 0.01 s⁻¹ to 0.1 s⁻¹ or from 0.1 s⁻¹ to 0.01 s⁻¹ at fixed true strains ε₁ = 0.2 or 0.4.
  - *Temperature ramps at 0.01 s⁻¹:* continuous linear temperature change between 950 °C and 1050 °C over strain intervals 0.2–0.3 or 0.4–0.5.

The Zener–Hollomon parameter Zₚ is used to characterize the combined effect of temperature and strain rate:
Zₚ = ε̇ exp(Q/RT), with Zₚ(II) evaluated at ε + Δε after the transition.

# Microstructure and Phase Evolution

- **Initial state:** Mixed-grain austenite microstructure with an average grain size of ~141.66 μm (experimental, SD = 54.54 μm); 3D cellular automaton simulations reproduce an average size of ~143.78 μm (SD = 58.25 μm), validating the initial structure model.
- **During deformation:** Inhomogeneous dislocation density develops, with higher densities at grain boundaries and within unrecrystallized regions. Dislocation density ranges from ~10¹¹ m⁻² (initial) to (0.3–10.9) × 10¹⁴ m⁻² depending on strain rate and strain.
- **Dynamic recrystallization (DRX):**  
  - At 850 °C and 0.01 s⁻¹, the DRX fraction reaches ~79.3% at ε = 0.9 (experimental) with an average grain size of 34.01 μm; at 1 s⁻¹ the DRX fraction is only ~42.8% with a larger grain size of 61.38 μm.  
  - Under constant high-temperature conditions (≥1050 °C, low strain rate) DRX is nearly complete (fraction > 96%), giving equiaxed recrystallized grains.  
  - In multi-stage deformation, the Zₚ history creates a bimodal grain structure: after a Zₚ increase, first-stage DRX grains (DRXGs I) are coarser than second-stage DRX grains (DRXGs II); after a Zₚ decrease, DRXGs I grow rapidly and the final grain size approaches that of constant conditions.

# Processing–Structure–Property Chain

**Processing** → **Microstructure** → **Property**

1. **Temperature and strain rate (Zₚ)** → **Dislocation accumulation / DRX kinetics**  
   Higher Zₚ (lower T, higher ε̇) raises dislocation storage rates, delays DRX nucleation, and refines first-stage DRX grains but suppresses second-stage nucleation. Lower Zₚ accelerates dynamic recovery and DRX.

2. **Transient Zₚ variations** → **Inhomogeneous dislocation density and multi-stage DRX**  
   - *Zₚ increase (e.g., strain rate jump 0.01→0.1 s⁻¹ or cooling 1050→950 °C):* The first-stage DRX fraction is initially high; after the transition, the enhanced dislocation accumulation drives abundant nucleation of fine second-stage DRX grains, leading to overall grain refinement but a lag in total DRX fraction compared to the constant high-Zₚ case.  
   - *Zₚ decrease (e.g., strain rate jump 0.1→0.01 s⁻¹ or heating 950→1050 °C):* Dynamic recovery reduces dislocation density, DRX kinetics accelerate dramatically, and the DRX fraction can temporarily exceed that of the corresponding constant-condition curve. First-stage grains coarsen, diminishing the grain size difference between stages.

3. **Microstructural outcome** → **Flow stress (mechanical property)**  
   - The inhomogeneous dislocation density and multi-stage DRX modify work hardening, dynamic recovery, and dynamic softening.  
   - When Zₚ is increased, the flow stress rises at the transition and subsequently softens as second-stage DRX consumes the deformed matrix.  
   - When Zₚ is decreased, an abrupt stress drop occurs, followed by further gradual softening to a new steady state.  
   - The phenomenological Model 2, which introduces a softening coefficient kₛ that depends on current DRX fraction and the Zₚ difference between stages, captures these transient stress evolutions; standard Model 1 without kₛ overestimates the loading force and fails to reproduce the softening rate.

4. **Integrated prediction:** The 3D cellular automaton model with inhomogeneous dislocation density reproduces the experimentally observed histories of flow stress, DRX fraction, and average grain size under all tested transient paths, providing a validated link from processing variables to mechanical response.

# Mechanistic Interpretation

- **Inhomogeneous dislocation density as the driver:** Dislocations are non-uniformly distributed, with highest densities near grain boundaries. This gradient creates local driving pressures for nucleation of new DRX grains preferentially at matrix grain boundaries.
- **Competition between DRX stages:** When Zₚ increases, the existing (first-stage) DRX grains are continuously refined by the newly nucleated second-stage grains, which exhibit lower dislocation density, thereby sustaining a dynamic refinement mechanism. This “pseudo-metadynamic” growth of only the DRX grains during the transient period explains the observed stress softening and grain size evolution.
- **Residual softening memory:** The stress softening coefficient kₛ captures the history effect: the larger the difference in Zₚ between stages and the higher the first-stage DRX fraction, the less residual work hardening remains for the second stage, resulting in lower saturation stress. This is essential for predicting multi-stage flow stress accurately.
- **Limit of homogeneous models:** A model that neglects dislocation density heterogeneity (Model 1) cannot reproduce the overshoot of DRX fraction under Zₚ decrease or the correct post-transient softening rate, illustrating that inhomogeneity must be explicitly accounted for in transient deformation simulations.

# Key Quantitative Findings

| Condition | Key measured/simulated value | Experimental | Simulation (3D CA / Model 2) |
|-----------|------------------------------|--------------|-----------------------------|
| 850 °C, 0.01 s⁻¹, ε = 0.9 | DRX fraction / avg. grain size | 79.3% / 34.01 μm | 84.98% / 34.53 μm |
| 850 °C, 1 s⁻¹, ε = 0.9 | DRX fraction / avg. grain size | 42.8% / 61.38 μm | 49.59% / 65.87 μm |
| 950 °C, 0.01→0.1 s⁻¹ at ε₁ = 0.2, ε = 0.9 | Final avg. grain size (EBSD) | 28.89 μm → 37.16 μm (transient) | – |
| 950 °C, 0.1→0.01 s⁻¹ at ε₁ = 0.4 | DRX fraction increase at transition | 38.9% (ε = 0.4) → 95.2% (ε = 0.5) | 42.9% → 99.1% |
| 1050→950 °C (cooling) at 0.01 s⁻¹, ε₁ = 0.2 | Final avg. grain size | 53.29 μm | – |
| 950→1050 °C (heating) at 0.01 s⁻¹, ε₁ = 0.4 | Final avg. grain size | 79.69 μm | 75.90 μm (CA) |
| All transient paths | Flow stress – Model 2 vs. Model 1 | Experimental force–stroke curves | Model 2 matches experimental force; Model 1 overestimates 2nd-stage force |

- The softening coefficient kₛ varies between 0.2 (maximum softening) and 1.0 (no softening) depending on ln Zₚ(I) and ln Zₚ(II) and first-stage DRX fraction.
- Dislocation density at 850 °C, 0.01 s⁻¹ reaches ~3.87 × 10¹⁴ m⁻² at ε = 0.9; at 1 s⁻¹ it reaches ~1.09 × 10¹⁵ m⁻².
- Increasing the transition strain ε₁ delays the second-stage DRX and coarsens the final grain size under both temperature and strain-rate transient paths.

# Visual Evidence

**figure_001** – Publisher icon; contains no experimental data.  
**figure_002** – Experimental workflow and thermomechanical processing schemes, establishing the hot compression protocols and transient path definitions.  
**figure_003** – Schematic of true stress–true strain curves under varying Zₚ, illustrating the characteristic stress responses (jump/drop) after a sudden change in deformation condition.  
**figure_004** – 3D surface plot of stress softening coefficient kₛ as function of ln Zₚ(I), ln Zₚ(II), and first-stage DRX fraction, quantifying the history-dependent softening behavior.  
**figure_005** – Comparison of experimental 3D optical metallography and simulated 3D CA initial microstructures, validating the inhomogeneous initial mixed-grain model.  
**figure_006** – Flowchart of the 3D CA algorithm with inhomogeneous dislocation density, explaining the integration of constitutive laws, nucleation, and grain boundary migration.  
**figure_007** – Experimental and simulated DRX fraction evolution curves at four temperatures and four strain rates, validating the acceleration of DRX kinetics with temperature and strain rate.  
**figure_008** – Experimental and simulated true stress–strain curves under constant conditions (850–1150 °C, 0.01–10 s⁻¹), confirming the CA model’s predictive accuracy for peak stress and softening.  
**figure_009** – Flow stress curves under strain-rate transient conditions (0.01↔0.1 s⁻¹) at 950 °C, comparing Model 1 and Model 2; Model 2 accurately captures the stress drop and new steady state.  
**figure_010** – Flow stress curves under temperature transient conditions (950↔1050 °C) at 0.01 s⁻¹, demonstrating Model 2’s superiority in predicting post-transition stress evolution.  
**figure_011** – Force–stroke curves comparing experiment, Model 1, and Model 2 for transient conditions; Model 2 yields correct load predictions, Model 1 overestimates second‑stage force.  
**figure_012** – CA-simulated dislocation density maps and flow curves at 850 °C, showing higher strain rates produce larger dislocation densities and delay DRX, consistent with the measured stress levels.  
**figure_013** – DRX kinetics and EBSD validation at 850 °C under 0.01 and 1 s⁻¹; the CA model reproduces the fraction–grain size trade-off and the microstructural maps.  
**figure_014** – Comprehensive flow-stress validation of the 3D CA model for all transient strain-rate and temperature paths; quantitative agreement supports the model’s universality.  
**figure_015** – Side‑by‑side comparison of DRX fraction evolution from Model 2 and 3D CA under varying conditions; CA captures the delayed nucleation (Zₚ increase) and overshoot (Zₚ decrease) that Model 2 misses.  
**figure_016** – Model 1 DRX fraction curves under transient conditions, showing monotonic behavior and confirming the model’s inability to reproduce non‑monotonic kinetics.  
**figure_017** – Experimental and simulated AGS evolution under transient conditions; validates the CA prediction of grain refinement/coarsening trends with transition strain and Zₚ change.  
**figure_018** – EBSD microstructures and CA maps for strain‑rate increase at 950 °C, revealing that earlier strain‑rate transition leads to finer final grain size due to prolonged second‑stage nucleation.  
**figure_019** – Bar charts of DRX fraction after strain‑rate and temperature variations at ε₁ = 0.4, quantitatively confirming the CA prediction accuracy at intermediate strains.  
**figure_020** – EBSD and CA comparison for decreasing temperature from 1050 to 950 °C, showing multi‑stage grain populations and grain size reduction.  
**figure_021** – Transient strain‑rate decrease (0.1→0.01 s⁻¹) at ε₁ = 0.4: EBSD and CA show rapid DRX completion and grain size convergence, validating the accelerated softening mechanism.  
**figure_022** – Heating from 950 to 1050 °C; demonstrates that temperature increase yields finer final grain size than isothermal 1050 °C, validating the model’s handling of transient heating.  
**figure_023** – Simulated DRX fraction and average dislocation density evolutions under Zₚ increase (strain-rate jump and cooling), detailing the competition between DRXGs I and DRXGs II.  
**figure_024** – Microstructure and dislocation density maps for Zₚ increase cases, visualizing the preferential nucleation of DRXGs II at matrix grain boundaries and the progressive refinement.  
**figure_025** – DRX fraction and dislocation density evolutions under Zₚ decrease, showing the initial rapid DRX surge and subsequent decline of DRXGs I fraction as refinement sets in.  
**figure_026** – CA maps for strain‑rate decrease at 950 °C, illustrating homogenization of dislocation density and faster DRX compared to constant low strain rate.  
**figure_027** – CA maps for heating from 950 to 1050 °C, demonstrating the acceleration of multi‑stage recrystallization compared to isothermal 1050 °C.  
**figure_028** – Evolution of average grain size of DRXGs I and DRXGs II under four transient conditions, quantifying the bimodal distribution upon Zₚ increase and the coarsening/growth balance upon Zₚ decrease.
