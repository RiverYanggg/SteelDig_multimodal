import unittest

from paper_extractor.unit_normalization import normalize_units


class UnitNormalizationTest(unittest.TestCase):
    def test_structured_quantities_are_converted_to_canonical_units(self) -> None:
        data = {
            "processing_steps": [
                {"temperature": "1073.15", "unit": "K", "duration": "30 min", "reduction_ratio": "0.5"}
            ],
            "structures": [
                {
                    "microstructure_list": [
                        {
                            "grain_structure": {
                                "average_grain_size": {"value": "500", "unit": "nm"}
                            }
                        }
                    ]
                }
            ],
            "properties": [
                {
                    "mechanical": {
                        "tensile_properties": {
                            "yield_strength": [{"value": "0.855", "unit": "GPa"}],
                            "elongation": [{"value": "35", "unit": "percent"}],
                            "strain_hardening_rate": [{"value": "0.5", "unit": "GPa"}],
                        }
                    }
                }
            ],
        }

        normalized, report = normalize_units(data)

        step = normalized["processing_steps"][0]
        self.assertEqual(step["temperature"], "800")
        self.assertEqual(step["unit"], "°C")
        self.assertEqual(step["duration"], "0.5 h")
        self.assertEqual(step["reduction_ratio"], "0.5")
        grain = normalized["structures"][0]["microstructure_list"][0]["grain_structure"]["average_grain_size"]
        self.assertEqual(grain, {"value": "0.5", "unit": "μm"})
        strength = normalized["properties"][0]["mechanical"]["tensile_properties"]["yield_strength"][0]
        self.assertEqual(strength, {"value": "855", "unit": "MPa"})
        elongation = normalized["properties"][0]["mechanical"]["tensile_properties"]["elongation"][0]
        self.assertEqual(elongation, {"value": "35", "unit": "%"})
        strain_hardening = normalized["properties"][0]["mechanical"]["tensile_properties"]["strain_hardening_rate"][0]
        self.assertEqual(strain_hardening, {"value": "500", "unit": "MPa"})
        self.assertGreaterEqual(report["summary"]["converted_count"], 5)

    def test_ambiguous_missing_unit_is_reported_without_mutation(self) -> None:
        data = {"properties": [{"mechanical": {"fracture_toughness": {"value": "55", "unit": None}}}]}

        normalized, report = normalize_units(data)

        self.assertEqual(normalized, data)
        self.assertEqual(report["summary"]["ambiguous_count"], 1)

    def test_free_text_is_not_rewritten(self) -> None:
        data = {"processes": [{"description": "Fe-10Mn-6Al was held at 800 °C for 30 min."}]}

        normalized, report = normalize_units(data)

        self.assertEqual(normalized, data)
        self.assertEqual(report["summary"]["converted_count"], 0)


if __name__ == "__main__":
    unittest.main()
