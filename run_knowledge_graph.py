import argparse
import json
from pathlib import Path

from paper_extractor.knowledge_graph import KnowledgeGraphBuilder, Neo4jConfig
from paper_extractor.knowledge_graph.neo4j_writer import Neo4jWriter


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build or import a Neo4j knowledge graph from outputs_dataset.")
    parser.add_argument("--dataset-root", default="outputs_dataset", help="Directory containing <paper_id>/final outputs.")
    parser.add_argument("--paper-id", action="append", default=[], help="Only ingest specific paper_id values. Repeatable.")
    parser.add_argument("--limit-papers", type=int, default=None, help="Optional limit after filtering paper ids.")
    parser.add_argument("--uri", default="bolt://127.0.0.1:7687", help="Neo4j bolt URI.")
    parser.add_argument("--username", default="neo4j", help="Neo4j username.")
    parser.add_argument("--password", default="neo4j", help="Neo4j password.")
    parser.add_argument("--database", default="neo4j", help="Neo4j database name.")
    parser.add_argument("--dry-run", action="store_true", help="Build the graph in memory and print a summary without writing to Neo4j.")
    parser.add_argument("--export-json", help="Write the normalized node/relationship payload to a JSON file.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    builder = KnowledgeGraphBuilder()
    result = builder.build_from_dataset(
        dataset_root=Path(args.dataset_root),
        paper_ids=args.paper_id,
        limit=args.limit_papers,
    )

    summary = result.summary()
    if args.export_json:
        export_path = Path(args.export_json).expanduser().resolve()
        export_path.parent.mkdir(parents=True, exist_ok=True)
        export_path.write_text(
            json.dumps(
                {
                    "summary": summary,
                    "nodes": result.nodes,
                    "relationships": result.relationships,
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

    if not args.dry_run:
        writer = Neo4jWriter(
            Neo4jConfig(
                uri=args.uri,
                username=args.username,
                password=args.password,
                database=args.database,
            )
        )
        try:
            writer.ensure_constraints()
            writer.upsert_graph(result.nodes, result.relationships)
        finally:
            writer.close()

    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
