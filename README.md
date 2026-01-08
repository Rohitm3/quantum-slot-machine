# Quantum Slot Machine 🎰

An interactive slot machine game built using **quantum computing concepts**, designed as an educational prototype for the Quantum Computing course.

The game uses real quantum circuit logic (simulated via Qiskit) to generate slot outcomes, demonstrating ideas such as **superposition**, **probabilistic measurement**, and a simple **quantum oracle**.

---

## Project Motivation

This project was created to explore how quantum computing can be used **inside application logic**, rather than only for random number generation.

By turning quantum concepts into a familiar game (a slot machine), the project aims to:
- Make quantum mechanics more intuitive
- Bridge theory and practical implementation
- Provide a hands-on, interactive learning experience

---

## 🎮 How the Game Works (High Level)

- Each **reel** of the slot machine is generated using a **quantum circuit**
- Qubits are placed into **superposition**
- Rotation gates control **probabilities**
- Measurement collapses the quantum state into classical symbols
- A **quantum oracle mode** demonstrates how a quantum circuit can flag winning states

---

## 🧠 Quantum Concepts Used

### Superposition
Each reel starts in a superposition of possible symbols.

### Quantum Measurement
When the circuit is measured, the superposition collapses into a concrete result.

### Probability Control
A rotation gate (RY) biases the probability distribution of outcomes.

### Quantum Oracle (Demo Mode)
In Oracle Demo Mode:
- A special quantum circuit checks whether all reels match
- An ancilla “flag” qubit is set to `1` if a winning condition is detected
- This demonstrates how **oracles mark solutions without classical comparison**

---

## 🕹️ Controls Explained

### Bias (θ)
- Controls the probability distribution of outcomes
- Higher values bias the result toward certain symbols

### Variation (%)
- Adds small random fluctuations to the bias
- Simulates noise and uncertainty

### Oracle Demo Mode
- Enables a simplified quantum oracle
- Winning states are detected directly in the quantum circuit

### SPIN Button
- Places a bet
- Runs the quantum circuit
- Displays the measured outcome

---

## 🧾 Project Structure

.
├── app.py              # Streamlit UI and game flow
├── quantum_logic.py    # Quantum circuits and oracle logic
├── game_logic.py       # Game state, credits, statistics
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation


## ▶️ How to Run the Project

### Prerequisites
- Python 3.9 or newer
- pip (Python package manager)

### 1. Install Dependencies
From the project root directory, run:
pip install -r requirements.txt

Run the Streamlit app with: streamlit run app.py
