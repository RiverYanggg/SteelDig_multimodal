# Material System
The material investigated is SPCE steel, a deep-drawing quality low-carbon steel sheet. SPCC cold-rolled steel sheet is also mentioned in comparative measurements. SPCE is a low-carbon ferritic steel designed for formability. The study focuses on the as-received cold-rolled condition, with subsequent plastic deformation introduced by uniaxial tensile testing.

# Processing Route and Variables
- **Initial state**: as-received cold-rolled SPCE sheet.
- **Plastic deformation**: uniaxial tensile pre-strain applied up to true plastic strains ε = 0–0.25. Specimens were strained to fixed levels, including a 15% pre-strain condition.
- **Post-deformation heat treatment**: selected specimens (e.g., 15% pre-strained SPCC) were heat-treated at 373 K for 90 h to partially recover Cottrell atmospheres.
- **Macroscopic modulus measurement**: precision tensile tests with an extensometer on pre-strained specimens; tangent modulus extracted from unloading or reloading slopes.
- **Spring-back evaluation**: V-bending tests on SPCE sheet; bend angles before unloading ranging from ~160° to 90°; spring-back angle measured experimentally. Finite element simulations performed with both a constant Young's modulus and a modulus that varies with plastic strain according to the fitted polynomial \(E = E_0 (351\varepsilon^2 - 160\varepsilon + 93.8)\).
- **Nano-indentation sample preparation**:
  - Surface etched to reveal grain boundaries.
  - Vickers hardness indents applied as position markers (diamond-shaped array) for exact location identification.
  - Chemical mechanical polishing (CMP) to flatten the surface and eliminate the etched ditch at grain boundaries, ensuring reliable nano-indentation contact.
- **Nano-indentation setup**: integrated scanning probe microscopy (SPM) and nano-indentation system with a 3-D piezo actuator and transducer; spherical indenter tip of nominal radius 50 µm (some measurements also with 200 µm tip); low indentation depths of a few nanometers to ~12 nm. Load–displacement (P–h) curves recorded, contact stiffness S = dP/dh from initial unloading slope used to derive local reduced modulus via Oliver–Pharr method.

# Microstructure and Phase Evolution
- The as-received SPCE sheet has a polycrystalline ferritic microstructure. No explicit phase transformation is reported.
- Plastic deformation introduces mobile dislocations that are released from Cottrell atmospheres (interstitial carbon atoms pinning dislocations in low-carbon steel).
- Dislocation pile-up occurs at grain boundaries, creating a heterogeneous dislocation density: higher near grain boundaries, lower in grain interiors.
- Post-deformation heat treatment at 373 K for 90 h allows diffusion of carbon atoms back to dislocations, partially restoring Cottrell atmospheres and reducing mobile dislocation density.
- No new phases or precipitates are reported; microstructural changes are entirely in the dislocation substructure and solute–dislocation interactions.

# Processing-Structure-Property Chain
1. **Plastic deformation (ε = 0–0.25)** → generation and motion of dislocations, release from Cottrell pinning → mobile dislocations pile up against grain boundaries → **microscopic heterogeneity**: dislocation density is elevated near grain boundaries, depleted in grain interiors.
2. **Mobile dislocations near boundaries** → during unloading after deformation (or during elastic reloading), these dislocations can move backward under reverse stress, contributing an apparent anelastic strain component → **macroscopic elastic modulus reduction**: the slope of the stress–strain curve during small reloading is lower than the intrinsic Young's modulus. Experimentally measured normalized modulus \(\delta E = E/E_0\) drops from 100% to ~72–75% at ε = 0.25 (over 20% reduction).
3. **Local effect detected by nano-indentation**: in the vicinity of a grain boundary, the reduced modulus \(E_r\) drops to approximately 50–150 GPa, while grain interiors show 200–350 GPa. The modulus minimum coincides with the grain boundary position, directly confirming spatial correlation with dislocation pile-up.
4. **Partial recovery by heat treatment**: an SPCC specimen pre-strained 15% and then heated at 373 K for 90 h shows partial recovery of the elastic modulus, evidenced by a less pronounced nonlinearity and a smaller reduction in tangent modulus compared to the as-pre-strained condition. This supports the Cottrell atmosphere mechanism: re-pinning of dislocations reduces their mobility.
5. **Spring-back prediction**: V-bending experiments on SPCE show that spring-back angle increases as the bend angle decreases. Simulations adopting a variable (plastic-strain-dependent) Young's modulus accurately track experimental spring-back values (within ~0.1–0.25°), whereas simulations with a constant modulus systematically underestimate spring-back.

# Mechanistic Interpretation
The observed reduction in apparent elastic modulus after plastic deformation is attributed to the **dislocation pile-up and Cottrell effect** mechanism. In low-carbon steel, dislocations are initially pinned by interstitial carbon atoms (Cottrell atmospheres). Plastic deformation tears dislocations away from their atmospheres, rendering them mobile. These mobile dislocations glide and accumulate at grain boundaries, forming pile-up arrays. When external load is reduced or reversed (as during unloading in a tensile test, or after bending), the stress concentrated at pile-up tips can drive dislocations back toward the grain interior. This back‑motion constitutes an anelastic strain that reduces the measured elastic slope. Consequently, the macroscopic elastic modulus depends on the density of mobile dislocations and the magnitude of prior plastic strain. The local modulus minima detected by nano-indentation precisely at grain boundaries provide direct microstructural evidence linking pile-up configuration to property degradation. The partial restoration of modulus after aging at 373 K confirms that carbon diffusion back to dislocations reduces dislocation mobility, thereby recovering a portion of the true elastic modulus.

# Key Quantitative Findings
- For SPCE steel, the normalized elastic modulus \(\delta E = E/E_0\) follows the polynomial fit \(E = E_0 (351\varepsilon^2 - 160\varepsilon + 93.8)\) over the plastic strain range 0 ≤ ε ≤ 0.25. At ε = 0.25, δE ≈ 72–75%, corresponding to >20% reduction in Young's modulus.
- V-bending spring-back angles: experimental values range from ~0.9° to 1.4°. Simulations with variable modulus match experiments, whereas constant-modulus simulations under-predict spring-back by approximately 0.1–0.25°.
- Nano-indentation near grain boundaries in SPCE: reduced modulus \(E_r\) drops to 50–150 GPa at the boundary, compared to 200–350 GPa in the grain interior (depending on grain orientation). This trend is reproducible along multiple scan lines.
- Tangent modulus of pre-strained SPCC (condition B: 15% pre-strain) decreases drastically from ~200–240 GPa (initial) to near zero within 0.3% reloading strain; the annealed specimen (condition E) maintains a nearly constant modulus ~200 GPa. Heat treatment (condition C: 15% pre-strain + 373 K/90 h) partially restores the modulus, showing intermediate degradation.
- Nano-indentation load–displacement curves on SPCE (spherical tip, R=50 µm) show sawtooth patterns characteristic of discrete plasticity events, at depths h=0–12 nm and loads up to 400 µN.

# Visual Evidence
- **Figure 1**: Normalized elastic modulus versus true plastic strain for SPCE/SPCC. The rapid initial drop and saturation beyond ~0.1 strain directly support the strain-dependent modulus reduction. The fitted polynomial is the basis for the variable-modulus approach in simulations.
- **Figure 2**: Comparison of experimental and simulated spring-back in V-bending. The agreement between variable-modulus simulations and experiment, versus systematic under-prediction by constant-modulus, validates the necessity of incorporating plastic-strain-dependent elastic properties.
- **Figure 3**: Schematic of dislocation pile-up at a grain boundary. Panels (a) and (b) illustrate how mobile dislocations accumulate, providing the microstructural mechanism for local modulus depression.
- **Figure 4**: Stress–strain curves and tangent modulus evolution for SPCC under various conditions. The nonlinearity and modulus decay in pre-strained conditions (B, C) versus linearity of the annealed (E) condition prove the role of mobile dislocations; partial recovery by heat treatment (C) links to Cottrell pinning.
- **Figure 5**: Nano-indentation setup schematic, confirming the integration of SPM for topography and transducer for P‑h data. This experimental capability enables the localized modulus measurements.
- **Figure 6**: Representative nano-indentation P‑h curve, defining the contact stiffness S used to calculate Er. This illustrates the measurement principle.
- **Figure 7**: AFM image of SPCE surface near a grain boundary after CMP, showing the three measurement lines for nano-indentation. The image validates the precise positioning of indents relative to the grain boundary.
- **Figure 8**: Actual nano-indentation P‑h curve on SPCE with spherical 50 µm tip. The sawtooth pattern and shallow depth confirm local probing of elastic properties.
- **Figure 9**: Spatial distribution of reduced modulus Er across grain boundaries on three scan lines. Each plot shows a pronounced dip at the grain boundary location (to ~50–150 GPa) compared to interior regions (200–350 GPa). This is direct visual evidence of the position-dependent elastic modulus and dislocation pile-up effect.
- **Figure 10**: Schematic of Vickers indentation markers used to locate measurement positions after CMP treatment. This is a methodological reference.
- **Figure 11**: Optical micrograph and measurement grid layout before CMP. The grain boundary and coordinate origin are identified, providing context for the nano-indentation mapping.
- **Figure 12**: Another presentation of nano-indentation modulus (Er) across a grain boundary, with data distinguished by tip radius (50 µm and 200 µm) and three Y‑positions. The consistent modulus minimum at the boundary across all conditions reinforces the pile-up mechanism and demonstrates measurement repeatability.
