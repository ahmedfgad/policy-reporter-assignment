from fsm import State, FSM

# Create the set of states Q
# is_accepting defines whether this is a final state or not.
s0 = State("S0", is_accepting=False)
s1 = State("S1", is_accepting=False)
s2 = State("S2", is_accepting=True)

# Create the Finite State Machine (FSM) object.
# Start state or Initial state
fsm = FSM(s0)

# Add states to the FSM
fsm.add_state(s1)
fsm.add_state(s2)

# Add transitions to the FSM
fsm.add_transition("S0", 0, "S0")
fsm.add_transition("S0", 1, "S1")
fsm.add_transition("S1", 0, "S2")
fsm.add_transition("S1", 1, "S0")
fsm.add_transition("S2", 0, "S1")
fsm.add_transition("S2", 1, "S2")

# Create the input sequence Segma
input_sequence = [1, 0, 1, 0, 1]

# Process input sequence
final_state = fsm.process_input(input_sequence)

if fsm.is_accepting():
    print(f"Final State: {final_state.name}")
else:
    print(f"The FSM stopped at the non-final state {final_state.name}")
