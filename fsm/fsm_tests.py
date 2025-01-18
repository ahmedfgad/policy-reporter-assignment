import unittest

from fsm import State, FSM, ModThreeFSM

class TestState(unittest.TestCase):
    def test_large_number_of_transitions(self):
        state = State("S1")
        next_states = [State(f"S{i}") for i in range(1, 101)]
        for i, next_state in enumerate(next_states):
            state.add_transition(i, next_state)

        for i, next_state in enumerate(next_states):
            self.assertEqual(state.get_next_state(i), next_state)

        # Out-of-range transition
        self.assertIsNone(state.get_next_state(101))

    def test_transition_with_edge_values(self):
        s1 = State("S1")
        s2 = State("S2")
        s1.add_transition(-1, s2)  # Negative transition
        s1.add_transition(0, s2)   # Zero transition
        s1.add_transition(2**31-1, s2)  # Max int transition

        self.assertEqual(s1.get_next_state(-1), s2)
        self.assertEqual(s1.get_next_state(0), s2)
        self.assertEqual(s1.get_next_state(2**31-1), s2)

    def test_state_initialization(self):
        state = State("S1", is_accepting=True)
        self.assertEqual(state.name, "S1")
        self.assertTrue(state.is_accepting)
        self.assertEqual(state.transitions, {})

        with self.assertRaises(ValueError):
            State("", is_accepting=True)
        with self.assertRaises(ValueError):
            State("S1", is_accepting="not_boolean")

    def test_add_transition(self):
        s1 = State("S1")
        s2 = State("S2")

        s1.add_transition(0, s2)
        self.assertEqual(s1.transitions[0], s2)

        with self.assertRaises(ValueError):
            # Duplicate transition
            s1.add_transition(0, s2)
        with self.assertRaises(ValueError):
            # The transition input is not an integer.
            s1.add_transition("not_int", s2)
        with self.assertRaises(TypeError):
            # The transition next state is not an object of the State class.
            s1.add_transition(1, "not_a_state")

    def test_get_next_state(self):
        s1 = State("S1")
        s2 = State("S2")
        s1.add_transition(0, s2)

        self.assertEqual(s1.get_next_state(0), s2)
        self.assertIsNone(s1.get_next_state(1))

class TestFSM(unittest.TestCase):
    def setUp(self):
        self.s0 = State("S0", is_accepting=False)
        self.s1 = State("S1", is_accepting=True)
        self.s2 = State("S2", is_accepting=False)
        self.fsm = FSM(self.s0)
        self.fsm.add_state(self.s1)
        self.fsm.add_state(self.s2)

    def test_long_input_sequence(self):
        self.fsm.add_transition("S0", 0, "S1")
        self.fsm.add_transition("S1", 1, "S2")
        self.fsm.add_transition("S2", 0, "S0")

        final_state = self.fsm.process_input([0, 1, 0, 0, 1, 0])
        # Cycles back to S0
        self.assertEqual(final_state.name, "S0")

    def test_is_accepting(self):
        self.fsm.add_transition("S0", 0, "S1")
        self.assertFalse(self.fsm.is_accepting())
        self.fsm.process_input([0])
        self.assertTrue(self.fsm.is_accepting())

    def test_resetting_fsm(self):
        self.fsm.add_transition("S0", 0, "S1")
        self.fsm.process_input([0])
        self.assertEqual(self.fsm.current_state, self.s1)
        self.fsm.current_state = self.s0
        self.assertEqual(self.fsm.current_state, self.s0)

    def test_fsm_initialization(self):
        self.assertEqual(self.fsm.current_state, self.s0)
        self.assertIn("S0", self.fsm.states)
        self.assertIn("S1", self.fsm.states)

        with self.assertRaises(TypeError):
            FSM("not_a_state")

    def test_add_transition(self):
        self.fsm.add_transition("S0", 0, "S1")
        self.assertEqual(self.s0.get_next_state(0), self.s1)

        with self.assertRaises(ValueError):
            self.fsm.add_transition("non_existent", 0, "S1")
        with self.assertRaises(ValueError):
            self.fsm.add_transition("S0", 0, "non_existent")

    def test_process_input(self):
        self.fsm.add_transition("S0", 0, "S1")
        self.assertEqual(self.fsm.process_input([0]), self.s1)

        with self.assertRaises(ValueError):
            self.fsm.process_input([1])  # No transition defined for input 1

class TestModThreeFSM(unittest.TestCase):
    def setUp(self):
        self.mod_fsm = ModThreeFSM()

    def test_mod_three_long_input_sequence(self):
        result = self.mod_fsm.process_three_mod_input([1, 0, 1, 1, 0, 1, 1, 0, 1, 1])
        # 731 (mod 3) = 2
        self.assertEqual(result, 2)

    def test_math_remainder_equal_fsm_remainder(self):
        input_sequence = [1, 0, 1, 1, 0, 0]
        # 43 (mod 3) = 1
        self.assertEqual(self.mod_fsm.process_three_mod_input(input_sequence), ModThreeFSM.binary_to_decimal(input_sequence)%3)

    def test_empty_input_sequence(self):
        with self.assertRaises(ValueError):
            self.mod_fsm.process_three_mod_input([])

    def test_invalid_input_format(self):
        with self.assertRaises(TypeError):
            # Non-list input
            self.mod_fsm.process_three_mod_input("101")
        with self.assertRaises(TypeError):
            # String in list
            self.mod_fsm.process_three_mod_input([1, "0", 1])
        with self.assertRaises(TypeError):
            # Non-binary input
            self.mod_fsm.process_three_mod_input([1, 2, 1])
        with self.assertRaises(TypeError):
            # Non-binary input
            self.mod_fsm.process_three_mod_input([2])
        with self.assertRaises(TypeError):
            # Input sequence is not a list.
            self.mod_fsm.process_three_mod_input("not_a_list")

    def test_mod_three_initialization(self):
        self.assertEqual(self.mod_fsm.current_state.name, "S0")
        self.assertTrue(self.mod_fsm.states["S0"].is_accepting)

    def test_process_three_mod_input(self):
        # Binary 011 = 3, mod 3 = 0
        self.assertEqual(self.mod_fsm.process_three_mod_input([0, 1, 1]), 0)
        # Binary 10 = 2, mod 3 = 2
        self.assertEqual(self.mod_fsm.process_three_mod_input([1, 0]), 2)

    def test_binary_to_decimal(self):
        self.assertEqual(ModThreeFSM.binary_to_decimal([1, 0, 1]), 5)
        self.assertEqual(ModThreeFSM.binary_to_decimal([0, 1]), 1)
        # Edge cases
        # Single 0
        self.assertEqual(ModThreeFSM.binary_to_decimal([0]), 0)
        # Single 1
        self.assertEqual(ModThreeFSM.binary_to_decimal([1]), 1)
        # Leading 1, binary for 8
        self.assertEqual(ModThreeFSM.binary_to_decimal([1, 0, 0, 0]), 8)
        # All zeros
        self.assertEqual(ModThreeFSM.binary_to_decimal([0, 0, 0, 0]), 0)

    def test_binary_to_decimal_large_numbers(self):
        # Binary with 30 ones
        large_binary = [1] * 30
        self.assertEqual(ModThreeFSM.binary_to_decimal(large_binary), 2**30 - 1)

    def test_mod_three_with_large_input(self):
        # Alternating binary digits, length 100
        long_input = [1, 0] * 20
        # Sum is divisible by 3
        self.assertEqual(self.mod_fsm.process_three_mod_input(long_input), 1)

if __name__ == "__main__":
    unittest.main()
