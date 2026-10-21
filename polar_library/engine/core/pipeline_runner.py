"""Execute pipeline nodes in dependency order through operation facades."""

from collections.abc import Mapping
from pathlib import Path
from typing import Any

import polars as pl

from .operation_registry import get_interface
from .pipeline_graph import collect_nodes, topological_order


class PipelineRunner:
	"""Resolve each node's inputs and parameters, then delegate to its facade."""

	def __init__(self, pipeline: Mapping[str, Any], base_dir: str | Path | None = None) -> None:
		self.nodes = collect_nodes(pipeline)
		self.edges = pipeline["edges"]
		self.order = topological_order(self.nodes, self.edges)
		self.base_dir = Path(base_dir) if base_dir is not None else None

	def _inputs(
		self,
		node: Mapping[str, Any],
		datasources: Mapping[str, pl.DataFrame],
		results: Mapping[str, pl.DataFrame],
		edges_by_port: Mapping[str, Mapping[str, Any]],
	) -> list[pl.DataFrame]:
		"""Resolve each input port from an upstream result or an external datasource."""
		frames = []
		for port in sorted(node.get("input_ports", []), key=lambda item: item.get("ordinal", 0)):
			edge = edges_by_port.get(port["id"])
			if edge is not None:
				frames.append(results[edge["source_node_id"]])
				continue
			frame = datasources.get(port["id"])
			if frame is None:
				raise ValueError(f"Missing datasource for input port {port['id']!r}")
			frames.append(frame)
		return frames

	def _parameters(
		self,
		node: Mapping[str, Any],
		overrides: Mapping[str, Mapping[str, Any]],
	) -> dict[str, Any]:
		"""Merge stored and runtime parameters, resolving relative file paths."""
		stored = node.get("parameters")
		resolved = {**(stored if isinstance(stored, Mapping) else {}), **overrides.get(node["id"], {})}
		filepath = resolved.get("filepath")
		if self.base_dir is not None and isinstance(filepath, str) and not Path(filepath).is_absolute():
			resolved["filepath"] = self.base_dir / filepath
		return resolved

	def run(
		self,
		datasources: Mapping[str, pl.DataFrame] | None = None,
		parameters: Mapping[str, Mapping[str, Any]] | None = None,
	) -> dict[str, pl.DataFrame]:
		"""Execute every node and return the resulting dataframes keyed by node ID."""
		datasources = datasources or {}
		parameters = parameters or {}
		edges_by_port = {edge["target_input_port_id"]: edge for edge in self.edges}
		results: dict[str, pl.DataFrame] = {}
		for node_id in self.order:
			node = self.nodes[node_id]
			operation = (node.get("operation") or {}).get("name", "").lower()
			inputs = self._inputs(node, datasources, results, edges_by_port)
			interface = get_interface(operation)
			results[node_id] = interface.execute(operation, inputs, **self._parameters(node, parameters))
		return results

	@property
	def output_node_ids(self) -> tuple[str, ...]:
		"""Return nodes with no downstream consumers."""
		has_downstream = {edge["source_node_id"] for edge in self.edges}
		return tuple(node_id for node_id in self.nodes if node_id not in has_downstream)

	@property
	def datasource_port_ids(self) -> tuple[str, ...]:
		"""Return input ports without an incoming edge, which need external data."""
		connected = {edge["target_input_port_id"] for edge in self.edges}
		return tuple(sorted(
			port["id"]
			for node in self.nodes.values()
			for port in node.get("input_ports", [])
			if port["id"] not in connected
		))
