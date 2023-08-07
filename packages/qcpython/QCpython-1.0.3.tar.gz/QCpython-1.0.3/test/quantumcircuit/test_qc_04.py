from QCpy import QuantumCircuit
import numpy as np


def inc(x):
    qc = QuantumCircuit(qubits=x, little_endian=True, prep='z')
    qc.hadamard(0)
    qc.cnot(0, x - 1)
    return qc.state()


def test_04a():
    assert (
        inc(2) == np.array([
            0.707 + 0j, 0 + 0j, 0 + 0j, 0.707 + 0j
        ], 'F').reshape(4, 1)
    ).all(), "test_04a Failed on hadamard and cnot"


def test_04b():
    assert (
        inc(3) == np.array([
            0.707 + 0j, 0 + 0j, 0 + 0j, 0 + 0j,
            0 + 0j, 0.707 + 0j, 0 + 0j, 0 + 0j
        ], 'F').reshape(8, 1)
    ).all(), "test_04b Failed on hadamard and cnot"


def test_04c():
    assert (
        inc(4) == np.array([
            0.707 + 0j, 0 + 0j, 0 + 0j, 0 + 0j, 0 + 0j, 0 + 0j, 0 + 0j, 0 + 0j,
            0 + 0j, 0.707 + 0j, 0 + 0j, 0 + 0j, 0 + 0j, 0 + 0j, 0 + 0j, 0 + 0j
        ], 'F').reshape(16, 1)
    ).all(), "test_04c Failed on hadamard and cnot"
