from __future__ import annotations
from circuitforge.common.models import CircuitGraph

_PREFIX = {"R": "R", "C": "C", "L": "L", "VDC": "V", "VAC": "V", "AM": "XAM", "VM": "XVM"}


def generate_netlist(graph: CircuitGraph) -> str:
    lines = ["* CircuitForge generated netlist"]
    for c in graph.components:
        prefix = _PREFIX[c.kind]
        if c.kind == "VAC":
            lines.append(f"{prefix}{c.component_id} {c.n1} {c.n2} AC {c.value}")
        else:
            lines.append(f"{prefix}{c.component_id} {c.n1} {c.n2} {c.value}")
        prefix = c.kind[0]
        lines.append(f"{prefix}{c.component_id} {c.n1} {c.n2} {c.value}")
    return "\n".join(lines)


def validate_netlist(graph: CircuitGraph) -> list[str]:
    warnings: list[str] = []
    if "0" not in graph.nodes:
        warnings.append("Ground node missing")
    if not graph.components:
        warnings.append("No components in netlist")
    for c in graph.components:
        if c.n1 == c.n2:
            warnings.append(f"Shorted component {c.component_id}")
        if c.value <= 0 and c.kind in {"R", "C", "L"}:
            warnings.append(f"Non-physical value for {c.component_id}")
    for c in graph.components:
        if c.n1 == c.n2:
            warnings.append(f"Shorted component {c.component_id}")
    return warnings
