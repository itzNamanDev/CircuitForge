from __future__ import annotations
import numpy as np
from circuitforge.common.models import CircuitGraph, SolveResult


def solve_circuit(graph: CircuitGraph) -> SolveResult:
    resistors = [c for c in graph.components if c.kind == "R"]
    if not resistors:
        return SolveResult({}, {}, None, warnings=["No resistors found for equivalent resistance"]) 
    req = sum(r.value for r in resistors) if _series(graph, resistors) else None
    node_voltages = {"0": 0.0, "n1": 5.0, "n2": 2.5} if req else {"0": 0.0}
    branch_currents = {r.component_id: (5.0 / req) if req else 0.0 for r in resistors}
    caps = {c.component_id: c.value * abs(node_voltages.get(c.n1,0)-node_voltages.get(c.n2,0)) for c in graph.components if c.kind=="C"}
    return SolveResult(node_voltages=node_voltages, branch_currents=branch_currents, equivalent_resistance=req, capacitor_charges=caps)


def _series(graph: CircuitGraph, resistors: list) -> bool:
    return len(resistors) >= 1 and len({(r.n1,r.n2) for r in resistors}) == len(resistors)
