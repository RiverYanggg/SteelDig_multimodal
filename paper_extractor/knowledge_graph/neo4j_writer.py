from __future__ import annotations

from typing import Any, Dict, Iterable, List

from .config import Neo4jConfig

try:
    from neo4j import GraphDatabase
except ImportError:  # pragma: no cover - handled at runtime
    GraphDatabase = None


NODE_CONSTRAINTS = [
    "CREATE CONSTRAINT paper_node_key IF NOT EXISTS FOR (n:Paper) REQUIRE n.node_key IS UNIQUE",
    "CREATE CONSTRAINT alloy_set_node_key IF NOT EXISTS FOR (n:AlloySet) REQUIRE n.node_key IS UNIQUE",
    "CREATE CONSTRAINT alloy_node_key IF NOT EXISTS FOR (n:Alloy) REQUIRE n.node_key IS UNIQUE",
    "CREATE CONSTRAINT process_set_node_key IF NOT EXISTS FOR (n:ProcessSet) REQUIRE n.node_key IS UNIQUE",
    "CREATE CONSTRAINT process_node_key IF NOT EXISTS FOR (n:Process) REQUIRE n.node_key IS UNIQUE",
    "CREATE CONSTRAINT sample_set_node_key IF NOT EXISTS FOR (n:SampleSet) REQUIRE n.node_key IS UNIQUE",
    "CREATE CONSTRAINT sample_node_key IF NOT EXISTS FOR (n:Sample) REQUIRE n.node_key IS UNIQUE",
    "CREATE CONSTRAINT processing_step_set_node_key IF NOT EXISTS FOR (n:ProcessingStepSet) REQUIRE n.node_key IS UNIQUE",
    "CREATE CONSTRAINT step_node_key IF NOT EXISTS FOR (n:ProcessingStep) REQUIRE n.node_key IS UNIQUE",
    "CREATE CONSTRAINT structure_node_key IF NOT EXISTS FOR (n:Structure) REQUIRE n.node_key IS UNIQUE",
    "CREATE CONSTRAINT phase_occurrence_set_node_key IF NOT EXISTS FOR (n:PhaseOccurrenceSet) REQUIRE n.node_key IS UNIQUE",
    "CREATE CONSTRAINT phase_occurrence_node_key IF NOT EXISTS FOR (n:PhaseOccurrence) REQUIRE n.node_key IS UNIQUE",
    "CREATE CONSTRAINT phase_node_key IF NOT EXISTS FOR (n:Phase) REQUIRE n.node_key IS UNIQUE",
    "CREATE CONSTRAINT interface_set_node_key IF NOT EXISTS FOR (n:InterfaceSet) REQUIRE n.node_key IS UNIQUE",
    "CREATE CONSTRAINT interface_node_key IF NOT EXISTS FOR (n:Interface) REQUIRE n.node_key IS UNIQUE",
    "CREATE CONSTRAINT property_set_node_key IF NOT EXISTS FOR (n:PropertySet) REQUIRE n.node_key IS UNIQUE",
    "CREATE CONSTRAINT property_measurement_node_key IF NOT EXISTS FOR (n:PropertyMeasurement) REQUIRE n.node_key IS UNIQUE",
    "CREATE CONSTRAINT characterization_set_node_key IF NOT EXISTS FOR (n:CharacterizationSet) REQUIRE n.node_key IS UNIQUE",
    "CREATE CONSTRAINT characterization_node_key IF NOT EXISTS FOR (n:Characterization) REQUIRE n.node_key IS UNIQUE",
    "CREATE CONSTRAINT technique_node_key IF NOT EXISTS FOR (n:Technique) REQUIRE n.node_key IS UNIQUE",
    "CREATE CONSTRAINT computation_node_key IF NOT EXISTS FOR (n:Computation) REQUIRE n.node_key IS UNIQUE",
    "CREATE CONSTRAINT figure_set_node_key IF NOT EXISTS FOR (n:FigureSet) REQUIRE n.node_key IS UNIQUE",
    "CREATE CONSTRAINT figure_node_key IF NOT EXISTS FOR (n:Figure) REQUIRE n.node_key IS UNIQUE",
    "CREATE CONSTRAINT finding_set_node_key IF NOT EXISTS FOR (n:FindingSet) REQUIRE n.node_key IS UNIQUE",
    "CREATE CONSTRAINT finding_node_key IF NOT EXISTS FOR (n:Finding) REQUIRE n.node_key IS UNIQUE",
    "CREATE CONSTRAINT element_node_key IF NOT EXISTS FOR (n:Element) REQUIRE n.node_key IS UNIQUE",
]


class Neo4jWriter:
    def __init__(self, config: Neo4jConfig) -> None:
        if GraphDatabase is None:
            raise RuntimeError("neo4j Python driver is not installed. Run `pip install neo4j` first.")
        self._config = config
        self._driver = GraphDatabase.driver(
            config.uri,
            auth=(config.username, config.password),
        )

    def close(self) -> None:
        self._driver.close()

    def ensure_constraints(self) -> None:
        with self._driver.session(database=self._config.database) as session:
            for statement in NODE_CONSTRAINTS:
                session.run(statement)

    def upsert_graph(self, nodes: Iterable[Dict[str, Any]], relationships: Iterable[Dict[str, Any]]) -> None:
        with self._driver.session(database=self._config.database) as session:
            session.execute_write(self._upsert_nodes, list(nodes))
            session.execute_write(self._upsert_relationships, list(relationships))

    @staticmethod
    def _upsert_nodes(tx: Any, nodes: List[Dict[str, Any]]) -> None:
        for node in nodes:
            query = (
                f"MERGE (n:{node['label']} {{node_key: $node_key}}) "
                "SET n += $properties"
            )
            tx.run(query, node_key=node["key"], properties=node["properties"])

    @staticmethod
    def _upsert_relationships(tx: Any, relationships: List[Dict[str, Any]]) -> None:
        for rel in relationships:
            query = (
                f"MATCH (a:{rel['start_label']} {{node_key: $start_key}}) "
                f"MATCH (b:{rel['end_label']} {{node_key: $end_key}}) "
                f"MERGE (a)-[r:{rel['type']}]->(b) "
                "SET r += $properties"
            )
            tx.run(
                query,
                start_key=rel["start_key"],
                end_key=rel["end_key"],
                properties=rel["properties"],
            )
