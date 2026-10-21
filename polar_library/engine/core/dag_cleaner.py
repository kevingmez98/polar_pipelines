def merge_pipeline_clean(edges_json, nodes_json, operations_json):
    """
    Merge and clean the data from edges, nodes and operations
    """
    # Clean and index operations
    ops_dict = {}
    op_raw = operations_json.get("data", {})
    for op_raw in operations_json.get("data", []):
        if op_raw:
            ops_dict[op_raw["id"]] = {"id": op_raw.get("id"), "name": op_raw.get("name")}

    # Clean and index nodes
    nodes_dict = {}
    for node in nodes_json.get("data", []):
        node_id = node.get("id")
        op_id = node.get("operation_id")

        # Filter node ports
        input_ports = [
            {"id": p["id"], "ordinal": p.get("ordinal")}
            for p in node.get("input_ports", [])
        ]
        output_ports = [
            {"id": p["id"], "ordinal": p.get("ordinal")}
            for p in node.get("output_ports", [])
        ]

        nodes_dict[node_id] = {
            "id": node_id,
            "input_ports": input_ports,
            "output_ports": output_ports,
            "operation": ops_dict.get(op_id, None),  # Inyectar operación limpia
        }

    # Clean and enrich edges
    edges_cleaned = []
    for edge in edges_json.get("data", []):
        source_id = edge.get("source_node_id")
        target_id = edge.get("target_node_id")

        edge_clean = {
            "id": edge.get("id"),
            "source_node_id": source_id,
            "target_node_id": target_id,
            "source_output_port_id": edge.get("source_output_port_id"),
            "target_input_port_id": edge.get("target_input_port_id"),
        }
        edges_cleaned.append(edge_clean)

    return {"nodes": list(nodes_dict.values()), "edges": edges_cleaned}
