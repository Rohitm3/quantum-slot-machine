from typing import Dict, List, Optional, Tuple
import math
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

class SpinResult:
    def __init__(self, reel_bits: List[str], reels: List[str], circuit: QuantumCircuit, oracle_flag: Optional[str] = None):
        self.reel_bits = reel_bits
        self.reels = reels
        self.circuit = circuit
        self.oracle_flag = oracle_flag 

class QuantumSlotMachine:
    def __init__(self, n_reels: int = 3, qubits_per_reel: int = 3, entangle: bool = True):
        self.n_reels = n_reels
        self.qubits_per_reel = qubits_per_reel
        self.total_qubits = n_reels * qubits_per_reel
        self.entangle = entangle
        
        # Oracle mode uses 1 qubit per reel, so it only has 2 possible states (0 or 1)
        self.oracle_symbols = {0: "🍒", 1: "💎"}
        self.backend = AerSimulator()

        # normal mode symbols
        self.symbols: Dict[int, str] = {
            0: "🍒", 1: "🍋", 2: "🍊", 3: "🍇",
            4: "🔔", 5: "⭐", 6: "💎", 7: "7️⃣"
        }

        # base payouts for calculations
        self.base_payouts: Dict[str, int] = {
            "🍒": 10, "🍋": 15, "🍊": 20, "🍇": 25,
            "🔔": 30, "⭐": 50, "💎": 100, "7️⃣": 200
        }

    def _get_quantum_random_bit(self) -> int:
       
        # Quantum random-bit sampling from a local Qiskit Aer simulator, not quantum hardware
        qrng_qc = QuantumCircuit(1, 1)
        qrng_qc.h(0) 
        qrng_qc.measure(0, 0)
        #executing a quick quantum flip to check the variation is actually random
        result = self.backend.run(qrng_qc, shots=1, memory=True).result()
        return int(result.get_memory()[0])

    def build_spin_circuit(self, angle_val: float = math.pi / 2, variation_pct: float = 0.0) -> QuantumCircuit:
        # 9 qubits total (3 for each reel)
        qc = QuantumCircuit(self.total_qubits, self.total_qubits)
        
        # superposition start
        for q in range(self.total_qubits):
            qc.h(q)
        qc.barrier(label="H")

        # applying the rotation (Bias)
        angles = []
        for _ in range(self.total_qubits):
            if variation_pct > 0:
                # using Quantum bit to decide if we shift left or right
                q_bit = self._get_quantum_random_bit()
                direction = 1 if q_bit == 1 else -1
                
                delta = (angle_val * variation_pct/100) * direction
                theta = float(np.clip(angle_val + delta, 0.0, math.pi))
            else:
                theta = float(angle_val)
            angles.append(theta)

        for q, th in enumerate(angles):
            qc.ry(th, q)
        qc.barrier(label="RY")

        # entanglement logic, CNOT gates to link the reels together
        if self.entangle:
            qc.cx(0, self.qubits_per_reel)
            qc.cx(0, 2 * self.qubits_per_reel)
            qc.barrier(label="CNOT")

        qc.measure(range(self.total_qubits), range(self.total_qubits))
        return qc

    def run_spin(self, angle_val: float = math.pi / 2, variation_pct: float = 0.0) -> SpinResult:
        qc = self.build_spin_circuit(angle_val, variation_pct)
        job = self.backend.run(qc, shots=1, memory=True)
        raw = job.result().get_memory()[0]
        bitstring = raw[::-1] # flip because qiskit order

        reel_bits = []
        reels = []
        for r in range(self.n_reels):
            start = r * self.qubits_per_reel
            end = start + self.qubits_per_reel
            bits = bitstring[start:end]
            reel_bits.append(bits)
            idx = int(bits, 2)
            reels.append(self.symbols[idx])
        return SpinResult(reel_bits=reel_bits, reels=reels, circuit=qc)

    def check_win(self, reels: List[str]) -> Tuple[str, int]:
        # scoring logic
        a, b, c = reels
        if a == b == c:
            base = self.base_payouts.get(a, 10)
            return "triple", base * 2 
        if a == b or b == c or a == c:
            sym = a if a==b or a==c else b
            base = self.base_payouts.get(sym, 10)
            return "double", base
        return "none", 0

    def run_spin_with_oracle_demo(self, angle_val: float = math.pi / 2, variation_pct: float = 0.0) -> Tuple[SpinResult, str, int]:
        """Run a three-reel oracle demonstration.

        Each reel has one qubit (two symbols). Variation perturbs each reel's
        RY angle, matching the slider behaviour of normal spin mode.
        """
        qc = QuantumCircuit(4, 4)

        for q in range(3):
            theta = float(angle_val)
            if variation_pct > 0:
                direction = 1 if self._get_quantum_random_bit() else -1
                delta = angle_val * (variation_pct / 100.0) * direction
                theta = float(np.clip(angle_val + delta, 0.0, math.pi))
            qc.ry(theta, q)

        qc.barrier(label="Reels")
        # XOR each reel with reel 0, flag equality, then uncompute the XORs.
        qc.cx(0, 1)
        qc.cx(0, 2)
        qc.x(1)
        qc.x(2)
        qc.ccx(1, 2, 3)
        qc.x(1)
        qc.x(2)
        qc.cx(0, 1)
        qc.cx(0, 2)
        qc.barrier(label="Oracle")
        qc.measure(range(4), range(4))

        job = self.backend.run(qc, shots=1, memory=True)
        raw = job.result().get_memory()[0]
        bitstring = raw[::-1]
        reel_bits = [bitstring[0], bitstring[1], bitstring[2]]
        reels = [self.oracle_symbols[int(b)] for b in reel_bits]
        oracle_flag = bitstring[3]
        win_type, payout = self.check_win(reels)
        return SpinResult(
            reel_bits=reel_bits, reels=reels,
            circuit=qc, oracle_flag=oracle_flag
        ), win_type, payout
