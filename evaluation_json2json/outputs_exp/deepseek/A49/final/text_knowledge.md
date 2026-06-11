# Material System

- Austenitic Fe-Mn-Al-C steel (nominal base composition ~29 wt% Mn, ~9 wt% Al, ~0.9 wt% C)
- ESR-produced ingot with exact analyzed composition: Fe-28Mn-9Al-0.86C-0.7W-0.43Mo-0.49Nb (wt%)
- Two comparison martensitic chromium steels:
  - Fe-12Cr-1.5Ni-0.2V-1.8W-0.5Mo-0.15C (thermal fatigue reference)
  - Fe-13Cr-0.2C (elasto-plastic bending reference)

# Processing Route and Variables

- Solution treatment: heating to 1323 K followed by water quenching, establishing the initial microstructure for all cyclic tests.
- Fatigue testing (S-N curves): rotating bending on a Schenk machine, baseline endurance set at 2 × 10⁷ cycles.
- Fatigue test temperature conditions:
  - Isothermal at 293 K
  - Isothermal at 673 K
  - Thermocycling between 293 K and 673 K (heating to 673 K, then pulse cooling in distilled water to 293 K)
- Thermal fatigue test (restricted thermal expansion): 80 % restriction of thermal expansion; specimen heated by contact electric resistance to 873 K and cooled by compressed air to 313 K; cyclic temperature window 873 K ↔ 313 K.
- Elasto-plastic bending test: constant free-end deflection of 150 mm applied to cylindrical specimens with a gauge diameter of 50 mm, on a ZDM-200PU machine.
- Tensile test: specimen diameter 5 mm, gauge length 25 mm, strain rate 1 mm/min.
- Metallographic etching: 4–7 % nitric acid in ethanol.
- TEM foil preparation: electropolishing in a chromic‑phosphoric acid electrolyte (60 g CrO₃ + 400 mL H₃PO₄) at 20–50 °C, 15–20 V, current density 5–8 A/cm².

# Microstructure and Phase Evolution

- As‑solution‑treated microstructure (Fe-28Mn-9Al-0.86C-0.7W-0.43Mo-0.49Nb): equiaxed austenite grains with discrete κ‑phase precipitates decorating the grain boundaries (optical micrograph, Figure 3a).
- After thermal cycling (293 K ↔ 673 K): coarsening/thickening of grain‑boundary κ‑phase precipitates, consistent with thermal aging during fatigue exposure (Figure 3b). No indication of austenite decomposition is reported.
- In the martensitic Cr‑Ni comparison steel (Fe-12Cr-1.5Ni-0.2V-1.8W-0.5Mo-0.15C): initial lath martensite structure (Figure 3c) completely decomposes under the same thermal cycling to an equilibrium ferrite‑carbide mixture with loss of original crystallographic orientation (Figure 3d).
- Dislocation substructure after cold working (same Fe-28Mn-9Al-0.86C base)
  - 10 % cold working (TEM, Figure 6a): moderate dislocation density, dislocations distributed in slip‑system arrays.
  - 20 % cold working (TEM, Figure 6b): sharp increase in dislocation density, formation of localized dislocation tangles at slip‑system intersections.
- Tensile deformation promotes mechanical twinning; deformation twins are observed and act as barriers to dislocation motion, contributing to persistent strain hardening (deduced from the true stress–true strain curve and stated mechanism).

# Processing-Structure-Property Chain

1. **Solution treatment (1323 K WQ) → austenite + grain‑boundary κ‑phase** serves as the baseline for all cyclic loading investigations.
2. **Isothermal fatigue at 673 K** produces time‑dependent deformation aging (precipitation strengthening) in the microplastic zones, raising the fatigue strength above the room‑temperature level (Figure 2: S‑N curve at 673 K lies above that at 293 K).
3. **Thermocycling (293 K ↔ 673 K)** superimposes periodic quenching stresses and microstructure evolution; the observed coarsening of κ‑phase (Figure 3b) does not cause embrittlement and the fatigue strength remains intermediate between the two isothermal curves (Figure 2, curve 3).
4. **Thermal fatigue (873 K ↔ 313 K, 80 % restriction)** – in the martensitic steel leads to decomposition into ferrite‑carbide mixture; in the Fe‑Mn‑Al‑C steel only κ‑phase coarsening occurs, preserving cyclic resistance (Figure 3b vs. 3d).
5. **Elasto‑plastic bending (constant 150 mm deflection, φ50 mm)** → cold‑work‑induced mechanical twinning and intense dislocation tangles (Figure 6) create highly strengthened local volumes that maintain an invariant hysteresis energy per cycle (Figure 4) and extend the lifetime to about **four times** that of the martensitic chromium steel (Fe-13Cr-0.2C) under identical cyclic conditions.
6. **Monotonic tensile deformation** at 1 mm/min produces continuous strain hardening to ~1400 MPa true stress at 0.4 true strain (Figure 5), driven by the same twinning‑induced hardening mechanism, which underpins the high endurance in the elasto‑plastic regime.

# Mechanistic Interpretation

- **Anomalous temperature dependence of fatigue strength**: At 673 K the enhanced fatigue resistance compared with 293 K is attributed to **time‑dependent precipitation hardening (deformation aging) in the microplastic deformation zones**, a mechanism that is active during prolonged high‑temperature cycling and strengthens regions that experience cyclic microyielding.
- **High endurance in elasto‑plastic bending**: The alloy undergoes **mechanical twinning** during the early cycles, generating twin boundaries that hinder dislocation glide. With increasing cycles, **dislocation density rises sharply and localized tangles form** (Figure 6). These highly strengthened domains act as obstacles that localise further plastic flow, keeping the **absorbed energy per cycle nearly constant** (as seen by nearly overlapping 2nd and 12th cycle hysteresis loops in Figure 4). Failure occurs only after the entire working volume has been consumed by this stable cyclic hardening.
- **Microstructural stability under thermal cycling**: κ‑phase coarsening does not degrade fatigue performance, while the martensitic comparison alloy undergoes brittle equilibrium‑phase decomposition, explaining the poorer thermal fatigue response of the Cr‑based steel.
- **Strain hardening capacity**: The 1400 MPa true stress at 0.4 strain in uniaxial tension (Figure 5) quantitatively demonstrates the large work‑hardening reserve that sustains cyclic elasto‑plastic loading without softening.

# Key Quantitative Findings

| Measurement | Condition | Value / Observation | Source Figure |
|------------|-----------|---------------------|---------------|
| Fatigue stress amplitude range | Rotating bending, 293 K–673 K, 2×10⁷ baseline | 220 – 540 MPa (S‑N curves) | Figure 2 |
| Relative fatigue resistance | 673 K isothermal vs. 293 K isothermal | 673 K curve lies above 293 K curve; thermocycling curve lies between them | Figure 2 |
| Run‑out specimens | 673 K and thermocycling | Specimens survived > 2×10⁷ cycles (marked by horizontal arrows) | Figure 2 |
| Thermal‑fatigue microstructural change (austenitic steel) | 873 K ↔ 313 K, 80 % restriction | κ‑phase coarsening, no decomposition | Figure 3a,b |
| Thermal‑fatigue microstructural change (martensitic steel) | Same conditions | Martensite → ferrite‑carbide mixture | Figure 3c,d |
| Elasto‑plastic bending hysteresis | φ50 mm, 150 mm deflection | Load range ± 50 kN, deflection ± 200 mm; loops stabilize by 2nd cycle; 12th loop nearly identical | Figure 4 |
| Relative elasto‑plastic fatigue life | Fe-Mn-Al-C vs Fe-13Cr-0.2C | Fe-Mn-Al-C endures ≈4× the number of cycles to failure | Figure 4 caption/description |
| True stress–true strain in tension | 1 mm/min, 293 K, φ5 ×25 mm | ~1400 MPa at 0.4 true strain; continuous hardening | Figure 5 |
| Dislocation structure after cold work | 20 % reduction | High dislocation density, localized tangles at slip intersections | Figure 6b |

# Visual Evidence

- **Figure 1 (chart_schematic)**: Experiment setups for thermocycling (873 K ↔ 313 K, 80 % restriction, φ5 mm specimen, resistance heating) and elasto‑plastic bending (φ50 mm, 150 mm constant deflection). Provides the precise geometric and thermal constraints used in the study.
- **Figure 2 (property_mechanical)**: S‑N curves for Fe‑Mn‑Al‑C steel at 293 K, 673 K, and under 293 K ↔ 673 K thermocycling. Directly demonstrates higher fatigue strength at 673 K and intermediate behaviour under cycling, with run‑out data points.
- **Figure 3 (microscopy_optical)**: Optical micrographs (scale bar 30 µm) comparing as‑received and thermally cycled microstructures. Subfigure a/b confirm κ‑phase coarsening in the austenitic steel; c/d show full martensite decomposition in the Cr‑Ni steel, supporting the contrast in thermal stability.
- **Figure 4 (property_mechanical)**: Force‑deflection hysteresis loops for 1st, 2nd, and 12th cycles. Evidence of rapid stabilization and invariant energy absorption, underpinning the ≈4× life improvement over martensitic Cr steels.
- **Figure 5 (property_mechanical)**: True stress–true strain curve showing ~1400 MPa at 0.4 strain, with continuous hardening. Links the high work‑hardening capacity (mechanical twinning) to the observed cyclic endurance.
- **Figure 6 (microscopy_tem)**: TEM bright‑field images (scale bar 625 nm) after 10 % and 20 % cold work. Reveals the evolution from dispersed dislocations to dense tangles, visualising the microstructural basis for invariant hysteresis energy and high elasto‑plastic fatigue resistance.
