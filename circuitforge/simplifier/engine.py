"""Deterministic simplification engine.

Generates one reduction per step with reason + updated netlist.
"""
from __future__ import annotations
from copy import deepcopy
from circuitforge.common.models import CircuitComponent, CircuitGraph, SimplificationStep
from circuitforge.netlist.generator import generate_netlist


def simplify(graph: CircuitGraph) -> list[SimplificationStep]:
    g = deepcopy(graph)
    steps: list[SimplificationStep] = []

    while True:
        reduced = _reduce_once(g)
        if reduced is None:
            break
        g, step = reduced
        steps.append(step)
    return steps


def _reduce_once(g: CircuitGraph) -> tuple[CircuitGraph, SimplificationStep] | None:
    resistors = [c for c in g.components if c.kind == "R"]

    for i in range(len(resistors)):
        for j in range(i + 1, len(resistors)):
            r1, r2 = resistors[i], resistors[j]
            if {r1.n1, r1.n2} == {r2.n1, r2.n2}:
                req = 1 / ((1 / r1.value) + (1 / r2.value))
                new = CircuitComponent(f"REQP_{r1.component_id}_{r2.component_id}", "R", req, "ohm", r1.n1, r1.n2)
                g.components = [c for c in g.components if c.component_id not in {r1.component_id, r2.component_id}] + [new]
                step = SimplificationStep(
                    description=f"Combined {r1.component_id} and {r2.component_id} in parallel",
                    reason="Both resistors share the same two nodes.",
                    new_component=new,
                    removed_components=[r1.component_id, r2.component_id],
                    netlist_after=generate_netlist(g),
                    graph_after=deepcopy(g),
                )
                return g, step

    for r1 in resistors:
        for r2 in resistors:
            if r1.component_id == r2.component_id:
                continue
            if r1.n2 == r2.n1:
                new = CircuitComponent(f"REQS_{r1.component_id}_{r2.component_id}", "R", r1.value + r2.value, "ohm", r1.n1, r2.n2)
                g.components = [c for c in g.components if c.component_id not in {r1.component_id, r2.component_id}] + [new]
                step = SimplificationStep(
                    description=f"Combined {r1.component_id} and {r2.component_id} in series",
                    reason="They are end-to-end with an unbranched intermediate node.",
                    new_component=new,
                    removed_components=[r1.component_id, r2.component_id],
                    netlist_after=generate_netlist(g),
                    graph_after=deepcopy(g),
                )
                return g, step
    return None
