"""
H2 ground-state energy estimation using Qiskit Nature + VQE.

This script is intended as a small, reproducible baseline for PS-C1.
Run it and verify the output before submitting or describing results.
"""

from __future__ import annotations

import sys
import numpy as np

from qiskit.primitives import StatevectorEstimator
from qiskit_algorithms import VQE
from qiskit_algorithms.optimizers import SLSQP
from qiskit_algorithms.minimum_eigensolvers import NumPyMinimumEigensolver

from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.second_q.mappers import JordanWignerMapper
from qiskit_nature.second_q.circuit.library import HartreeFock, UCCSD
from qiskit_nature.second_q.algorithms import GroundStateEigensolver


def main() -> int:
    print("H2 Ground-State Energy Estimation with VQE")
    print("=" * 48)
    print(f"Python: {sys.version.split()[0]}")

    # H-H distance in angstroms. Change only if the challenge specifies
    # a different benchmark geometry.
    bond_distance = 0.735
    geometry = f"H 0 0 0; H 0 0 {bond_distance}"

    print(f"Molecule: H2")
    print(f"Geometry: H-H distance = {bond_distance:.3f} Angstrom")
    print("Basis: STO-3G")
    print("Backend: noiseless statevector simulator")

    driver = PySCFDriver(
        atom=geometry,
        basis="sto3g",
        charge=0,
        spin=0,
    )
    problem = driver.run()

    mapper = JordanWignerMapper()
    hamiltonian = problem.hamiltonian
    qubit_hamiltonian = mapper.map(hamiltonian.second_q_op())

    num_spatial_orbitals = problem.num_spatial_orbitals
    num_particles = problem.num_particles

    initial_state = HartreeFock(
        num_spatial_orbitals=num_spatial_orbitals,
        num_particles=num_particles,
        qubit_mapper=mapper,
    )
    ansatz = UCCSD(
        num_spatial_orbitals=num_spatial_orbitals,
        num_particles=num_particles,
        qubit_mapper=mapper,
        initial_state=initial_state,
    )

    estimator = StatevectorEstimator()
    optimizer = SLSQP(maxiter=250)
    rng = np.random.default_rng(7)
    initial_point = 0.01 * rng.standard_normal(ansatz.num_parameters)

    vqe = VQE(
        estimator=estimator,
        ansatz=ansatz,
        optimizer=optimizer,
        initial_point=initial_point,
    )

    # Solve the electronic problem with VQE.
    vqe_solver = GroundStateEigensolver(mapper, vqe)
    vqe_result = vqe_solver.solve(problem)

    # Exact diagonalization of the same mapped electronic Hamiltonian.
    exact_solver = GroundStateEigensolver(
        mapper,
        NumPyMinimumEigensolver(),
    )
    exact_result = exact_solver.solve(problem)

    print("\nResults")
    print("-" * 48)
    print(f"VQE total ground-state energy:   {vqe_result.total_energies[0]: .10f} Hartree")
    print(f"Exact total ground-state energy: {exact_result.total_energies[0]: .10f} Hartree")
    difference = abs(
        float(np.real(vqe_result.total_energies[0]))
        - float(np.real(exact_result.total_energies[0]))
    )
    print(f"Absolute difference:             {difference:.3e} Hartree")
    print("\nInterpretation:")
    print("- The VQE value is a variational estimate from the optimizer.")
    print("- The exact value is a classical reference for this small model.")
    print("- Save this output only after checking that the run completed successfully.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
