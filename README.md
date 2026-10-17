# Quantum Sprint — H₂ Ground-State Energy with VQE

**Problem statement:** PS-C1 — H₂ Ground-State Energy Estimation  
**Method:** Variational Quantum Eigensolver (VQE)  
**Basis:** STO-3G  
**Team:** Quantum_Sprint

## Project overview

This project estimates the electronic ground-state energy of the hydrogen molecule (H₂) using a quantum-chemistry workflow and the Variational Quantum Eigensolver (VQE). The molecular geometry is specified in `h2_vqe.py`. PySCF supplies the molecular integrals, Qiskit Nature builds the electronic Hamiltonian, and Qiskit Algorithms runs VQE on a local statevector simulator.

The script also computes a classical exact-diagonalization reference for the same mapped Hamiltonian. This is a useful baseline for checking the VQE estimate; it is not a claim of quantum advantage.

## Important scientific notes

- The reported energy depends on the H–H bond distance and the selected basis.
- This implementation uses a noiseless local simulator. Real quantum hardware may produce different results.
- The exact diagonalization value is a reference for validation, not a quantum-computing speedup.
- Do not report numerical results until you have run the script and checked the output.

## Files

- `h2_vqe.py` — molecule setup, Hamiltonian mapping, VQE, and reference calculation.
- `requirements.txt` — Python package dependencies.
- `results/` — place your actual run output here after testing.

## Setup

Use Python 3.10 or 3.11 in a virtual environment.

```bash
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

macOS/Linux:
```bash
source .venv/bin/activate
```

Install packages:
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Run:
```bash
python h2_vqe.py
```

## Method summary

1. Define H₂ at a chosen bond distance.
2. Use PySCF with the STO-3G basis to calculate molecular integrals.
3. Convert the electronic Hamiltonian to a qubit operator using the Jordan–Wigner mapping.
4. Prepare a Hartree–Fock initial state and a UCCSD variational ansatz.
5. Optimize circuit parameters using VQE with a local statevector estimator.
6. Compare the VQE result with exact diagonalization of the same qubit Hamiltonian.

## Reproducibility

Record the Python version, package versions, terminal output, and any changes to geometry or algorithm settings. If you add plots, generate them from saved run data and label axes and units.

## Team contributions

Fill this section in truthfully before final evaluation:

- Member 1: [actual contribution]
- Member 2: [actual contribution]
- Member 3: [actual contribution]

## Current status

This repository template must be run and verified by the team before claiming that the implementation works. Replace this note with the tested results, output, and any limitations.
