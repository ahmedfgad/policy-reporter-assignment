class State:
    """Represents a state in the FSM."""
    def __init__(self, name, is_accepting=False):
        """
        Initialize a state.
            name: Unique name of the state.
            is_accepting: Whether this state is an accepting state.
        """
        if not name or not isinstance(name, str):
            raise ValueError("State name must be a non-empty string.")
        if not isinstance(is_accepting, bool):
            raise ValueError("is_accepting must be a boolean value.")
        
        # The state name. It must be unique.
        self.name = name
        # Whether the state is accepting/final.
        self.is_accepting = is_accepting
        # The set of transitions from the current state to other next states.
        self.transitions = {}

    def add_transition(self, input_symbol, next_state):
        """
        Add a transition for the state.
            input_symbol: Input symbol that triggers the transition.
            next_state: The next state to transition to.
        """
        if not isinstance(input_symbol, int):
            raise ValueError("Input symbol must be an integer.")
        if input_symbol in self.transitions:
            raise ValueError(f"Transition for input '{input_symbol}' already exists.")
        if not isinstance(next_state, State):
            raise TypeError("next_state must be an instance of State.")

        # Add a transition/link from the current state (self) to the next state given the passed input symbol.
        self.transitions[input_symbol] = next_state

    def get_next_state(self, input_symbol):
        """
        Get the next state based on the input symbol.
            input_symbol: The input symbol.
        return: The next state or None if no transition exists.
        """

        # Get the next state given the input symbol and the current state (self).
        return self.transitions.get(input_symbol, None)


class FSM:
    """A generic Finite State Machine."""
    def __init__(self, initial_state):
        """
        Initialize the FSM.
            initial_state: The initial state of the FSM.
        """
        if not isinstance(initial_state, State):
            raise TypeError("initial_state must be an instance of State.")

        # Set the current state to the initial state.
        # The current_state propertly will be updated to reflect the current state at which the FSM stops at each step.
        self.current_state = initial_state
        # Initialize the states attribute with the initial state.
        self.states = {initial_state.name: initial_state}

    def add_state(self, state):
        """
        Add a state to the FSM.
            state: A State object.
        """
        if not isinstance(state, State):
            raise TypeError("state must be an instance of State.")
        if state.name in self.states:
            raise ValueError(f"A state with the name '{state.name}' already exists.")

        # Add a new state to the states dictionary.        
        self.states[state.name] = state

    def add_transition(self, from_state_name, input_symbol, to_state_name):
        """
        Add a transition between states.
            from_state_name: Name of the source state.
            input_symbol: Input symbol for the transition.
            to_state_name: Name of the target state.
        """
        if from_state_name not in self.states:
            raise ValueError(f"Source state '{from_state_name}' does not exist.")
        if to_state_name not in self.states:
            raise ValueError(f"Target state '{to_state_name}' does not exist.")
        if not isinstance(input_symbol, int):
            raise ValueError("Input symbol must be an integer.")

        # Add a transition from from_state to to_state given the input input_symbol.
        from_state = self.states[from_state_name]
        to_state = self.states[to_state_name]
        # Update the transitions attribute of the state to reflect the next state given the input input_symbol.
        from_state.add_transition(input_symbol, to_state)

    def process_input(self, input_sequence):
        """
        Process an input sequence and determine the final state.
            input_sequence: A list of input symbols.
        return: The final state after processing the input sequence.
        """
        if not hasattr(input_sequence, "__iter__"):
            raise TypeError("Input sequence must be iterable.")
        if not input_sequence:
            raise ValueError("Input sequence cannot be empty.")

        # Loop through the input sequence until reaching a final state.
        for input_symbol in input_sequence:
            next_state = self.current_state.get_next_state(input_symbol)
            if next_state is None:
                raise ValueError(f"No transition for input '{input_symbol}' from state '{self.current_state.name}'.")
            # Update the current_state attribute of the FSM.
            self.current_state = next_state
        return self.current_state

    def is_accepting(self):
        """
        Check if the current state is an accepting state.
        return: True if the current state is accepting, False otherwise.
        """

        # Return the is_accepting property of the current state.
        return self.current_state.is_accepting

class ModThreeFSM(FSM):
    """Finite State Machine to solve the mod-three problem."""
    def __init__(self):
        # Create the three states representing remainders 0, 1, and 2
        # The state name must have 2 components: 1) A character 2) An integer.
        # The integer defines the remainder value.
        s0 = State("S0", is_accepting=True) # Remainder 0
        s1 = State("S1", is_accepting=True) # Remainder 1
        s2 = State("S2", is_accepting=True) # Remainder 2

        # Initialize the FSM with the initial state being S0
        super().__init__(s0)

        # Add the states to the FSM
        self.add_state(s1)
        self.add_state(s2)

        # Add transitions for binary input (0 and 1)
        # S0 transitions
        s0.add_transition(0, s0) # 0 -> state 0
        s0.add_transition(1, s1) # 1 -> state 1

        # S1 transitions
        s1.add_transition(0, s2) # 0 -> state 2
        s1.add_transition(1, s0) # 1 -> state 0

        # S2 transitions
        s2.add_transition(0, s1) # 0 -> state 1
        s2.add_transition(1, s2) # 1 -> state 2

    def process_three_mod_input(self, input_sequence):
        """
        Process the input sequence and return the state reflecting the remainder of sum divided by 3.
            input_sequence: A list of binary numbers (0 or 1).
        return: The state object.
        """

        if not type(input_sequence) is list:
            raise TypeError(f"Input sequence must be a list but {type(input_sequence)} found.")
        for val in input_sequence:
            if not isinstance(val, int):
                raise TypeError(f"Each input in the sequence must be an integer but the input {val} of type {type(val)} found.")
            if not val in [0, 1]:
                raise TypeError(f"Each input value must be binary (0 or 1) but the value {val} found.")

        # Process the input sequence.
        final_state = self.process_input(input_sequence)

        # Return the remainder.
        return int(final_state.name[1:])

    def binary_to_decimal(input_sequence):
        """
        Returns the decimal value out of the binary sequence.
            input_sequence: A list of binary numbers (0 or 1).
        return: The decimal value.
        """
        return sum(bit * (2 ** idx) for idx, bit in enumerate(reversed(input_sequence)))
