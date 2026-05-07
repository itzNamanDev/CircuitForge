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


def test_preprocessing():
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    out = preprocess_image(img)
    assert "edges" in out and out["gray"].shape == (100, 100)


def test_ocr_parser():
    assert parse_value("1k ohm")[0] == 1000


def test_symbol_detection_integration():
    img = np.zeros((100, 200), dtype=np.uint8)
    img[20:50, 20:90] = 255
    det = detect_symbols(img)
    assert isinstance(det, list)


def test_graph_netlist_solver_simplify_render(tmp_path):
    from circuitforge.common.models import DetectedComponent
    d = [DetectedComponent("1", "R", (0,0,20,10)), DetectedComponent("2", "R", (30,0,20,10))]
    g = extract_graph(d)
    nl = generate_netlist(g)
    assert "R" in nl
    assert validate_netlist(g) == []
    sol = solve_circuit(g)
    assert sol.equivalent_resistance is not None
    steps = simplify(g)
    assert len(steps) >= 1
    out = render_circuit(g, str(tmp_path / "c.svg"))
    assert Path(out).exists()


def test_ambiguity_handling():
    from circuitforge.common.models import DetectedComponent
    try:
        extract_graph([DetectedComponent("1", "R", (0,0,5,5))])
    except ValueError as e:
        assert "Ambiguous" in str(e)
