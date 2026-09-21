import os

class TuringMachine:
    def __init__(self):
        self.states = []  # list of all the rows in the turing machine
        self.current_state_num = 0  # increment each time a state is required
        self.__write_start_state()  # start state

# -- high level methods --
    
    def compare():
        pass

    def swap():
        pass

# -- helper macros --
    allowedCharsForMove = "0 1 2 3 4 5 6 7 8 9 A B C D E F [ ] ,"

    def move_forward_n(self, steps: int):
        if steps > 0:
            for n in range(steps):
                state = f"move_forward_{n}"
                next_state = f"move_forward_{n-1}"
                self.__write_state(state, self.allowedCharsForMove, "→", "", next_state)
                self.current_state_num += 1

    def move_backward_n(self, steps: int):
        if steps > 0:
            for n in range(steps):
                state = f"move_backward_{n}"
                next_state = f"move_backward_{n-1}"
                self.__write_state(state, self.allowedCharsForMove, "←", "", next_state)
                self.current_state_num += 1

    def move_forward_n_remember_x(self, steps: int, remember: str):
        if steps > 0:
            for n in range(steps):
                state = f"move_forward_{n}_remember_{remember}"
                next_state = f"move_forward_{n-1}_remember_{remember}"
                self.__write_state(state, self.allowedCharsForMove, "→", "", next_state)
                self.current_state_num += 1

    def move_backward_n_remember_x(self, steps: int, remember: str):
        if steps > 0:
            for n in range(steps):
                state = f"move_backward_{n}_remember_{remember}"
                next_state = f"move_backward_{n-1}_remember_{remember}"
                self.__write_state(state, self.allowedCharsForMove, "←", "", next_state)
                self.current_state_num += 1

    # the turing machine writes to the input string tape
    # TODO: workout params
    def write_tape(self):
        pass

# -- private methods --

    # internal class method just for writing to the output file
    def __write_state(self, current_state: str, current_symbol: str, move: str, next_symbol: str, next_state: str):
        self.states.append([current_state, current_symbol, move, next_symbol, next_state])

    def __write_start_state(self):
        pass
        #self.__write_state("⎆", "[", "")

# -- out to file --

    def output_to_file(self):
        output_path = os.path.join(os.path.dirname(__file__), "..", "turing-machine-output.tsv")
        with open(output_path, "w", encoding="utf-8") as f:
            for state in self.states:
                f.write("\t".join(state))
                f.write("\n")