from fsm import ModThreeFSM

# Instantiate the mod 3 FSM
mod_three_fsm = ModThreeFSM()

# Example binary input sequences
# Decimal: 4, not divisible by 3 with remainder 1.
binary_sequence = [1, 0, 0]
# Decimal: 6, divisible by 3 with remainder 0.
# binary_sequence = [1, 1, 0]
# Decimal: 11, not divisible by 3 with remainder 2.
# binary_sequence = [1, 0, 1, 1]

# Check divisibility
remainder = mod_three_fsm.process_three_mod_input(binary_sequence)
decimal = ModThreeFSM.binary_to_decimal(binary_sequence)
print(f"Mod 3 remainder of {decimal} is {remainder}")
