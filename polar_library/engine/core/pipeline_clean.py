"""Merge API node, edge, and operation responses into a compact graph."""

from collections.abc import Mapping
from typing import Any


def _records(response: Any, label: str) -> list[dict[str, Any]]:
	"""Normalize an API envelope, one record, or a record list to a list.

	The result is always a list of dictionaries, regardless of the input form.
	"""
	if isinstance(response, Mapping) and "data" in response:
		response = response["data"]
	if response is None:
		return []
	if isinstance(response, Mapping):
		return [dict(response)]
	if isinstance(response, list) and all(isinstance(item, Mapping) for item in response):
		return [dict(item) for item in response]
	raise ValueError(f"{label} must contain an object or a list of objects")


def _parameters(raw: Any, node_id: str) -> dict[str, Any]:
	"""Keep parameter values typed; normalize API name/value lists to objects."""
	if raw is None:
		return {}
	if isinstance(raw, Mapping):
		return dict(raw)
	if not isinstance(raw, list):
		raise TypeError(f"Node {node_id!r} parameters must be an object or a name/value list")
	parameters = {}
	for parameter in raw:
		if not isinstance(parameter, Mapping):
			raise TypeError(f"Node {node_id!r} parameter must be an object")
		if parameter.get("is_deleted"):
			continue
		name = parameter.get("name")
		if not isinstance(name, str) or not name or "value" not in parameter:
			raise ValueError(f"Node {node_id!r} parameter requires name and value")
		if name in parameters:
			raise ValueError(f"Node {node_id!r} has duplicate parameter {name!r}")
		parameters[name] = parameter["value"]
	return parameters


def merge_pipeline_clean(
	edges_json: Mapping[str, Any],
	nodes_json: Mapping[str, Any],
	operations_json: Any,
) -> dict[str, list[dict[str, Any]]]:
	"""Build the runner's nodes/edges schema without inventing input configuration."""
	operations = {
		operation.get("id"): {
			"id": operation.get("id"),
			"name": operation.get("name"),
		}
		for operation in _records(operations_json, "operations")
		if operation.get("id") is not None and not operation.get("is_deleted")
	}
	nodes: dict[str, dict[str, Any]] = {}
	deleted_nodes = set()
	for node in _records(nodes_json, "nodes"):
		node_id = node.get("id")
		if node.get("is_deleted"):
			deleted_nodes.add(node_id)
			continue
		if not isinstance(node_id, str) or not node_id:
			raise ValueError("Node must have a nonempty string ID")
		if node_id in nodes:
			raise ValueError(f"Duplicate node ID {node_id!r}")
		operation = operations.get(node.get("operation_id"))
		if operation is None or not operation.get("name"):
			raise ValueError(f"Node {node_id!r} references a missing operation")
		nodes[node_id] = {
			"id": node_id,
			"input_ports": [
				{
					"id": port.get("id"),
					"ordinal": port.get("ordinal") if port.get("ordinal") is not None else 0,
				}
				for port in node.get("input_ports", [])
				if not port.get("is_deleted")
			],
			"output_ports": [
				{
					"id": port.get("id"),
					"ordinal": port.get("ordinal") if port.get("ordinal") is not None else 0,
				}
				for port in node.get("output_ports", [])
				if not port.get("is_deleted")
			],
			"operation": operation,
			"parameters": _parameters(node.get("parameters"), node_id),
		}
	clean_edges = []
	for edge in _records(edges_json, "edges"):
		if edge.get("is_deleted"):
			continue
		source_id = edge.get("source_node_id")
		target_id = edge.get("target_node_id")
		if source_id in deleted_nodes or target_id in deleted_nodes:
			continue
		if source_id not in nodes or target_id not in nodes:
			raise ValueError(f"Edge {edge.get('id')!r} references an unknown node")
		clean_edges.append(
			{
				"id": edge.get("id"),
				"source_node_id": source_id,
				"target_node_id": target_id,
				"source_output_port_id": edge.get("source_output_port_id"),
				"target_input_port_id": edge.get("target_input_port_id"),
			}
		)
	return {"nodes": list(nodes.values()), "edges": clean_edges}