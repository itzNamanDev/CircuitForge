from __future__ import annotations
import tempfile
from pathlib import Path
import streamlit as st
from circuitforge.pipeline.orchestrator import run_pipeline

st.set_page_config(page_title="CircuitForge", layout="wide")
st.title("CircuitForge AI Circuit Solver")
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
for msg in st.session_state.history:
    st.chat_message(msg["role"]).write(msg["content"])
