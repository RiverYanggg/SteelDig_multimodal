# Material System
The studied material is a low-density austenitic steel with nominal composition Fe–20Mn–9Al-1.5C–2Ni–3Cr (wt.%). The analyzed chemical composition is Fe-20.3Mn-8.6Al-1.4C-2.1Ni-2.9Cr (wt.%). The steel is designed with high Mn, Al, and C contents to achieve low density and high strength-ductility synergy. Ni and Cr are added to influence grain boundary precipitation and toughening behavior. The microstructural constituents include an austenite (γ) matrix, coherent nanoscale κ-carbides (3–10 nm) uniformly dispersed within grains, intergranular Cr₇C₃ precipitates, and low-energy special grain boundaries (Σ ≤ 29, primarily Σ3 annealing twins) alongside random high-angle grain boundaries (RHAGBs).

# Processing Route and Variables
Ingots were produced by vacuum induction melting. The cast ingots were homogenized at 1200 °C for 2 h, then hot-rolled at 1050–950 °C to a final thickness of 6 mm and air-cooled. Four heat treatment routes were applied to the hot-rolled sheets:
- **S1000**: single-stage heat treatment at 1000 °C for 3 min followed by quenching.
- **S1050**: single-stage heat treatment at 1050 °C for 3 min followed by quenching.
- **S1100**: single-stage heat treatment at 1100 °C for 3 min followed by quenching (used for tensile comparison only).
- **MHT**: multi-stage heat treatment consisting of 1000 °C / 3 min → quench → 750 °C / 15 min → quench → 1050 °C / 3 min → quench.

All heat treatments terminated with quenching to room temperature. The key variable distinguishing MHT from single-stage treatments is the intermediate annealing at 750 °C for 15 min, which intentionally precipitates grain-boundary phases that act as nucleation sites for special boundaries during subsequent re-austenitization at 1050 °C.

# Microstructure and Phase Evolution
- **Grain size (effective grain size)**: S1000, 3.17 μm; S1050, 3.84 μm; MHT, 7.31 μm. The MHT route yields the largest grain size due to the additional thermal cycle.
- **Grain boundary character (EBSD)**: The fractions of Σ ≤ 29 special boundaries are 71.7% for S1000, 68.3% for S1050, and 71.2% for MHT. Misorientation angle distributions for all conditions exhibit a strong peak near 60°, corresponding to Σ3 annealing twins. In MHT, twin density is increased relative to S1050, and twin sizes are smaller, but the overall special-boundary fraction remains high and comparable to S1000.
- **Precipitates (TEM and SAED)**:
  - **κ-carbides**: Coherent nanoscale κ-carbides (3–10 nm) are uniformly present in the austenite matrix under all heat treatment conditions, with the orientation relationship [011]γ // [011]κ.
  - **S1000**: Elongated, stripe-like Cr₇C₃ precipitates are observed along austenite grain boundaries. SAED indexed along the [112̄]Cr₇C₃ zone axis confirms (220) and (021̄) reflections.
  - **S1050**: Cr₇C₃ is dissolved; instead, intragranular B2-structured precipitates (20–160 nm) form within austenite grains. SAED confirms the B2 phase along the [1̄11] zone axis.
  - **MHT**: Cr₇C₃ is absent; B2 precipitates are present within grains with sizes slightly smaller than those in S1050. SAED confirms B2 along the [113] zone axis.
- **Intermediate 750 °C stage (MHT)**: Dense grain-boundary precipitates form during the 15 min hold at 750 °C. These precipitates serve as nucleation sites for annealing twins during the final 1050 °C/3 min step, thereby enhancing the special boundary network while fragmenting random boundary connectivity.

# Processing-Structure-Property Chain
## Processing → Structure
- The single-stage S1000 (lowest temperature) retains intergranular Cr₇C₃ and achieves the smallest grain size (~3.17 μm) with a high special-boundary fraction (71.7%) but with precipitates that embrittle random grain boundaries.
- Increasing the single-stage temperature to 1050 °C (S1050) dissolves Cr₇C₃, slightly increases grain size to 3.84 μm, introduces intragranular B2 precipitates, and reduces the special-boundary fraction to 68.3%.
- The multi-stage MHT route (1000 °C → 750 °C → 1050 °C) eliminates Cr₇C₃, increases grain size to 7.31 μm, and restores a high special-boundary fraction of 71.2% while generating a finer twin network via the intermediate precipitation step.

## Structure → Property
- **Tensile properties (room temperature)**:
  - S1000: YS ~955 MPa, UTS ~1126 MPa, total elongation 55.5%.
  - S1050: YS ~945 MPa, UTS ~1113 MPa, total elongation 55.8%.
  - S1100: YS ~827 MPa, UTS ~998 MPa (elongation not explicitly reported in quantified form but the lowest strength among conditions, supporting lower grain-boundary and precipitation strengthening contributions).
  - MHT: YS ~910 MPa, UTS ~1076 MPa, total elongation 50.9%.
  - All conditions exhibit three-stage strain hardening, with maximum strain hardening rates approaching ~2000 MPa at true strains of 0.20–0.22. The MHT sample maintains a favorable strength–ductility balance despite a larger effective grain size (7.31 μm vs. 3.84 μm for S1050).
- **Impact toughness (Charpy, room temperature)**:
  - S1000: total absorbed energy 29.2 J (crack initiation energy ~18 J; crack propagation energy 9.87 J).
  - S1050: total absorbed energy 42.8 J (crack propagation energy 26.64 J).
  - MHT: total absorbed energy 55.1 J (crack propagation energy 36.78 J).
  - **Relative improvement**: MHT achieves an 88.6% increase in impact toughness over S1000 (55.1 J vs. 29.2 J). The crack initiation energies remain similar across all conditions (~16–19 J), identifying enhanced crack propagation resistance as the primary source of toughening.
- **Fractography**:
  - S1000 tensile fracture surfaces show dimples mixed with quasi-cleavage features, microcracks, and microvoids.
  - S1050 tensile fracture surfaces exhibit more uniform dimple morphology consistent with ductile fracture.
  - MHT tensile fracture surfaces are dominated by fine, dense dimples without quasi-cleavage facets, and a larger macroscopic shear zone.
  - Impact fracture surfaces: S1000 and S1050 display quasi-cleavage morphologies with flat facets, microcracks, and microvoids. MHT shows a transition to ductile dimple rupture.

# Mechanistic Interpretation
- **Strength**: Strength is sustained by solid-solution strengthening (Mn, C, Al, Ni, Cr), grain boundary strengthening (Hall–Petch effect), and nanoscale κ-carbide precipitation strengthening. The slight reduction in YS and UTS for MHT relative to S1000 and S1050 is attributed to the larger grain size (7.31 μm), partially compensated by the dense special-boundary network and B2 precipitates.
- **Toughening**: The dramatic improvement in impact toughness arises primarily from increased crack propagation energy, whereas crack initiation energy remains nearly constant (~18 J).  
  - In S1000, intergranular Cr₇C₃ precipitates act as preferential crack nucleation sites and promote rapid, straight crack propagation along RHAGBs, despite a 71.7% special-boundary fraction.  
  - In S1050, dissolution of Cr₇C₃ eliminates brittle grain-boundary precipitates, allowing cracks to interact with special boundaries, producing deflection and propagation through annealing twins. The lower special-boundary fraction (68.3%) limits the full toughening potential.  
  - In MHT, the combination of (i) complete elimination of Cr₇C₃, (ii) a high special-boundary fraction (71.2%) with a fine twin network, and (iii) larger effective grain size (7.31 μm) forces extensive, repeated zigzag crack deflection along special boundaries and through twins. This tortuous crack path absorbs more energy and effectively fragments the random boundary network, resulting in transgranular dimple fracture instead of intergranular quasi-cleavage.  
  - The 750 °C intermediate stage is critical: grain-boundary precipitates formed at this step promote twin nucleation during the final 1050 °C step, enhancing special boundary connectivity while dissolving the deleterious Cr₇C₃ phase.

# Key Quantitative Findings
- **Special boundary (Σ ≤ 29) fractions**: S1000 71.7%; S1050 68.3%; MHT 71.2%.
- **Grain size (effective)**: S1000 3.17 μm; S1050 3.84 μm; MHT 7.31 μm.
- **κ-carbides**: coherent, 3–10 nm, uniform in all conditions.
- **Cr₇C₃**: present at grain boundaries in S1000 only; dissolved in S1050 and MHT.
- **B2 precipitates**: intragranular, 20–160 nm, present in S1050 and MHT; slightly smaller in MHT.
- **Tensile properties (room temperature)**:  
  - S1000: YS ~955 MPa, UTS ~1126 MPa, TEL 55.5%.  
  - S1050: YS ~945 MPa, UTS ~1113 MPa, TEL 55.8%.  
  - MHT: YS ~910 MPa, UTS ~1076 MPa, TEL 50.9%.
- **Impact toughness**:  
  - S1000: 29.2 J (initiation ~18 J, propagation 9.87 J).  
  - S1050: 42.8 J (propagation 26.64 J).  
  - MHT: 55.1 J (propagation 36.78 J).  
  - MHT exhibits an 88.6% increase over S1000, driven entirely by enhanced crack propagation energy.
- **Strain hardening**: Three-stage hardening observed in all samples; maximum hardening rate ~2000 MPa at εtrue ≈ 0.20–0.22.

# Visual Evidence
- **Figure 2 (fabrication schematic)** illustrates the complete thermomechanical process route, distinguishing the single-stage S1000, S1050, S1100 pathways from the multi-stage MHT route, and visually emphasizes the role of the 750 °C intermediate treatment in grain boundary engineering.
- **Figure 3 (SEM and EBSD boundary maps)** supports the microstructural hierarchy:  
  - S1000 shows intergranular Cr₇C₃ (white arrows) with 71.7% special boundaries.  
  - S1050 shows clean grain boundaries without Cr₇C₃ but lower twin density and 68.3% special boundaries.  
  - MHT shows larger grain size, increased twin density, smaller twin size, and 71.2% special boundaries.  
  The EBSD maps (red = Σ ≤ 29, black = RHAGBs) and 60° misorientation peaks confirm the dominance of Σ3 twins.
- **Figure 4 (TEM and SAED)** provides direct evidence of precipitate evolution:  
  - κ-carbides (3–10 nm) in all samples, with superlattice spots confirming the [011]γ//[011]κ relationship.  
  - Cr₇C₃ at grain boundaries of S1000 only, with SAED along [112̄] showing (220) and (021̄) reflections.  
  - B2 particles (20–160 nm) in S1050 and MHT with SAED along [1̄11] and [113] zone axes, and slightly smaller B2 sizes in MHT.
- **Figure 5 (tensile curves)** supports the conclusion that MHT retains high strength and ductility: YS ~910 MPa, UTS ~1076 MPa, TEL ~50.9% versus S1000 (955 MPa, 1126 MPa, 55.5%) and S1050 (945 MPa, 1113 MPa, 55.8%). The true stress–strain and strain hardening rate curves confirm three-stage hardening behavior with maximum hardening rates near 2000 MPa.
- **Figure 6 (instrumented Charpy curves and energy decomposition)** directly supports the 88.6% increase in total impact energy (55.1 J for MHT vs. 29.2 J for S1000) and demonstrates that crack initiation energy is nearly constant (~16–19 J), while propagation energy increases from 9.87 J (S1000) to 26.64 J (S1050) to 36.78 J (MHT). Load–displacement curves show the largest displacement for MHT (8.04 mm).
- **Figure 7 (tensile fractography SEM)** shows a progression from mixed dimple/quasi-cleavage in S1000, to uniform dimples in S1050, to fine dense dimples without quasi-cleavage in MHT, consistent with improved ductile fracture behavior from grain boundary optimization.
- **Figure 8 (impact fractography SEM)** shows quasi-cleavage facets with microcracks and microvoids in S1000 and S1050, while MHT exhibits a transition to ductile dimple fracture, visually corroborating the impact toughness enhancement.
- **Figure 9 (cross-sectional crack paths SEM)** directly visualizes the toughening mechanism: in S1000, intergranular Cr₇C₃ leads to straight intergranular crack paths; in S1050, cracks partially deflect along special boundaries and cut twins; in MHT, pronounced zigzag cracking across multiple twins occurs with continuous deflection, supporting the crack deflection/dissipation mechanism.
- **Figure 10 (intermediate 750 °C stage SEM)** confirms dense grain-boundary precipitates formed at 750 °C, which act as nucleation sites for twins in the subsequent 1050 °C step, thereby enhancing MHT’s special boundary network.
- **Figure 11 (schematic of crack propagation mechanisms)** summarizes the contrast between rapid propagation along RHAGBs in S1000 (with Cr₇C₃) and the tortuous, deflected crack path through special boundaries in MHT.
