# Phase Transformation and Austenite Stability During Thermomechanical Processing of High (~5%) Al Added Low-Density Medium Mn Steel

## Material System
- **Nominal composition**: Fe-8Mn-5Al-0.2C (wt.%)
- **Actual composition**: Fe-7.79Mn-4.88Al-0.84Si-0.2C (wt.%)
- **Alloy class**: High-Al low-density medium Mn steel designed for TRIP-assisted deformation
- **Phase constituents identified**: δ-ferrite (BCC), austenite/retained austenite (FCC), martensite (α', BCT/BCC), reverted austenite (γ_rev), intercritical ferrite (α, formed during annealing)
- **Notable**: κ-carbide precipitation was mentioned as a possibility but not observed in any condition, including the optimally annealed IA750_60Min sample (confirmed by TEM/EDS, figure_010)

## Processing Route and Variables
- **Melting and casting**: Open-air induction furnace
- **Homogenization**: 1100 °C for 2 h
- **Primary hot working (forging)**: Hot forging at 1050–800 °C, 50% thickness reduction, air cooling. This step breaks down the as-cast dendritic structure but retains elongated austenite in δ-ferrite matrix.
- **Secondary hot working (rolling)**: Soaking at 1100 °C for 2 h, then hot rolling at 1050–800 °C in two passes with 50% reduction per pass and 5 min reheating between passes, terminated by water quenching → **HRQ condition** (hot rolled and water quenched)
- **Intercritical annealing**: All HRQ material subjected to 750 °C for varying times: 5, 30, 60, 120, 180 min, followed by air cooling. Sample aliases: **IA750_5Min, IA750_30Min, IA750_60Min, IA750_120Min, IA750_180Min**
- **Key processing contrast**: Air cooling (forging, annealing) vs. water quenching (rolling). The HRQ condition generates martensite within prior austenite regions, while intercritical annealing triggers martensite reversion and elemental partitioning.

## Microstructure and Phase Evolution
- **Cast + Hot-forged condition (figure_003)**:
  - XRD confirms dual-phase: α-ferrite (δ/α, BCC) + γ-austenite (FCC) in both cast and hot-forged states.
  - Rietveld refinement: ~26% austenite in cast, ~29% austenite in hot-forged.
  - Cast structure: dendritic austenite (blue arrows in optical micrographs) within ferrite matrix.
  - Hot-forged structure: residual elongated austenite grains in δ-ferrite matrix, partially dissolved compared to as-cast dendritic morphology.
  
- **HRQ condition (hot rolled + water quenched, figure_004)**:
  - Optical micrograph: grains elongated along RD, showing δ-ferrite and α/γ regions.
  - SEM: δ-ferrite matrix + lenticular martensite within prior austenite regions (α/γ). The martensite forms due to water quenching from the hot rolling finish temperature (~800 °C).
  - EBSD: ~19% retained/untransformed austenite (FCC, green) + BCC matrix (red, δ-ferrite + martensite). The 19% represents austenite that did not transform to martensite upon quenching.
  - EDS elemental partitioning (figure_004c): Mn is enriched in austenite/martensite regions (8.36±0.16 wt%) compared to δ-ferrite (7.02±0.25 wt%), while Al is higher in δ-ferrite (5.61±0.11 wt%) vs. austenite/martensite (4.75±0.11 wt%).

- **Annealed conditions (IA750, 5–180 min, figure_005)**:
  - **IA750_5Min**: Sharp, needle-shaped reverted austenite forms within prior martensite, measuring ~2.83±0.30 µm in length.
  - **IA750_60Min**: Morphological transition from needle-like → globular reverted austenite with increased aspect ratio. Reverted austenite partially dissolves into intercritical ferrite.
  - **IA750_180Min**: Near-complete dissolution of reverted austenite, leaving predominantly intercritical ferrite + untransformed austenite.
  - **Chemical partitioning across all annealing times (EDS, figure_005 A3–E3)**:
    - **δ-ferrite**: High Al (~5.2–5.9 wt%), moderate Mn (~6.6–7.4 wt%)
    - **Reverted austenite (γ_rev)**: Mn content ~7.6–8.3 wt%
    - **Untransformed austenite (γ_original)**: Mn-rich, 9.1–9.8 wt% Mn — confirms Mn partitioning from dissolving martensite/reverted austenite into untransformed austenite during annealing.
  - **Austenite volume fraction from XRD (pre-deformation, figure_008c)**: Decreases from ~46% (5 min) → ~30% (180 min). The highest volume fraction of austenite is present at the shortest annealing time, but this austenite has lower mechanical stability.

## Processing-Structure-Property Chain
- **Thermo-Calc equilibrium calculation (figure_002b, TCFE9 database)**: Predicted dual-phase BCC_A2 (δ-ferrite) + FCC_A1 (austenite) region spans ~650–1350 °C. This justifies 750 °C as an appropriate intercritical annealing temperature to avoid kappa-carbide and stay within the dual-phase window.
- **Dilatometry of hot-forged material (figure_002c)**: Heating to 750 °C with 5 and 15 min holding shows only a slight deviation at ~600 °C (attributed to carbide dissolution), with no significant length contraction. This indicates minimal ferrite-to-austenite transformation upon heating, confirming the high thermal stability of δ-ferrite in this high-Al composition.

- **Nanoindentation hardness evolution (figure_006)**:
  - **δ-ferrite**: Hardness remains nearly constant across conditions: 4439±206 MPa (HRQ) → 4267±264 MPa (IA750_5Min) → 4150±200 MPa (IA750_60Min). δ-ferrite is mechanically stable and largely unaffected by annealing.
  - **Martensite → Reverted austenite**: Hardness drops dramatically from 8897±550 MPa (HRQ martensite, penetration depth ~384 nm at 30 mN) → 3867±110 MPa (IA750_5Min, needle-shaped γ_rev) → 3478±334 MPa (IA750_60Min, globular γ_rev). This confirms progressive dissolution of hard martensite into softer reverted austenite with annealing.
  - **Untransformed austenite**: Stable hardness ~4080–4196 MPa across all tested conditions (HRQ, IA750_5Min, IA750_60Min).

- **Tensile properties (figure_007, figure_008d)**:
  - **HRQ**: Highest YS, lowest ductility (brittle behavior due to martensite).
  - **IA750_5Min**: Some ductility improvement but still limited.
  - **IA750_60Min**: **Optimal combination** — UTS = 658±6 MPa, total elongation (TE) = 12±1%, highest Product of Strength and Elongation (PSE).
  - **IA750_180Min**: Lower UTS than 60 min, reduced ductility vs. 60 min, corresponding to near-complete dissolution of reverted austenite.
  - **Yield strength (YS) range (figure_008d)**: 427–465 MPa across all annealed conditions.
  - **Trend**: Total elongation peaks at 60 min and decreases for longer annealing times. The improvement in ductility over HRQ is attributed to the formation of reverted austenite and its TRIP effect during deformation.

- **Work hardening behavior (figure_007, B1–B4)**:
  - All annealed conditions exhibit two-stage work hardening: **Stage S1** — sharp decrease attributed to δ-ferrite deformation; **Stage S2** — gradual linear decrease attributed to competing softening (dislocation recovery) and hardening (TRIP effect from austenite → martensite transformation).
  - **Mean WHR in Stage S2**: Evolves with annealing time — 1100–400 MPa (5 min) → 2000–1000 MPa (60 min) → 1500–900 MPa (180 min). The highest WHR at 60 min indicates the most sustained TRIP effect, providing enhanced work hardening capacity and delaying necking.

- **Austenite stability and TRIP effect (figure_008c)**:
  - **Initial austenite fraction (pre-deformation)**: 46% (5 min), 40% (30 min), 35% (60 min), 32% (120 min), 30% (180 min) — decreasing trend.
  - **Austenite fraction after tensile deformation**: Drops in all conditions due to deformation-induced martensitic transformation (TRIP).
  - **Transformation ratio (ΔVγ)**: Peaks at ~20% for IA750_60Min, meaning the largest absolute amount of austenite transforms to martensite during straining in this condition.
  - **Mechanical stability parameter K**: Exhibits inverse correlation with transformation ratio. IA750_60Min achieves an intermediate K value — neither too stable (5 min condition, insufficient TRIP) nor too unstable (180 min, austenite transforms too early and is exhausted). This intermediate stability provides sustained TRIP over a broad strain range, maximizing work hardening and ductility.

## Mechanistic Interpretation
- **Schematic model (figure_009)**:
  - **HRQ (initial state)**: Lenticular martensite (α') surrounded by untransformed austenite (γ_original), all within δ-ferrite matrix.
  - **5 min at 750 °C**: Martensite begins to dissolve; sharp needle-shaped reverted austenite (γ_rev) + intercritical ferrite (α) nucleate at martensite/austenite interfaces.
  - **30–60 min**: Needles coarsen and spheroidize into globular γ_rev; Mn partitions from dissolving γ_rev into adjacent untransformed γ_original, enriching it and increasing its stability.
  - **60 min (optimum)**: Globular reverted austenite achieves a size, morphology, and composition that provides **optimal mechanical stability**. Upon tensile loading, it transforms progressively to martensite (TRIP), providing sustained work hardening.
  - **120–180 min**: Continued elemental partitioning and coarsening lead to dissolution of γ_rev. Untransformed austenite becomes excessively enriched in Mn, but the total austenite fraction drops too low, reducing overall TRIP capacity.

- **60-minute condition rationale**: The 60 min annealing balances several competing factors:
  1. Sufficiently high austenite volume fraction (~35% initial) to contribute meaningful TRIP.
  2. Intermediate mechanical stability — austenite transforms progressively over a wide strain range rather than instantly (too unstable) or negligibly (too stable).
  3. Globular morphology with appropriate Mn content (from partitioning) that yields optimal stability.
  4. Work hardening in Stage S2 is maximized (2000–1000 MPa WHR), delaying necking and enhancing uniform elongation.
  This combination produces the peak PSE (UTS × TE) among all conditions.

- **No precipitation strengthening**: TEM/EDS of IA750_60Min (figure_010) reveals no evidence of κ-carbides or elemental clustering. The enhanced mechanical properties derive entirely from the optimized TRIP effect, not from precipitation hardening.

## Key Quantitative Findings
| Property | HRQ | IA750_5Min | IA750_60Min (Optimum) | IA750_180Min |
|----------|-----|------------|-----------------------|--------------|
| **UTS (MPa)** | Not reported in table (highest strength, lowest ductility) | Lower than 60 min | **658±6** | Lower than 60 min |
| **TE (%)** | Minimal | Improved | **12±1** | Reduced vs. 60 min |
| **YS range (MPa)** | – | 427–465 across all annealed conditions |
| **PSE** | Lowest | Moderate | **Highest** | Reduced |
| **Austenite fraction pre-test (%)** | ~19 (retained) | 46 | 35 | 30 |
| **Austenite fraction post-test (%)** | – | ~30 | ~15 | ~15 |
| **Transformation ratio ΔVγ (%)** | – | ~16 | **~20 (peak)** | ~15 |
| **δ-ferrite nanoindentation hardness (MPa)** | 4439±206 | 4267±264 | 4150±200 | – |
| **Martensite/γ_rev nanoindentation hardness (MPa)** | 8897±550 (α') | 3867±110 (γ_rev needle) | 3478±334 (γ_rev globular) | – |
| **Untransformed γ nanoindentation hardness (MPa)** | ~4080 | ~4196 | ~4130 | – |
| **Mn in δ-ferrite (wt%, EDS)** | 7.02±0.25 | 6.6–7.4 range | within range | within range |
| **Mn in γ_rev (wt%, EDS)** | – | 7.6–8.3 range | within range | – |
| **Mn in untransformed γ (wt%, EDS)** | 8.36±0.16 (α'+γ) | 9.1–9.8 range | within range | within range |
| **Al in δ-ferrite (wt%, EDS)** | 5.61±0.11 | 5.2–5.9 range | within range | within range |

## Visual Evidence

- **figure_002**: Thermomechanical processing route schematic, Thermo-Calc phase diagram establishing the BCC+FCC dual-phase window (650–1350 °C), and dilatometry curves confirming minimal ferrite-to-austenite transformation during heating to 750 °C. These collectively support the selection of 750 °C as the intercritical annealing temperature and the thermal stability of δ-ferrite.

- **figure_003**: XRD and optical/SEM/EBSD characterization of cast and hot-forged conditions. Confirms dual-phase BCC+FCC in both states, dendritic-to-elongated austenite morphology evolution, and small increase in austenite fraction from cast (~26%) to forged (~29%).

- **figure_004**: HRQ condition characterization — optical and SEM micrographs showing δ-ferrite + lenticular martensite in prior austenite regions; EDS confirms Mn partitioning to γ/α' regions and Al partitioning to δ-ferrite; EBSD phase map supports ~19% retained untransformed austenite. Provides the baseline microstructure prior to intercritical annealing.

- **figure_005**: SEM + EDS evolution across all five annealing times (5–180 min). Critically documents the morphological transition of reverted austenite from sharp needles (2.83±0.30 µm at 5 min) → globular (60 min) → near-complete dissolution (180 min). EDS tables provide quantitative elemental partitioning data for δ-ferrite, reverted austenite, and untransformed austenite in each condition, directly linking annealing time to chemical evolution.

- **figure_006**: Nanoindentation load-displacement curves comparing HRQ, IA750_5Min, and IA750_60Min. Provides quantitative hardness values proving dramatic softening from martensite (8897 MPa) to reverted austenite (3867→3478 MPa) while δ-ferrite and untransformed austenite remain mechanically stable. Directly supports the martensite reversion mechanism.

- **figure_007**: Engineering and true stress-strain curves for all conditions, plus work hardening rate curves. Shows IA750_60Min achieves highest UTS (~658 MPa) and TE (~12%), and the two-stage WHR behavior with Stage S2 mean WHR peaking at 2000–1000 MPa for the 60 min condition. Provides the primary evidence linking annealing time → TRIP effect → mechanical properties.

- **figure_008**: XRD before and after deformation, quantification of austenite fraction evolution, transformation ratio, mechanical stability K, and summary tensile property plots. Provides the critical quantitative link between austenite stability metrics (K, ΔVγ) and tensile properties (UTS, TE, PSE), establishing 60 min as the optimum due to intermediate austenite stability maximizing TRIP.

- **figure_009**: Six-panel schematic of microstructural evolution during annealing. Visually explains the martensite → reverted austenite → dissolution pathway and the morphological/compositional changes underlying the mechanical stability optimization at 60 min.

- **figure_010**: HRTEM and EDS mapping of IA750_60Min. Confirms Mn enrichment and Al depletion in reverted austenite regions, and critically — the absence of κ-carbides or any precipitates — ruling out precipitation strengthening and reinforcing that the enhanced PSE derives solely from optimized TRIP behavior.
