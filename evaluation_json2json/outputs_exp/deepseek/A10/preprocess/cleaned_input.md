# Extreme high accuracy prediction and design of Fe-C-Cr-Mn-Si steel using machine learning

![](images/36b14554370d46ae1d8472f8658758c138a81af87398e96c22576eef330e455d.jpg)

Hao Wu , Jianyuan Zhang , Jintao Zhang , Chengjie Ge , Lu Ren , Xinkun Suo

Multidimensional Additive Manufacturing Institute, Faculty of Mechanical Engineering and Mechanics, Ningbo University, 315211 Ningbo, PR China

# A R T I C L E I N F O

Keywords:

Fe-C-Cr-Mn-Si steel

Machine learning

Conditional generative adversarial networks

Solid solution strengthening

Firefly optimization algorithm

# A B S T R A C T

Solid solution strengthening theory is essential for designing steel with high microhardness. Experimental determination is quite time consuming and costly. It is necessary to develop an alternate approach to rapidly and accurately predict new solid solution strengthening theory for steel. In this study, a data-driven model combining machine learning (ML), firefly optimization algorithm (FA) and conditional generative adversarial networks (CGANs) were proposed to predict solid solution strengthening theory of Fe-C-Cr-Mn-Si steel. Three alloys were fabricated using cladding to validate the predict accuracy of the models. The results show that the trained support vector regression (SVR) model demonstrated the highest prediction precision for microhardness. The coefficient of determination $( R ^ { 2 } )$ value increased from 0.85 to 0.89 and root mean square error (RMSE) decreased from 0.39 to 0.31 after introducing the modified solid solution strengthening theory. The experimental validation revealed a minimum error of 1.17% between the predicted value and the experimental value. The investigation provides a valuable method to expedite design of Fe-C-Cr-Mn-Si steel with extreme high accuracy.

# 1. Introduction

Fe-C-Cr-Mn-Si alloy steel is susceptible to wear and cracking due to low surface hardness. Various efforts have been made to improve the surface hardness and service life of the steel [1]. Machine learning (ML) is an effective method to develop new theory and new materials with low time and cost [2–5]. Huang et al. developed a ML model for the prediction of time–temperature-transformation diagrams of high-alloy steel [6] and stainless steel [7].Geng et al. [8] proposed a ML approach to predict the continuous cooling transformation diagrams in synthetic weld heat-affected zones for Ni-Cr-Mo steel. Wei et al. [9] constructed a ML model for predicting the creep life of the austenitic steel. The gaussian regression model exhibited high predictive accuracy, with a determination coefficient $( R ^ { 2 } )$ of 0.97. Wang et al. [10] employed ML and stochastic optimization to accelerate the design of the Fe-based soft magnetic materials. The $R ^ { 2 }$ value with random forest (RF) model was 0.86 and 0.82 for predicting magnetic saturation and magnetostriction, respectively. Ruiz et al. [11] constructed a regression model based on the gradient boosting algorithm with the $R ^ { 2 ^ { \cdot } }$ value of 0.87, revealing the correlation between the tempering temperature and fatigue life. Yang et al. [12] predicted the hardness and yield strength of the oxide dispersion strengthened steel using six ML models. The results showed that the extreme gradient boosting model (XGBoost) had the lowest RMSE value of 63.78 and the highest $R ^ { 2 }$ value of 0.91 for hardness prediction. In terms of yield strength prediction, the XGBoost model had the lowest RMSE value of 54.06 and the highest $R ^ { 2 }$ value of 0.90.

Prediction accuracy of ML is affected by many factors, for example material science theory and quantity of data [13]. Solid solution strengthening is a basic mechanism in metallurgy, playing a crucial role in improving microhardness of alloys. Ren et al. [14] proposed a datadriven ML model combined with the modified solid solution strengthening theory $( \Delta \sigma _ { S S S } = Z \xi G ^ { * } M . E )$ for the hardness prediction of the high entropy alloys. The $R ^ { 2 }$ and RMSE value was 0.97 and 39.25 respectively. The prediction error of the model was 2.01 %. Gao et al. [15] constructed the generic model combining solid solution strengthening for hardness prediction of the high entropy alloys. The $R ^ { 2 }$ value reached 0.91 in an independent test set. However, the investigation on the solid solution strengthening theory for Fe-based alloy steel has not been found.

In this study, a ML-based prediction model combining firefly optimization algorithm (FA) was proposed to predict the microhardness of the Fe-C-Cr-Mn-Si steel. Conditional generative adversarial networks (CGANs) were employed to generate synthetic data to overcome the limitation of the data set. Modified solid solution strengthening theory √ Difference in cohesive energy $\delta _ { E c }$

![](images/43b273b0dc8df305846876fc148d948f6751b6d2ee4dfaa48c4a20dc5fce7f00.jpg)

<details>
<summary>text_image</summary>

Data set
Importance ranking
Cr
Ni
Mo
...
</details>

Data collection and pre-processing

![](images/359c00afaab19ea50f57848b3049e8127b984625c563020c45c0f34a2c611590.jpg)

<details>
<summary>bar</summary>

| Category | Value |
|---|---|
| Fusion and the Fusion of the Fusion | 0.15 |
| Fusion and the Fusion of the Fusion | 0.20 |
| Fusion and the Fusion of the Fusion | 0.25 |
| Fusion and the Fusion of the Fusion | 0.30 |
| Fusion and the Fusion of the Fusion | 0.35 |
| Fusion and the Fusion of the Fusion | 0.40 |
| Fusion and the Fusion of the Fusion | 0.45 |
| Fusion and the Fusion of the Fusion | 0.50 |
| Fusion and the Fusion of the Fusion | 0.55 |
| Fusion and the Fusion of the Fusion | 0.60 |
| Fusion and the Fusion of the Fusion | 0.65 |
| Fusion and the Fusion of the Fusion | 0.70 |
| Fusion and the Fusion of the Fusion | 0.75 |
| Fusion and the Fusion of the Fusion | 0.80 |
| Fusion and the Fusion of the Fusion | 0.85 |
| Fusion and the Fusion of the Fusion | 0.90 |
| Fusion and the Fusion of the Fusion | 0.95 |
| Fusion and the Fusion of the Fusion | 1.00 |
| Fusion and the Fusion of the Fusion | 1.05 |
| Fusion and the Fusion of the Fusion | 1.10 |
| Fusion and the Fusion of the Fusion | 1.15 |
| Fusion and the Fusion of the Fusion | 1.20 |
| Fusion and the Fusion of the Fusion | 1.25 |
| Fusion and the Fusion of the Fusion | 1.30 |
| Fusion and the Fusion of the Fusion | 1.35 |
| Fusion and the Fusion of the Fusion | 1.40 |
| Fusion and the Fusion of the Fusion | 1.45 |
| Fusion and the Fusion of the Fusion | 1.50 |
| Fusion and the Fusion of the Fusion | 1.55 |
| Fusion and the Fusion of the Fusion | 1.60 |
| Fusion and the Fusion of the Fusion | 1.65 |
| Fusion and the Fusion of the Fusion | 1.70 |
| Fusion and the Fusion of the Fusion | 1.75 |
| Fusion and the Fusion of the Fusion | 1.80 |
| Fusion and the Fusion of the Fusion | 1.85 |
| Fusion and the Fusion of the Fusion | 1.90 |
| Fusion and the Fusion of the Fusion | 1.95 |
| Fusion and the Fusion of the Fusion | 2.00 |
| Fusion and the Fusion of the Fusion | 2.05 |
| Fusion and the Fusion of the Fusion | 2.10 |
| Fusion and the Fusion of the Fusion | 2.15 |
| Fusion and the Fusion of the Fusion | 2.20 |
| Fusion and the Fusion of the Fusion | 2.25 |
| Fusion and the Fusion of the Fusion | 2.30 |
| Fusion and the Fusion of the Fusion | 2.35 |
| Fusion and the Fusion of the Fusion | 2.40 |
| Fusion and the Fusion of the Fusion | 2.45 |
| Fusion and the Fusion of the Fusion | 2.50 |
| Fusion and the Fusion of the Fusion | 2.55 |
| Fusion and the Fusion of the Fusion | 2.60 |
| Fusion and the Fusion of the Fusion | 2.65 |
| Fusion and the Fusion of the Fusion | 2.70 |
| Fusion and the Fusion of the Fusion | 2.75 |
| Fusion and the Fusion of the Fusion | 2.80 |
| Fusion and the Fusion of the Fusion | 2.85 |
| Fusion and the Fusion of the Fusion | 2.90 |
| Fusion and the Fusion of the Fusion | 2.95 |
| Fusion and the Fusion of the Fusion | 3.00 |
| Tissue (F) = -1, -2, -3, -4, -5, -6, -7, -8, -9, -10, -11, -12, -13, -14, -15, -16, -17, -18, -19, -20, -21, -22, -23, -24, -25, -26, -27, -28, -29, -30, -31, -32, -33, -34, -35, -36, -37, -38, -39, -40, -41, -42, -43, -44, -45, -46, -47, -48, -49, -50, -51, -52, -53, -54, -55, -56, -57, -58, -59, -60, -61, -62, -63, -64, -65, -66, -67, -68, -69, -70, -71, -72, -73, -74, -75, -76, -77, -78, -79, -80, -81, -82, -83, -84, -85, -86, -87, -88, -89, -90, -91, -92, -93, -94, -95, -96, -97, -98, -99, -100 |
| Tissue (F) = 1-3 | 0.15 |
| Tissue (F) = 4-6 | 0.20 |
| Tissue (F) = 7-9 | 0.25 |
| Tissue (F) = 12-16 | 0.30 |
| Tissue (F) = 17-24 | 0.35 |
| Tissue (F) = 21-32 | 0.40 |
| Tissue (F) = 26-40 | 0.45 |
| Tissue (F) = 31-48 | 0.50 |
| Tissue (F) = 36-56 | 0.55 |
| Tissue (F) = 41-64 | 0.60 |
| Tissue (F) = 46-72 | 0.65 |
| Tissue (F) = 51-80 | 0.70 |
| Tissue (F) = 56-88 | 0.75 |
| Tissue (F) = 61-96 | 0.80 |
| Tissue (F) = 66-104 | 0.85 |
| Tissue (F) = 71-112 | 0.90 |
| Tissue (F) = 76-120 | 0.95 |
| Tissue (F) = 81-128 | 1.00 |
| Tissue (F) = 86-136 | 1.05 |
| Tissue (F) = 91-144 | 1.10 |
| Tissue (F) = 96-152 | 1.15 |
| Tissue (F) = 101-160 | 1.20 |
| Tissue (F) = 106-168 | 1.25 |
| Tissue (F) = 111-176 | 1.30 |
| Tissue (F) = 116-184 | 1.35 |
| Tissue (F) = 121-192 | 1.40 |
| Tissue (F) = 126-200 | 1.45 |
| Tissue (F) = 131-208 | 1.50 |
| Tissue (F) = 136-216 | 1.55 |
| Tissue (F) = 141-224 | 1.60 |
| Tissue (F) = 146-232 | 1.65 |
| Tissue (F) = 151-240 | 1.70 |
| Tissue (F) = 156-248 | 1.75 |
| Tissue (F) = 161-256 | 1.80 |
| Tissue (F) = 166-264 | 1.85 |
| Tissue (F) = 171-272 | 1.90 |
| Tissue (F) = 176-280 | 1.95 |
| Tissue (F) = 181-288 | 2.00 |
| Tissue (F) = 186-296 | 2.05 |
| Tissue (F) = 191-304 | 2.10 |
| Tissue (F) = 196-312 | 2.15 |
| Tissue (F) = 201-320 | 2.20 |
| Tissue (F) = 206-328 | 2.25 |
| Tissue (F) = 211-336 | 2.30 |
| Tissue (F) = 216-344 | 2.35 |
| Tissue (F) = 221-352 | 2.40 |
| Tissue (F) = 226-360 | 2.45 |
| Tissue (F) = 231-368 | 2.50 |
| Tissue (F) = 236-376 | 2.55 |
| Tissue (F) = 241-384 | 2.60 |
| Tissue (F) = 246-392 | 2.65 |
| Tissue (F) = 251-400 | 2.70 |
| Tissue (F) = 256-408 | 2.75 |
| Tissue (F) = 261-416 | 2.80 |
| Tissue (F) = 266-424 | 2.85 |
| Tissue (F) = 271-432 | 2.90 |
| Tissue (F) = 276-440 | 2.95 |
| Tissue (F) = 281-448 | 3.00 |
| Tissue (F) = 286-456 | 3.05 |
| Tissue (F) = 291-464 | 3.10 |
| Tissue (F) = 296-472 | 3.15 |
| Tissue (F) = 301-480 | 3.20 |
| Tissue (F) = 306-488 | 3.25 |
| Tissue (F) = 311-496 | 3.30 |
| Tissue (F) = 316-494 | 3.35 |
| Tissue (F) = 321-504 | 3.40 |
| Tissue (F) = 326-512 | 3.45 |
| Tissue (F) = 331-520 | 3.50 |
| Tissue (F) = 336-528 | 3.55 |
| Tissue (F) = 341-536 | 3.60 |
| Tissue (F) = 346-544 | 3.65 |
| Tissue (F) = 351-552 | 3.70 |
| Tissue (F) = 356-560 | 3.75 |
| Tissue (F) = 361-568 | 3.80 |
| Tissue (F) = 366-576 | 3.85 |
| Tissue (F) = 371-584 | 3.90 |
| Tissue (F) = 376-592 | 3.95 |
| Tissue (F) = 381-600 | 4.00 |

Tissue (F) = N (%) vs N (%) for each category on X-axis; Y-axis represents percentage values; Legend indicates categories based on color coding; Color legend indicates corresponding color coding; Trend line indicates direction from left to right; Color line indicates direction from left to right; Trend line indicates direction from left to right; Trend line indicates direction from left to right; Color line indicates direction from left to right; Trend line indicates direction from left to right; Color line indicates direction from left to right; Trend line indicates direction from left to right; Color line indicates direction from left to right; Trend line indicates direction from left to right; Color line indicates direction from left to right; Trend line indicates direction from left to right; Color line indicates direction from left to right; Trend line indicates direction from left to right; Color line indicates direction from left to right; Trend lines indicate direction from left to right; Color lines indicate direction from left to right; Color lines indicate direction from left to right; Color lines indicate direction from left to right; Color lines indicate direction from left to right; Color lines indicate direction from left to right; Color lines indicate direction from left to right; Color lines indicate direction from left to right; Color lines indicate direction from left to right; Color lines indicate direction from left to right; Color lines indicate direction from left to right; Color lines indicate direction from left to right; Color line indicates direction from left to right; Color line indicates direction from left to right; Color line indicates direction from left to right; Color line indicates direction from left to right; Color line indicates direction from left to right; Color line indicates direction from left to right; Color line indicates direction from left to right; Color line indicates direction from left to right; Color line indicates direction from left to right; Color line indicates direction from left to right; Color line indicates direction from left to right; Color line indicates directional from left to right; Color line indicates direction from left to right; Color line indicates direction from left to right; Color line indicates direction from left to right; Color line indicates direction from left to right; Color line indicates direction from left to right; Color line indicates direction from left to right; Color line indicates direction from left to right; Color line indicates direction from left to right; Color line indicates direction from left to right; Color line indicates direction from left to right; Color line indicates direction to left to right; Color line indicates direction from left to right; Color line indicates direction from left to right; Color line indicates direction from left to right; Color line indicates direction from left to right; Color line indicates direction from left to right; Color line indicates direction from left to right; Color line indicates direction from left to right; Color line indicates direction from left to right; Color line indicates direction from left to right; Color line indicates direction from left to right; Color line indicates direction from right to left; Color line indicates direction from left to right; Color line indicates direction from left to right; Color line indicates direction from left to right; Color line indicates direction from left to right; Color line indicates direction from left to right; Color line indicates direction from left to right; Color line indicates direction from left to right; Color line indicates direction from left to right; Color line indicates direction from left to right; Color line indicates direction from left to right; Color line indicates direction from left to right: The trend is not explicitly labeled in this image but visually represents a single data point across all categories.
</details>

![](images/f70c66de5d3148bb2918a61a7e99a4acbc94d2b675aea8a5dbac2725c9109db7.jpg)

√ Local cohesive energy mismatch $D _ { E c }$

√ Shear modulus G

Feature engineering
![](images/cf8ee17a13a264ee7acb67cb9b57f74d4f8bfe1ffc1566a79e0114326456b62f.jpg)

<details>
<summary>scatter</summary>

| Experimental Δσ_sss (MPa) | Predicted Δσ_sss (MPa) |
| ------------------------- | ---------------------- |
| 1200                      | 1200                   |
| 1300                      | 1300                   |
| 1400                      | 1400                   |
| 1500                      | 1500                   |
| 1600                      | 1600                   |
| 1700                      | 1700                   |
| 1800                      | 1800                   |
</details>

$$
\Delta \sigma_ {s s s} = Z \cdot M \cdot G \cdot \delta_ {E c} \cdot D _ {E c}
$$

Model construction

![](images/9ca73ca66364493c62717647d15cb8b9002e4c6286981a796fbd28feb3148385.jpg)

<details>
<summary>bar</summary>

| Sample | Predicted values (HV) | Experimental values (HV) | Percentage (%) |
| :--- | :--- | :--- | :--- |
| Sample 1 | 521 | 515 | 1.17 |
| Sample 2 | 490 | 500 | 2.00 |
| Sample 3 | 415 | 424 | 2.09 |
</details>

$$
\text{The minimum error} 1.17 \%
$$

Inverse design

Fig. 1. Flow chart of microhardness prediction and design of Fe-C-Cr-Mn-Si steel.
Table 1 Parameters of CGANs.

<table><tr><td colspan="3">Generator network</td><td colspan="3">Discriminator network</td></tr><tr><td>Layer name</td><td>Architecture</td><td>Detail</td><td>Layer</td><td>Architecture</td><td>Detail</td></tr><tr><td>Input layer</td><td>Random noise</td><td>100</td><td>Input layer</td><td>Feature + property</td><td>12(11 + 1)</td></tr><tr><td rowspan="4">Hidden layer 1</td><td>Dense layer</td><td>64</td><td>Hidden layer 1</td><td>Dense layer</td><td>128</td></tr><tr><td>Activation</td><td>Relu</td><td></td><td>Activation</td><td>Relu</td></tr><tr><td>Batch normalization</td><td>Yes</td><td></td><td>Batch normalization</td><td>Yes</td></tr><tr><td>Regularizer</td><td>L2 = 0.01</td><td></td><td>Regularizer</td><td>L2 = 0.01</td></tr><tr><td rowspan="4">Hidden layer 2</td><td>Dense layer</td><td>128</td><td>Hidden layer 2</td><td>Dense layer</td><td>64</td></tr><tr><td>Activation</td><td>Relu</td><td></td><td>Activation</td><td>Relu</td></tr><tr><td>Batch normalization</td><td>Yes</td><td></td><td>Batch normalization</td><td>Yes</td></tr><tr><td>Regularizer</td><td>L2 = 0.01</td><td></td><td>Regularizer</td><td>L2 = 0.01</td></tr><tr><td rowspan="3">Output layer</td><td>Feature + property</td><td>12(11 + 1)</td><td>Output layer</td><td>Dense layer</td><td>1</td></tr><tr><td>Activation</td><td>Tanh</td><td></td><td>Activation</td><td>Sigmoid</td></tr><tr><td>Regularizer</td><td>L2 = 0.01</td><td></td><td>Regularizer</td><td>L2 = 0.01</td></tr></table>

was introduced to improve the physical interpretability and predictive accuracy of the model. The Fe-C-Cr-Mn-Si steel with the predicted composition was produced by cladding to validate the prediction accuracy of the ML model.

# 2. Materials and methodology

# 2.1. Construction of the ML model

The design strategy of the ML model is summarized in Fig. $^ { 1 , }$ consisting of data collection and pre-processing, feature engineering, model construction, and inverse design.

# 2.1.1. Data collection and pre-processing

173 Fe-C-Cr-Mn-Si steel data points were obtained from the widely recognized material information repository MatWeb [16]. In the dataset, 11 elements were collected, including C, Si, Mn, Cr, S, Ni, P, Fe, Mo, V and $\mathsf { W } ,$ as well as microhardness of steel.

The Z-score method was applied to screen each feature in the dataset, and the data points with |z| > 1.50 were defined as the outliers. Subsequently, the isolation forest model was used to further refine the outlier detection process based on the pre-screened dataset. The data points lower than 0 or higher than 0.15 were classified as the outliers, and then they were removed from the data set.

CGANs were used to augment the rest of the data set. The double hidden layers were employed to strengthen the learning ability of the generator and the accuracy of the discriminator. The detailed parameters of the CGANs are shown in Table 1. As a result, the data set was expanded from 98 data points to 192 data points.

The correlation scatter matrix graph was employed to reveal the relationship between the composition and microhardness of the steel, in which the elements and microhardness of the data set was employed to create a variable list, and the Seaborn library was used to plot the graph [17].

# 2.1.2. Feature engineering

41 features were collected and standardized to ensure equal contribution of each feature and eliminated the bias from the scale differences. The feature calculation formulas are shown in Table 2.

Here, $c _ { i }$ and $c _ { j }$ are the mole fractions of the $i ^ { t h }$ and $j ^ { t h }$ elements, respectively. k is the corresponding element parameter.

The process of feature engineering was as follows [18,19]:

(1) Feature importance voting: The Recursive Feature Elimination (RFE) models wrapped the random forest (RF), light gradient boosting machine (LightGBM) or extreme gradient boosting (XGBoost) algorithm separately were used to rank the features. Only the first features ranked by all the three models were selected as the candidate features.

Table 2 List of input material features.

<table><tr><td>Feature name</td><td>Abbreviation</td><td>Calculation formula</td></tr><tr><td>Weighting parameters</td><td></td><td></td></tr><tr><td>Valence electron concentration</td><td>VEC</td><td> $k = \sum_{i=1}^{n} c_i * k_i$ </td></tr><tr><td>Melting point</td><td>Tm</td><td></td></tr><tr><td>Number of itinerant electrons</td><td>e/a</td><td></td></tr><tr><td>Shear modulus</td><td>G</td><td></td></tr><tr><td>Young&#x27;s modulus</td><td>E</td><td></td></tr><tr><td>Cohesive energy</td><td>Ec</td><td></td></tr><tr><td>Work function</td><td>w</td><td></td></tr><tr><td>Atomic radii</td><td>r</td><td></td></tr><tr><td>Pauling electronegativity</td><td> $\chi$ </td><td></td></tr><tr><td>Bulk modulus</td><td>B</td><td></td></tr><tr><td>Poisson&#x27;s ratio</td><td> $\nu$ </td><td></td></tr><tr><td>First ionization energy</td><td> $E_{I-1st}$ </td><td></td></tr><tr><td>Second ionization energy</td><td> $E_{I-2nd}$ </td><td></td></tr><tr><td>Thermodynamic parameters</td><td></td><td></td></tr><tr><td>Mixing entropy</td><td> $\Delta Smix$ </td><td><img src="images/3e73c7ef77e09131945dd3b97ba6e092509a279e2a18beb9a3345f044ce820dd.jpg"/></td></tr><tr><td>Mixing enthalpy</td><td> $\Delta Hmix$ </td><td><img src="images/013f2608309a2ef893b87b044f8ff562cd53671947afb2b8c08cd9b4a0d6c8fa.jpg"/></td></tr><tr><td>Gibbs free energy</td><td>Gmix</td><td>Gmix =  $Hmix - Tm*Smix$ </td></tr><tr><td>Mismatch parameters</td><td></td><td></td></tr><tr><td>Shear module mismatch in strengthening model</td><td> $\eta_G$ </td><td><img src="images/cbef2246d0db93079d4e5933bae2e301206fa27e4f24e3c27f37894e356c1e59.jpg"/></td></tr><tr><td>Bulk module mismatch in strengthening model</td><td> $\eta_B$ </td><td></td></tr><tr><td></td><td></td><td><img src="images/fdfedf69b12b5a38424171afd0d5750402535381e72cbe66fd4e0f566ea3cccd.jpg"/></td></tr><tr><td>Difference in shear modulus</td><td> $\delta G$ </td><td></td></tr><tr><td>Difference in bulk modulus</td><td> $\delta B$ </td><td><img src="images/dbeed965463caced1708c237949e8827d2cc4badca0484198baf2b3513eb4079.jpg"/></td></tr><tr><td>Difference in poisson&#x27;s ratio</td><td> $\delta_\nu$ </td><td></td></tr><tr><td>Difference of radius</td><td> $\delta_r$ </td><td></td></tr><tr><td>Difference in melting temperature</td><td> $\delta_{Tm}$ </td><td></td></tr><tr><td>Difference in valence electron concentration</td><td> $\delta_{VEC}$ </td><td></td></tr><tr><td>Difference in free electron concentration</td><td> $\delta_{e/a}$ </td><td></td></tr><tr><td>Difference in cohesive energy</td><td> $\delta_{Ec}$ </td><td></td></tr><tr><td>Difference in first ionization energy</td><td> $\delta_{EI-1st}$ </td><td></td></tr><tr><td>Difference in second ionization energy</td><td> $\delta_{EI-2nd}$ </td><td></td></tr><tr><td> $\gamma$  parameter</td><td> $\gamma$ </td><td></td></tr><tr><td></td><td></td><td><img src="images/0a6e7bea8c7cd15161eb594b2916277b64f3f0fb392f153e5f179e2ca90359be.jpg"/></td></tr><tr><td>Difference in electronegativity</td><td> $\Delta \chi$ </td><td><img src="images/83909eefd2bce85b13a3da95fb06b09d7c55c7d6c0d3499738f949fed4b1c86c.jpg"/></td></tr><tr><td>Local shear modulus mismatch</td><td> $D_G$ </td><td><img src="images/e4d839e57abc1deb8ce45718398959a72311fb7acf9ef0a6443be7dab6ab268c.jpg"/></td></tr><tr><td>Local bulk modulus mismatch</td><td> $D_B$ </td><td></td></tr><tr><td>Local radius mismatch</td><td> $D_r$ </td><td></td></tr><tr><td>Local poisson&#x27;s ratio mismatch</td><td> $D_\nu$ </td><td></td></tr><tr><td>Local electronegativity mismatch</td><td> $D_\chi$ </td><td></td></tr><tr><td>Local melting temperature mismatch</td><td> $D_{Tm}$ </td><td></td></tr><tr><td>Local valence electron concentration mismatch</td><td> $D_{VEC}$ </td><td></td></tr><tr><td>Local free electron concentration mismatch</td><td> $D_{e/a}$ </td><td></td></tr><tr><td>Local cohesive energy mismatch</td><td> $D_{Ec}$ </td><td></td></tr><tr><td>Local first ionization energy mismatch</td><td> $D_{EI-1st}$ </td><td></td></tr><tr><td>Local second ionization energy mismatch</td><td> $D_{EI-2nd}$ </td><td></td></tr></table>

Table 3 Parameter configurations of the optimization algorithms.

<table><tr><td>Algorithm</td><td>Parameter configurations</td></tr><tr><td>FA</td><td>max_iter = 500, firefly_num = 100, alpha = 0.01, betamin = 0.2, gamma = 1,</td></tr><tr><td>SA</td><td>max_iter = 500, initial_temperature = 100, cooling_rate = 0.95,</td></tr><tr><td>PSO</td><td>max_iter = 500, particle_num = 100, c1 = 0.8, c2 = 0.5, w = 0.5</td></tr><tr><td>GWO</td><td>max_iter = 500, num_wolves = 100, alpha = 2, beta = 1.5, delta = 0.5, a = 2,</td></tr></table>

Table 4 Parameters of cladding.

<table><tr><td>Current (A)</td><td>Voltage (V)</td><td>Cladding speed (m/h)</td><td>Interlayer temperature (°C)</td><td>Wire feed speed (m/h)</td></tr><tr><td>440 ~ 600</td><td>30 ~ 32</td><td>24</td><td>380 ~ 410</td><td>76.8</td></tr></table>

(2) Feature correlation analysis: The Pearson Correlation Coefficient (PCC) of the candidate features was calculated, which can be calculated by the formula as follows:

$$
P C C = \sum_ {i = 1} ^ {n} (y _ {i} - \frac {\overline {{{{y}}}} _ {i}) (\widehat {y} _ {i} - \widehat {\overline {{{{y}}}}} _ {i})}{\sqrt {\sum_ {i = 1} ^ {n} (y _ {i} - \overline {{{{y}}}} _ {i}) ^ {2} \sum_ {i = 1} ^ {n} (\widehat {y} _ {i} - \widehat {\overline {{{{y}}}}} _ {i}) ^ {2}}} \tag {1}
$$

where $y _ { i }$ and $\widehat { y _ { i } }$ represent two different features of the $i ^ { t h }$ sample in the N-samples dataset; $\overline { { y _ { i } } }$ and $\widehat { \overline { { y _ { i } } } }$ are their average values. The two features were judged as high correlation features if the absolute value of their PCC was greater than or equal to 0.95.

(3) Redundant feature elimination: One of the high correlation features was remained through the average importance scores of the candidate features using the extra tree (ET), decision tree (DT), RF and XGBoost algorithm, and the features with higher scores were remained. The calculation of the average importance scores was described in detail by Chen [20].

Exhaustive screening was employed to optimize the feature combination. The details of the exhaustive screening were described by Fang [21]. The feature combination with the lowest score was selected as the final feature combination.

# 2.1.3. Algorithm selection and optimization

Ten different ML models were trained to optimize the composition and predict the microhardness of Fe-C-Cr-Mn-Si steel, including support vector machine (SVR), ET, XGBoost, ridge regression (Ridge), LightGBM, multilayer perceptron (MLP), RF, linear regression (LR), DT, and k-nearest neighbor (KNN) [22–26]. The coefficient of determination $( R ^ { 2 } )$ and root mean square error (RMSE) were employed to ensure the reliability of the prediction model. The $R ^ { 2 }$ and RMSE defined by the formula [16]:

$$
R ^ {2} = 1 - \frac {\sum_ {i = 1} ^ {n} \left(\widehat {y _ {P _ {i}}} - y _ {P _ {i}}\right) ^ {2}}{\sum_ {i = 1} ^ {n} \left(\overline {{y _ {P _ {i}}}} - y _ {P _ {i}}\right) ^ {2}} \# \tag {2}
$$

$$
R M S E = \sqrt {\frac {1}{n} \sum_ {i = 1} ^ {n} \left(\widehat {y _ {P _ {i}}} - y _ {P _ {i}}\right) ^ {2}} \# \tag {3}
$$

$R ^ { 2 }$ is a value between 0 and 1 that represents the proportion of variability in the dependent variable. RMSE represents the average of the model prediction error. $\widehat { y _ { P _ { i } } } , \overline { { y _ { P _ { i } } } } , y _ { P _ { i } }$ represent the predicted, mean and experimental value of each attribute, respectively. Subsequently, Bayesian optimization algorithm was employed with the optimization criterion of minimizing the RMSE to optimize the hyperparameters of ML model. Finally, the optimal model was selected by comparing the $R ^ { 2 }$

![](images/d07fa09a84828d7ee3a083cfaf8e29330c87b31abdb4e94312478ab293f55eaa.jpg)

<details>
<summary>scatter</summary>

| Category | C (wt.%) | Si (wt.%) | Mn (wt.%) | Cr (wt.%) | S (wt.%) | Ni (wt.%) | P (wt.%) | Fe (wt.%) | Mo (wt.%) | V (wt.%) | W (wt.%) | Microhardness (HIV) |
| -------- | -------- | --------- | --------- | --------- | -------- | --------- | -------- | --------- | --------- | -------- | -------- | ------------------- |
| Microhardness (HIV) | 1.5 | 2.0 | 0.5 | 1.0 | 0.5 | 1.0 | 0.5 | 1.0 | 0.5 | 1.0 | 0.5 | 600 |
| V (wt.%) | 2.0 | 1.5 | 1.0 | 1.5 | 1.0 | 1.5 | 1.0 | 1.5 | 1.0 | 1.5 | 1.0 | 400 |
| Mo (wt.%) | 2.0 | 1.5 | 1.0 | 1.5 | 1.0 | 1.5 | 1.0 | 1.5 | 1.0 | 1.5 | 1.0 | 400 |
| Fe (wt.%) | 2.0 | 1.5 | 1.0 | 1.5 | 1.0 | 1.5 | 1.0 | 1.5 | 1.0 | 1.5 | 1.0 | 400 |
| Ni (wt.%) | 2.0 | 1.5 | 1.0 | 1.5 | 1.0 | 1.5 | 1.0 | 1.5 | 1.0 | 1.5 | 1.0 | 400 |
| P (wt.%) | 2.0 | 1.5 | 1.0 | 1.5 | 1.0 | 1.5 | 1.0 | 1.5 | 1.0 | 1.5 | 1.0 | 400 |
| Cr (wt.%) | 2.0 | 1.5 | 1.0 | 1.5 | 1.0 | 1.5 | 1.0 | 1.5 | 1.0 | 1.5 | 1.0 | 400 |
| Mn (wt.%) | 2.0 | 1.5 | 1.0 | 1.5 | 1.0 | 1.5 | 1.0 | 1.5 | 1.0 | 1.5 | 1.0 | 400 |
| Si (wt.%) | 2.0 | 1.5 | 1.0 | 1.5 | 1.0 | 1.5 | 1.0 | 1.5 | 1.0 | 1.5 | 1.0 | 400 |
| C (wt.%)| 2.0 | 1.5 | 1.0 | 1.5 | 1.0 | 1.5 | 1.0 | 1.5 | 1.0 | 1.5 | 1.0 | 400 |
The chart displays multiple density plots with varying densities from the left to the right, likely representing the distribution of sample weights or particle sizes at each percentile of the sample size.
</details>

Fig. 2. Correlation scatter matrix graph.

and RMSE of the model.

The original solid solution strengthening theory was modified by the selected features to further improve the prediction accuracy of the model [14]. The original solid solution theory could be found in the reference [27].

Finally, 117 data points from the material information repository MatWeb were served as a validation data set to verify the prediction performance of the model through the ten-fold cross-validation and Bayesian optimization method, respectively.

# 2.2. Inverse design

C, Si, Mn, Cr, S, Ni, P, Mo, V and W elements were optimized, and the composition ranges were [0.02 wt%, 2 wt%], [0.1 wt%, 1 wt%], [0.15 wt%, 2 wt%], [0.5 wt%, 25 wt%], [0, 0.035 wt%], [0, 2 wt%], [0, 0.045 wt%], [0, 3 wt%], [0, 0.5 wt%], [0, 2 wt%], respectively, according to the relative references [28–31]. The element content was determined using firefly optimization algorithm (FA), simulated annealing algorithm (SA), particle swarm optimization (PSO) and grey wolf optimization algorithm (GWO) [32]. Table 3 shows the parameter configurations of the algorithms. The microhardness was optimized by the selected ML model.

# 2.3. Coating preparation and characterization

The wire with the optimized element content was used as the feeding material. The ASTM A36 steel plates with the size of 300 mm × 120 mm × 40 mm were used as the substrates in the experiment. The arc cladding equipment (IDEALARC DC-1000, Lincoln Electric, America) was used to prepare the Fe-C-Cr-Mn-Si coatings. The cladding parameters were shown in Table 4.

![](images/9e0181a3247bd196616d44b1afed90f7bf274c2006252f26435bdf9f273f0268.jpg)

![](images/eaabd1ed08a635cdcaf6ef5bf812df2dbe5d4d182f7c721ee53e512d05c2575b.jpg)

<details>
<summary>heatmap</summary>

(b)
| | e/a | G | ω | EI-2nd | ηB | δEc | δEI-2nd | DEc | γ |
|---|---|---|---|---|---|---|---|---|---|
| e/a | -0.89 | -0.24 | 0.08 | -0.98 | -1.00 | 0.86 | 0.83 | 0.86 | -0.95 |
| G | -0.89 | -0.24 | 0.08 | -0.98 | -1.00 | 0.86 | 0.83 | 0.86 | -0.95 |
| ω | 0.29 | 0.08 | 0.08 | -0.98 | -1.00 | 0.86 | 0.83 | 0.86 | -0.95 |
| EI-2nd | -0.14 | 0.08 | 0.08 | -0.98 | -1.00 | 0.86 | 0.83 | 0.86 | -0.95 |
| ηB | 0.15 | -0.10 | 0.98 | 0.98 | -1.00 | 0.86 | 0.83 | 0.86 | -0.95 |
| δEc | 0.61 | -0.54 | 0.92 | -0.86 | 0.86 | 0.86 | 0.83 | 0.86 | -0.95 |
| δEI-2nd | -0.10 | -0.04 | 0.97 | -1.00 | 1.00 | 0.83 | 0.86 | 0.86 | -0.95 |
| DEc | 0.57 | -0.51 | 0.94 | -0.88 | 0.88 | 1.00 | 0.86 | 0.86 | -0.95 |
| γ | -0.67 | 0.63 | -0.85 | 0.77 | -0.78 | -0.96 | -0.75 | -0.95 | 0.75 |
</details>

![](images/802cc3a7845aa9d4f8a00b4b51b3f0554e7e417474c01db01348ce6bb20188bd.jpg)

<details>
<summary>bar</summary>

| Features | Importance score |
| -------- | ---------------- |
| E_I-2nd  | 0.47             |
| η_B      | 0.15             |
| ω       | 0.13             |
| δ_E_I-2nd| 0.10             |
| D_Ec     | 0.04             |
| δ_Ec     | 0.04             |
| γ        | 0.03             |
| G        | 0.02             |
| e/a      | 0.01             |
</details>

Fig. 3. Feature selection: (a) Feature selection by RFE voting. (b) Heatmap showing the PCC between the 9 features (c) The importance ranking of the 9 features.

![](images/131f2b4b7649c77bc644c3bf1a0792744b1b9da792a12758531053481cf61b5c.jpg)

<details>
<summary>scatter</summary>

| Numbers of Features | Cross-validation scores |
| ------------------- | ----------------------- |
| 1                   | 1.28                    |
| 1                   | 0.95                    |
| 1                   | 0.57                    |
| 1                   | 0.34                    |
| 2                   | 0.69                    |
| 2                   | 0.41                    |
| 2                   | 0.35                    |
| 2                   | 0.30                    |
| 2                   | 0.28                    |
| 3                   | 0.33                    |
| 3                   | 0.31                    |
| 3                   | 0.26                    |
| 4                   | 0.29                    |
| 4                   | 0.28                    |
| 5                   | 0.27                    |
</details>

Fig. 4. Exhaustive screening results with different numbers of features.

The phases of the coatings were analyzed by X-ray diffraction (SmartLab SE, Rigaku, Japan) with Cu Kα radiation, operated at a working voltage of 40 kV and current of 40 mA. The Vicker’s microhardness of the coatings was measured using a microhardness indenter (HVS-1000A, Laizhou Huayin Testing Instrument Co., Ltd., China). The load was 1 kg with the holding time of 20 s.

# 3. Results and discussion

# 3.1. ML algorithm modeling

# 3.1.1. Screening results of elements

Fig. 2 presents the correlation scatter matrix graph, revealing the correlation between the chemical composition and microhardness of the alloy. The diagonal probability density histograms indicated that the Cr element exhibited a positive correlation with the microhardness, followed by Ni, Mo. Whereas, Mn, V and W showed weaker correlations. Cr, Ni and Mo can form solid solution alloys and carbides as the strengthening phases [33], and Ni can reduce the grain size of the alloys [34].

# 3.1.2. Screening results of features

The recursive feature elimination (RFE) method wrapped the RF, LightGBM and XGBoost algorithm was used to rank the importance of the original features, and the results are shown in Fig. 3a. The dark blue cells in Fig. 3a indicated the significant features (marked by 1). The result shows that EI-2nd, ηB, w, δEI-2nd, DEc, δEc, r, G and e/a presented the highest importance ranking in the RF, LightGBM and XGBoost algorithm. Fig. 3b shows the heat map of the selected features used to predict microhardness. It is found that the PCC absolute value of the E and w, $\eta _ { B }$ and w, $E _ { I - 2 n d }$ and $\eta _ { B } ,$ r and $D _ { E C } , E _ { I - 2 n d }$ and $\delta E _ { I - 2 n d } , \delta E _ { I - 2 n d }$ and $\eta _ { B }$ pair were equal to or greater than 0.95, showing the high correlation. The importance scores of the nine features were employed to remove one of the features with the high correlation in the six pairs, shown in Fig. 3c. It is found that $\eta _ { B } , w , \delta E _ { I - 2 n d }$ and r were removed in the pairs due to the low importance scores. Finally, e/a, G, E , δ and $D _ { E C }$ were found to be the key features for the microhardness. The $e / a$ ratio affected the phase stability of alloys during the formation of FCC and BCC phases: i $\dot { \mathbf { \eta } } e / a <$ 1.65, the alloy tended to form the FCC phase; if $e / a > 2 . 0 5 $ , the alloy tended to form the BCC phase [35]. The shear modulus G was crucial in increasing the plastic deformation resistance by increasing the solute atom-dislocation interaction energy, thereby increasing the hardness [36]. The second ionization energy $E _ { I - 2 n d }$ was also an important factor influencing solid solution strengthening involving in the electron cloud interaction and charge redistribution between adjacent atoms [37].The cohesive energy mismatch parameters, δ and $D _ { E c } ,$ were utilized to describe the bonding states and bonding strength [38].

![](images/eb80958c1f4d0496a1529816bc1dd1a22a3719f9f08a18c879454d18b12ec8dc.jpg)

<details>
<summary>scatter</summary>

| Data Type     | RMSE  | R²    |
| ------------- | ----- | ----- |
| Testing Data  | -     | -     |
| Training Data | -     | -     |
</details>

![](images/36bcd5a9117fe62e80a419b64c121f726de4a57ea1836c4a7a72376e209d363a.jpg)

<details>
<summary>scatter</summary>

| Data Type       | Experimental Microhardness (HV) | Prediction Microhardness (HV) |
| --------------- | ------------------------------- | ----------------------------- |
| Testing Data    | 350                             | 320                           |
| Training Data   | 400                             | 380                           |
| Testing Data    | 450                             | 430                           |
| Training Data   | 500                             | 480                           |
| Testing Data    | 550                             | 530                           |
| Training Data   | 600                             | 580                           |
| Testing Data    | 650                             | 630                           |
| Training Data   | 700                             | 680                           |
| Testing Data    | 750                             | 730                           |
| Training Data   | 800                             | 780                           |
</details>

![](images/97c06a93384397fdc11598580021873a17bb8ebe7e437c3e5befdf2a47ea16a5.jpg)

<details>
<summary>scatter</summary>

| Data Type       | Experimental Microhardness (HV) | Prediction Microhardness (HV) |
| --------------- | ------------------------------- | ----------------------------- |
| Testing Data    | ~550                            | ~580                          |
| Training Data   | ~600                            | ~570                          |
</details>

![](images/abf81e03af544b918fca2ef102b10579d89c4741c599af968a181f1f39b0c8e7.jpg)

<details>
<summary>scatter</summary>

| Data Type     | RMSE  | R²    |
| ------------- | ----- | ----- |
| Testing Data  | -     | -     |
| Training Data | -     | -     |
</details>

![](images/b27850f1f888174d8fbbc8553a6ac1386aa90cadb1500319fef8e1c9bb48c4c3.jpg)

<details>
<summary>scatter</summary>

| Data Type     | Experimental microhardness (HV) | Prediction microhardness (HV) |
| ------------- | ------------------------------- | ----------------------------- |
| Testing Data  | 400                             | 400                           |
| Training Data | 500                             | 500                           |
</details>

![](images/1d2fe215814a75fc553900c4eadc5063ed468b16c8a1bab3a081c13d7812c812.jpg)

<details>
<summary>scatter</summary>

| Data Type     | Experimental microhardness (HV) | Prediction microhardness (HV) |
| ------------- | ------------------------------- | ----------------------------- |
| Testing Data  | 350                             | 320                           |
| Training Data | 400                             | 380                           |
| Testing Data  | 450                             | 430                           |
| Training Data | 500                             | 480                           |
| Testing Data  | 550                             | 530                           |
| Training Data | 600                             | 580                           |
| Testing Data  | 650                             | 630                           |
| Training Data | 700                             | 680                           |
| Testing Data  | 750                             | 730                           |
| Training Data | 800                             | 780                           |
</details>

![](images/1a73624f7217990a5fe42834b00ddc5778f310c2b7a7981763f616f692cfd81c.jpg)

<details>
<summary>scatter</summary>

| Experimental microhardness (HV) | Prediction microhardness (HV) | Data Type     |
| ------------------------------- | ----------------------------- | ------------- |
| 300                             | 300                           | Testing Data  |
| 350                             | 350                           | Training Data |
| 400                             | 400                           | Testing Data  |
| 450                             | 450                           | Training Data |
| 500                             | 500                           | Testing Data  |
| 550                             | 550                           | Training Data |
| 600                             | 600                           | Testing Data  |
| 650                             | 650                           | Training Data |
| 700                             | 700                           | Testing Data  |
| 750                             | 750                           | Training Data |
| 800                             | 800                           | Testing Data  |
</details>

![](images/2a8fae9db5673bc19f5097f9830df0aa1224359f806613986fd93d17a3938746.jpg)

<details>
<summary>scatter</summary>

| Data Type     | Experimental microhardness (HV) | Prediction microhardness (HV) |
| ------------- | ------------------------------- | ----------------------------- |
| Testing Data  | 500                             | 550                           |
| Training Data | 450                             | 500                           |
</details>

![](images/bf42d952f7bc017682f9e3563fa4b087cbe7c2e060a94f427248cef1ea10dfb8.jpg)

<details>
<summary>scatter</summary>

| Data Type     | Experimental microhardness (HV) | Prediction microhardness (HV) |
| ------------- | ------------------------------- | ----------------------------- |
| Testing Data  | 350                             | 350                           |
| Training Data | 400                             | 400                           |
| Testing Data  | 450                             | 450                           |
| Training Data | 500                             | 500                           |
| Testing Data  | 550                             | 550                           |
| Training Data | 600                             | 600                           |
| Testing Data  | 650                             | 650                           |
| Training Data | 700                             | 700                           |
| Testing Data  | 750                             | 750                           |
| Training Data | 800                             | 800                           |
</details>

Fig. 5. The predictive microhardness based on the SVR model (a), ET model (b), MLP model (c), Ridge model (d), LightGBM model (e), XGBoost model (f), RF model (g), LR model (h), and DT model (i).

Table 5 Hyperparameter configurations of the SVR model.

<table><tr><td>Model</td><td colspan="8">Hyperparameter configuration</td></tr><tr><td>SVR</td><td>C</td><td>cache_size</td><td>coef0</td><td>degree</td><td>epsilon</td><td>gamma</td><td>kernel</td><td>tol</td></tr><tr><td>____</td><td>4.98</td><td>118.85</td><td>0.63</td><td>4</td><td> $1.87 \times 10^{-4}$ </td><td> $3.57 \times 10^{-2}$ </td><td>ploy</td><td> $1.22 \times 10^{-3}$ </td></tr></table>

Fig. 4 illustrates the result of the exhaustive search analysis, revealing the cross-validation scores as a function of the number of the features. It is found that the minimum RMSE was 0.341, 0.267, 0.257, 0.271, 0.281 for the cross-validation scores with the 1, 2, 3, 4, 5 features, respectively, indicating that 3 features presented the optimal prediction accuracy. Besides, the feature combination $\{ \delta _ { E c } , D _ { E c } , G \}$ presented the smallest RMSE value (0.257), and was identified as the key factors. The local cohesive energy mismatch $\delta _ { E C }$ and the difference in cohesive energy $D _ { E C }$ were the parameters related to cohesive energy $E c ,$ , which changed linearly with the chemical composition in complete solid solution systems [39]. The shear modulus change was suggested as one of the most predominant effects in solid solution, which was related to the interaction force between the solid solution obstacles and dislocation

[40].

# 3.1.3. Screening results of models

The SVR, ET, MLP, Ridge, LightGBM, XGBoost, RF, LR and DT model were trained to select the optimal model. The hyperparameters of each model were optimized using Bayesian optimization and ten-fold crossvalidation. The three key features $\{ G , \delta _ { E c } , D _ { E c } \}$ were used as the input parameters and the microhardness was used as an output parameter. Fig. 5 shows the $R ^ { 2 }$ and RMSE values of the different ML models. It is found that the $R ^ { 2 }$ values obtained by SVR, ET, MLP, Ridge, LightGBM, XGBoost, RF, LR and DT were 0.85, 0.80, 0.81, 0.82, 0.63, 0.79, 0.74, 0.76 and 0.72 respectively, and the RMSE values were 0.39, 0.45, 0.44, 0.43, 0.62, 0.46, 0.52, 0.48 and 0.54 respectively. The $R ^ { 2 }$ values obtained by SVR, ET, MLP and Ridge were higher than 0.80, and the RMSE values were lower than 0.45, indicating great linear correlation. Although the $R ^ { 2 }$ values of ET, XGBoost and DT reached 0.80, 0.79 and 0.72, there was a potential risk of overfitting between these three models based on testing data. The SVR model presented the highest $R ^ { 2 }$ value (0.85) and the lowest RMSE value (0.39), suggesting the SVR model had the best prediction capability. The key hyperparameter configurations of the SVR model are listed in Table 5.

![](images/9ca90681da2dc1c9cd5386ea1ac40fa690904677cde1c47a56225cb1e301e2e7.jpg)

<details>
<summary>scatter</summary>

| Experimental Δσ_SSS (MPa) | Predicted Δσ_SSS (MPa) | Error |
| ------------------------- | ---------------------- | ----- |
| 1200                      | 1200                   | 0.60  |
| 1300                      | 1300                   | 7.93  |
| 1400                      | 1400                   | 15.25 |
| 1500                      | 1500                   | 22.58 |
| 1600                      | 1600                   | 29.90 |
| 1700                      | 1700                   | 29.90 |
| 1800                      | 1800                   | 29.90 |
</details>

Fig. 6. The prediction results of solid solution strengthening under ten-fold cross validation with $\{ \delta _ { E c } , $ , D , G} as the input features.

![](images/ec326fec27498b19dcfaeb015e42eff0bd7fb7ce481b3e035a2d8ef352f6c2d1.jpg)

<details>
<summary>bar</summary>

| The optimization algorithm | Microhardness (HV) |
| :--- | :--- |
| FA | 733.59 |
| PSO | 730.04 |
| SA | 700.37 |
| GWO | 708.60 |
</details>

Fig. 7. The microhardness of the inverse designed material through different algorithms.

# 3.1.4. Model optimization by solid solution strengthening theory

The solid solution strengthening equation was introduced to modify the SVR model, and the equation was as follow:

$$
\Delta \sigma_ {s s s} = Z \cdot M \cdot G \cdot \delta_ {E c} \cdot D _ {E c} \tag {4}
$$

Z is a fitting parameter with a value of 0.0056; M is the Taylor factor and its value was 3.06 for both FCC and BCC structures.

Fig. 6 shows the validation result of the SVR model equipped with the modified solid solution strengthening theory. 117 experiment results from the materials information repository MatWeb were served as the validation dataset. It is found that the $R ^ { 2 }$ and RMSE value was 0.89 and 0.31, respectively. The $R ^ { 2 }$ increased by 4.71 %, and the RMSE decreased by 8.34 %, compared to the values without the modified solid solution strengthening theory (Fig. 5a).

# 3.1.5. Screening results of inverse design

Four intelligent optimization techniques, including simulated annealing (SA) [41], firefly optimization algorithm (FA) [42], particle swarm optimization (PSO) [43], and grey wolf optimization algorithm (GWO) [44] were employed to predict the alloy microhardness with the designed composition, and the results are shown in Fig. 7. The maximum microhardness calculated through the FA, PSO, SA, and GWO algorithm was 733.59 HV, 730.04 HV, 700.37 HV, and 708.60 HV, respectively. The alloy microhardness designed using the FA algorithm presented the highest value, followed by PSO, GWO and SA. FA was a generalized form of SA, PSO and differential evolution (DE), exhibiting superior local attraction capacity [42].

# 3.2. Experimental verification

The developed microhardness prediction model was validated by experiments. The mass percentages of the three Fe-C-Cr-Mn-Si alloy samples were listed in Table 6. Fig. 8 shows the XRD patterns of the three samples. The main phase structure of the sample 1 was Fe-Cr phase with the diffraction peaks of 100, 200 and 211. The Cr atoms randomly substituted Fe atoms in FCC lattice. With the Ni content increased, the main phase structure of the sample transferred to the Fe-Cr-Ni phase with the diffraction peaks of 100, 200 and 211. Fig. 8b reveals the enlarged XRD peaks at 2θ of 40-50◦. Compared with the standard diffraction peak of Fe, it is found that the diffraction peak of the alloy was shifted to the right at the corresponding diffraction peak, which was due to the atomic radius differences between Cr, Ni and Fe, resulting in lattice distortion [45,46].

Fig. 9 shows the microhardness values of the alloys with the predicted composition. It is noteworthy that the minimum error between the predicted value and experimental value was 1.17 %, lower than 2.01 % and 2.96 % for predicting the hardness of high entropy alloys reported by Ren et al. [14] and Huang et al. [47]. The microhardness of the samples can reach 515 HV, which can also be attributed to the solid solution phases. It was reported that the solid solution phases were formed when $\delta _ { r } < 0 . 0 6 6$ and − $1 1 . 6 < \Delta H _ { m i x } < 3 . 2$ kJ/mol [48]. We can find that the δ values of the samples were in a range of 0.0335 to 0.0595, lower than 0.066, and the $\Delta H _ { m i x }$ values were in a range of − 1.213 to − 0.451 kJ/mol, belonging to the range of − 11.6 to 3.2 kJ/mol.

# 4. Conclusions

A machine learning model combined the modified solid solution strengthening theory was built to predict the microhardness of the Fe-C-Cr-Mn-Si steel. There steels with the predicted composition were prepared using cladding to verify the prediction accuracy of the model. The main conclusions can be drawn:

(1) Cr had the greatest positive impact on the microhardness of the Fe-C-Cr-Mn-Si steel, followed by Ni and Mo.

Table 6 Mass percentages of the three Fe-C-Cr-Mn-Si alloys used for model validation.

<table><tr><td colspan="12">CSiMnCrSNiPFeMoVW mass percentage</td><td rowspan="2"> $\delta_r$ </td><td rowspan="2"> $\Delta H_{mix}$ (kJ/mol)</td></tr><tr><td></td><td>C</td><td>Si</td><td>Mn</td><td>Cr</td><td>S</td><td>Ni</td><td>P</td><td>Fe</td><td>Mo</td><td>V</td><td>W</td></tr><tr><td>Sample 1</td><td>0.45</td><td>0.19</td><td>1.53</td><td>14</td><td>0.01</td><td>0</td><td>0.014</td><td>83.806</td><td>0</td><td>0</td><td>0</td><td>0.0542</td><td>-0.914</td></tr><tr><td>Sample 2</td><td>0.53</td><td>0.4</td><td>1.9</td><td>5.3</td><td>0.01</td><td>1.13</td><td>0.013</td><td>89.277</td><td>0</td><td>0.25</td><td>1.19</td><td>0.0595</td><td>-1.213</td></tr><tr><td>Sample 3</td><td>0.15</td><td>0.5</td><td>1.5</td><td>5.2</td><td>0</td><td>1.2</td><td>0</td><td>89.7</td><td>1.5</td><td>0.25</td><td>0</td><td>0.0335</td><td>-0.451</td></tr></table>

![](images/bebeb0dae3f7227c93b5b7d5081f80f51f1e5da4c7b4687034418752ad1a9e18.jpg)

<details>
<summary>line</summary>

| Sample    | Peak Label     | 2θ (degree) |
| --------- | -------------- | ----------- |
| Sample 1  | (1 1 0)       | ~45         |
| Sample 1  | (2 0 0)       | ~65         |
| Sample 1  | (2 1 1)       | ~82         |
| Sample 2  | Fe-Cr-Ni       | ~45         |
| Sample 2  | Fe-Cr-Ni       | ~65         |
| Sample 3  | Fe-Cr-Ni       | ~45         |
</details>

![](images/613267133d7e830e53619f72fcf5b665ce690453ad56d4980f2ec1791400a9c5.jpg)

<details>
<summary>line</summary>

| Sample    | Peak Label |
| --------- | ---------- |
| Sample 1  | Fe-Cr      |
| Sample 2  | Fe-Cr-Ni   |
| Sample 3  | Fe-Cr-Ni   |
</details>

Fig. 8. XRD patterns of three samples (a), and the enlarged peaks at 40-50◦(b).

![](images/19e7d8a7f87b54825e03695d58fb7c6f7c8981f8a2491becbe061258c404ad91.jpg)

<details>
<summary>bar</summary>

| Sample | Predicted values (HV) | Experimental values (HV) | Percentage (%) |
| :--- | :--- | :--- | :--- |
| Sample 1 | 521 | 515 | 1.17 |
| Sample 2 | 490 | 500 | 2.00 |
| Sample 3 | 415 | 424 | 2.09 |
</details>

Fig. 9. Predicted versus actual microhardness of three samples of Fe-C-Cr-Mn-Si alloys.

(2) The difference in cohesive energy, local cohesive energy mismatch and shear modulus exhibited more pronounced impacts on the microhardness of the steel.
(3) The solid solution strengthening theory was modified using the difference in cohesive energy, local cohesive energy mismatch and shear modulus, and the predicted $R ^ { 2 }$ and RMSE value achieved 0.89 and 0.31.
(4) The microhardness of the predicted samples reached 515 HV, with the error between the predicted value and experimental value of 1.17 %.

# CRediT authorship contribution statement

Hao Wu: Writing – original draft, Software, Resources. Jianyuan Zhang: Validation. Jintao Zhang: Visualization. Chengjie Ge: Validation. Lu Ren: Software, Resources. Xinkun Suo: Writing – review & editing, Supervision.

# Declaration of competing interest

The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.

# Data availability

Data will be made available on request.
