# CircuitForge

Production-ready modular circuit-analysis app with a ChatGPT-like interface. The pipeline is structured so that:
- **Netlist = source of truth for circuit structure**
- **Physics solver = source of truth for numeric results**
- **LLM layer = explanation only**

## Features (V1)
- Image upload and chat-style UI (Streamlit)
- OpenCV preprocessing (grayscale, denoise, threshold, edges, lines)
- Pluggable symbol detection module
- OCR value parsing and normalization
- Graph extraction into structured nodes/components
- SPICE-style netlist generation + validation
- Deterministic simplification (series/parallel scaffold, series implemented)
- Physics-based solving scaffold for node/branch outputs
- Equivalent circuit rendering from netlist-derived graph
- Grounded natural-language explanation from structured outputs only

## Architecture and Data Flow
`upload -> preprocessing -> symbol detection -> OCR -> graph extraction -> netlist generation -> validation -> solving -> simplification -> rendering -> explanation -> UI`

## Repository Layout
- `app/streamlit_app.py` UI module
- `circuitforge/image` preprocessing
- `circuitforge/symbols` symbol detection
- `circuitforge/ocr` OCR parsing
- `circuitforge/graph` graph extraction
- `circuitforge/netlist` netlist generation/validation
- `circuitforge/solver` physics solver interface
- `circuitforge/simplifier` deterministic simplification engine
- `circuitforge/renderer` circuit rendering
- `circuitforge/explanation` LLM explanation layer
- `circuitforge/pipeline` orchestrator
- `tests/` module tests
- `sample_inputs/` sample images

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

## Run
```bash
streamlit run app/streamlit_app.py
```

## Test
```bash
pytest -q
```

## Notes on Reliability
- If extraction is ambiguous, the graph extractor raises an explicit ambiguity error.
- The LLM explanation layer never computes circuit math; it only verbalizes structured outputs.
- Hand-drawn/noisy circuit support is intentionally limited in V1; clean textbook-style diagrams are the target.
