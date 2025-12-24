from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import Aer
from qiskit.visualization import circuit_drawer
import numpy as np


class QuantumSlotLogic:
    """
    Handles all quantum operations for the slot machine
    """
    
    def __init__(self, n_qubits_per_reel=3):
        """
        Step 1: Initialize quantum backend
        
        Args:
            n_qubits_per_reel: Number of qubits per reel
                              1 qubit = 2 symbols
                              2 qubits = 4 symbols
                              3 qubits = 8 symbols (default)
        """
        self.backend = Aer.get_backend('qasm_simulator')
        self.n_qubits_per_reel = n_qubits_per_reel
        
    def create_circuit_step1_initialization(self):
        """
        STEP 1: Quantum State Initialization
        Create quantum circuit with qubits in |0⟩ ground state
        """
        qr = QuantumRegister(self.n_qubits_per_reel, 'q')
        cr = ClassicalRegister(self.n_qubits_per_reel, 'c')
        qc = QuantumCircuit(qr, cr)
        
        return qc
    
    def apply_step2_superposition(self, qc):
        """
        STEP 2: Create Superposition
        Apply Hadamard gates to all qubits
        Creates equal superposition of all possible states
        """
        for i in range(self.n_qubits_per_reel):
            qc.h(i)
        qc.barrier()
        
        return qc
    
    def apply_step3_rotation(self, qc, theta_list=None):
        """
        STEP 3: Probability Weighting
        Apply RY rotation gates to adjust probability amplitudes
        
        Args:
            theta_list: List of rotation angles for each qubit
                       If None, uses random rotations
        """
        if theta_list is None:
            theta_list = [np.random.uniform(0, np.pi) for _ in range(self.n_qubits_per_reel)]
        
        for i, theta in enumerate(theta_list):
            qc.ry(theta, i)
        qc.barrier()
        
        return qc
    
    def apply_step4_measurement(self, qc):
        """
        STEP 4: Quantum Measurement
        Measure all qubits and collapse wavefunction to classical bits
        """
        for i in range(self.n_qubits_per_reel):
            qc.measure(i, i)
        
        return qc
    
    def execute_circuit(self, qc, shots=1):
        """
        STEP 5: Execute Quantum Circuit
        Run the circuit on quantum simulator
        """
        job = self.backend.run(qc, shots=shots)
        result = job.result()
        counts = result.get_counts(qc)
        
        return counts


# ==================== 8-SYMBOL FUNCTIONS ====================

def quantum_spin_one_reel_8symbols(theta_list=None, shots=1):
    """
    Complete quantum spin for one reel with 8 symbols
    Uses 3 qubits to generate 8 possible outcomes
    
    Args:
        theta_list: List of 3 rotation angles [θ1, θ2, θ3]
        shots: Number of measurements
        
    Returns:
        String: 3-bit string like "000", "001", "010", etc.
    """
    quantum_logic = QuantumSlotLogic(n_qubits_per_reel=3)
    
    # Step 1: Initialize
    qc = quantum_logic.create_circuit_step1_initialization()
    
    # Step 2: Superposition
    qc = quantum_logic.apply_step2_superposition(qc)
    
    # Step 3: Rotation (probability weighting)
    qc = quantum_logic.apply_step3_rotation(qc, theta_list)
    
    # Step 4: Measurement
    qc = quantum_logic.apply_step4_measurement(qc)
    
    # Step 5: Execute
    counts = quantum_logic.execute_circuit(qc, shots=shots)
    
    # Return most common result
    if shots == 1:
        return list(counts.keys())[0]
    else:
        return max(counts, key=counts.get)


def quantum_spin_counts_8symbols(theta_list=None, shots=100):
    """
    Get frequency counts for 8-symbol quantum measurements
    
    Args:
        theta_list: List of 3 rotation angles
        shots: Number of measurements
        
    Returns:
        Dictionary with counts: {"000": count, "001": count, ...}
    """
    quantum_logic = QuantumSlotLogic(n_qubits_per_reel=3)
    
    # Create complete circuit
    qc = quantum_logic.create_circuit_step1_initialization()
    qc = quantum_logic.apply_step2_superposition(qc)
    qc = quantum_logic.apply_step3_rotation(qc, theta_list)
    qc = quantum_logic.apply_step4_measurement(qc)
    
    # Execute multiple times
    counts = quantum_logic.execute_circuit(qc, shots=shots)
    
    # Ensure all 8 keys exist
    result = {f"{i:03b}": 0 for i in range(8)}
    result.update(counts)
    
    return result


# ==================== BACKWARDS COMPATIBILITY (2 symbols) ====================

def quantum_spin_one_reel_biased(theta, shots=1):
    """
    Original 2-symbol version (backwards compatible)
    Uses 1 qubit
    """
    quantum_logic = QuantumSlotLogic(n_qubits_per_reel=1)
    
    qc = quantum_logic.create_circuit_step1_initialization()
    qc = quantum_logic.apply_step2_superposition(qc)
    qc = quantum_logic.apply_step3_rotation(qc, [theta])
    qc = quantum_logic.apply_step4_measurement(qc)
    
    counts = quantum_logic.execute_circuit(qc, shots=shots)
    
    if shots == 1:
        return list(counts.keys())[0]
    else:
        return max(counts, key=counts.get)


def quantum_spin_counts_one_reel_biased(theta, shots=100):
    """
    Original 2-symbol statistical version (backwards compatible)
    """
    quantum_logic = QuantumSlotLogic(n_qubits_per_reel=1)
    
    qc = quantum_logic.create_circuit_step1_initialization()
    qc = quantum_logic.apply_step2_superposition(qc)
    qc = quantum_logic.apply_step3_rotation(qc, [theta])
    qc = quantum_logic.apply_step4_measurement(qc)
    
    counts = quantum_logic.execute_circuit(qc, shots=shots)
    
    result = {"0": 0, "1": 0}
    result.update(counts)
    
    return result


# ==================== ADVANCED FEATURES ====================

class QuantumSlotAdvanced:
    """
    Advanced quantum features: Entanglement, Multi-reel, Oracles
    Now supports 8 symbols per reel
    """
    
    def __init__(self, n_reels=3, n_qubits_per_reel=3):
        """
        Initialize with multiple reels and configurable qubits
        """
        self.backend = Aer.get_backend('qasm_simulator')
        self.n_reels = n_reels
        self.n_qubits_per_reel = n_qubits_per_reel
        self.total_qubits = n_reels * n_qubits_per_reel
    
    def create_entangled_reels_circuit(self, theta_list=None):
        """
        Create entangled circuit for multiple reels
        Uses CNOT gates to create quantum correlations
        """
        qr = QuantumRegister(self.total_qubits, 'q')
        cr = ClassicalRegister(self.total_qubits, 'c')
        qc = QuantumCircuit(qr, cr)
        
        # Apply superposition to all qubits
        for i in range(self.total_qubits):
            qc.h(i)
        
        qc.barrier()
        
        # Apply rotations
        if theta_list is None:
            theta_list = [np.random.uniform(0, np.pi) for _ in range(self.total_qubits)]
        
        for i, theta in enumerate(theta_list):
            qc.ry(theta, i)
        
        qc.barrier()
        
        # Create entanglement between reels
        # Entangle first qubit of each reel with first qubit of next reel
        for reel in range(self.n_reels - 1):
            control_qubit = reel * self.n_qubits_per_reel
            target_qubit = (reel + 1) * self.n_qubits_per_reel
            qc.cx(control_qubit, target_qubit)
        
        qc.barrier()
        
        # Measure all qubits
        for i in range(self.total_qubits):
            qc.measure(i, i)
        
        return qc
    
    def spin_three_reels_8symbols(self, theta_list=None):
        """
        Spin 3 reels with 8 symbols each
        
        Returns:
            List of 3 measurement results (3-bit strings)
        """
        qc = self.create_entangled_reels_circuit(theta_list)
        
        job = self.backend.run(qc, shots=1)
        result = job.result()
        counts = result.get_counts(qc)
        
        # Get the result (9-bit string for 3 reels × 3 qubits)
        bitstring = list(counts.keys())[0]
        
        # Split into 3 reels
        reel_results = []
        for i in range(self.n_reels):
            start = i * self.n_qubits_per_reel
            end = start + self.n_qubits_per_reel
            reel_bits = bitstring[start:end]
            reel_results.append(reel_bits)
        
        return reel_results


# ==================== CIRCUIT VISUALIZATION ====================

def get_circuit_diagram_8symbols(theta_list=None):
    """
    Generate text representation of 3-qubit circuit
    """
    quantum_logic = QuantumSlotLogic(n_qubits_per_reel=3)
    qc = quantum_logic.create_circuit_step1_initialization()
    qc = quantum_logic.apply_step2_superposition(qc)
    qc = quantum_logic.apply_step3_rotation(qc, theta_list)
    qc = quantum_logic.apply_step4_measurement(qc)
    
    return str(qc.draw(output='text'))


# ==================== TESTING ====================

if __name__ == "__main__":
    print("=" * 60)
    print("QUANTUM SLOT MACHINE - 8 SYMBOLS TEST")
    print("=" * 60)
    
    # Test 1: Single 8-symbol spin
    print("\n[TEST 1] 8-Symbol Quantum Spin:")
    result = quantum_spin_one_reel_8symbols(shots=1)
    print(f"Measurement result (3 bits): {result}")
    print(f"Decimal value: {int(result, 2)}")
    
    # Test 2: Statistical analysis
    print("\n[TEST 2] Statistical Analysis (1000 shots):")
    counts = quantum_spin_counts_8symbols(shots=1000)
    print("Distribution of 8 symbols:")
    for bits, count in sorted(counts.items()):
        symbol_num = int(bits, 2)
        percentage = count / 1000 * 100
        print(f"  {bits} (symbol {symbol_num}): {count:4d} times ({percentage:5.1f}%)")
    
    # Test 3: Three reels with 8 symbols
    print("\n[TEST 3] Three Reels (8 symbols each):")
    advanced = QuantumSlotAdvanced(n_reels=3, n_qubits_per_reel=3)
    results = advanced.spin_three_reels_8symbols()
    print(f"Reel results: {results}")
    print(f"As decimal: {[int(r, 2) for r in results]}")
    
    # Test 4: Circuit diagram
    print("\n[TEST 4] 3-Qubit Circuit Diagram:")
    print(get_circuit_diagram_8symbols())
    
    print("\n" + "=" * 60)
    print("All tests completed!")
    print("=" * 60)