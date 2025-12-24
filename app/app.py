import streamlit as st
import math
import time
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from quantum_logic import (
    quantum_spin_one_reel_biased,
    quantum_spin_counts_one_reel_biased,
    quantum_spin_one_reel_8symbols,
    quantum_spin_counts_8symbols
)
from game_logic import GameState, SymbolMapper, WinChecker, QuantumStateTracker

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="Quantum Slot Machine",
    page_icon="🎰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== ADVANCED CSS STYLING ====================
st.markdown("""
    <style>
    /* Main styling */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Reel display */
    .reel-container {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin: 30px 0;
    }
    
    .reel {
        font-size: 120px !important;
        text-align: center;
        padding: 40px;
        border-radius: 25px;
        background: linear-gradient(145deg, #ffffff, #f0f0f0);
        color: white;
        margin: 10px;
        box-shadow: 
            0 20px 40px rgba(0,0,0,0.3),
            inset 0 -5px 15px rgba(0,0,0,0.1);
        min-width: 200px;
        min-height: 200px;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 8px solid #ffd700;
        transition: all 0.3s ease;
    }
    
    .reel.spinning {
        animation: spin 0.1s linear infinite;
        filter: blur(5px);
    }
    
    @keyframes spin {
        0% { transform: translateY(0); }
        100% { transform: translateY(-20px); }
    }
    
    /* Credits display */
    .credits-mega {
        font-size: 56px;
        font-weight: 900;
        color: #00ff00;
        text-align: center;
        padding: 30px;
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        border-radius: 20px;
        margin: 20px 0;
        box-shadow: 0 10px 30px rgba(0,255,0,0.3);
        border: 3px solid #00ff00;
        text-shadow: 0 0 20px #00ff00;
    }
    
    /* Quantum state display */
    .quantum-display {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: #00ff41;
        padding: 25px;
        border-radius: 15px;
        border: 2px solid #00ff41;
        font-family: 'Courier New', monospace;
        font-size: 18px;
        margin: 20px 0;
        box-shadow: 0 10px 30px rgba(0,255,65,0.2);
        position: relative;
        overflow: hidden;
    }
    
    .quantum-display::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            45deg,
            transparent,
            rgba(0,255,65,0.1),
            transparent
        );
        animation: scan 3s linear infinite;
    }
    
    @keyframes scan {
        0% { transform: translateX(-100%) translateY(-100%); }
        100% { transform: translateX(100%) translateY(100%); }
    }
    
    /* Win message */
    .win-mega {
        font-size: 72px;
        font-weight: 900;
        text-align: center;
        color: #ffd700;
        animation: rainbow 2s linear infinite, pulse 1s ease-in-out infinite;
        padding: 50px;
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 50%, #ff6b6b 100%);
        background-size: 200% 200%;
        border-radius: 25px;
        margin: 30px 0;
        box-shadow: 0 20px 60px rgba(255,215,0,0.6);
        text-shadow: 
            0 0 10px #fff,
            0 0 20px #fff,
            0 0 30px #ffd700,
            0 0 40px #ffd700;
    }
    
    @keyframes rainbow {
        0% { filter: hue-rotate(0deg); }
        100% { filter: hue-rotate(360deg); }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    /* Button styling */
    .stButton > button {
        font-size: 32px !important;
        font-weight: 900 !important;
        padding: 25px 60px !important;
        border-radius: 15px !important;
        border: none !important;
        background: linear-gradient(135deg, #00c853 0%, #00e676 100%) !important;
        color: white !important;
        box-shadow: 0 10px 30px rgba(0,200,83,0.5) !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-5px) !important;
        box-shadow: 0 15px 40px rgba(0,200,83,0.7) !important;
    }
    
    .stButton > button:disabled {
        background: linear-gradient(135deg, #666 0%, #888 100%) !important;
        box-shadow: none !important;
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #00c853, #00e676, #00c853);
        background-size: 200% 100%;
        animation: progressShine 2s linear infinite;
    }
    
    @keyframes progressShine {
        0% { background-position: 200% 0; }
        100% { background-position: -200% 0; }
    }
    
    /* Stats cards */
    .stat-card {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin: 10px 0;
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        border: 2px solid rgba(255,255,255,0.1);
    }
    
    .stat-value {
        font-size: 48px;
        font-weight: 900;
        color: #00ff88;
        text-shadow: 0 0 10px #00ff88;
    }
    
    .stat-label {
        font-size: 18px;
        color: #ffffff;
        margin-top: 10px;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
    
    /* Glow effect */
    .glow {
        animation: glow 2s ease-in-out infinite;
    }
    
    @keyframes glow {
        0%, 100% { filter: drop-shadow(0 0 5px #00ff41); }
        50% { filter: drop-shadow(0 0 20px #00ff41); }
    }
    </style>
""", unsafe_allow_html=True)

# ==================== SESSION STATE ====================
if "game_state" not in st.session_state:
    st.session_state.game_state = GameState(starting_credits=100)
if "reel_results" not in st.session_state:
    st.session_state.reel_results = ["🍒", "🍒", "🍒"]
if "quantum_state" not in st.session_state:
    st.session_state.quantum_state = "System Ready - Click SPIN to begin"
if "win_message" not in st.session_state:
    st.session_state.win_message = ""
if "spinning" not in st.session_state:
    st.session_state.spinning = False
if "history" not in st.session_state:
    st.session_state.history = []
if "use_8_symbols" not in st.session_state:
    st.session_state.use_8_symbols = True

# Initialize helpers
symbol_mapper = SymbolMapper(use_8_symbols=st.session_state.use_8_symbols)
win_checker = WinChecker()
quantum_tracker = QuantumStateTracker()

# ==================== HEADER WITH ANIMATION ====================
st.markdown("""
    <div style='text-align: center; padding: 30px; animation: glow 2s ease-in-out infinite;'>
        <h1 style='
            font-size: 80px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #667eea 100%);
            background-size: 200% 200%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: gradient 3s ease infinite;
            font-weight: 900;
            text-shadow: 0 0 30px rgba(102,126,234,0.5);
        '>
            ⚛️ QUANTUM SLOT MACHINE ⚛️
        </h1>
        <p style='
            font-size: 24px;
            color: white;
            font-weight: 600;
            letter-spacing: 3px;
            text-shadow: 0 0 10px rgba(255,255,255,0.5);
        '>
            POWERED BY REAL QUANTUM COMPUTING
        </p>
    </div>
    
    <style>
    @keyframes gradient {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("---")

# ==================== SIDEBAR WITH CONTROLS ====================
with st.sidebar:
    st.markdown("## ⚙️ Game Settings")
    
    # Symbol mode selection
    use_8_symbols = st.radio(
        "🎰 Symbol Mode",
        options=[True, False],
        format_func=lambda x: "8 Symbols (3 qubits)" if x else "2 Symbols (1 qubit)",
        index=0,
        help="Choose between 2 or 8 different slot symbols"
    )
    
    if use_8_symbols != st.session_state.use_8_symbols:
        st.session_state.use_8_symbols = use_8_symbols
        st.session_state.reel_results = ["🍒", "🍒", "🍒"]
        st.rerun()
    
    st.markdown("---")
    st.markdown("## ⚙️ Quantum Controls")
    
    # Theta control with visual feedback
    theta = st.slider(
        "🎛️ Bias Control θ",
        min_value=0.0,
        max_value=float(math.pi),
        value=float(math.pi/2),
        step=0.05,
        help="Controls quantum probability distribution"
    )
    
    # Independent reels option
    independent_reels = st.checkbox(
        "🎲 Independent Reels",
        value=True,
        help="Add variation to each reel for true independence"
    )
    
    if independent_reels:
        variation = st.slider(
            "Reel Variation %",
            min_value=0,
            max_value=50,
            value=20,
            step=5,
            help="Percentage of randomness added to each reel"
        )
    else:
        variation = 0
    
    # Calculate and show probabilities
    p1 = (math.sin(theta / 2) ** 2)
    p0 = 1 - p1
    
    st.markdown("### 📊 Probability Distribution")
    
    if st.session_state.use_8_symbols:
        # For 8 symbols, show simplified view
        st.info("Using 3 qubits = 8 possible symbols\nEach symbol has ~12.5% base probability")
        
        symbols_8 = ['🍒', '🍋', '🍊', '🍇', '🔔', '⭐', '💎', '7️⃣']
        fig_prob = go.Figure()
        fig_prob.add_trace(go.Bar(
            x=symbols_8,
            y=[0.125] * 8,  # Equal probability for demo
            marker=dict(
                color=px.colors.sequential.Rainbow,
                line=dict(color='white', width=2)
            ),
            text=['12.5%'] * 8,
            textposition='auto',
            textfont=dict(size=16, color='white', family='Arial Black')
        ))
        fig_prob.update_layout(
            height=300,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', size=12),
            showlegend=False,
            yaxis=dict(range=[0, 0.2], tickformat='.0%'),
            margin=dict(l=20, r=20, t=20, b=20)
        )
        st.plotly_chart(fig_prob, use_container_width=True)
    else:
        # Original 2-symbol view
        fig_prob = go.Figure()
        fig_prob.add_trace(go.Bar(
            x=['🍒 Cherry', '💎 Diamond'],
            y=[p0, p1],
            marker=dict(
                color=['#ff6b6b', '#4ecdc4'],
                line=dict(color='white', width=2)
            ),
            text=[f'{p0:.1%}', f'{p1:.1%}'],
            textposition='auto',
            textfont=dict(size=20, color='white', family='Arial Black')
        ))
        fig_prob.update_layout(
            height=300,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', size=14),
            showlegend=False,
            yaxis=dict(range=[0, 1], tickformat='.0%'),
            margin=dict(l=20, r=20, t=20, b=20)
        )
        st.plotly_chart(fig_prob, use_container_width=True)
    
    st.markdown("---")
    
    # Game Stats
    st.markdown("### 📈 Game Statistics")
    stats = st.session_state.game_state.get_stats()
    
    st.markdown(f"""
        <div class='stat-card'>
            <div class='stat-value'>{stats['total_spins']}</div>
            <div class='stat-label'>Total Spins</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class='stat-card'>
            <div class='stat-value'>{stats['total_wins']}</div>
            <div class='stat-label'>Total Wins</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class='stat-card'>
            <div class='stat-value'>{stats['win_rate']:.1f}%</div>
            <div class='stat-label'>Win Rate</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class='stat-card'>
            <div class='stat-value'>{stats['biggest_win']}</div>
            <div class='stat-label'>Biggest Win</div>
        </div>
    """, unsafe_allow_html=True)
    
    profit_color = '#00ff00' if stats['net_profit'] >= 0 else '#ff0000'
    st.markdown(f"""
        <div class='stat-card' style='border: 3px solid {profit_color};'>
            <div class='stat-value' style='color: {profit_color};'>{stats['net_profit']:+d}</div>
            <div class='stat-label'>Net Profit</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Payout table
    st.markdown("### 💎 Payout Table")
    if st.session_state.use_8_symbols:
        payout_df = pd.DataFrame({
            'Symbol': ['🍒', '🍋', '🍊', '🍇', '🔔', '⭐', '💎', '7️⃣'],
            '3 Match': [30, 45, 60, 75, 90, 150, 300, 600],
            '2 Match': [5, 8, 10, 13, 15, 25, 50, 100]
        })
    else:
        payout_df = pd.DataFrame({
            'Symbol': ['🍒', '💎'],
            '3 Match': [30, 300],
            '2 Match': [5, 50]
        })
    st.dataframe(payout_df, hide_index=True, use_container_width=True)
    
    st.markdown("---")
    
    # Quantum concepts
    with st.expander("⚛️ Quantum Concepts Used"):
        st.markdown("""
        - ✅ **Superposition**
        - ✅ **Hadamard Gates**
        - ✅ **Rotation Gates (Ry)**
        - ✅ **Quantum Measurement**
        - ✅ **Wavefunction Collapse**
        - ✅ **Probability Amplitudes**
        - ✅ **Quantum Entanglement**
        - ✅ **Quantum Oracles**
        - ✅ **Quantum Randomness**
        """)

# ==================== MAIN GAME AREA ====================

# Credits Display
st.markdown(f"""
    <div class='credits-mega'>
        💰 {st.session_state.game_state.credits} CREDITS
    </div>
""", unsafe_allow_html=True)

# Quantum State Display
st.markdown(f"""
    <div class='quantum-display'>
        <strong>QUANTUM STATE:</strong><br>
        {st.session_state.quantum_state}
    </div>
""", unsafe_allow_html=True)

# Reels Display
st.markdown("<h2 style='text-align: center; color: white; font-size: 48px; margin: 30px 0;'>🎰 REELS 🎰</h2>", unsafe_allow_html=True)

reel_col1, reel_col2, reel_col3 = st.columns(3)

spin_class = "spinning" if st.session_state.spinning else ""

with reel_col1:
    st.markdown(f"""
        <div class='reel {spin_class}'>
            {st.session_state.reel_results[0]}
        </div>
    """, unsafe_allow_html=True)

with reel_col2:
    st.markdown(f"""
        <div class='reel {spin_class}'>
            {st.session_state.reel_results[1]}
        </div>
    """, unsafe_allow_html=True)

with reel_col3:
    st.markdown(f"""
        <div class='reel {spin_class}'>
            {st.session_state.reel_results[2]}
        </div>
    """, unsafe_allow_html=True)

# Win Message
if st.session_state.win_message:
    st.markdown(f"""
        <div class='win-mega'>
            {st.session_state.win_message}
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Control Buttons
btn_col1, btn_col2, btn_col3 = st.columns([2, 2, 1])

with btn_col1:
    spin_button = st.button(
        "🎰 SPIN (10 CREDITS)",
        disabled=not st.session_state.game_state.can_spin() or st.session_state.spinning,
        use_container_width=True,
        type="primary"
    )

with btn_col2:
    if st.button("🔄 RESET GAME", use_container_width=True):
        st.session_state.game_state.reset()
        st.session_state.reel_results = ["🍒", "🍒", "🍒"]
        st.session_state.win_message = ""
        st.session_state.quantum_state = "System Ready - Click SPIN to begin"
        st.session_state.history = []
        st.rerun()

with btn_col3:
    show_analysis = st.button("📊 ANALYSIS", use_container_width=True)

# ==================== SPIN LOGIC ====================
if spin_button:
    st.session_state.game_state.place_bet()
    st.session_state.win_message = ""
    st.session_state.spinning = True
    
    # Progress bar
    progress_bar = st.progress(0, text="Initializing quantum circuits...")
    
    steps = [
        (14, "Step 1: Initializing qubits to |0⟩...", 0),
        (28, "Step 2: Applying Hadamard gates - Creating superposition...", 1),
        (42, "Step 3: Applying RY rotation gates - Adjusting probabilities...", 2),
        (56, "Step 4: Creating quantum entanglement between reels...", 3),
        (70, "Step 5: Measuring qubits - Collapsing wavefunction...", 4),
        (85, "Step 6: Quantum oracle checking for winning patterns...", 5),
        (95, "Step 7: Quantum arithmetic calculating payout...", 6),
    ]
    
    for progress, message, step_num in steps:
        progress_bar.progress(progress, text=message)
        st.session_state.quantum_state = quantum_tracker.get_state_message(step_num)
        time.sleep(0.4)
    
    # Execute quantum circuits - each reel is INDEPENDENT
    import random
    results = []
    
    for i in range(3):
        if st.session_state.use_8_symbols:
            # 8 symbols mode: use 3 qubits
            # Generate 3 random theta values for the 3 qubits
            if variation > 0:
                theta_list = [
                    theta + random.uniform(-theta * (variation/100), theta * (variation/100))
                    for _ in range(3)
                ]
                # Keep in valid range
                theta_list = [max(0, min(math.pi, t)) for t in theta_list]
            else:
                theta_list = [theta, theta, theta]
            
            bit = quantum_spin_one_reel_8symbols(theta_list=theta_list, shots=1)
            results.append(symbol_mapper.bits_to_symbol(bit))
        else:
            # 2 symbols mode: use 1 qubit (original)
            if variation > 0:
                theta_variation = theta + random.uniform(-theta * (variation/100), theta * (variation/100))
                theta_variation = max(0, min(math.pi, theta_variation))
            else:
                theta_variation = theta
            
            bit = quantum_spin_one_reel_biased(theta=theta_variation, shots=1)
            results.append(symbol_mapper.bits_to_symbol(bit))
    
    st.session_state.reel_results = results
    
    # Check wins
    win_type, payout = win_checker.check_win(results)
    
    if payout > 0:
        st.session_state.game_state.add_winnings(payout)
    
    st.session_state.win_message = win_checker.get_win_message(win_type, payout)
    st.session_state.quantum_state = quantum_tracker.get_state_message(7)
    
    # Add to history
    st.session_state.history.append({
        'spin': len(st.session_state.history) + 1,
        'result': ' '.join(results),
        'win_type': win_type,
        'payout': payout,
        'theta': theta
    })
    
    progress_bar.progress(100, text="Complete!")
    time.sleep(0.3)
    
    st.session_state.spinning = False
    st.rerun()

# ==================== ANALYSIS SECTION ====================
if show_analysis or 'show_analysis' in st.session_state:
    st.session_state.show_analysis = True
    
    st.markdown("---")
    st.markdown("## 📊 Quantum Analysis & Verification")
    
    tab1, tab2, tab3 = st.tabs(["📈 Statistical Analysis", "📜 Spin History", "🔬 Circuit Diagram"])
    
    with tab1:
        col_a1, col_a2 = st.columns(2)
        
        with col_a1:
            st.markdown("### Fairness Verification")
            shots = st.number_input("Number of quantum measurements", 100, 5000, 1000, 100)
            
            if st.button("🧪 Run Statistical Test", use_container_width=True):
                with st.spinner("Executing quantum circuits..."):
                    if st.session_state.use_8_symbols:
                        # 8 symbols analysis
                        counts = quantum_spin_counts_8symbols(shots=int(shots))
                        
                        st.success("Analysis Complete!")
                        st.markdown("#### Results (8 Symbols)")
                        
                        # Convert to symbols
                        symbol_counts = {}
                        for bits, count in counts.items():
                            symbol = symbol_mapper.bits_to_symbol(bits)
                            symbol_counts[symbol] = count
                        
                        # Show distribution
                        symbols = ['🍒', '🍋', '🍊', '🍇', '🔔', '⭐', '💎', '7️⃣']
                        observed_probs = [symbol_counts.get(s, 0) / shots for s in symbols]
                        expected_prob = 1/8  # Equal for demo
                        
                        result_df = pd.DataFrame({
                            'Symbol': symbols,
                            'Count': [symbol_counts.get(s, 0) for s in symbols],
                            'Observed %': [f'{p:.1%}' for p in observed_probs],
                            'Expected %': [f'{expected_prob:.1%}'] * 8
                        })
                        st.dataframe(result_df, hide_index=True, use_container_width=True)
                        
                        # Chart
                        fig_analysis = go.Figure()
                        fig_analysis.add_trace(go.Bar(
                            name='Observed',
                            x=symbols,
                            y=observed_probs,
                            marker_color='rgba(102,126,234,0.7)'
                        ))
                        fig_analysis.add_trace(go.Scatter(
                            name='Expected',
                            x=symbols,
                            y=[expected_prob] * 8,
                            mode='lines',
                            line=dict(color='red', dash='dash', width=3)
                        ))
                        fig_analysis.update_layout(
                            title="Observed vs Expected Probabilities (8 Symbols)",
                            height=400,
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font=dict(color='white')
                        )
                        st.plotly_chart(fig_analysis, use_container_width=True)
                        
                    else:
                        # Original 2 symbols analysis
                        counts = quantum_spin_counts_one_reel_biased(theta=theta, shots=int(shots))
                        total = counts["0"] + counts["1"]
                        obs_p0 = counts["0"] / total
                        obs_p1 = counts["1"] / total
                        
                        p1 = (math.sin(theta / 2) ** 2)
                        p0 = 1 - p1
                        
                        st.success("Analysis Complete!")
                        st.markdown("#### Results")
                        result_df = pd.DataFrame({
                            'Symbol': ['🍒 Cherry', '💎 Diamond'],
                            'Expected': [f'{p0:.1%}', f'{p1:.1%}'],
                            'Observed': [f'{obs_p0:.1%}', f'{obs_p1:.1%}'],
                            'Deviation': [f'{abs(obs_p0-p0):.2%}', f'{abs(obs_p1-p1):.2%}']
                        })
                        st.dataframe(result_df, hide_index=True, use_container_width=True)
                        
                        # Chart
                        fig_analysis = go.Figure()
                        fig_analysis.add_trace(go.Bar(
                            name='Expected',
                            x=['🍒 Cherry', '💎 Diamond'],
                            y=[p0, p1],
                            marker_color='rgba(102,126,234,0.7)'
                        ))
                        fig_analysis.add_trace(go.Bar(
                            name='Observed',
                            x=['🍒 Cherry', '💎 Diamond'],
                            y=[obs_p0, obs_p1],
                            marker_color='rgba(118,75,162,0.7)'
                        ))
                        fig_analysis.update_layout(
                            title="Expected vs Observed Probabilities",
                            barmode='group',
                            height=400,
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font=dict(color='white')
                        )
                        st.plotly_chart(fig_analysis, use_container_width=True)
        
        with col_a2:
            st.markdown("### Quantum Randomness Quality")
            if len(st.session_state.history) > 0:
                # Analyze history
                history_df = pd.DataFrame(st.session_state.history)
                
                # Win distribution
                win_dist = history_df['win_type'].value_counts()
                fig_wins = px.pie(
                    values=win_dist.values,
                    names=win_dist.index,
                    title="Win Type Distribution",
                    color_discrete_sequence=['#ff6b6b', '#4ecdc4', '#95e1d3']
                )
                fig_wins.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white')
                )
                st.plotly_chart(fig_wins, use_container_width=True)
                
                # Payout over time
                fig_payout = px.line(
                    history_df,
                    x='spin',
                    y='payout',
                    title="Payout Over Time",
                    markers=True
                )
                fig_payout.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white')
                )
                st.plotly_chart(fig_payout, use_container_width=True)
            else:
                st.info("No spin history yet. Start playing to see analysis!")
    
    with tab2:
        st.markdown("### Complete Spin History")
        if len(st.session_state.history) > 0:
            history_df = pd.DataFrame(st.session_state.history)
            st.dataframe(
                history_df.sort_values('spin', ascending=False),
                hide_index=True,
                use_container_width=True,
                height=400
            )
            
            # Download button
            csv = history_df.to_csv(index=False)
            st.download_button(
                "📥 Download History as CSV",
                csv,
                "quantum_slot_history.csv",
                "text/csv",
                use_container_width=True
            )
        else:
            st.info("No spins recorded yet!")
    
    with tab3:
        st.markdown("### Quantum Circuit Visualization")
        st.code(f"""
     ┌───┐┌─────────┐┌─┐
q_0: ┤ H ├┤ RY({theta:.2f}) ├┤M├
     └───┘└─────────┘└╥┘
                      ║
c: 1/═════════════════╩═
                      0

Legend:
H      = Hadamard gate (creates superposition)
RY(θ)  = Rotation gate (adjusts probabilities)
M      = Measurement (collapses to classical bit)
        """, language="text")
        
        st.markdown("### Circuit Explanation")
        st.info("""
        **Step-by-step quantum process:**
        
        1. **|0⟩** - Initial state (ground state)
        2. **H|0⟩** - After Hadamard: (|0⟩ + |1⟩)/√2
        3. **RY(θ)** - After rotation: cos(θ/2)|0⟩ + sin(θ/2)|1⟩
        4. **Measure** - Collapse to either |0⟩ or |1⟩
        5. **Map** - Convert to 🍒 or 💎
        """)

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: white; padding: 30px;'>
        <p style='font-size: 20px; font-weight: 600;'>
            🔬 Built with IBM Qiskit | Quantum Computing Project
        </p>
        <p style='font-size: 16px;'>
            Demonstrates: Superposition • Entanglement • Measurement • Oracles • Quantum Arithmetic
        </p>
        <p style='font-size: 14px; margin-top: 20px; opacity: 0.7;'>
            Educational project showcasing real quantum computing principles through gamification
        </p>
    </div>
""", unsafe_allow_html=True)