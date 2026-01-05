# Quantum Slot Machine 🎰⚛️  
A simple, interactive game that demonstrates core quantum computing concepts using Qiskit.

This project is designed as a beginner-friendly prototype for a university Quantum Computing final project (Industry grading scheme).  
The goal is to show *real quantum concepts inside gameplay logic*, not just “random numbers”.

---

## What the game does

- You press **SPIN**
- A **quantum circuit** runs (simulated with Qiskit Aer)
- The circuit creates:
  - **Superposition** using Hadamard gates (H)
  - **Controlled probability bias** using rotation gates (RY(θ))
  - **Optional correlations** between reels using entanglement (CNOT)
- The circuit is **measured**, producing classical bits
- Bits are mapped to slot symbols (🍒 🍋 ⭐ 💎 7️⃣ etc.)
- Win detection and payout are handled in simple, transparent classical logic

---

## Repo structure

quantum-slot-machine/
│
├── app/
│ ├── app.py # Streamlit UI (main entry point)
│ ├── quantum_logic.py # Qiskit circuits + symbol mapping
│ ├── game_logic.py # Credits, bet handling, stats
│
├── assets/
│ └── screenshots/ # Screenshots for report/presentation
│
├── report/ # Individual reports / abstract / notes
│
├── requirements.txt
└── README.md


---

## Prerequisites

- Python **3.9+**
- Git (optional, but recommended)
- Works on **Windows** and **macOS**

Check Python version:
```bash
python --version
# or on macOS:
python3 --version
