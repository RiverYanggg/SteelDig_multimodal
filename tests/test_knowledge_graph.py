import unittest
from pathlib import Path

from paper_extractor.knowledge_graph.builder import KnowledgeGraphBuilder


class KnowledgeGraphBuilderTest(unittest.TestCase):
    def setUp(self) -> None:
        self.project_root = Path(__file__).resolve().parent.parent
        self.dataset_root = self.project_root / "outputs_dataset"

    def test_build_a0_graph_contains_core_semantics(self) -> None:
        builder = KnowledgeGraphBuilder()
        result = builder.build_from_dataset(dataset_root=self.dataset_root, paper_ids=["A0"])
        summary = result.summary()

        self.assertEqual(summary["papers"], 1)
        self.assertEqual(summary["node_labels"]["Paper"], 1)
        self.assertEqual(summary["node_labels"]["AlloySet"], 1)
        self.assertEqual(summary["node_labels"]["ProcessSet"], 1)
        self.assertEqual(summary["node_labels"]["SampleSet"], 1)
        self.assertEqual(summary["node_labels"]["Sample"], 2)
        self.assertEqual(summary["node_labels"]["Figure"], 3)
        self.assertGreaterEqual(summary["node_labels"]["Finding"], 6)
        self.assertEqual(summary["node_labels"]["ProcessingStepSet"], 2)
        self.assertEqual(summary["node_labels"]["PhaseOccurrenceSet"], 2)
        self.assertEqual(summary["node_labels"]["CharacterizationSet"], 2)
        self.assertEqual(summary["node_labels"]["FigureSet"], 1)
        self.assertEqual(summary["node_labels"]["FindingSet"], 1)
        self.assertEqual(summary["relationship_types"]["OF_ALLOY"], 2)
        self.assertEqual(summary["relationship_types"]["PROCESSED_BY"], 2)
        self.assertEqual(summary["relationship_types"]["SUMMARIZED_AS"], 3)
        self.assertIn("HAS_ALLOY_SET", summary["relationship_types"])
        self.assertIn("HAS_ALLOY_ITEM", summary["relationship_types"])
        self.assertIn("HAS_PROCESS_SET", summary["relationship_types"])
        self.assertIn("HAS_PROCESS_ITEM", summary["relationship_types"])
        self.assertIn("HAS_SAMPLE_SET", summary["relationship_types"])
        self.assertIn("HAS_SAMPLE_ITEM", summary["relationship_types"])
        self.assertIn("HAS_PROCESSING_STEP_SET", summary["relationship_types"])
        self.assertIn("NEXT_STEP", summary["relationship_types"])
        self.assertIn("HAS_PHASE_OCCURRENCE_SET", summary["relationship_types"])
        self.assertIn("HAS_PHASE_OCCURRENCE_ITEM", summary["relationship_types"])
        self.assertIn("HAS_CHARACTERIZATION_SET", summary["relationship_types"])
        self.assertIn("HAS_CHARACTERIZATION", summary["relationship_types"])
        self.assertNotIn("HAS_STEP", summary["relationship_types"])
        self.assertNotIn("EXHIBITS_PHASE", summary["relationship_types"])
        self.assertNotIn("CHARACTERIZED_BY", summary["relationship_types"])
        self.assertNotIn("HAS_FIGURE", summary["relationship_types"])
        self.assertNotIn("HAS_FINDING", summary["relationship_types"])
        self.assertNotIn("EVIDENCE_FOR", summary["relationship_types"])
        self.assertNotIn("ABOUT", summary["relationship_types"])

    def test_build_full_dataset_graph_is_nonempty(self) -> None:
        builder = KnowledgeGraphBuilder()
        result = builder.build_from_dataset(dataset_root=self.dataset_root)
        summary = result.summary()

        self.assertGreaterEqual(summary["papers"], 80)
        self.assertGreater(summary["node_count"], 1000)
        self.assertGreater(summary["relationship_count"], 5000)
        self.assertIn("PhaseOccurrence", summary["node_labels"])
        self.assertIn("HAS_SAMPLE", summary["relationship_types"])

    def test_same_local_ids_from_different_papers_do_not_merge(self) -> None:
        builder = KnowledgeGraphBuilder()
        result = builder.build_from_dataset(dataset_root=self.dataset_root, paper_ids=["A58", "A71"])

        sample_nodes = {
            node["key"]: node for node in result.nodes if node["label"] == "Sample"
        }
        alloy_nodes = {
            node["key"]: node for node in result.nodes if node["label"] == "Alloy"
        }
        process_nodes = {
            node["key"]: node for node in result.nodes if node["label"] == "Process"
        }

        self.assertIn("A58::sample_6al", sample_nodes)
        self.assertIn("A71::sample_6al", sample_nodes)
        self.assertIn("A58::alloy_6al", alloy_nodes)
        self.assertIn("A71::alloy_6al", alloy_nodes)

        of_alloy_edges = [
            rel for rel in result.relationships
            if rel["type"] == "OF_ALLOY" and rel["start_key"] in {"A58::sample_6al", "A71::sample_6al"}
        ]
        processed_by_edges = [
            rel for rel in result.relationships
            if rel["type"] == "PROCESSED_BY" and rel["start_key"] in {"A58::sample_6al", "A71::sample_6al"}
        ]

        self.assertEqual(
            sorted((rel["start_key"], rel["end_key"]) for rel in of_alloy_edges),
            [
                ("A58::sample_6al", "A58::alloy_6al"),
                ("A71::sample_6al", "A71::alloy_6al"),
            ],
        )
        self.assertTrue(all(rel["start_key"].split("::", 1)[0] == rel["end_key"].split("::", 1)[0] for rel in processed_by_edges))


if __name__ == "__main__":
    unittest.main()
