"""Typed models shared by all pipeline modules.

These models enforce a structured pipeline so the app never relies on free-form
LLM guesses for topology or math.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Literal

ComponentType = Literal["R", "C", "L", "VDC", "VAC", "AM", "VM"]


@dataclass
class DetectedComponent:
    component_id: str
    kind: ComponentType
    bbox: tuple[int, int, int, int]
    confidence: float
    value_text: str | None = None
    value: float | None = None
    unit: str | None = None
    terminal_points: tuple[tuple[int, int], tuple[int, int]] | None = None
    orientation: Literal["h", "v"] = "h"


@dataclass
class CircuitComponent:
    component_id: str
    kind: ComponentType
    value: float
    unit: str
    n1: str
    n2: str
    orientation: Literal["h", "v"] = "h"


@dataclass
class CircuitGraph:
    nodes: set[str]
    components: list[CircuitComponent]


@dataclass
class SimplificationStep:
    description: str
    reason: str
    new_component: CircuitComponent
    removed_components: list[str]
    netlist_after: str
    graph_after: CircuitGraph


@dataclass
class SolveResult:
    node_voltages: dict[str, float]
    branch_currents: dict[str, float]
    equivalent_resistance: float | None
    capacitor_charges: dict[str, float] = field(default_factory=dict)
    meter_readings: dict[str, float] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
