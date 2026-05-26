from dataclasses import dataclass


@dataclass(frozen=True)
class Neo4jConfig:
    uri: str = "bolt://127.0.0.1:7687"
    username: str = "neo4j"
    password: str = "neo4j"
    database: str = "neo4j"
