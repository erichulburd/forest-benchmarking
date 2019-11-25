from typing import Sequence

from pyquil.quilbase import Gate
from pyquil.api import BenchmarkConnection
from forest.benchmarking.volumetrics._main import CircuitTemplate
from forest.benchmarking.volumetrics._generators import *
from forest.benchmarking.volumetrics._transforms import *


def get_rand_1q_template(gates: Sequence[Gate]):
    """
    Creates a CircuitTemplate representing the family of circuits generated by repeated layers of
    random single qubit gates pulled from the input set of gates.

    :param gates:
    :return:
    """

    def func(graph, **kwargs):
        return random_single_qubit_gates(graph, gates=gates)

    return CircuitTemplate([func])


def get_rand_2q_template(gates: Sequence[Gate]):
    """
    Creates a CircuitTemplate representing the family of circuits generated by repeated layers of
    random two qubit gates pulled from the input set of gates.

    :param gates:
    :return:
    """

    def func(graph, **kwargs):
        return random_two_qubit_gates(graph, gates=gates)

    return CircuitTemplate([func])


def get_rand_1q_cliff_template(bm: BenchmarkConnection):
    """
    Creates a CircuitTemplate representing the family of circuits generated by repeated layers of
    random single qubit Clifford gates.
    """

    def func(graph, **kwargs):
        return random_single_qubit_cliffords(bm, graph)

    return CircuitTemplate([func])


def get_rand_2q_cliff_template(bm: BenchmarkConnection):
    """
    Creates a CircuitTemplate representing the family of circuits generated by repeated layers of
    random two qubit Clifford gates.
    """

    def func(graph, **kwargs):
        return random_two_qubit_cliffords(bm, graph)

    return CircuitTemplate([func])


def get_dagger_previous(n: int = 1):
    """
    Creates a CircuitTemplate that can be appended to another template to generate families of
    circuits with repeated (layer, inverse-layer) units.
    """

    def func(sequence, **kwargs):
        return dagger_previous(sequence, n)

    return CircuitTemplate([func])


def get_rand_su4_template():
    """
    Creates a CircuitTemplate representing the family of circuits generated by repeated layers of
    Haar-random two qubit gates acting on random pairs of qubits. This is the generator used in
    quantum volume [QVol]_ .
    """

    def func(graph, sequence, **kwargs):
        return random_su4_pairs(graph, len(sequence))

    return CircuitTemplate([func])


def get_quantum_volume_template():
    """
    Creates a quantum volume CircuitTemplate. See [QVol]_ .
    """
    template = get_rand_su4_template()
    template.sequence_transforms.append(compile_merged_sequence)
    return template