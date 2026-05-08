from dataclasses import dataclass
import unittest

from paper_extractor.knowledge.chunker import Chunk
from paper_extractor.knowledge.extractor import ModelResponseError, _extract_chat_content
from paper_extractor.knowledge.normalizer import normalize_claims
from paper_extractor.knowledge.synthesis_payload import build_synthesis_payload


@dataclass
class DummyCompletion:
    choices: object


class KnowledgeRobustnessTest(unittest.TestCase):
    def test_empty_model_choices_raises_readable_error(self) -> None:
        with self.assertRaisesRegex(ModelResponseError, "no choices"):
            _extract_chat_content(DummyCompletion(choices=None))

    def test_normalize_claims_skips_invalid_records(self) -> None:
        chunk = Chunk(
            chunk_id="A53_c0001",
            paper_id="A53",
            section="Intro",
            section_index=0,
            paragraph_start=0,
            paragraph_end=0,
            char_start=0,
            char_end=17,
            token_estimate=3,
            text="Steel alloy text.",
        )

        claims, warnings = normalize_claims(
            [
                None,
                {"paper_id": "A53", "chunk_id": "A53_c0001", "section": "Intro", "claims": None},
                {"paper_id": "A53", "chunk_id": "A53_c0001", "section": "Intro", "claims": [None]},
            ],
            [chunk],
        )

        self.assertEqual(claims, [])
        self.assertEqual(
            [warning["validation_status"] for warning in warnings],
            ["invalid_record", "invalid_claims", "invalid_claim"],
        )

    def test_synthesis_payload_ignores_invalid_items(self) -> None:
        payload = build_synthesis_payload(
            paper_map=None,
            claims=[
                None,
                {
                    "claim_id": "c_00001",
                    "claim_type": "processing",
                    "subject": "heat treatment",
                    "claim": "The alloy processing route included homogenization before tensile testing.",
                    "confidence": "high",
                    "validation_status": "matched",
                },
            ],
            visual_evidence=[None, {"figure_id": "Figure 1", "description": "SEM image of the microstructure."}],
        )

        self.assertIsNone(payload["paper_focus"]["title"])
        self.assertEqual(payload["core_facts"]["processing"][0]["id"], "c_00001")
        self.assertEqual(payload["visual_evidence"][0]["figure_id"], "Figure 1")


if __name__ == "__main__":
    unittest.main()
