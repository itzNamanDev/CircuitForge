"""Graph extraction from structured detections.

This module refuses to invent topology: if terminals cannot be mapped to
junctions confidently, it raises an ambiguity error.
"""
from __future__ import annotations
from circuitforge.common.models import CircuitComponent, CircuitGraph, DetectedComponent


def extract_graph(detected: list[DetectedComponent], node_snap_px: int = 12) -> CircuitGraph:
    if not detected:
        raise ValueError("Ambiguous circuit: no components detected")

    node_points: list[tuple[int, int]] = []
    node_names: dict[tuple[int, int], str] = {}

    def snap(pt: tuple[int, int]) -> str:
        for ept in node_points:
            if abs(ept[0] - pt[0]) <= node_snap_px and abs(ept[1] - pt[1]) <= node_snap_px:
                return node_names[ept]
        node_points.append(pt)
        name = f"n{len(node_points)}"
        node_names[pt] = name
        return name

    components: list[CircuitComponent] = []
    for d in detected:
        if d.terminal_points is None or d.value is None or d.unit is None:
            raise ValueError(f"Ambiguous circuit: missing terminals/value for {d.component_id}")
        n1 = snap(d.terminal_points[0])
        n2 = snap(d.terminal_points[1])
        if n1 == n2:
            raise ValueError(f"Invalid topology: shorted terminals on {d.component_id}")
        components.append(CircuitComponent(d.component_id, d.kind, d.value, d.unit, n1, n2, d.orientation))

    if len(node_points) < 2:
        raise ValueError("Ambiguous circuit: insufficient distinct junction nodes")

    # Promote a stable reference node as SPICE ground.
    old_to_new = {"n1": "0"}
    for c in components:
        c.n1 = old_to_new.get(c.n1, c.n1)
        c.n2 = old_to_new.get(c.n2, c.n2)
    nodes = {old_to_new.get(f"n{i+1}", f"n{i+1}") for i in range(len(node_points))}

    return CircuitGraph(nodes=nodes, components=components)
