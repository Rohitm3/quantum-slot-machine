from quantum_logic import quantum_spin_one_reel_biased, quantum_spin_counts_one_reel_biased

import math
import streamlit as st
from quantum_logic import quantum_spin_one_reel_biased

st.title("Quantum Slot Machine (Prototype)")
st.write("One reel = one qubit. Use a quantum rotation RY(θ) to control probabilities, then measure.")

symbol_map = {"0": "🍒", "1": "💎"}

# Slider for theta
theta = st.slider("Bias control θ (radians)", min_value=0.0, max_value=float(math.pi), value=float(math.pi/2), step=0.05)

p1 = (math.sin(theta / 2) ** 2)
p0 = 1 - p1

st.caption(f"Expected probabilities: P(🍒=0) ≈ {p0:.3f},  P(💎=1) ≈ {p1:.3f}")

if "last_result" not in st.session_state:
    st.session_state.last_result = None

if st.button("🎰 SPIN (Quantum)"):
    bit = quantum_spin_one_reel_biased(theta=theta, shots=1)
    st.session_state.last_result = bit

st.markdown("---")
st.subheader("Fairness / Frequency check")

shots = st.number_input("Number of spins (shots)", min_value=10, max_value=5000, value=200, step=10)

if st.button("Run many spins"):
    counts = quantum_spin_counts_one_reel_biased(theta=theta, shots=int(shots))
    total = counts["0"] + counts["1"]
    obs_p0 = counts["0"] / total
    obs_p1 = counts["1"] / total

    st.write("Counts:", counts)
    st.write(f"Observed: P(🍒=0) ≈ {obs_p0:.3f},  P(💎=1) ≈ {obs_p1:.3f}")

    st.write("Difference (Observed - Expected):")
    st.write(f"ΔP(🍒) = {obs_p0 - p0:.3f}")
    st.write(f"ΔP(💎) = {obs_p1 - p1:.3f}")


if st.session_state.last_result is None:
    st.info("Move the slider, then click SPIN.")
else:
    bit = st.session_state.last_result
    st.success(f"Measured: {bit}  →  Symbol: {symbol_map[bit]}")
    st.write("Interpretation: the reel was in a superposition with probabilities set by RY(θ).")
