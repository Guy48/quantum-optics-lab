# Quantum Optics Lab

This repository was created to document and analyze quantum optics lab experiments in a clear and reproducible way, combining: theoretical modeling, experimental measurement data, and quantum hardware execution where applicable.

This repository contains Python code used to analyze and reproduce three quantum optics lab experiments:
- **CHSH** Bell inequality test
- **Hong–Ou–Mandel (HOM)** interference experiment
- **Quantum state tomography (TOM)**

Each experiment has its own directory, and each directory includes the `.xlsx` file with the actual lab measurements used in the analysis.

## Repository Contents

```
/quantum-optics
│   README.md 
├───CHSH
│   │   CHSH_computational.py
│   │   CHSH_IBM.py
│   │   CHSH_measurements.xlsx
│   │   
│   └───figures
│           alpha_sweep.svg
│           beta_sweep.svg
│           qubits.svg
│           setup.svg
│           SPDC.png
├───HOM
│       HOM.py
│       HOM_dip.svg
│       HOM_measurements.xlsx
└───TOM
        TOM.py
        TOM_measurements.xlsx
```

## Experiments

### CHSH

This folder contains the code and results for the CHSH Bell-inequality experiment.

It includes two Python scripts:

**CHSH_computational.py**
A theoretical / numerical simulation of the experiment. It calculates the CHSH $S$ value from the quantum state or density matrix, and includes parameter sweeps and plots for different experimental conditions.

**CHSH_IBM.py**
A version of the experiment implemented with Qiskit. It can run the Bell-state circuit on a simulator and also connect to IBM Quantum hardware to reproduce the experiment on real quantum devices.

The folder also includes a figures/ directory with plots and setup images related to the experiment, including the optical setup, qubits, and result visualizations.

The file CHSH_measurements.xlsx contains the measurement data recorded in the lab.

### HOM

This folder contains the analysis code for the Hong–Ou–Mandel interference experiment.

The script HOM.py reads the measured coincidence data from HOM_measurements.xlsx, fits the HOM dip, and extracts key quantities such as the visibility and coherence time.

The file HOM_dip.svg contains the plotted result of the experiment.

### TOM

This folder contains the code for quantum state tomography.

The script TOM.py reads tomography measurement data from TOM_measurements.xlsx, reconstructs the density matrix, and computes quantities such as purity and fidelity.

## Notes
- The .xlsx files in each experiment folder contain the raw experimental measurements used in the analysis.
- The CHSH folder also includes a figures/ subdirectory with supporting experimental diagrams and result plots.
- The code is written in Python and uses standard scientific libraries such as NumPy, Pandas, Matplotlib, SciPy, and Qiskit.
- Running the Code: Each script can be run independently from its own folder or from the repository root, depending on how file paths are configured in the script.
