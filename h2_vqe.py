
import sys
import numpy as np

from qiskit.quantum_info import SparsePauliOp
from qiskit.primitives import StatevectorEstimator
from qiskit.circuit.library import TwoLocal
from qiskit_algorithms import VQE
from qiskit_algorithms.optimizers import SLSQP
from qiskit_algorithms.minimum_eigensolvers import NumPyMinimumEigensolver


def main():
    print("H2 Ground-State Energy Estimation using VQE")
    print("=" * 48)
    print("Python:", sys.version.split()[0])
    print("Molecule: H2")
    print("Geometry: 0.735 Angstrom")
    print("Basis: STO-3G")
    print("Hamiltonian: precomputed, symmetry-reduced 2-qubit model")
    print("Backend: statevector simulation")

    hamiltonian = SparsePauliOp.from_list([
        ("II", -1.052373245772859),
        ("IZ",  0.39793742484318045),
        ("ZI", -0.39793742484318045),
        ("ZZ", -0.01128010425623538),
        ("XX",  0.18093119978423156),
    ])

    ansatz = TwoLocal(
        num_qubits=2,
        rotation_blocks="ry",
        entanglement_blocks="cx",
        reps=2,
        entanglement="linear",
    )

    exact_result = NumPyMinimumEigensolver().compute_minimum_eigenvalue(
        hamiltonian
    )
    exact_energy = float(np.real(exact_result.eigenvalue))

    vqe = VQE(
        estimator=StatevectorEstimator(),
        ansatz=ansatz,
        optimizer=SLSQP(maxiter=500),
        initial_point=np.random.default_rng(7).uniform(
            -0.1, 0.1, ansatz.num_parameters
        ),
    )

    result = vqe.compute_minimum_eigenvalue(hamiltonian)
    vqe_energy = float(np.real(result.eigenvalue))

    print("\nResults")
    print("-" * 48)
    print(f"VQE energy:   {vqe_energy:.10f} Hartree")
    print(f"Exact energy: {exact_energy:.10f} Hartree")
    print(
        f"Absolute difference: "
        f"{abs(vqe_energy - exact_energy):.3e} Hartree"
    )
    print("\nNote: This uses a precomputed reduced Hamiltonian.")
    print("Verify convergence and benchmark provenance before reporting results.")


if __name__ == "__main__":
    main()
