from __future__ import annotations
from circuitforge.common.models import CircuitGraph


def generate_netlist(graph: CircuitGraph) -> str:
    lines = ["* CircuitForge generated netlist"]
    for c in graph.components:
        prefix = c.kind[0]
        lines.append(f"{prefix}{c.component_id} {c.n1} {c.n2} {c.value}")
    return "\n".join(lines)


def validate_netlist(graph: CircuitGraph) -> list[str]:
    warnings: list[str] = []
    if "0" not in graph.nodes:
        warnings.append("Ground node missing")
    for c in graph.components:
        if c.n1 == c.n2:
            warnings.append(f"Shorted component {c.component_id}")
    return warnings
