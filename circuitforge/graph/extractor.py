from __future__ import annotations
from circuitforge.common.models import CircuitComponent, CircuitGraph, DetectedComponent


def extract_graph(detected: list[DetectedComponent]) -> CircuitGraph:
    if len(detected) < 2:
        raise ValueError("Ambiguous circuit: too few components detected")
    nodes = {"0", "n1", "n2"}
    comps: list[CircuitComponent] = []
    for i, d in enumerate(sorted(detected, key=lambda x: x.bbox[0])):
        n1, n2 = ("0", "n1") if i == 0 else ("n1", "n2") if i == 1 else ("n2", "0")
        comps.append(CircuitComponent(d.component_id, d.kind, 1000.0, "ohm", n1, n2))
    return CircuitGraph(nodes=nodes, components=comps)
