"""
QuantumCircuit.py
"""
from ..qubit import Qubit
from ..QuantumGate import *
from .tools import amplitude, phaseAngle, probabilities, measure
import numpy as np

"""
Purpose:
    To apply various quantum gates to a quantum wire given any amount of qubits. With this, to then return the state at any given moment
    alongside calculations to be examined upon.
Methods:
    __init__:
        Constructor that initilizes the quantum state in a vector given the number of qubits, endian positioning, and prepping of the qubits.
    __operator_matrix__:
        Return a matrix from the tensor product calculation algorithm from any inplaced quantum gate.
    __controlled_phase_handler__:
        Calls a control_qubit and target_qubit qubits represented as integers and will then correctly create a system of mathematic implementations of
        any given controlled quantum gate.
    circuit:
        Returns the dictionary representation of the circuit and the values within it.
    amplitude:
        Return a vector of all possible amplitudes for the given state.
    phaseAngle:
        Calculates an array of possible phase angles based off the state. Converts each value using np.angle() function then degree to radian.
    state:
        Return a numpy array of the current quantum circuit.
    probabilities:
        Return a matrix with all the probabilities for each state.
    measure:
        Collapes the quantum circuit into classical bits.
    reverse:
        Reverses the quantum state.
    toffoli:
        A 3-qubit quantum gate that takes in two control_qubit qubits and one target_qubit qubit.
    rccx:
        A 3-qubit quantum gate that takes in two control_qubit qubits and one target_qubit qubit.
    rc3x:
        A 4-qubit quantum gate that is a simplified Toffoli gate and can be used in placed where the Toffoli gate is uncomputed again.
    cnot:
        A 2-qubit quantum gate that takes in control_qubit and target_qubit qubits, and will entangle the qubits if the control_qubit qubit is greater than 0.
    cr:
        A 2-qubit quantum gate that takes in control_qubit and target_qubit qubits to perform calculations upon the state.
    cz:
        A 2-qubit quantum gate that takes in control_qubit and target_qubit qubits to perform calculations upon the state.
    swap:
        A 2-qubit quantum gate that takes in two qubits to swap the qubits values they represent.
    rxx:
        A 2-qubit quantum gate that takes in two qubits and a representation of theta to initialize in the quantum state.
    rzz:
        A 2-qubit quantum gate that takes in two qubits and a representation of theta to initialize in the quantum state.
    customControlPhase:
        Used to insert single qubit based quantum gates to have a control_qubit qubit apart of it and committing to the quantum state.
    identity:
        Used to confirm value that a qubit is representing and does nothing to manipulate the value of such qubit.
    x:
        Used to invert the value of what a qubit is representing.
    hadamard:
        Used to put a given qubit into superposition.
    y:
        Changes the state of a qubit by pi around the y-axis of a Bloch Sphere.
    z:
        Changes the state of a qubit by pi around the z-axis of a Bloch Sphere.
    phase:
        Commits to a rotation around the z-axis based off of the inputted theta value.
    s:
        Is a Phase gate where the inputted theta value is given as a constant of theta = pi / 2.
    sdg:
        Is a Phase gate and inverse of the S gate where the inputted theta value is given as a constant of theta = -pi / 2.
    t:
        T gate is a special use case gate that in implemented from the P Gate.
    tdg:
        TDG gate is a special use case gate that in implemented from the P Gate and is the inverse of the T gate.
    rz:
        RZ gate commits a rotation around the z-axis for a qubit.
    ry:
        RY gate commits a rotation around the y-axis for a qubit.
    rx:
        RX gate commits a rotation around the x-axis for a qubit.
    sx:
        SX gate is the square root of the Inverse gate (X, PauliX Gate).
    sxdg:
        SXDG gate is the negative square root of the Inverse gate (X, PauliX Gate) and inverse of the SX gate.
    u:
        U gate is given three inputs (theta, phi, and lambda) that allow the inputs to manipulate the base matrix to allow for the position of the enacted qubit
        around the bloch sphere representation.
    custom:
        Will take in a custom single qubit quantum gate and implement it on a qubit.
--------

"""


class QuantumCircuit:
    def __init__(
            self,
            qubits: int,
            little_endian: bool = False,
            prep: chr = 'z'):
        """
        Constructor that initilizes the quantum state in a vector given the number of qubits, endian positioning, and prepping of the qubits.
        Args:
            qubits:
                The number of qubits that will be within the circuit.
            little_endian:
                a boolean variable to determine the placement of values, as well as determining the inverse of tensor product.
            prep:

        ------
        Variables:
            _little_endian :
                the number of qubits on the circuit
            _circuit_size :
                all the states of the qubits on the circuit
            _probabilities :
                an array of all the probabilities of the qubits being measured
            _percents :
                the array of probabilities turned into an array of values adding to 100
            _state :
                the state values for the qubit being taken into consideration
        """
        if (qubits < 1):
            exit(
                f"Error: QuantumCircuit().__init__ -- Quantum Circuit size must be 1 or more qubits. Current number of qubits is: {qubits}")
        # Determines if tensor calculation of __operator_matrix__ will be
        # reversed or not.
        self._little_endian = little_endian
        # Gets the number of qubits in play to store for later use.
        self._circuit_size = qubits
        # Makes tensored vector state of all qubits, and stores it within
        # _state to get a vector of [[1], [0], [0],....2^n].
        self._state = Qubit(prep).state
        # represent the circuit in dict
        self._circuit = []
        # increases the current vector size on the number of qubits - 1.
        for _ in range(qubits - 1):
            # _state is converted into the new lengthed vector based on the
            # kronocker product on the prepped qubit state.
            self._state = np.kron(self._state, Qubit(prep).state)

    def __operator_matrix__(
            self,
            gate_matrix: np.array,
            qubit: int,
            double: bool = False):
        """
        Return a matrix from the tensor product calculation algorithm from any inplaced quantum gate.
        Params:
            gate_matrix: np.array
            qubit: integer
            double: boolean
        Returns:
            operator_matrix (numpy array):
                Matrix after final calculation from the tensor product algorithm.
        """
        # Identity matrix is called.
        i_matrix = Identity().matrix
        # gate queue for the computation
        gate_queue = [i_matrix for _ in range(self._circuit_size)]
        # replaces the placement of the identity gate at the qubit index with
        # the gate to get a correct calculation of final product
        gate_queue[qubit] = gate_matrix
        # if double is true, then CNOT, toffli, or any gate more than one qubit
        # is being asked to be implemented.
        if double:
            gate_queue.pop(qubit + 1)
        # if little_endian variable is true to follow IBM and Qiskit notation.
        # Inverses queue of operation.
        if (self._little_endian):
            gate_queue = gate_queue[::-1]
        # stores final value to be stored into operator_matrix value
        operator_matrix = gate_queue[0]
        # uses np.kron() function to tensor product the queue
        for gate in gate_queue[1:]:
            operator_matrix = np.kron(operator_matrix, gate)

        return operator_matrix

    def __controlled_phase_handler__(
            self,
            matrix_to_calculate: np.array,
            control_qubit: int,
            target_qubit: int):
        """
        Calls a control_qubit and target_qubit represented as integers and will then correctly create a system of mathematic implementations of
        any given controlled quantum gate.
        Params:
            matrix_to_calculate: np.array
            control_qubit: integer
            target_qubit: integer
        Returns:
            None.
        """
        # inverse bool variable to determine if controlled gate representation
        # needs to invert for confirming logic structuring.
        inverse = False
        # checking to see if target_qubit is less than control_qubit indices:
        if (target_qubit < control_qubit):
            inverse = True
        # create temp target_qubit variable
        temp_target_qubit = target_qubit
        # call from QuantumGate and stores Hadamard gate into variable.
        hadamard = Hadamard().matrix
        # If target_qubit and control_qubit qubits are next to each other, then no further
        # logic needs to be done and calls base system.
        if (abs(target_qubit - control_qubit) == 1):
            # calls from called bool variable to see if the base CNOT matrix
            # needs to be inverted to confirm correct logic structuring.
            if inverse:
                # This is implemented due to other controlled gates not needing
                # this implementation.
                self._state = np.dot(
                    self.__operator_matrix__(
                        hadamard, temp_target_qubit), self._state)
                self._state = np.dot(
                    self.__operator_matrix__(
                        hadamard, temp_target_qubit + 1), self._state)
                # Call to _state to commit a dot product on the state to
                # include the given gate of the method.
                self._state = np.dot(
                    self.__operator_matrix__(
                        matrix_to_calculate,
                        temp_target_qubit,
                        double=True),
                    self._state)
                # This is implemented due to other controlled gates not needing
                # this implementation.

                self._state = np.dot(
                    self.__operator_matrix__(
                        hadamard, temp_target_qubit), self._state)
                self._state = np.dot(
                    self.__operator_matrix__(
                        hadamard, temp_target_qubit + 1), self._state)
                # used for inversing all other gates that the target_qubit is less
                # than the control_qubit to make it inversed in logic.
            else:
                # if not inverse, what the controlled gate is will be enacted
                # on the _state using dot product system.
                self._state = np.dot(
                    self.__operator_matrix__(
                        matrix_to_calculate,
                        control_qubit,
                        double=True),
                    self._state)
            return
        # while the difference between the temp target_qubit and control_qubit is not -1 or
        # 1.
        while (abs(temp_target_qubit - control_qubit) != 1):
            # calls from called bool variable to see if the base CNOT matrix
            # needs to be inverted to confirm correct logic structuring.
            if inverse:
                # This is implemented due to other controlled gates not needing
                # this implementation.
                self.swap(temp_target_qubit, temp_target_qubit + 1)
                # update temp target_qubit position.
                temp_target_qubit += 1
            else:
                # swap the temp target_qubit closer to the target_qubit.
                self.swap(temp_target_qubit - 1, temp_target_qubit)
                # update temp target_qubit position.
                temp_target_qubit -= 1
        # calls from called bool variable to see if the base CNOT matrix needs
        # to be inverted to confirm correct logic structuring.
        if inverse:
            # will create inversed controlled_phase of what is inputted through here, determined if the inversed variable is marked true.
            # call hadamard gates on control_qubit and target_qubit variables.
            self._state = np.dot(
                self.__operator_matrix__(
                    hadamard, temp_target_qubit), self._state)
            self._state = np.dot(
                self.__operator_matrix__(
                    hadamard,
                    temp_target_qubit + 1),
                self._state)
            # Call to _state to commit a dot product on the state to include
            # the given gate of the method.
            self._state = np.dot(
                self.__operator_matrix__(
                    matrix_to_calculate,
                    temp_target_qubit,
                    double=True),
                self._state)
            # This is implemented due to other controlled gates not needing
            # this implementation.
            self._state = np.dot(
                self.__operator_matrix__(
                    hadamard, temp_target_qubit),
                self._state)
            self._state = np.dot(
                self.__operator_matrix__(
                    hadamard,
                    temp_target_qubit + 1),
                self._state)
            # used for inversing all other gates that the target_qubit is less than
            # the control_qubit to make it inversed in logic.
        else:
            # if not inverse, what the controlled gate is will be enacted on
            # the _state using dot product system.
            self._state = np.dot(
                self.__operator_matrix__(
                    matrix_to_calculate,
                    control_qubit,
                    double=True),
                self._state)

        # while the temp target_qubit does not equal the original target_qubit
        while (temp_target_qubit != target_qubit):
            if inverse:
                # swap the temp target_qubit with the position closer to original
                # target_qubit
                self.swap(temp_target_qubit - 1, temp_target_qubit)
                # update temp target_qubit position
                temp_target_qubit -= 1
            else:
                # swap the temp target_qubit with the position closer to original
                # target_qubit
                self.swap(temp_target_qubit, temp_target_qubit + 1)
                # update temp target_qubit position
                temp_target_qubit += 1



    def circuit(self):
        """
        Returns the dictionary representation of the circuit and the values within it.
        Params:
            None.
        Returns:
            np.array self._circuit
        """
        return self._circuit

    def amplitude(self, show_bit=-1, round: int = 3, radian: bool = False):
        """
        Return a vector of all possible amplitudes for the given state.
        Params:
            show_bit: string or int
            round: int
            radian: bool
        Returns:
            np.around(statevector) (numpy array):
                Matrix after final calculation from the sqrt(x^2 + y^2) algorithm for finding the amplitude.
        """
        return amplitude(self._state, self._circuit_size, show_bit, round, radian)

    def phaseAngle(self, show_bit = -1, round: int = 3, radian: bool = True):
        """
        Calculates an array of possible phase angles based off the state. Converts each value using np.angle() function then degree to radian.
        Params:
            show_bit: string or int
            round: int
            radian: bool
        Returns:
            np.around(phaseAngles) (numpy array):
                Matrix after final calculation from the phase angle algorithm.
        """
        return phaseAngle(self._state, self._circuit_size, show_bit, round, radian)

    def state(self, round: int = 3):
        """
        Return a numpy array of the current quantum circuit.
        Params:
            round: int
        Returns:
            np.around(self._state) (numpy array):
                vector of the given state rounded based off of the parameter
        """
        if (round < 0):
            exit(
                f"Error: QuantumCircuit().state -- round placement must be a value greater than 0.")
        return np.around(self._state, decimals=round)
    
    def circuitQueue(self):
        return self._circuit
    
    def circuitSize(self):
        return self._circuit_size

    def probabilities(self, show_percent: bool = False, show_bit: int = -1, round: int = 3):
        """
        Return a matrix with all the probabilities for each state
        Params:
            show_percent: bool
            show_bit: string or int
            round: int
        Returns:
            prob_matrix (numpy array):
                matrix with all the weighted probabilities of being measured
        """
        return probabilities(self._state, self._circuit_size, show_percent, show_bit, round)

    def measure(self):
        """
        Collapes the quantum circuit into classical bits
        Params:
            None
        Returns:
            final_state (str):
                the winning state displayed in classical bits notation
        """
        # randomly selects the measured state using self.probabilities()
        return measure(self._state, self._circuit_size, self.probabilities())

    def reverse(self):
        """
        Reverses the quantum state.
        Params:
            None.
        Returns:
            None.
        """
        # reverses the entire state, useful for quantum algorithms.
        self._state = self._state[::-1]
    """
    Multiple qubit quantum gates
    """

    def toffoli(self, control_1: int, control_2: int, target_qubit: int):
        """
        A 3-qubit quantum gate that takes in two control_qubit qubits and one target_qubit qubit.
        Params:
            control_1: int
            control_2: int
            target_qubit: int
        Returns:
            None.
        """
        # If circuit is less than 3, means Toffoli gate cannot be allowed.
        if (self._circuit_size < 3):
            exit(
                f"Error: QuantumCircuit().toffoli -- Quantum Circuit size must be 3 or more qubits. Current number of qubits is: {self._circuit_size}")
        # Calls of gates here represent the Toffoli matrix using other quantum
        # gates.
        self.customControlPhase(control_2, target_qubit, Sx().matrix)
        self.cnot(control_1, control_2)
        self.customControlPhase(control_2, target_qubit, Sxdg().matrix)
        self.cnot(control_1, control_2)
        self.customControlPhase(control_1, target_qubit, Sx().matrix)
        # append gate to self._circuit
        self._circuit.append(('toffoli', control_1, control_2, target_qubit))

    def rccx(self, control_1: int, control_2: int, target_qubit: int):
        """
        A 3-qubit quantum gate that takes in two control_qubit qubits and one target_qubit qubit.
        Params:
            control_1: int
            control_2: int
            target_qubit: int
        Returns:
            None.
        """
        # If circuit is less than 3, means RCCX gate cannot be allowed.
        if (self._circuit_size < 3):
            exit(
                f"Error: QuantumCircuit().rccx -- Quantum Circuit size must be 3 or more qubits. Current number of qubits is: {self._circuit_size}")
        # Calls of gates here represent the RCCX matrix using other quantum
        # gates.
        self.u(target_qubit, np.pi / 2, 0, np.pi)
        self.u(target_qubit, 0, 0, np.pi / 4)
        self.cnot(control_2, target_qubit)
        self.u(target_qubit, 0, 0, (-1 * np.pi) / 4)
        self.cnot(control_1, target_qubit)
        self.u(target_qubit, 0, 0, np.pi / 4)
        self.cnot(control_2, target_qubit)
        self.u(target_qubit, 0, 0, (-1 * np.pi) / 4)
        self.u(target_qubit, np.pi / 2, 0, np.pi)
        # append gate to self._circuit
        self._circuit.append(('rccx', control_1, control_2, target_qubit))

    def rc3x(self, a: int, b: int, c: int, d: int):
        """
        A 4-qubit quantum gate that is a simplified Toffoli gate and can be used in placed where the Toffoli gate is uncomputed again.
        Params:
            a: int
            b: int
            c: int
            d: int
        Returns:
            None.
        """
        # If circuit is less than 4, means RC3X gate cannot be allowed.
        if (self._circuit_size < 4):
            exit(
                f"Error: QuantumCircuit().rc3x -- Quantum Circuit size must be 4 or more qubits. Current number of qubits is: {self._circuit_size}")
        # Calls of gates here represent the RC3X matrix using other quantum
        # gates.
        self.u(d, np.pi / 2, 0, np.pi)
        self.u(d, 0, 0, np.pi / 4)
        self.cnot(c, d)
        self.u(d, 0, 0, (-1 * np.pi) / 4)
        self.u(d, np.pi / 2, 0, np.pi)
        self.cnot(a, d)
        self.u(d, 0, 0, np.pi / 4)
        self.cnot(b, d)
        self.u(d, 0, 0, (-1 * np.pi / 4))
        self.cnot(a, d)
        self.u(d, 0, 0, np.pi / 4)
        self.cnot(b, d)
        self.u(d, 0, 0, (-1 * np.pi) / 4)
        self.u(d, np.pi / 2, 0, np.pi)
        self.u(d, 0, 0, np.pi / 4)
        self.cnot(c, d)
        self.u(d, 0, 0, (-1 * np.pi / 4))
        self.u(d, np.pi / 2, 0, np.pi)
        # append gate to self._circuit
        self._circuit.append(('rc3x', a, b, c, d))

    def cnot(self, control_qubit: int, target_qubit: int):
        """
        A 2-qubit quantum gate that takes in control_qubit and target_qubit qubits, and will entangle the qubits if the control_qubit qubit is greater than 0.
        Params:
            control_qubit: int
            target_qubit: int
        Returns:
            None.
        """
        # If circuit is less than 2, means CNOT gate cannot be allowed.
        if (self._circuit_size < 2):
            exit(
                f"Error: QuantumCircuit().cnot -- Quantum Circuit size must be 2 or more qubits. Current number of qubits is: {self._circuit_size}")
        # Determines if the little endian or big endian CNOT gate needs to be
        # established for calculations.
        if self._little_endian:
            cnot_matrix = CNot().matrix
        else:
            cnot_matrix = CNot(inverse=True).matrix
        # Sends to __controlled_phase_handler alongside a boolean confirming
        # the gate is indeed a CNOT gate
        self.__controlled_phase_handler__(
            cnot_matrix, control_qubit, target_qubit)
        # append gate to self._circuit
        self._circuit.append(('cnot', control_qubit, target_qubit))

    def cr(self, control_qubit: int, target_qubit: int):
        """
        A 2-qubit quantum gate that takes in control_qubit and target_qubit qubits to perform calculations upon the state.
        Params:
            control_qubit: int
            target_qubit: int
        Returns:
            None.
        """
        # If circuit is less than 2, means CR gate cannot be allowed.
        if (self._circuit_size < 2):
            exit(
                f"Error: QuantumCircuit().cr -- Quantum Circuit size must be 2 or more qubits. Current number of qubits is: {self._circuit_size}")
        self.__controlled_phase_handler__(
            Cr().matrix, control_qubit, target_qubit)
        # append gate to self._circuit
        self._circuit.append(('cr', control_qubit, target_qubit))

    def cz(self, control_qubit: int, target_qubit: int):
        """
        A 2-qubit quantum gate that takes in control_qubit and target_qubit qubits to perform calculations upon the state.
        Params:
            control_qubit: int
            target_qubit: int
        Returns:
            None.
        """
        # If circuit is less than 2, means CZ gate cannot be allowed.
        if (self._circuit_size < 2):
            exit(
                f"Error: QuantumCircuit().cz -- Quantum Circuit size must be 2 or more qubits. Current number of qubits is: {self._circuit_size}")
        self.__controlled_phase_handler__(
            Cz().matrix, control_qubit, target_qubit)
        # append gate to self._circuit
        self._circuit.append(('cz', control_qubit, target_qubit))

    def swap(self, qubit_1: int, qubit_2: int):
        """
        A 2-qubit quantum gate that takes in two qubits to swap the qubits values they represent.
        Params:
            qubit_1: int
            qubit_2: int
        Returns:
            None.
        """
        # If circuit is less than 2, means SWAP gate cannot be allowed.
        if (self._circuit_size < 2):
            exit(
                f"Error: QuantumCircuit().swap -- Quantum Circuit size must be 2 or more qubits. Current number of qubits is: {self._circuit_size}")
        # get the swap matrix
        swap_matrix = Swap().matrix
        # determines if the two values at play are at distance greater than
        # one, if so it will call in private method for larger matrix
        # operations.
        if (qubit_1 - qubit_2 != 1 and qubit_1 - qubit_2 != -1):
            self.__controlled_phase_handler__(swap_matrix, qubit_1, qubit_2)
        # if qubit_2 is above qubit_1 on the quantum wire, then it will use
        # qubit_2 as the call to __operator_matrix__.
        elif (qubit_1 > qubit_2):
            self._state = np.dot(
                self.__operator_matrix__(
                    swap_matrix,
                    qubit_2,
                    double=True),
                self._state)
        # simply commits a normal SWAP quantum gate functionality.
        else:
            self._state = np.dot(
                self.__operator_matrix__(
                    swap_matrix,
                    qubit_1,
                    double=True),
                self._state)
        # append gate to self._circuit
        self._circuit.append(('swap', qubit_1, qubit_2))

    def rxx(self, qubit_1: int, qubit_2: int, theta: float = np.pi / 2):
        """
        A 2-qubit quantum gate that takes in two qubits and a representation of theta to initialize in the quantum state.
        Params:
            qubit_1: int
            qubit_2: int
            theta: float
        Returns:
            None.
        """
        # If circuit is less than 2, means RXX gate cannot be allowed.
        if (self._circuit_size < 2):
            exit(
                f"Error: QuantumCircuit().rxx -- Quantum Circuit size must be 2 or more qubits. Current number of qubits is: {self._circuit_size}")
        rxx_matrix = Rxx(theta).matrix
        self.__controlled_phase_handler__(rxx_matrix, qubit_1, qubit_2)
        # append gate to self._circuit
        self._circuit.append(('rxx', qubit_1, qubit_2))

    def rzz(self, qubit_1: int, qubit_2: int, theta: float = np.pi / 2):
        """
        A 2-qubit quantum gate that takes in two qubits and a representation of theta to initialize in the quantum state.
        Params:
            qubit_1: int
            qubit_2: int
            theta: float
        Returns:
            None.
        """
        # If circuit is less than 2, means RZZ gate cannot be allowed.
        if (self._circuit_size < 2):
            exit(
                f"Error: QuantumCircuit().rzz -- Quantum Circuit size must be 2 or more qubits. Current number of qubits is: {self._circuit_size}")
        if (qubit_2 < qubit_1):
            qubit_2, qubit_1 = qubit_1, qubit_2
        rzz_matrix = Rzz(theta).matrix
        # determines if the two values at play are at distance greater than
        # one, if so it will call in private method for larger matrix
        # operations.
        self.__controlled_phase_handler__(rzz_matrix, qubit_1, qubit_2)
        # append gate to self._circuit
        self._circuit.append(('rzz', qubit_1, qubit_2))

    def customControlPhase(
            self,
            control_qubit: int,
            target_qubit: int,
            custom_matrix: np.array):
        """
        Used to insert single qubit based quantum gates to have a control_qubit qubit apart of it and committing to the quantum state.
        Params:
            control_qubit: int
            target_qubit: int
            custom_matrix: np.array
        Returns:
            None.
        """
        # custom quantum gate can only call in a single qubit based matrix to
        # manipulate the state.
        if (custom_matrix.shape != (2, 2)):
            exit(f"Error: QuantumCircuit().customControlPhase -- can only include a single qubit based quantum gate (2,2) matrix for state manipulation.")
        # Determines if the matrix needs to be representing in little or big
        # endian format.
        if self._little_endian:
            # If little endian format is being used.
            controlled_custom_matrix = np.array([
                [1 + 0j, 0 + 0j, 0 + 0j, 0 + 0j],
                [0 + 0j, custom_matrix[0][0], 0 + 0j, custom_matrix[0][1]],
                [0 + 0j, 0 + 0j, 1 + 0j, 0 + 0j],
                [0 + 0j, custom_matrix[1][0], 0 + 0j, custom_matrix[1][1]]
            ])

        else:
            # If big endian format is in being used.
            controlled_custom_matrix = np.array([
                [1 + 0j, 0 + 0j, 0 + 0j, 0 + 0j],
                [0 + 0j, 1 + 0j, 0 + 0j, 0 + 0j],
                [0 + 0j, 0 + 0j, custom_matrix[0][0], custom_matrix[0][1]],
                [0 + 0j, 0 + 0j, custom_matrix[1][0], custom_matrix[1][1]]
            ])
        self.__controlled_phase_handler__(
            controlled_custom_matrix, control_qubit, target_qubit)
        self._circuit.append(('C', control_qubit, target_qubit))

    """
    Single Qubit Gates
    """

    def identity(self, qubit: int):
        """
        Used to confirm value that a qubit is representing and does nothing to manipulate the value of such qubit.
        Params:
            qubit: int
        Returns:
            None.
        """
        if qubit is None:
            exit(
                f"Error: QuantumCircuit().identity -- Must select a qubit to enact on quantum gate.")
        self._state = np.dot(
            self.__operator_matrix__(
                Identity().matrix,
                qubit),
            self._state)
        # append gate to self._circuit
        self._circuit.append((Identity().symbol, qubit))

    def x(self, qubit: int):
        """
        Used to invert the value of what a qubit is representing.
        Params:
            qubit: int
        Returns:
            None.
        """
        if qubit is None:
            exit(
                f"Error: QuantumCircuit().x -- Must select a qubit to enact on quantum gate.")
        # get the not matrix
        self._state = np.dot(
            self.__operator_matrix__(
                PauliX().matrix, qubit), self._state)
        # append gate to self._circuit
        self._circuit.append((PauliX().symbol, qubit))

    def hadamard(self, qubit: int):
        """
        Used to put a given qubit into superposition.
        Params:
            qubit: int
        Returns:
            None.
        """
        if qubit is None:
            exit(
                f"Error: QuantumCircuit().hadamard -- Must select a qubit to enact on quantum gate.")
        # get the hadamard matrix
        self._state = np.dot(
            self.__operator_matrix__(
                Hadamard().matrix, qubit), self._state)
        # append gate to self._circuit
        self._circuit.append((Hadamard().symbol, qubit))

    def y(self, qubit: int):
        """
        Changes the state of a qubit by pi around the y-axis of a Bloch Sphere.
        Params:
            qubit: int
        Returns:
            None.
        """
        if qubit is None:
            exit(
                f"Error: QuantumCircuit().y -- Must select a qubit to enact on quantum gate.")
        # get the Y matrix
        self._state = np.dot(
            self.__operator_matrix__(
                PauliY().matrix, qubit), self._state)
        # append gate to self._circuit
        self._circuit.append(PauliY().symbol)

    def z(self, qubit: int):
        """
        Changes the state of a qubit by pi around the z-axis of a Bloch Sphere.
        Params:
            qubit: int
        Returns:
            None.
        """
        if qubit is None:
            exit(
                f"Error: QuantumCircuit().z -- Must select a qubit to enact on quantum gate.")
        # get the Z matrix
        self._state = np.dot(
            self.__operator_matrix__(
                PauliZ().matrix, qubit), self._state)
        # append gate to self._circuit
        self._circuit.append((PauliZ().symbol, qubit))

    def phase(self, qubit: int, theta: float = np.pi / 2):
        """
        Commits to a rotation around the z-axis based off of the inputted theta value.
        Params:
            qubit: int
            theta: float
        Returns:
            None.
        """
        if qubit is None:
            exit(
                f"Error: QuantumCircuit().phase -- Must select a qubit to enact on quantum gate.")
        # get the Phase matrix
        self._state = np.dot(
            self.__operator_matrix__(
                Phase(theta).matrix, qubit), self._state)
        # append gate to self._circuit
        self._circuit.append((Phase(theta).symbol, qubit))

    def s(self, qubit: int):
        """
        Is a Phase gate where the inputted theta value is given as a constant of theta = pi / 2.
        Params:
            qubit: int
        Returns:
            None.
        """
        if qubit is None:
            exit(
                f"Error: QuantumCircuit().s -- Must select a qubit to enact on quantum gate.")
        # get the Phase matrix
        self._state = np.dot(
            self.__operator_matrix__(
                S().matrix, qubit), self._state)
        # append gate to self._circuit
        self._circuit.append((S().symbol, qubit))

    def sdg(self, qubit: int):
        """
        Is a Phase gate and inverse of the S gate where the inputted theta value is given as a constant of theta = -pi / 2.
        Params:
            qubit: int
        Returns:
            None.
        """
        if qubit is None:
            exit(
                f"Error: QuantumCircuit().sdg -- Must select a qubit to enact on quantum gate.")
        # get the Sdg matrix
        self._state = np.dot(
            self.__operator_matrix__(
                Sdg().matrix, qubit), self._state)
        # append gate to self._circuit
        self._circuit.append((Sdg().symbol, qubit))

    def t(self, qubit: int):
        """
        T gate is a special use case gate that in implemented from the P Gate.
        Params:
            qubit: int
        Returns:
            None.
        """
        if qubit is None:
            exit(
                f"Error: QuantumCircuit().t -- Must select a qubit to enact on quantum gate.")
        # get the T matrix
        self._state = np.dot(
            self.__operator_matrix__(
                T().matrix, qubit), self._state)
        # append gate to self._circuit
        self._circuit.append((T().symbol, qubit))

    def tdg(self, qubit: int):
        """
        TDG gate is a special use case gate that in implemented from the P Gate and is the inverse of the T gate.
        Params:
            qubit: int
        Returns:
            None.
        """
        if qubit is None:
            exit(
                f"Error: QuantumCircuit().tdg -- Must select a qubit to enact on quantum gate.")
        # get the Tdg matrix
        self._state = np.dot(
            self.__operator_matrix__(
                Tdg().matrix, qubit), self._state)
        # append gate to self._circuit
        self._circuit.append((Tdg().symbol, qubit))

    def rz(self, qubit: int, theta: float = np.pi / 2):
        """
        RZ gate commits a rotation around the z-axis for a qubit.
        Params:
            qubit: int
            theta: float
        Returns:
            None.
        """
        if qubit is None:
            exit(
                f"Error: QuantumCircuit().rz -- Must select a qubit to enact on quantum gate.")
        # get the Rz matrix
        self._state = np.dot(
            self.__operator_matrix__(
                Rz(theta).matrix, qubit), self._state)
        # append gate to self._circuit
        self._circuit.append((Rz(theta).matrix, qubit))

    def ry(self, qubit: int, theta: float = np.pi / 2):
        """
        RY gate commits a rotation around the y-axis for a qubit.
        Params:
            qubit: int
            theta: float
        Returns:
            None.
        """
        if qubit is None:
            exit(
                f"Error: QuantumCircuit().ry -- Must select a qubit to enact on quantum gate.")
        # get the Ry matrix
        self._state = np.dot(
            self.__operator_matrix__(
                Ry(theta).matrix, qubit), self._state)
        # append gate to self._circuit
        self._circuit.append((Ry().symbol, qubit))

    def rx(self, qubit: int, theta: float = np.pi / 2):
        """
        RX gate commits a rotation around the x-axis for a qubit.
        Params:
            qubit: int
            theta: float
        Returns:
            None.
        """
        if qubit is None:
            exit(
                f"Error: QuantumCircuit().rx -- Must select a qubit to enact on quantum gate.")
        # get the Rx matrix
        self._state = np.dot(
            self.__operator_matrix__(
                Rx(theta).matrix, qubit), self._state)
        # append gate to self._circuit
        self._circuit.append((Rx(theta).matrix, qubit))

    def sx(self, qubit: int):
        """
        SX gate is the square root of the Inverse gate (X, PauliX Gate).
        Params:
            qubit: int
        Returns:
            None.
        """
        if qubit is None:
            exit(
                f"Error: QuantumCircuit().sx -- Must select a qubit to enact on quantum gate.")
        # get the Sx matrix
        self._state = np.dot(
            self.__operator_matrix__(
                Sx().matrix, qubit), self._state)
        # append gate to self._circuit
        self._circuit.append((Sx().symbol, qubit))

    def sxdg(self, qubit: int):
        """
        SXDG gate is the negative square root of the Inverse gate (X, PauliX Gate) and inverse of the SX gate.
        Params:
            qubit: int
        Returns:
            None.
        """
        if qubit is None:
            exit(
                f"Error: QuantumCircuit().sxdg -- Must select a qubit to enact on quantum gate.")
        # get the Sxdg matrix
        self._state = np.dot(
            self.__operator_matrix__(
                Sxdg().matrix, qubit), self._state)
        # append gate to self._circuit
        self._circuit.append((Sxdg().symbol, qubit))

    def u(
        self,
        qubit: int,
        theta: float = np.pi / 2,
        phi: float = np.pi / 2,
            lmbda: float = np.pi / 2):
        """
        U gate is given three inputs (theta, phi, and lambda) that allow the inputs to manipulate the base matrix to allow for the position of the enacted qubit
        around the bloch sphere representation.
        Params:
            qubit: int
            theta: float
            phi: float
            lmbda: float
        Returns:
            None.
        """
        if qubit is None:
            exit(
                f"Error: QuantumCircuit().u -- Must select a qubit to enact on quantum gate.")
        # get the U matrix
        self._state = np.dot(
            self.__operator_matrix__(
                U(theta, phi, lmbda).matrix, qubit), self._state)
        # append gate to self._circuit
        self._circuit.append((U().symbol, qubit))

    def custom(self, qubit: int, custom_matrix: np.array):
        """
        Will take in a custom single qubit quantum gate and implement it on a qubit.
        Params:
            qubit: int
            custom_matrix: np.array
        Returns:
            None.
        """
        # if gate is not a single qubit, will exit.
        if (custom_matrix.shape != (2, 2)):
            exit(f"Error: QuantumCircuit().insertGate -- can only include a single qubit based quantum gate (2,2) matrix for state manipulation.")
        # calls gate and will operate on state as per usual
        self._state = np.dot(
            self.__operator_matrix__(
                custom_matrix,
                qubit),
            self._state)
        self._circuit.append(('C', qubit))
