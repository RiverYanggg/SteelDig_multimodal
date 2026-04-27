材料科学文献图像 `image_type` 分类体系（严格枚举）

使用要求：
1. 只能从下列枚举中选择 1 个 `image_type`，禁止输出枚举外新值。
2. 优先根据图像视觉特征判断；文字（caption/正文）只作为辅助证据。
3. 若存在重叠，按“更具体优先”原则：仪器专属图 > 通用图表。
4. 若确实难以精确区分，在最接近类型中选择，不留空、不输出 unknown。

---

- microscopy_sem — 扫描电子显微镜图像，用于展示材料表面形貌、颗粒尺寸、孔隙结构及断裂特征。
- microscopy_tem — 透射电子显微镜图像，用于展示纳米尺度形貌、晶格条纹、高分辨结构及选区电子衍射花样。
- microscopy_afm — 原子力显微镜图像，用于展示材料表面三维形貌、粗糙度及相分布。
- microscopy_optical — 光学显微镜图像，用于展示金相组织、腐蚀形貌、偏光特征及宏观缺陷。

- diffraction_xrd — X射线衍射图谱，用于物相鉴定、结晶度分析及晶格参数测定。
- diffraction_saed — 选区电子衍射图，用于确定晶体结构、取向关系及单晶/多晶判别。
- diffraction_ebsd — 电子背散射衍射图，用于晶粒取向成像、织构分析及晶界特征表征。

- spectroscopy_eds — 能谱元素分布图，用于微区元素定性与面分布分析。
- spectroscopy_eels — 电子能量损失谱图，用于元素价态、化学键合及薄膜厚度测定。
- spectroscopy_xps — X射线光电子能谱图，用于表面元素组成、化学态及定量分析。
- spectroscopy_ftir — 傅里叶变换红外光谱图，用于官能团识别与分子结构分析。
- spectroscopy_raman — 拉曼光谱图，用于分子振动模式、应力状态及碳材料结构表征。

- property_mechanical — 力学性能曲线图，包括应力-应变、蠕变、疲劳及纳米压痕数据。
- property_electrochemical — 电化学性能曲线图，包括充放电、循环伏安、交流阻抗及极化曲线。
- property_magnetic — 磁性能曲线图，包括磁滞回线、磁化温度依赖性及磁损耗。
- property_thermal — 热分析曲线图，包括差示扫描量热、热重分析及热膨胀数据。
- property_optical — 光谱性能图，包括吸收、发射、透射、光致发光及紫外可见光谱。

- calculation_dft — 密度泛函理论计算结果图，包括能带结构、态密度及差分电荷密度。
- calculation_md — 分子动力学模拟结果图，包括原子轨迹、径向分布函数及扩散行为。
- calculation_fe — 有限元模拟结果图，包括应力场、温度场及裂纹扩展模拟。

- structure_crystal — 晶体结构模型图，用于展示晶胞、原子占位、空间群及配位环境。
- structure_phase_diagram — 相图，用于展示成分-温度-压力条件下的相区与相变关系。

- fabrication_synthesis — 材料合成路线图，用于展示制备流程、反应条件及前驱体转化。
- fabrication_device — 器件加工流程图，用于展示薄膜沉积、光刻、刻蚀及封装步骤。

- chart_schematic — 原理示意图，用于展示工作机制、反应机理及能量转换过程。
- chart_flow — 流程图，用于展示实验步骤、工艺路线或研究框架。
- chart_plot — 通用数据图表，用于展示统计分析、对比结果及参数优化。
- chart_table — 数据表格图，用于展示成分配比、性能参数及实验条件汇总。

- photo_sample — 样品实物照片，用于展示宏观形貌、颜色、尺寸及组装状态。
- photo_equipment — 实验装置照片，用于展示仪器设备、反应釜及测试系统。
- photo_device — 器件实物照片，用于展示电池、传感器、催化剂等器件外观与封装。

---

易混淆场景建议：
- 若图中明确出现 XRD 峰型曲线，优先 `diffraction_xrd`，不要归为 `chart_plot`。
- 若是 CV/GCD/EIS/极化曲线，优先 `property_electrochemical`，不要归为 `chart_plot`。
- 若是拉曼/FTIR/XPS 等标准谱图，优先对应 `spectroscopy_*`，不要归为 `property_optical` 或 `chart_plot`。
- 若是样品/器件/装置实拍照片，优先 `photo_*`，不要归为 `chart_schematic`。