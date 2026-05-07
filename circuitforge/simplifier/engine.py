from __future__ import annotations
from copy import deepcopy
from circuitforge.common.models import CircuitComponent, CircuitGraph, SimplificationStep
from circuitforge.netlist.generator import generate_netlist


def simplify(graph: CircuitGraph) -> list[SimplificationStep]:
    g = deepcopy(graph)
    steps: list[SimplificationStep] = []
    resistors = [c for c in g.components if c.kind == "R"]
    if len(resistors) >= 2:
        r1, r2 = resistors[0], resistors[1]
        new = CircuitComponent("REQ1", "R", r1.value + r2.value, "ohm", r1.n1, r2.n2)
        g.components = [c for c in g.components if c.component_id not in {r1.component_id, r2.component_id}] + [new]
        steps.append(SimplificationStep(
            description=f"Combined {r1.component_id} and {r2.component_id}",
            reason="Series resistors share a node with no branch.",
            new_component=new,
            removed_components=[r1.component_id, r2.component_id],
            netlist_after=generate_netlist(g)
        ))
    return steps
