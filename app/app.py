import streamlit as st
from quantum_logic import quantum_spin_one_reel

st.title("Quantum Slot Machine (Prototype)")
st.write("One reel = one qubit. Spin applies a Hadamard gate (superposition), then measures.")

# Optional: map outputs to symbols
symbol_map = {
    "0": "🍒",
    "1": "💎"
}

if "last_result" not in st.session_state:
    st.session_state.last_result = None

spin = st.button("🎰 SPIN (Quantum)")

if spin:
    bit = quantum_spin_one_reel(shots=1)
    st.session_state.last_result = bit

if st.session_state.last_result is None:
    st.info("Click SPIN to run a quantum circuit.")
else:
    bit = st.session_state.last_result
    st.success(f"Measured: {bit}  →  Symbol: {symbol_map[bit]}")
    st.write("Interpretation: before measurement, the reel is in a superposition of 0 and 1.")
