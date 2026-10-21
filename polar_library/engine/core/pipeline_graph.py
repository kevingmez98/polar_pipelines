"""Read pipeline nodes and order them by their edge dependencies."""

from collections.abc import Mapping
from typing import Any


def collect_nodes(pipeline: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
	"""Use the declared ``nodes`` list, or the nodes embedded in each edge."""
	if not isinstance(pipeline.get("edges"), list):
		raise TypeError("Pipeline JSON must contain an edges list")
	declared = pipeline.get("nodes")
	if declared is not None:
		nodes = {node["id"]: node for node in declared}
		if len(nodes) != len(declared):
			raise ValueError("Pipeline node IDs must be unique")
		return nodes

	nodes: dict[str, dict[str, Any]] = {}
	for edge in pipeline["edges"]:
		for endpoint in ("source_node", "target_node"):
			node = edge.get(endpoint)
			if node is None:
				continue
			node_id = node.get("id")
			if not node_id:
				raise ValueError(f"Edge endpoint {endpoint!r} has no node ID")
			if node_id in nodes and nodes[node_id] != node:
				raise ValueError(f"Conflicting definitions for node {node_id!r}")
			nodes[node_id] = node
	return nodes


def topological_order(
	nodes: Mapping[str, Any],
	edges: list[Mapping[str, Any]],
) -> list[str]:
	"""Return node IDs with every producer before its consumers."""
	dependencies: dict[str, set[str]] = {node_id: set() for node_id in nodes}
	for edge in edges:
		source, target = edge["source_node_id"], edge["target_node_id"]
		if source not in nodes or target not in nodes:
			raise ValueError(f"Edge {edge.get('id')!r} references an unknown node")
		dependencies[target].add(source)

	ordered: list[str] = []
	visiting: set[str] = set()
	visited: set[str] = set()

	def visit(node_id: str) -> None:
		if node_id in visiting:
			raise ValueError(f"Cycle detected at node {node_id!r}")
		if node_id in visited:
			return
		visiting.add(node_id)
		for source in dependencies[node_id]:
			visit(source)
		visiting.remove(node_id)
		visited.add(node_id)
		ordered.append(node_id)

	for node_id in nodes:
		visit(node_id)
	return ordered
