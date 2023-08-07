from QCpy import QuantumCircuit
import numpy as np


def inc(x):
    qc = QuantumCircuit(qubits=x, little_endian=True, prep='z')
    qc.hadamard(x - 1)
    qc.hadamard(x - 2)
    qc.toffoli(x - 1, x - 2, 0)
    return qc.state()


def test_09a():
    assert (
        inc(3) == np.array([
            0.5 + 0j, 0 + 0j, 0.5 + 0j, 0 + 0j,
            0.5 + 0j, 0 + 0j, 0 + 0j, 0.5 + 0j
        ], 'F').reshape(8, 1)
    ).all(), "test_09a Failed on hadamard -> hadamard -> toffoli"


def test_09b():
    assert (
        inc(4) == np.array([
            0.5 + 0j, 0 + 0j, 0 + 0j, 0 + 0j,
            0.5 + 0j, 0 + 0j, 0 + 0j, 0 + 0j,
            0.5 + 0j, 0 + 0j, 0 + 0j, 0 + 0j,
            0 + 0j, 0.5 + 0j, 0 + 0j, 0 + 0j
        ], 'F').reshape(16, 1)
    ).all(), "test_09b Failed on hadamard -> hadamard -> toffoli"


def test_09c():
    assert (
        inc(5) == np.array([
            0.5 + 0j, 0 + 0j, 0 + 0j, 0 + 0j,
            0 + 0j, 0 + 0j, 0 + 0j, 0 + 0j,
            0.5 + 0j, 0 + 0j, 0 + 0j, 0 + 0j,
            0 + 0j, 0 + 0j, 0 + 0j, 0 + 0j,
            0.5 + 0j, 0 + 0j, 0 + 0j, 0 + 0j,
            0 + 0j, 0 + 0j, 0 + 0j, 0 + 0j,
            0 + 0j, 0.5 + 0j, 0 + 0j, 0 + 0j,
            0 + 0j, 0 + 0j, 0 + 0j, 0 + 0j
        ], 'F').reshape(32, 1)
    ).all(), "test_09c Failed on hadamard -> hadamard -> toffoli"
