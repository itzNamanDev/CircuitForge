import numpy as np
from pathlib import Path
from circuitforge.image.preprocess import preprocess_image
from circuitforge.ocr.parser import parse_value
from circuitforge.symbols.detector import detect_symbols
from circuitforge.graph.extractor import extract_graph
from circuitforge.netlist.generator import generate_netlist, validate_netlist
from circuitforge.solver.solver import solve_circuit
from circuitforge.simplifier.engine import simplify
from circuitforge.renderer.draw import render_circuit
from circuitforge.common.models import DetectedComponent


def test_preprocessing():
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    out = preprocess_image(img)
    assert "edges" in out and "junction_map" in out


def test_ocr_parser():
    v, u = parse_value("1k ohm")
    assert v == 1000 and u == "ohm"


def test_symbol_detection_integration():
    img = np.zeros((100, 200), dtype=np.uint8)
    img[20:50, 20:90] = 255
    det = detect_symbols(img)
    assert isinstance(det, list)


def test_graph_netlist_solver_simplify_render(tmp_path):
    d = [
        DetectedComponent("R1", "R", (0, 0, 20, 10), 0.9, value=100.0, unit="ohm", terminal_points=((5, 5), (45, 5))),
        DetectedComponent("R2", "R", (50, 0, 20, 10), 0.9, value=200.0, unit="ohm", terminal_points=((45, 5), (80, 5))),
        DetectedComponent("V1", "VDC", (0, 20, 20, 20), 0.9, value=10.0, unit="v", terminal_points=((5, 25), (80, 25))),
    ]
    g = extract_graph(d)
    nl = generate_netlist(g)
    assert "R" in nl and "V" in nl
    assert validate_netlist(g) == []
    sol = solve_circuit(g)
    assert "0" in sol.node_voltages
    steps = simplify(g)
    assert isinstance(steps, list)
    out = render_circuit(g, str(tmp_path / "c.svg"))
    assert Path(out).exists()


def test_ambiguity_handling():
    d = [DetectedComponent("R1", "R", (0, 0, 20, 10), 0.9)]
    try:
        extract_graph(d)
        assert False, "Expected ambiguity error"
    except ValueError as e:
        assert "Ambiguous" in str(e)
