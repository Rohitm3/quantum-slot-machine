from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def quantum_spin_one_reel(shots: int = 1) -> str:
    """
    1-qubit 'slot reel' spin:
    - Start in |0>
    - Apply H to create superposition
    - Measure -> returns '0' or '1' as the symbol
    """
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    qc.measure(0, 0)

    backend = AerSimulator()
    job = backend.run(qc, shots=shots, memory=True)
    # memory gives list like ['0'] or ['1']
    result = job.result().get_memory()[0]
    return result

import math
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def quantum_spin_one_reel_biased(theta: float, shots: int = 1) -> str:
    """
    1-qubit biased spin using RY(theta).
    theta in radians.
    P(1) = sin^2(theta/2), P(0) = cos^2(theta/2)
    """
    qc = QuantumCircuit(1, 1)
    qc.ry(theta, 0)
    qc.measure(0, 0)

    backend = AerSimulator()
    job = backend.run(qc, shots=shots, memory=True)
    result = job.result().get_memory()[0]
    return result

def quantum_spin_counts_one_reel_biased(theta: float, shots: int = 200) -> dict:
    """
    Run the 1-qubit biased spin for many shots and return counts, e.g. {'0': 83, '1': 117}.
    """
    qc = QuantumCircuit(1, 1)
    qc.ry(theta, 0)
    qc.measure(0, 0)

    backend = AerSimulator()
    job = backend.run(qc, shots=shots)
    counts = job.result().get_counts(qc)
    # Ensure both keys exist
    counts.setdefault('0', 0)
    counts.setdefault('1', 0)
    return counts
