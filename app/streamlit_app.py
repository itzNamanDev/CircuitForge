from __future__ import annotations
import sys
from pathlib import Path

# Ensure repo root is importable when Streamlit executes from app/ directory.
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import tempfile
import tempfile
from pathlib import Path
import streamlit as st
from circuitforge.pipeline.orchestrator import run_pipeline

st.set_page_config(page_title="CircuitForge", layout="wide")
st.title("CircuitForge AI Circuit Solver")
st.caption("Circuit analysis pipeline: extraction + netlist + physics solver. LLM is explanation-only.")

if "history" not in st.session_state:
    st.session_state.history = []
if "result_data" not in st.session_state:
    st.session_state.result_data = None

uploaded = st.file_uploader("Upload circuit image", type=["png", "jpg", "jpeg"])
query = st.chat_input("Ask: solve this circuit / show first simplification / show next step / why combined?")
st.caption("Structured extraction + netlist + physics solver. LLM used for explanations only.")

if "history" not in st.session_state:
    st.session_state.history = []

uploaded = st.file_uploader("Upload circuit image", type=["png", "jpg", "jpeg"])
query = st.chat_input("Ask follow-up (e.g., show next simplification step)")

if uploaded:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        tmp.write(uploaded.read())
        img_path = tmp.name
    st.image(img_path, caption="Uploaded circuit", use_container_width=True)
    try:
        st.session_state.result_data = run_pipeline(img_path, render_dir="outputs")
    except ValueError as exc:
        st.error(str(exc))
        st.stop()

if st.session_state.result_data:
    data = st.session_state.result_data
    st.subheader("Extracted Components")
    st.write([vars(d) for d in data["detected"]])
    st.subheader("Generated Netlist")
    st.code(data["netlist"])
    data = run_pipeline(img_path, render_dir="outputs")

    st.subheader("Extracted Components")
    st.write([vars(d) for d in data["detected"]])

    st.subheader("Generated Netlist")
    st.code(data["netlist"])

    st.subheader("Simplification Steps")
    for i, step in enumerate(data["steps"], 1):
        st.markdown(f"**Step {i}**: {step.description}")
        st.caption(step.reason)
        st.code(step.netlist_after)
    st.subheader("Equivalent Circuit Images")
    for p in data["render_paths"]:
        if Path(p).exists():
            st.image(p)
    st.subheader("Final Numerical Results")
    st.json({"node_voltages": data["result"].node_voltages, "branch_currents": data["result"].branch_currents,
             "equivalent_resistance": data["result"].equivalent_resistance, "capacitor_charges": data["result"].capacitor_charges,
             "meter_readings": data["result"].meter_readings, "warnings": data["warnings"]})

    st.subheader("Rendered Equivalents")
    for p in data["render_paths"]:
        if Path(p).exists():
            st.image(p)

    st.subheader("Numerical Results")
    st.json({
        "node_voltages": data["result"].node_voltages,
        "branch_currents": data["result"].branch_currents,
        "equivalent_resistance": data["result"].equivalent_resistance,
        "warnings": data["warnings"],
    })

    st.subheader("Explanation")
    st.write(data["explanation"])

if query:
    st.session_state.history.append({"role": "user", "content": query})
    answer = "Please upload and solve a circuit first."
    d = st.session_state.result_data
    if d:
        q = query.lower()
        if "first simplification" in q and d["steps"]:
            s = d["steps"][0]; answer = f"Step 1: {s.description}. {s.reason}"
        elif "next step" in q:
            answer = "V1 currently returns deterministic step list; see Simplification Steps section."
        elif "why" in q and "combined" in q and d["steps"]:
            answer = d["steps"][0].reason
        elif "equivalent" in q:
            answer = f"Equivalent resistance from solver/simplifier outputs: {d['result'].equivalent_resistance}"
        else:
            answer = d["explanation"]
    st.session_state.history.append({"role": "assistant", "content": answer})

for msg in st.session_state.history:
    st.chat_message(msg["role"]).write(msg["content"])
