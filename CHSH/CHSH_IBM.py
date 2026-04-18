import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler

# Original set from lab
ANGLES = [
    (0, np.pi/8),        # (0°, 22.5°)
    (0, 3*np.pi/8),     # (0°, 67.5°)
    (np.pi/4, np.pi/8), # (45°, 22.5°)
    (np.pi/4, 3*np.pi/8) # (45°, 67.5°)
]

# backend
BACKEND = {"b": 'ibm_brisbane', "s": 'ibm_sherbrooke', "a": 'ibm_aachen'}["s"]

# Number of shots for each circuit run
NUM_SHOTS = 1000

def run_on_simulator(shots=NUM_SHOTS):
    # Step 1: Set up the simulator
    simulator = AerSimulator()
    print("Running on simulator:", simulator.name)
    print(f"Number of shots: {shots}")

    # Step 2: Create and run circuits
    expectation_values = []
    for theta1, theta2 in ANGLES:
        # Create a new circuit for each angle pair
        qc = QuantumCircuit(2, 2)
        # prepare a Bell state
        qc.h(0)
        qc.cx(0, 1)
        # rotate measurement basis
        qc.ry(-2*theta1, 0)
        qc.ry(-2*theta2, 1)
        # measure qubits, map it to classical bits
        qc.measure_all()

        job = simulator.run(qc, shots=shots)
        result = job.result()
        counts = result.get_counts()

        # calculate expectation value from counts using parity
        expectation = 0
        for outcome, count in counts.items():
            # outcome[0] is qubit0’s bit, outcome[1] is qubit1’s bit
            parity = (-1) ** (int(outcome[0]) + int(outcome[1]))
            expectation += parity * count
        expectation /= shots
        expectation_values.append(expectation)

        # RS: calculate expectation E out of the counts C_ab which are in `count`
        
    # Step 4: Compute and print CHSH value
    S = expectation_values[0] - expectation_values[1] + expectation_values[2] + expectation_values[3]    
    print(f"CHSH S-value: {S:.16f}")



def run_on_hardware(shots=NUM_SHOTS):

    QiskitRuntimeService.save_account(
    channel="ibm_quantum_platform",
    token="REuO5aqS1vGVBFoNr5YmR57MYtYpMeFgcDsFJKKHOQYO",
    instance="ibm-q/open/main",
    overwrite=True,
    set_as_default=True
    )
    print("Saved account successfully.")
 
    # Step 1: Connect to IBM Quantum
    try:
        service = QiskitRuntimeService()
        print([backend.name for backend in service.backends()])  # See which backends are available 
        backend = service.backend(BACKEND)
    except Exception as e:
        print("Error connecting to IBM Quantum:", e)
        exit()

    print("Running on hardware:", backend.name)
    print(f"Number of shots: {shots}")
    print("Total jobs in queue for", backend.name, ":", backend.status().pending_jobs)

    # Step 2: Create circuits
    circuits = []
    for theta1, theta2 in ANGLES:
        qc = QuantumCircuit(2, 2)
        qc.h(0)
        qc.cx(0, 1)
        qc.ry(-2 * theta1, 0)
        qc.ry(-2 * theta2, 1)
        # use measure_all() just like the simulator version
        qc.measure_all()
        circuits.append(qc)

    # Step 3: Transpile circuits to match hardware gates
    transpiled = transpile(circuits, backend=backend, optimization_level=1)

    # Step 4: Set up the Sampler for hardware
    sampler = Sampler(mode=backend)
    sampler.options.default_shots = shots
    job = sampler.run(transpiled)
    print("Job ID:", job.job_id())
    result = job.result()

    # Step 6: Calculate expectation values from results
    expectation_values = []
    for i in range(len(ANGLES)):
        # Get counts from the result (Sampler returns a list of PubResults)
        data = result[i].data
        counts = data.meas.get_counts()  # 'meas' is the classical register name from measure_all()

        # Calculate expectation value
        total_shots = sum(counts.values())
        expectation = 0
        for outcome, count in counts.items():
            # Parity: +1 for '00' or '11', -1 for '01' or '10'
            parity = (-1) ** (int(outcome[0]) + int(outcome[1]))
            expectation += parity * count
        expectation = expectation / total_shots
        expectation_values.append(expectation)

    # Step 6: CHSH combination, same sign convention as the simulator
    S = expectation_values[0] - expectation_values[1] + expectation_values[2] + expectation_values[3]
    print(f"CHSH S-value: {S:.16f}")


if __name__ == "__main__":
    print("angles:", ANGLES)
    run_on_simulator()
    # run_on_hardware()
    print("2√2 = ", np.sqrt(2)*2)
    