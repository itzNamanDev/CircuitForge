from __future__ import annotations
import cv2
from pathlib import Path
from circuitforge.image.preprocess import preprocess_image
from circuitforge.symbols.detector import detect_symbols
from circuitforge.graph.extractor import extract_graph
from circuitforge.netlist.generator import generate_netlist, validate_netlist
from circuitforge.solver.solver import solve_circuit
from circuitforge.simplifier.engine import simplify
from circuitforge.renderer.draw import render_circuit
from circuitforge.explanation.llm import explain


def run_pipeline(image_path: str, render_dir: str = "outputs") -> dict:
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Could not read image")
    prep = preprocess_image(image)
    detected = detect_symbols(prep["thresh"])
    graph = extract_graph(detected)
    netlist = generate_netlist(graph)
    warnings = validate_netlist(graph)
    result = solve_circuit(graph)
    steps = simplify(graph)
    Path(render_dir).mkdir(parents=True, exist_ok=True)
    render_paths = [render_circuit(graph, f"{render_dir}/step0.svg")]
    for i, _ in enumerate(steps, 1):
        render_paths.append(render_circuit(graph, f"{render_dir}/step{i}.svg"))
    narrative = explain(steps, result)
    return {
        "detected": detected,
        "graph": graph,
        "netlist": netlist,
        "warnings": warnings + result.warnings,
        "result": result,
        "steps": steps,
        "render_paths": render_paths,
        "explanation": narrative,
    }
