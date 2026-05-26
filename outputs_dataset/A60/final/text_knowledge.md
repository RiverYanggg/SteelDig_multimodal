# Material System
The material under investigation is a Fe-Mn-Al-C low-density steel (LDS) with a nominal composition of Fe-30.34Mn-8.93Al-0.9C (wt.%). The material system is studied in multiple microstructural states, defined by solution treatment temperature: S950 (fine-grained), S1050 (medium-grained), and S1150 (coarse-grained). An as-hot-rolled, non-solution-treated state, S0, serves as a baseline. The matrix is a single-phase face-centered cubic (FCC) austenite. The nanoscale κ-carbides present in the S0 state dissolve during solution treatment. The primary protective feature is a surface Al-rich oxide film formed in a 3.5 wt% NaCl solution.

# Processing Route and Variables
The primary processing route involves hot rolling followed by a solution treatment at varying temperatures and subsequent water quenching.
- **Sample S0 (Baseline)**: As-hot-rolled and water-quenched. This results in a heterogeneous, deformed grain structure with high dislocation density and the presence of nanoscale κ-carbides (5-10 nm).
- **Sample S950 (Fine-grained)**: Solution treated at 950 °C for 2 h, followed by water quenching. This process produces a fully recrystallized, equiaxed austenite grain structure.
- **Sample S1050 (Medium-grained)**: Solution treated at 1050 °C for 2 h, followed by water quenching.
- **Sample S1150 (Coarse-grained)**: Solution treated at 1150 °C for 2 h, followed by water quenching. This produces coarse, equiaxed austenite grains.
- **Corrosion Test Medium**: All electrochemical and immersion corrosion tests were conducted in a 3.5 wt% NaCl solution.

# Microstructure and Phase Evolution
The processing variables directly dictate the microstructural features, primarily grain size and grain boundary character, while the phase constitution remains austenitic.
- **Phase Constitution**: X-ray diffraction confirms all samples (S0, S950, S1050, S1150) maintain a single-phase FCC austenitic structure. The (111) and (220) peak intensities vary, indicating textural changes with solution temperature. S0 contains nanoscale κ-carbides, which are dissolved in S950, S1050, and S1150.
- **Grain Structure and Size**: 
    - S0 exhibits a heterogeneous, deformed grain structure with an average grain size of 7.6 μm and high kernel average misorientation (KAM) of 1.62.
    - S950 shows uniform, equiaxed grains with an average size of 8.7 μm and a KAM value of ~0.4.
    - S1050 exhibits a larger average grain size of 21.1 μm.
    - S1150 displays coarse grains averaging 32.0 μm, with a size distribution tail extending up to 140 μm.
- **Grain Boundary Characteristics**:
    - High-angle grain boundary (HAGB) density is highest in S950 at 0.114 μm/μm², decreasing through S1050 (0.029 μm/μm²) to S1150 (0.019 μm/μm²).
    - Annealing twin boundary (ATB, Σ3) density follows the same trend, from 0.146 μm/μm² in S950 down to 0.040 μm/μm² in S1150.

# Processing-Structure-Property Chain
The chain links a lower solution treatment temperature to a finer grain size, higher grain boundary density, a superior Al-rich oxide film, and ultimately, enhanced corrosion resistance.
- **Grain Boundary Density and Oxide Film Quality**: The high HAGB density in S950 (0.114 μm/μm²) promotes the rapid formation of a protective oxide film that is thick (25.2 nm), highly Al-rich (90.17 at.% Al), and defect-poor (donor density, N_D = 0.26×10²¹/cm³). In contrast, the low HAGB density in S1150 (0.019 μm/μm²) leads to a thinner (18.0 nm), less Al-rich (69.91 at.% Al), and more defective film (N_D = 0.49×10²¹/cm³).
- **Oxide Film Quality and Corrosion Resistance**: The superior oxide film on S950 directly results in the best corrosion performance. Its corrosion rate from a 30-day immersion test is 0.160 mm/y, the lowest among all tested samples. The inferior film on S1150 correlates with a significantly higher corrosion rate of 0.281 mm/y. The as-rolled S0 sample, lacking this protective film, has the highest corrosion rate at 0.326 mm/y.
- **Pitting Resistance**: Post-polarization SEM analysis confirms this trend. S950 exhibits the least pitting corrosion, while S0 and S1150 show extensive and severe pitting, respectively.

# Mechanistic Interpretation
The mechanism is governed by the density of high-angle grain boundaries (HAGBs), which serve as preferential sites for Al dissolution.
- **Thermodynamic Basis**: Pourbaix diagrams for the Fe-Mn-Al-H₂O system confirm that under the experimental conditions, Al is thermodynamically driven to form a stable, dense Al₂O₃ passive film.
- **Kinetic Pathway via Microstructure**: Scanning Kelvin probe force microscopy (SKPFM) and initial dissolution observation reveal that HAGBs are cathodic sites with lower potential relative to the matrix, leading to preferential anodic dissolution of Al at these boundaries. The high HAGB density in the fine-grained S950 provides abundant active sites for this dissolution, enabling rapid, uniform coverage by a dense Al-rich oxide film. This film subsequently suppresses further oxidation of Fe and Mn, as evidenced by cyclic voltammetry where S950 shows a strong Al oxidation peak in the first cycle and a weak Fe/Mn peak in the second.
- **Failure Mechanism in Coarse-Grained Steel**: In S1150, the sparse HAGB network leads to discontinuous, island-like oxide growth. This allows for the continued participation of Fe and Mn in the film formation, resulting in a mixed, more defective, and less protective oxide film with cracks and pits.

# Key Quantitative Findings
- **S950 Corrosion Rate**: 0.160 mm/y (30-day immersion in 3.5 wt% NaCl).
- **S1150 Corrosion Rate**: 0.281 mm/y, a 43% increase over S950.
- **S0 Corrosion Rate**: 0.326 mm/y.
- **S950 Oxide Film Thickness**: 25.2 ± 1.2 nm (AES).
- **S1150 Oxide Film Thickness**: 18.0 ± 0.9 nm.
- **S950 Oxide Film Al Content**: 90.17 at.% (XPS).
- **S1150 Oxide Film Al Content**: ~69.91 at.% (derived from visual_evidence, figure_001).
- **S950 Film Defect Density (N_D)**: 0.26 × 10²¹/cm³ (Mott-Schottky).
- **S1150 Film Defect Density (N_D)**: 0.49 × 10²¹/cm³.
- **S950 HAGB Density**: 0.114 μm/μm².
- **S1150 HAGB Density**: 0.019 μm/μm².
- **S950 Breakdown Current Density (i_bre)**: 2.72 μA/cm².
- **S1150 Breakdown Current Density (i_bre)**: 8.84 μA/cm².

# Visual Evidence
- **Figure_002 (XRD)**: Confirms a single-phase austenitic structure for all samples, with textured intensity variations. This validates that property changes are not due to phase transformations.
- **Figure_003 & Figure_004 (SEM, EBSD)**: Visually demonstrate the microstructural evolution from a deformed S0 state to recrystallized, equiaxed grains in S950, and further coarsening in S1150. EBSD IPF and GB maps show the drastic reduction in HAGB density from S950 to S1150.
- **Figure_005 (Chart)**: Quantifies the grain size distribution and the specific HAGB and ATB densities. The sharp drop in boundary density from S950 to S1150 is the key structural link in the processing-structure-property chain.
- **Figure_001 & Figure_010 (Property-Electrochemical, Chart)**: A multi-panel summary figure and a dedicated bar chart respectively confirm the central property finding: S950 achieves the lowest corrosion rate (0.160 mm/y) and S0 the highest (0.326 mm/y). Figure_001 also maps this to the oxide film's Al content and thickness.
- **Figure_007 & Figure_011 (Property-Electrochemical)**: Potentiodynamic polarization and potentiostatic curves show S950 with the lowest breakdown current density (2.72 μA/cm²) and the lowest stable current density, indicating the best passivation behavior.
- **Figure_009 & Figure_012 (Property-Electrochemical, EIS)**: Nyquist plots confirm S950 has the largest capacitive arc and highest polarization resistance, quantitatively supported by Figure_019 showing Rp values for S950 stabilizing at ~114.9 kΩ·cm², far exceeding S0 and S1150.
- **Figure_013 (Mott-Schottky)**: The positive and negative slopes of the C⁻² vs. potential plot quantify the donor (N_D) and acceptor densities. S950's lowest values (N_D = 0.26×10²¹/cm³) provide direct evidence for its defect-poor passive film.
- **Figure_014 & Figure_015 (XPS)**: The XPS spectra deconvolution and the subsequent cation fraction chart provide direct chemical proof that the S950 film is nearly pure Al³⁺ (90.17 at.%), with minimal Fe and Mn, while coarser-grained samples contain a mixed, less protective oxide.
- **Figure_016 (AES Depth Profiles)**: These profiles visually validate the XPS findings, showing a thick (25.2 nm), Al-rich layer on S950 that is compositionally uniform with depth, contrasting with the thinner films and falling Al content in S1050 and S1150.
- **Figure_018 (SEM/SKPFM)**: Illustrates the mechanistic link by showing preferential dissolution at HAGBs in fine-grained S950 and the lower electrochemical potential of HAGBs, confirming them as the active sites for Al oxidation.
- **Figure_020 (Cyclic Voltammetry)**: Supports the preferential Al-dissolution mechanism. S950 shows a strong Al oxidation peak and a suppressed Fe/Mn peak in the second cycle, whereas S1150 shows the opposite trend.
- **Figure_021 (Schematic)**: Summarizes the complete proposed mechanism, contrasting rapid, uniform Al-rich oxide formation at a high-density HAGB network (fine grain) with discontinuous, defective, and Fe/Mn-rich film growth on a sparse HAGB network (coarse grain).
