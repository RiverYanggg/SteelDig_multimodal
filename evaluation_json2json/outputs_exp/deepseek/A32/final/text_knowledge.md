# Material System
- **Base alloy**: Fe-15.05Ni-11.06Cr-1.09Mn-0.028C-0.002Si-0.05Al (wt.%)
- **2.5 Si alloy**: Fe-14.99Ni-10.98Cr-1.10Mn-0.028C-2.50Si-0.06Al
- **2.5 Al alloy**: Fe-15.04Ni-11.02Cr-1.08Mn-0.030C-0.034Si-2.47Al
All three are fully austenitic at room temperature after solution treatment, selected to isolate the effects of Si and Al alloying on lattice parameter and stacking fault energy (SFE) in an Fe-Ni-Cr-based austenitic steel matrix.

# Processing Route and Variables
- **Homogenization**: 20 h at 1200 °C, followed by hot rolling.
- **Solution annealing**:  
  - Base: 1040 °C  
  - 2.5 Si: 1075 °C  
  - 2.5 Al: 1060 °C  
  (Temperatures chosen to achieve comparable austenite grain sizes.)
- **Grain size**: ~140 μm after solution annealing (coarse‑grained condition).
- **Pre‑deformation**: 5% compression true strain introduced to generate dislocations for SFE measurements.
- **XRD specimen preparation**: ground to 600 grit, then chemically polished to remove deformed surface layers; Ni filter used for Cu-Kα radiation; lattice parameter obtained by extrapolation method using multiple austenite reflections.
- **TEM specimen preparation**: thin foils prepared by electropolishing in 95% acetic acid + 5% perchloric acid at room temperature; weak‑beam dark‑field (WBDF) imaging performed under g//b two‑beam conditions to measure partial dislocation separation distances.

# Microstructure and Phase Evolution
- All alloys remain fully austenitic after solution treatment; no secondary phases are reported.
- WBDF imaging (Figure 1) confirms that the dislocations introduced by 5% compression are dissociated into Shockley partials, characteristic of low-SFE austenite. The separation distance *d* and the dislocation character angle *α* were measured for multiple dislocations in each alloy to calculate SFE using anisotropic elasticity theory.

# Processing-Structure-Property Chain
- **Alloying → Lattice parameter (Figure 2)**:  
  - **2.5 wt.% Al** addition expands the austenite lattice parameter from ~0.3585 nm (Base) to ~0.3598 nm (a significant increase of ~0.0013 nm).  
  - **2.5 wt.% Si** addition has a negligible effect, raising the lattice parameter to only ~0.3587 nm (~0.0002 nm change).  
  - *Consequence*: Because the lattice parameter of austenite is commonly used to estimate dissolved carbon content, the substantial lattice expansion caused by Al may lead to **overestimation of carbon** if the Al effect is not accounted for.

- **Alloying → SFE (Figure 3)**:  
  - WBDF analysis yields the following SFE values (uncertainties as ±1 standard deviation):  
    - **Base**: 26.3 ± 3.0 mJ m⁻²  
    - **2.5 Si**: 19.9 ± 2.0 mJ m⁻² (a decrease of ~6.4 mJ m⁻² relative to the base)  
    - **2.5 Al**: 38.3 ± 6.1 mJ m⁻² (an increase of ~12.0 mJ m⁻² relative to the base)  
  - *Implications*: Lower SFE in the Si‑modified alloy promotes extended stacking faults and can favor deformation‑induced martensitic transformation (enhancing TRIP effect), while the higher SFE in the Al‑modified alloy stabilizes austenite against such transformations, shifting deformation mechanisms toward dislocation glide or twinning at appropriate SFE levels.

# Mechanistic Interpretation
- The differential influence of Si and Al on lattice parameter is consistent with their atomic sizes: Al having a larger metallic radius than Fe, Ni, and Cr expands the fcc lattice, whereas the size of Si is closer to that of the host atoms, leading to minimal lattice change.
- The SFE trends can be rationalized in terms of electronic and volume effects: Al is known to raise the SFE of austenitic steels by altering the electronic density of states and by increasing the lattice parameter, both of which reduce the Gibbs free energy difference between fcc and hcp. Si, despite also being a substitutional element, lowers SFE—likely due to its role in modifying the magnetic state and the local bonding character. These mechanistic connections are inferred from the observed data and are consistent with literature reports on thermodynamic SFE modeling; the present paper confirms the direction and magnitude of the effects for these specific compositions.

# Key Quantitative Findings
| Alloy | Lattice parameter (nm) | SFE (mJ m⁻²) | ΔSFE relative to Base |
|-------|------------------------|--------------|------------------------|
| Base  | ~0.3585               | 26.3 ± 3.0   | –                      |
| 2.5 Si| ~0.3587               | 19.9 ± 2.0   | −6.4  (decrease)       |
| 2.5 Al| ~0.3598               | 38.3 ± 6.1   | +12.0 (increase)       |

- All three alloys have a grain size of ~140 µm after solution treatment and before 5% compression.
- The XRD lattice parameter determination (extrapolation method) shows that **2.5 wt.% Al increases the lattice parameter by about 0.36%**, whereas 2.5 wt.% Si increases it by only ~0.06% compared to the Base.
- The SFE values demonstrate that Si acts as an **SFE‑reducing** element, whereas Al acts as an **SFE‑enhancing** element in this Fe‑15Ni‑11Cr austenitic matrix.

# Visual Evidence
- **Figure 1** – WBDF TEM micrograph of a dissociated dislocation in the Base alloy, with annotations for *d*, *α*, and the *g*//*b* condition. This image validates the methodology by which multiple (d, α) data pairs were collected and fed into anisotropic elasticity equations to compute SFE. It establishes the experimental baseline for comparing partial dislocation separations between the Base, 2.5 Si, and 2.5 Al conditions.
- **Figure 2** – Scatter plot of austenite lattice parameter vs. relative alloying content. The data directly demonstrate that 2.5 wt.% Al produces a marked increase in lattice parameter (to ~0.3598 nm) while 2.5 wt.% Si has a negligible effect (~0.3587 nm), documenting the element‑specific lattice expansion.
- **Figure 3** – Two‑part chart:  
  (a) Partial dislocation separation distance vs. dislocation character angle for the three alloys. The symbols are experimental points; solid curves represent theoretical trends for the average SFE, and dashed curves indicate ±1 standard deviation bounds. The clear separation of the curves confirms that SFE is systematically lowest for 2.5 Si and highest for 2.5 Al.  
  (b) SFE vs. alloying content, showing the ~6.4 mJ m⁻² decrease with 2.5 wt.% Si and the ~12.0 mJ m⁻² increase with 2.5 wt.% Al. This panel summarizes the quantitative SFE modulation caused by the two alloying elements.
