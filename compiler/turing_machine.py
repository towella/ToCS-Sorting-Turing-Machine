import os

class TuringMachine:
    def __init__(self, first_state: str):
        self.states = []  # list of all the rows in the turing machine
        self.current_state = "⎆"  # keep track of the current TM state (for writing etc)
        self.__write_start_state(first_state)  # start state

# -- high level methods --
    
    def compare():
        pass

    def swap():
        pass

# -- helper macros --

     # next state is the state to go into after moving is complete
    def move(self, steps: int, next_state: str, remember: str = "") -> None:
        if steps != 0:
            allowed_chars_for_move = "0 1 2 3 4 5 6 7 8 9 A B C D E F [ ] ,"
            move_char = "→" if steps > 0 else "←"
            state_direction = "forward" if steps > 0 else "backward"
            state_tail = f"_remember_{remember}" if remember else ""
            steps = abs(steps)

            # move
            for n in range(steps-1, 0, -1):  # decrememnt loop
                next_move_state = f"move_{state_direction}_{n}{state_tail}"
                self.__write_state(self.current_state, allowed_chars_for_move, move_char, "", next_move_state)
                self.current_state = next_move_state
            # final move transitions into next state
            self.__write_state(self.current_state, allowed_chars_for_move, move_char, "", next_state)
            self.current_state = next_state

        else:
            raise Exception("0 steps is not allowed when moving. Must be some positive or negative number of steps")
            
    # the turing machine writes to the input string tape
    # TODO: workout params
    def write_tape(self):
        pass

# -- private methods --

    # internal class method just for writing to the output file
    def __write_state(self, current_state: str, current_symbol: str, move: str, next_symbol: str, next_state: str) -> None:
        self.states.append([current_state, current_symbol, move, next_symbol, next_state])

    def __write_start_state(self, next_state: str) -> None:
        self.__write_state("⎆", "[", "→", "", next_state)
        self.current_state = next_state

# -- out to file --

    def output_to_file(self) -> None:
        output_path = os.path.join(os.path.dirname(__file__), "..", "turing-machine-output.tsv")
        with open(output_path, "w", encoding="utf-8") as f:
            for state in self.states:
                f.write("\t".join(state))
                f.write("\n")