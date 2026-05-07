# CircuitForge

CircuitForge is a modular AI-assisted **circuit analysis system** with a chat-style UI.
It enforces this contract:
- **Netlist is the structure truth source**
- **Physics solver is the numeric truth source**
- **LLM layer explains only structured outputs**

## Implemented Pipeline Order
`upload -> preprocessing -> symbol detection -> OCR parse -> graph extraction -> netlist generation -> validation -> physics solve -> simplification -> rendering -> explanation -> UI`

## Modules
- `app/streamlit_app.py`: ChatGPT-like UI + upload + grounded follow-up chat.
- `circuitforge/image/preprocess.py`: OpenCV grayscale/denoise/threshold/edges/lines/junction map/crop.
- `circuitforge/symbols/detector.py`: Lightweight pluggable detector for clean textbook diagrams.
- `circuitforge/ocr/parser.py`: Value parsing and unit normalization (`1kΩ`, `100uF`, `10V`).
- `circuitforge/graph/extractor.py`: Structured node-edge graph extraction with strict ambiguity errors.
- `circuitforge/netlist/generator.py`: SPICE-style netlist + consistency checks.
- `circuitforge/solver/solver.py`: MNA-based numeric solver (R/C/L + independent V sources).
- `circuitforge/simplifier/engine.py`: Deterministic series/parallel resistor simplification.
- `circuitforge/renderer/draw.py`: Equivalent-circuit rendering from structured graph/netlist.
- `circuitforge/explanation/llm.py`: Natural-language explanation from solver/simplifier outputs.
- `circuitforge/pipeline/orchestrator.py`: End-to-end execution wiring.

## Ambiguity Policy
The system does **not** silently guess topology or values.
If component values or connectivity are unclear, it raises explicit errors and requests a clearer image.

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .[dev]
```

## Run
```bash
streamlit run app/streamlit_app.py
```

## Tests
```bash
pytest -q
```

## Current V1 Scope
- Clean textbook-style circuit images only.
- Deterministic simplification for core resistor reductions.
- Full structured pipeline; detector is intentionally lightweight and swappable.
