from __future__ import annotations
from pathlib import Path
import schemdraw
import schemdraw.elements as elm
from circuitforge.common.models import CircuitGraph


def render_circuit(graph: CircuitGraph, out_file: str) -> str:
    out = Path(out_file)
    with schemdraw.Drawing(file=str(out)) as d:
        for c in graph.components:
            if c.kind == "R":
                d += elm.Resistor().label(f"{c.component_id} {c.value}")
            elif c.kind == "VDC":
                d += elm.SourceV().label(f"{c.component_id} {c.value}")
            elif c.kind == "C":
                d += elm.Capacitor().label(f"{c.component_id} {c.value}")
            elif c.kind == "L":
                d += elm.Inductor().label(f"{c.component_id} {c.value}")
    return str(out)
