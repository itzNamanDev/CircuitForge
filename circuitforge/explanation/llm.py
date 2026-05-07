from __future__ import annotations
from circuitforge.common.models import SolveResult, SimplificationStep


def explain(steps: list[SimplificationStep], result: SolveResult) -> str:
    s = ["Structured solver-backed explanation:"]
    for i, step in enumerate(steps, 1):
        s.append(f"Step {i}: {step.description}. Reason: {step.reason}")
    s.append(f"Equivalent resistance: {result.equivalent_resistance}")
    s.append(f"Node voltages: {result.node_voltages}")
    return "\n".join(s)
