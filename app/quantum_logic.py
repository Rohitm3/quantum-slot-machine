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
