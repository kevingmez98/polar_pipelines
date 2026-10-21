"""Build a DAG from saved response snapshots and run the local pipeline."""

import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import polars as pl

from polar_library.engine.core.dag_cleaner import merge_pipeline_clean
from polar_library.engine.core.pipeline_runner import PipelineRunner


def export_clean_pipeline(dag_directory: Path) -> None:
	"""Overwrite pipeline_clean.json with the runner-ready nodes/edges schema."""
	nodes_json = json.loads((dag_directory / "nodes.json").read_text(encoding="utf-8"))
	edges_json = json.loads((dag_directory / "edges.json").read_text(encoding="utf-8"))
	# Only active nodes determine which operation snapshots are needed.
	operation_ids = {
		node["operation_id"]
		for node in nodes_json.get("data", [])
		if not node.get("is_deleted") and node.get("operation_id")
	}
	operations_json = {"data": []}
	for operation_id in sorted(operation_ids):
		# Read operation contracts by ID instead of scanning unrelated JSON files.
		operation_path = dag_directory / f"{operation_id}.json"
		operation_response = json.loads(operation_path.read_text(encoding="utf-8"))
		operations_json["data"].append(operation_response["data"])

	clean_dag = merge_pipeline_clean(edges_json, nodes_json, operations_json)
	output_path = dag_directory / "pipeline_clean.json"
	output_path.write_text(
		json.dumps(clean_dag, indent=4, ensure_ascii=False) + "\n",
		encoding="utf-8",
	)
	print(f"Generated {len(clean_dag['nodes'])} nodes and {len(clean_dag['edges'])} edges in {output_path}")


def run_pipeline(
	project_root: Path,
	pipeline_path: Path,
	*,
	datasources: Mapping[str, pl.DataFrame] | None = None,
	parameters: Mapping[str, Mapping[str, Any]] | None = None,
) -> None:
	"""Execute a pipeline file and report each terminal node's result."""
	pipeline = json.loads(pipeline_path.read_text(encoding="utf-8"))
	# File paths inside the pipeline are relative to the project root.
	runner = PipelineRunner(pipeline, base_dir=project_root)
	results = runner.run(datasources=datasources, parameters=parameters)
	for node_id in runner.output_node_ids:
		result = results[node_id]
		print(f"{node_id}: {len(result)} rows, {len(result.columns)} columns")

def main(
	build_pipeline_clean: bool = True,
	pipeline_file: str = "pipeline_test.json",
	datasources: Mapping[str, pl.DataFrame] | None = None,
	parameters: Mapping[str, Mapping[str, Any]] | None = None,
) -> None:
	"""Optionally build pipeline_clean, then execute the selected DAG file."""
	project_root = Path(__file__).resolve().parent
	dag_directory = project_root / "polar_library/dag"
	if build_pipeline_clean:
		export_clean_pipeline(dag_directory)
	run_pipeline(
		project_root,
		dag_directory / pipeline_file,
		datasources=datasources,
		parameters=parameters,
	)


if __name__ == "__main__":
	main(False)
