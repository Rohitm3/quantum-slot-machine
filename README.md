# Quantum Slot Machine 🎰

An interactive **educational simulation** built with Python, Qiskit Aer and Streamlit for coursework in **Quantum Computation and Error Correction** at the University of Basel (2025–2026).

This was a **collaborative student project**, not a commercial application. It runs quantum circuits on a **classical simulator**, not quantum hardware, and uses virtual game credits only.

## Application preview

![Actual Quantum Slot Machine application screenshot](assets/Quantum%20Slot%20Machine%20%E2%80%94%20Actual%20Application%20Screenshot.png)

*Actual screenshot of the Streamlit application running locally.*

## What it demonstrates

- **Superposition:** Hadamard gates prepare possible measurement outcomes.
- **Probability controls:** RY rotation angles influence the distribution of measured symbols.
- **Entanglement:** CNOT gates connect selected qubits in normal spin mode.
- **Measurement:** Three groups of three measured bits map to eight possible symbols per reel.
- **Oracle demonstration:** A separate, simplified three-qubit reel circuit uses CNOT and CCX (Toffoli) gates with an ancilla flag to mark three matching outcomes; this mode uses two symbols per reel.
- **Game state:** Bets, virtual credits, payouts, session statistics and spin history.

The **Bias (θ)** and **Variation (%)** controls affect reel rotations. Variation is sampled using a *simulated* quantum bit; this is not a claim of hardware-generated true randomness.

## Project structure

```text
app/
  quantum_slot_machine.py  # Streamlit user interface
  quantum_logic.py         # Qiskit circuit building, simulation, payout checks
  game_logic.py            # Virtual credits, bets and statistics
tests/
  test_slot_machine.py     # Basic regression and circuit checks
requirements.txt
requirements-dev.txt
```

## Run locally

Use a suitable Python 3 environment (the project was originally developed on Python 3.11).

```bash
git clone https://github.com/Rohitm3/quantum-slot-machine.git
cd quantum-slot-machine
python -m venv .venv
# Activate .venv for your operating system
python -m pip install -r requirements.txt
python -m streamlit run app/quantum_slot_machine.py
```

This repository is currently private while being prepared for portfolio publication. Use an authorized GitHub account to clone it.

## Run the tests

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

Tests cover game credits and reset, payouts, measurement circuits, the oracle flag, and controlled variation angles. Statistical output will vary between runs.

## Known limitations

- This is a teaching/demo application, not a scientifically validated quantum advantage experiment.
- The Qiskit Aer backend is a *classical simulator*, not a quantum computer.
- The oracle demo deliberately uses a reduced two-symbol representation.
- The project currently has a basic local test suite; it has not undergone production security, accessibility or performance validation.
- Dependency versions were not pinned in the original project; environment compatibility should be verified before a public release.

## Contributors and attribution

**Rohit Mohite and Afzonia** — collaborators on this academic coursework project for *Quantum Computation and Error Correction* at the University of Basel (2025–2026).

This README reflects portfolio-preparation updates and should not be presented as the original submitted coursework documentation.

## Publication status

The repository remains private while publication permissions, attribution, installation and test execution are confirmed. No open-source license is specified yet; please do not assume the absence of a license grants reuse rights.
