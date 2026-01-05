import streamlit as st
import math
import pandas as pd

from quantum_logic import QuantumSlotMachine
from game_logic import GameState

st.set_page_config(page_title="Quantum Slot Machine", page_icon="🎰", layout="wide")

# -----------------------
# Session state
# -----------------------
if "game" not in st.session_state:
    st.session_state.game = GameState(starting_credits=100, bet_amount=10)
if "history" not in st.session_state:
    st.session_state.history = []
if "last_reels" not in st.session_state:
    st.session_state.last_reels = ["🍒", "🍒", "🍒"]
if "last_bits" not in st.session_state:
    st.session_state.last_bits = ["000", "000", "000"]
if "last_message" not in st.session_state:
    st.session_state.last_message = ""
if "last_oracle_flag" not in st.session_state:
    st.session_state.last_oracle_flag = None
    

# Quantum machine (simple + explainable)
quantum_slot = QuantumSlotMachine(n_reels=3, qubits_per_reel=3, entangle=True)

# -----------------------
# Header
# -----------------------
st.markdown(
    "<h1 style='text-align:center;'>⚛️ Quantum Slot Machine 🎰</h1>",
    unsafe_allow_html=True
)
st.write("Reels are produced by a quantum circuit: superposition (H), bias (RY), optional entanglement (CNOT), then measurement.")

st.markdown("---")

# -----------------------
# Sidebar controls
# -----------------------
with st.sidebar:
    st.markdown("## ⚙️ Settings")

    theta_base = st.slider(
        "Bias θ (radians)",
        min_value=0.0,
        max_value=float(math.pi),
        value=float(math.pi/2),
        step=0.05
    )

    variation_pct = st.slider("Variation (%)", 0, 50, 10, 5)
    oracle_mode = st.checkbox("Oracle Demo Mode (3 reels, 1 qubit each)", value=True)

    st.markdown("---")
    st.markdown("## 📊 Stats")
    stats = st.session_state.game.get_stats()
    st.metric("Credits", stats["credits"])
    st.metric("Total Spins", stats["total_spins"])
    st.metric("Total Wins", stats["total_wins"])
    st.metric("Win Rate", f"{stats['win_rate']:.1f}%")

    if st.button("🔄 Reset game", use_container_width=True):
        st.session_state.game.reset()
        st.session_state.history = []
        st.session_state.last_reels = ["🍒", "🍒", "🍒"]
        st.session_state.last_bits = ["000", "000", "000"]
        st.session_state.last_message = ""
        st.rerun()

# -----------------------
# Main UI: reels + controls
# -----------------------
st.markdown(f"## 💰 Credits: **{st.session_state.game.credits}**")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"<div style='font-size:70px; text-align:center;'>{st.session_state.last_reels[0]}</div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div style='font-size:70px; text-align:center;'>{st.session_state.last_reels[1]}</div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div style='font-size:70px; text-align:center;'>{st.session_state.last_reels[2]}</div>", unsafe_allow_html=True)

if st.session_state.last_message:
    st.success(st.session_state.last_message)
if oracle_mode and st.session_state.last_bits != ["000", "000", "000"]:
    # In oracle mode, bits are 1-bit strings, so display them clearly
    st.info("Oracle Demo Mode is ON (win flag is shown after spin).")
if oracle_mode and st.session_state.last_oracle_flag is not None:
    st.info(f"Oracle flag (win qubit) = {st.session_state.last_oracle_flag}  (1 means WIN)")
   

spin = st.button(
    "🎰 QUANTUM SPIN (10 credits)",
    disabled=not st.session_state.game.can_spin(),
    use_container_width=True,
    type="primary"
)

if spin:
    if not st.session_state.game.place_bet():
        st.warning("Not enough credits.")
    else:
        if oracle_mode:
            spin_result = quantum_slot.run_spin_with_oracle_demo(theta_base=theta_base, variation_pct=variation_pct)
            st.session_state.last_oracle_flag = spin_result.oracle_flag
            payout = quantum_slot.oracle_demo_payout(spin_result.oracle_flag)
            win_type = "oracle_jackpot" if payout > 0 else "none"            

        else:
            spin_result = quantum_slot.run_spin(theta_base=theta_base, variation_pct=variation_pct)
            st.session_state.last_oracle_flag = None

            win_type, payout = quantum_slot.check_win(spin_result.reels)


        # update state
        st.session_state.last_reels = spin_result.reels
        st.session_state.last_bits = spin_result.reel_bits

        if payout > 0:
            st.session_state.game.add_winnings(payout)
            st.session_state.last_message = f"✅ {win_type.upper()} match! You won {payout} credits."
        else:
            st.session_state.last_message = "❌ No match. Try again."

        st.session_state.history.append({
            "spin": len(st.session_state.history) + 1,
            "reels": " ".join(spin_result.reels),
            "bits": " ".join(spin_result.reel_bits),
            "win_type": win_type,
            "payout": payout,
            "theta": round(theta_base, 2),
            "variation_pct": variation_pct
        })

        st.rerun()

st.markdown("---")

# -----------------------
# Analysis / History
# -----------------------
st.markdown("## 📜 Spin history")

if st.session_state.history:
    df = pd.DataFrame(st.session_state.history).sort_values("spin", ascending=False)
    st.dataframe(df, hide_index=True, use_container_width=True, height=320)

    # Optional Plotly (won't crash if not installed)
    with st.expander("📊 Quick plots"):
        try:
            import plotly.graph_objects as go

            win_counts = df["win_type"].value_counts()
            fig = go.Figure(data=[go.Pie(labels=win_counts.index, values=win_counts.values, hole=0.35)])
            fig.update_layout(title="Win distribution")
            st.plotly_chart(fig, use_container_width=True)

        except ModuleNotFoundError:
            st.info("Plotly not installed. Run: pip install plotly (optional).")
else:
    st.info("No spins yet.")
