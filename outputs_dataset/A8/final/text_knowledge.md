## Material System
- **Alloy**: Fe-10Mn-10Al-0.7C (wt.%) low-density steel.
- **Phases**: Ferrite (α, BCC, Al-rich), austenite (γ, FCC, Mn- and C-rich), κ-carbide (κ, perovskite structure, Mn- and Al-rich).
- **Condition**: As-cast ingot → homogenized (1200 °C, 1 h) → forged (1200 °C) → hot-rolled (finishing ~880 °C, water quench to ~300 °C, air cool to RT) → annealed (700–1200 °C, 1 h, water quench). Hot-rolled (HR) state used as baseline.

## Processing Route and Variables
- **Full thermomechanical route**: Homogenization at 1200 °C for 1 h → forging at 1200 °C → multi-pass hot rolling with finishing temperature ~880 °C → water cooling to ~300 °C → air cooling to room temperature.
- **Annealing treatment**: Reheating hot-rolled plates to target temperatures in the range 700–1200 °C, holding for **1 h**, followed by **water quenching**.
- **Key processing variable**: Annealing temperature (700, 800, 850, 900, 950, 1000, 1100, 1200 °C). Holding time fixed at 1 h.

## Microstructure and Phase Evolution
### As-rolled (HR) baseline
- **Microstructure**: Banded duplex structure of elongated α-ferrite and γ-austenite along rolling direction. Coarse α-grains alternate with γ bands on RD-ND plane; inhomogeneous distribution on RD-TD plane.
- **κ-carbide in HR state**: Present as precipitates along **α/γ phase boundaries and α/α grain boundaries** (SEM evidence). Not detected by XRD, attributed to low volume fraction or coherency with α-matrix.

### Phase constitution vs. annealing temperature (XRD quantification)
| Temperature (°C) | α fraction | γ fraction | κ fraction | Notes |
|---|---|---|---|---|
| HR | dominant | present | ~0.15–0.16 | κ detected, γ peaks present |
| 700 | ~0.84 | **absent** | present | Near-complete γ→α+κ eutectoid decomposition; γ peaks disappear in XRD |
| 800 | decreases | ~0.29 | decreasing | Three-phase coexistence (α+γ+κ) |
| 850 | further decrease | ~0.39 | further reduced | κ-carbide fraction drops significantly |
| 900 | ~0.40 | ~0.60 | **zero (XRD)** | κ dissolves; stable α+γ dual-phase |
| 900–1200 | 0.37–0.43 | 0.57–0.63 | zero (matrix) | Dual-phase stability range; γ peaks at ~0.63 at 1000 °C then declines slightly to 0.57 at 1200 °C |

### κ-carbide evolution
- **Equilibrium dissolution temperature (Thermo-Calc, TCFE7)**: 823 °C, via eutectoid reaction γ → α + κ.
- **Actual dissolution temperature (experimental)**: **Between 850 and 900 °C**, higher than equilibrium prediction. Attributed to calculation errors and disequilibrium effects during quenching.
- **Morphology sequence**:
  - **700 °C**: Lamellar κ-carbide + α matrix from eutectoid decomposition of γ. Continuous κ along grain boundaries. TEM confirms alternating lamellar κ and α plates; some lamellae maintain Nishiyama–Wassermann (N–W) orientation relationship: (110)α∥(1-11)κ, [001]α∥[011]κ. Globular/coarsened κ also present, **without orientation relationship** to α.
  - **800 °C**: κ coarsens into **elongated rod-like or globular** shapes. Distributed primarily along α/α and α/γ boundaries. TEM shows no orientation relationship between coarsened κ and α matrix (loss of coherency observed at 700 °C).
  - **850 °C**: κ fraction decreases significantly; κ mainly along **α/α boundaries**, disappearing from γ-phase areas.
  - **≥900 °C**: κ dissolves into matrix (matrix free of κ by XRD). However, **boundary κ-carbide** precipitates along α/α grain boundaries during quenching at all temperatures 900–1200 °C. At 1200 °C, intragranular needle-shaped FCC particles also appear within large α grains, competing with boundary κ for Mn and C.
  - **Boundary κ at high temperature**: TEM on 1100 °C and 1200 °C specimens confirms κ along α/α boundaries; N–W orientation relationship with adjacent α grain is maintained, but adjacent κ particles exhibit **large orientation misalignment** (dark-field imaging shows only discrete segments illuminated), indicating independent nucleation/variants.

### Grain size evolution (≥900 °C, from SEM)
- **α₂ (banded ferrite, solidified first)**: Largest grains, fastest growth. ~26 μm (900 °C) → ~68 μm (1200 °C).
- **γ (austenite)**: Moderate growth. ~5.5 μm (900 °C) → ~36 μm (1200 °C).
- **α₁ (intergranular ferrite, distributed among γ grains)**: Smallest grains. ~3.2 μm (900 °C) → slight decrease to ~2.5 μm (950 °C) → ~22 μm (1200 °C).
- **Banded microstructure**: Pronounced at 800 °C; gradually eliminated with increasing temperature; reduced continuity at 900 °C.

### Elemental partitioning (EDS line scan)
- **800 °C**: κ-carbide shows highest Mn and Al content; γ-phase is Mn-rich and Al-lean relative to α-phase.
- **900 °C**: Uniform elemental distribution; no κ signature peaks, confirming dissolution.

### Lattice parameters (XRD)
- α-phase: 2.89–2.91 Å; γ-phase: 3.65–3.67 Å; κ-carbide: 3.76–3.79 Å. Lattice expansion attributed to Mn, Al, and C solid solution.

## Processing-Structure-Property Chain
**Annealing temperature ↑ (700–1200 °C)** →
  - **700 °C**: γ→α+κ eutectoid → continuous GB κ + lamellar κ → high strength (~971 MPa UTS) but **brittle fracture (elongation only 4.8%)**; distinct yield drop.
  - **800–850 °C**: Partial κ dissolution, γ fraction increases (29% → 39%), κ coarsens/spheroidizes, loses coherency → strength decreases, ductility improves but still limited; rapid initial work hardening followed by precipitous decline.
  - **900 °C**: κ fully dissolved in matrix, fine dual-phase α (~40%) + γ (~60%), banding reduced → **optimal strength–ductility combination**: UTS 855 MPa, YS 651 MPa, elongation 36.6%, product of strength and ductility ~31 GPa%. Continuous yielding, sustained work hardening.
  - **>900 °C (950–1200 °C)**: Grain coarsening (α₂ from ~26 to ~68 μm, γ from ~5.5 to ~36 μm), boundary κ persists → **monotonic decrease in both strength and ductility** (Hall–Petch effect). Elongation drops to 4.8% at 1200 °C. UTS decreases to ~610 MPa, YS to ~495 MPa at 1200 °C.
- **Fracture mode**: Mixed ductile (dimpled, γ-phase) + quasi-cleavage (river patterns, α-phase). At 800 °C, κ promotes cleavage; at 900 °C, ductile fracture area maximizes; at ≥1000 °C, ductile area decreases as grains coarsen. Secondary cracks parallel to rolling direction, associated with banded microstructure.

## Mechanistic Interpretation
1. **κ-carbide embrittlement below dissolution temperature**: Continuous κ along grain boundaries and lamellar κ from eutectoid decomposition provide easy crack paths, causing brittle fracture at 700 °C. Coarsening and loss of coherency at 800–850 °C partially mitigate embrittlement but still limit ductility.
2. **Optimal ductility at 900 °C**: Complete dissolution of κ in matrix removes brittle intergranular phase; fine dual-phase α+γ microstructure enables sustained work hardening and high elongation (36.6%). γ-phase (FCC) provides ductile fracture component (dimples).
3. **Strength–ductility trade-off above 900 °C**: Grain coarsening (α₂, γ) dominates property degradation. Hall–Petch strengthening diminishes with increasing grain size, reducing both YS and UTS. Ductility also declines, likely due to reduced grain boundary area for strain accommodation and persistent boundary κ.
4. **Boundary κ persistence**: Quenching from >900 °C precipitates boundary κ along α/α interfaces; although matrix is κ-free at annealing temperature, these quench-induced precipitates may influence fracture behavior at highest temperatures.

## Key Quantitative Findings
- **κ-carbide dissolution temperature (experimental)**: 850–900 °C (vs. Thermo-Calc equilibrium 823 °C).
- **Optimal annealing condition**: **900 °C for 1 h** → α ~40%, γ ~60%, κ dissolved → UTS 855 MPa, YS 651 MPa, total elongation 36.6%, **strength–ductility product ~31 GPa%**.
- **Worst ductility**: 700 °C (elongation 4.8%, UTS ~971 MPa); 1200 °C (elongation 4.8%, UTS ~610 MPa, YS ~495 MPa).
- **Phase fraction range (900–1200 °C)**: α 37–43%, γ 57–63%.
- **Grain size range (900–1200 °C)**: α₂: 26→68 μm; γ: 5.5→36 μm; α₁: 3.2→22 μm.
- **Lattice parameters**: α 2.89–2.91 Å, γ 3.65–3.67 Å, κ 3.76–3.79 Å.
- **Orientation relationship (700 °C, lamellar κ)**: N–W: (110)α∥(1-11)κ, [001]α∥[011]κ.

## Visual Evidence
- **Figure 1 (flow chart)**: Temperature–time profile of hot rolling + annealing schedule, establishing the thermal history linking processing to microstructure.
- **Figure 2 (Thermo-Calc diagram)**: Equilibrium phase fractions vs. temperature, predicting κ dissolution at 823 °C and providing theoretical baseline.
- **Figure 3 (OM+SEM, HR state)**: Banded α+γ microstructure with κ at phase/grain boundaries; establishes as-rolled reference.
- **Figure 4 (XRD)**: Phase identification across temperatures; γ peaks absent at 700 °C, κ peaks disappear by 900 °C; lattice parameter values.
- **Figure 5 (OM, 800/850/900 °C)**: Microstructural evolution – banding reduction, κ dissolution, γ fraction increase; dissolution temperature 850–900 °C.
- **Figure 6 (SEM, 700–1200 °C)**: κ morphology from lamellar→globular→dissolved; grain coarsening; eutectoid product at 700 °C.
- **Figure 7 (TEM, 700 °C)**: Lamellar κ+α eutectoid, N–W orientation relationship, globular κ without coherency.
- **Figure 8 (TEM, 800 °C)**: Three-phase coexistence; coarsened κ shows no orientation relationship.
- **Figure 9 (grain size plot)**: Grain size vs. temperature for α₁, α₂, γ; differential growth rates explained by solidification history.
- **Figure 10 (SEM, 900–1200 °C)**: Boundary κ persists; intragranular FCC at 1200 °C.
- **Figure 11 (TEM, 1100 °C)**: Boundary κ confirmed at α/α boundary.
- **Figure 12 (TEM, 1200 °C)**: Boundary κ with N–W relationship; DF shows misorientation between adjacent κ particles.
- **Figure 13 (EDS, 800 vs. 900 °C)**: Elemental partitioning (Mn, Al) at 800 °C with κ present; uniform distribution at 900 °C.
- **Figure 14 (phase fraction plot)**: Quantitative α, γ, κ fraction vs. temperature from XRD; κ zero at 900 °C; α+γ stable range.
- **Figure 15 (tensile curves)**: Engineering stress–strain; brittle at 700 °C, optimal ductility at 900 °C; true stress–strain + work hardening rate show sustained hardening at ≥900 °C.
- **Figure 16 (property summary plot)**: UTS, YS, elongation, strength–ductility product vs. temperature; peak at 900 °C.
- **Figure 17 (fractography, 800/900/1000 °C)**: Mixed ductile+quasi-cleavage; secondary cracks parallel to RD; maximum ductile area at 900 °C.
