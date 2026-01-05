from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import math
import numpy as np

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


@dataclass
class SpinResult:
    reel_bits: List[str]
    reels: List[str]
    circuit: QuantumCircuit
    oracle_flag: Optional[str] = None  # '0' or '1' (only in oracle mode)


class QuantumSlotMachine:
    """
    Beginner-friendly quantum slot machine.

    Quantum part (per spin):
      1) Initialize qubits (implicitly |0...0>)
      2) Superposition: Hadamard on all qubits
      3) Bias: RY(theta) on all qubits (optionally varied)
      4) Optional entanglement: a few CNOTs to correlate reels
      5) Measure -> classical bitstring -> symbols

    Classical part:
      - detect wins (double/triple)
      - compute payout
    """

    def __init__(self, n_reels: int = 3, qubits_per_reel: int = 3, entangle: bool = True):
        self.n_reels = n_reels
        self.qubits_per_reel = qubits_per_reel
        self.total_qubits = n_reels * qubits_per_reel
        self.entangle = entangle
        self.oracle_symbols = {0: "🍒", 1: "💎"}

        self.backend = AerSimulator()

        # 3 bits -> 8 symbols
        self.symbols: Dict[int, str] = {
            0: "🍒", 1: "🍋", 2: "🍊", 3: "🍇",
            4: "🔔", 5: "⭐", 6: "💎", 7: "7️⃣"
        }

        # Base payout for triple match (you can tune later)
        self.base_payouts: Dict[str, int] = {
            "🍒": 10, "🍋": 15, "🍊": 20, "🍇": 25,
            "🔔": 30, "⭐": 50, "💎": 100, "7️⃣": 200
        }

    # --------------------------
    # Quantum circuit building
    # --------------------------

    def build_spin_circuit(
        self,
        theta_base: float = math.pi / 2,
        variation_pct: float = 0.0,
    ) -> QuantumCircuit:
        """
        Build a single circuit that produces 3 reels × 3 bits.

        theta_base controls probability bias.
        variation_pct adds small random per-qubit variation (optional).
        """
        qc = QuantumCircuit(self.total_qubits, self.total_qubits)

        # 1) Superposition
        for q in range(self.total_qubits):
            qc.h(q)
        qc.barrier(label="H (superposition)")

        # 2) Bias via RY(theta)
        thetas = []
        for _ in range(self.total_qubits):
            if variation_pct > 0:
                delta = np.random.uniform(-theta_base * variation_pct/100, theta_base * variation_pct/100)
                theta = float(np.clip(theta_base + delta, 0.0, math.pi))
            else:
                theta = float(theta_base)
            thetas.append(theta)

        for q, th in enumerate(thetas):
            qc.ry(th, q)
        qc.barrier(label="RY (bias)")

        # 3) Optional entanglement (simple and explainable)
        if self.entangle:
            # Entangle the *first qubit* of reel 0 with first qubits of reel 1 and 2
            # This creates some correlation between reels without making the circuit huge.
            qc.cx(0, self.qubits_per_reel)                 # reel0 q0 -> reel1 q0
            qc.cx(0, 2 * self.qubits_per_reel)             # reel0 q0 -> reel2 q0
            qc.barrier(label="CNOT (entangle reels)")

        # 4) Measure all qubits
        qc.measure(range(self.total_qubits), range(self.total_qubits))
        return qc

    def run_spin(
        self,
        theta_base: float = math.pi / 2,
        variation_pct: float = 0.0,
    ) -> SpinResult:
        """
        Execute one spin and return reel bitstrings + symbols + circuit.
        """
        qc = self.build_spin_circuit(theta_base=theta_base, variation_pct=variation_pct)

        job = self.backend.run(qc, shots=1, memory=True)
        raw = job.result().get_memory()[0]  # e.g. "010011101..."

        # Important: Qiskit memory bit ordering can be confusing.
        # Since we measured qubit i into classical bit i, we’ll reverse to align index 0 with qubit 0.
        bitstring = raw[::-1]

        reel_bits: List[str] = []
        reels: List[str] = []

        for r in range(self.n_reels):
            start = r * self.qubits_per_reel
            end = start + self.qubits_per_reel
            bits = bitstring[start:end]
            reel_bits.append(bits)

            idx = int(bits, 2)  # 0..7
            reels.append(self.symbols[idx])

        return SpinResult(reel_bits=reel_bits, reels=reels, circuit=qc)

    # --------------------------
    # Classical win + payout
    # --------------------------

    def check_win(self, reels: List[str]) -> Tuple[str, int]:
        """
        Returns (win_type, payout).
        win_type: 'triple', 'double', 'none'
        payout: credits won
        """
        a, b, c = reels

        if a == b == c:
            base = self.base_payouts.get(a, 10)
            return "triple", base * 3

        # any two match
        if a == b or b == c or a == c:
            if a == b:
                sym = a
            elif b == c:
                sym = b
            else:
                sym = a
            base = self.base_payouts.get(sym, 10)
            return "double", max(base // 2, 5)

        return "none", 0

    def run_spin_with_oracle_demo(
        self,
        theta_base: float = math.pi / 2,
        variation_pct: float = 0.0,
    ) -> SpinResult:
        """
        ORACLE DEMO MODE (Beginner-friendly):
          - 3 reels = 3 qubits (1 qubit per reel)
          - ancilla qubit 'win_flag' = 1 iff all three reels match (000 or 111)
          - reels are still measured normally, plus the oracle flag is measured.
        """

        reel_qubits = 3
        flag = 3
        total_qubits = 4

        qc = QuantumCircuit(total_qubits, total_qubits)

        # 1) Superposition + Bias
        for q in range(reel_qubits):
            qc.h(q)
        qc.barrier(label="H")

        for q in range(reel_qubits):
            if variation_pct > 0:
                delta = np.random.uniform(
                    -theta_base * variation_pct / 100,
                    theta_base * variation_pct / 100
                )
                theta = float(np.clip(theta_base + delta, 0.0, math.pi))
            else:
                theta = float(theta_base)
            qc.ry(theta, q)
        qc.barrier(label="RY")

        # 2) ORACLE: set flag=1 iff q0 == q1 == q2
        qc.cx(0, 1)
        qc.cx(0, 2)
        qc.x(1)
        qc.x(2)
        qc.ccx(1, 2, flag)
        qc.x(1)
        qc.x(2)
        qc.cx(0, 1)
        qc.cx(0, 2)
        qc.barrier(label="Oracle: all-equal flag")

        # 3) Measurement
        qc.measure(range(total_qubits), range(total_qubits))

        job = self.backend.run(qc, shots=1, memory=True)
        raw = job.result().get_memory()[0]
        bitstring = raw[::-1]

        reel_bits = [bitstring[0], bitstring[1], bitstring[2]]
        reels = [self.oracle_symbols[int(b)] for b in reel_bits]
        oracle_flag = bitstring[3]

        return SpinResult(
            reel_bits=reel_bits,
            reels=reels,
            circuit=qc,
            oracle_flag=oracle_flag
        )

    def oracle_demo_payout(self, oracle_flag: str) -> int:
        """Simple payout rule for oracle demo."""
        return 50 if oracle_flag == "1" else 0


