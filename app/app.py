import math
import streamlit as st
import pandas as pd
import time
from quantum_logic import QuantumSlotMachine
from game_logic import GameState

# page config
st.set_page_config(page_title="Quantum Slot Machine", page_icon="🎰", layout="wide")

st.markdown("""
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

.reel-card {
    background: linear-gradient(145deg, #1f2933, #111827);
    border-radius: 16px;
    padding: 30px;
    text-align: center;
    font-size: 80px;
    box-shadow: 0 0 20px rgba(0,255,255,0.25);
}

.jackpot { 
    box-shadow: 0 0 35px rgba(255,215,0,0.9) !important; 
    transform: scale(1.1);
}

.stButton>button {
    font-size:48px; font-weight:900; text-transform:uppercase;
    padding:25px 0; border-radius:25px;
    border:6px solid gold; 
    color: white !important; /* Force text to stay white */
    background-color: red !important; /* Force background to stay red */
    width:100%;
}

.stButton>button:active, .stButton>button:focus, .stButton>button:hover {
    color: white !important;
    background-color: #ff0000 !important;
    border: 6px solid gold !important;
    opacity: 1 !important;
}
</style>
""", unsafe_allow_html=True)

# saving the game states
if "game" not in st.session_state:
    st.session_state.game = GameState()
if "history" not in st.session_state:
    st.session_state.history = []
if "last_reels" not in st.session_state:
    st.session_state.last_reels = ["🍒","🍒","🍒"]
if "last_message" not in st.session_state:
    st.session_state.last_message = ""
if "last_win_type" not in st.session_state:
    st.session_state.last_win_type = None

# introducing the quantum_logic
quantum_slot = QuantumSlotMachine()
all_symbols = ["🍒","🍋","🍊","🍇","🔔","⭐","💎","7️⃣"]

# sidebar for the quantum sliders
with st.sidebar:
    st.markdown("## ⚙️ Quantum Controls")
    angle_val = st.slider("Bias (θ)", 0.0, float(math.pi), float(math.pi/2), 0.05)
    variation_pct = st.slider("Variation (%)", 0, 50, 10, 5)
    oracle_mode = st.checkbox("Oracle Demo Mode", value=True)
    
    st.markdown("---")
    st.markdown("## 📊 Stats")
    stats = st.session_state.game.get_stats()
    st.metric("Credits", stats["credits"])
    st.metric("Total Spins", stats["total_spins"])
    st.metric("Total Wins", stats["total_wins"])
    st.metric("Win Rate", f"{stats['win_rate']:.1f}%")
    
    if st.button("🔄 Reset game"):
        st.session_state.game.reset()
        st.session_state.history = []
        st.session_state.last_reels = ["🍒","🍒","🍒"]
        st.session_state.last_message = ""
        st.rerun()

st.markdown("<h1 style='text-align:center;'>⚛️ Quantum Slot Machine 🎰</h1>", unsafe_allow_html=True)

# spin button
col_left, col_center, col_right = st.columns([1,2,1])
with col_center:
    spin_pressed = st.button("SPIN")

#reel results
col_r1, col_r2, col_r3 = st.columns(3)
reel1 = col_r1.empty()
reel2 = col_r2.empty()
reel3 = col_r3.empty()
message_placeholder = st.empty()

# animation loop for reels spining
def animate_reels(final_symbols, jackpot=False):
    for i in range(10):
        reel1.markdown(f"<div class='reel-card'>{all_symbols[i%len(all_symbols)]}</div>", unsafe_allow_html=True)
        reel2.markdown(f"<div class='reel-card'>{all_symbols[(i+3)%len(all_symbols)]}</div>", unsafe_allow_html=True)
        reel3.markdown(f"<div class='reel-card'>{all_symbols[(i+5)%len(all_symbols)]}</div>", unsafe_allow_html=True)
        time.sleep(0.05)
    
    #final state display
    cls = "reel-card jackpot" if jackpot else "reel-card"
    reel1.markdown(f"<div class='{cls}'>{final_symbols[0]}</div>", unsafe_allow_html=True)
    reel2.markdown(f"<div class='{cls}'>{final_symbols[1]}</div>", unsafe_allow_html=True)
    reel3.markdown(f"<div class='{cls}'>{final_symbols[2]}</div>", unsafe_allow_html=True)

# spin clicking mechanism
if spin_pressed:
    if not st.session_state.game.place_bet():
        st.session_state.last_message = "<div style='text-align:center;font-size:24px;color:red;'>Not enough credits!</div>"
    else:
        # checking if we use Oracle (2 symbols) or Normal (8 symbols)
        if oracle_mode:
            spin_result, win_type, payout = quantum_slot.run_spin_with_oracle_demo(angle_val, variation_pct)
        else:
            spin_result = quantum_slot.run_spin(angle_val, variation_pct)
            win_type, payout = quantum_slot.check_win(spin_result.reels)

        # update balance and history
        st.session_state.game.add_winnings(payout)
        st.session_state.last_reels = spin_result.reels
        st.session_state.last_win_type = win_type
        
        # start the spinning reels
        animate_reels(spin_result.reels, jackpot=(win_type=="triple"))

        # colors and messages for the banner
        if win_type == "triple":
            msg = f"🎉 JACKPOT! You won {payout} credits! 🎉"
            color = "gold"
        elif win_type == "double":
            msg = f"✅ You won {payout} credits! ({win_type.upper()})"
            color = "#16a34a"
        else:
            msg = "❌ No match, try again."
            color = "#b91c1c"

        st.session_state.last_message = f"<div style='text-align:center;font-size:32px;font-weight:bold;color:white;background:{color};padding:15px;border-radius:12px;'>{msg}</div>"

        st.session_state.history.append({
            "spin": len(st.session_state.history)+1,
            "reels": " ".join(spin_result.reels),
            "win_type": win_type,
            "payout": payout,
            #"angle": round(angle_val, 2)
        })

        st.rerun()

# displaying reels and messages
cls = "reel-card jackpot" if st.session_state.last_win_type=="triple" else "reel-card"
reel1.markdown(f"<div class='{cls}'>{st.session_state.last_reels[0]}</div>", unsafe_allow_html=True)
reel2.markdown(f"<div class='{cls}'>{st.session_state.last_reels[1]}</div>", unsafe_allow_html=True)
reel3.markdown(f"<div class='{cls}'>{st.session_state.last_reels[2]}</div>", unsafe_allow_html=True)
message_placeholder.markdown(st.session_state.last_message, unsafe_allow_html=True)

# history data display
st.markdown("## 📜 Spin history")
if st.session_state.history:
    df = pd.DataFrame(st.session_state.history).sort_values("spin", ascending=False)
    st.dataframe(df, hide_index=True, use_container_width=True)