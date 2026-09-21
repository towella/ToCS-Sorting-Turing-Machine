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
    allowedCharsForMove = "0 1 2 3 4 5 6 7 8 9 A B C D E F [ ] ,"

    # next state is the state to go into after moving is complete
    def move_forward_n(self, steps: int, next_state: str) -> None:
        if steps > 0:
            # move
            for n in range(steps-1, 0, -1):  # decrement loop
                next_move_state = f"move_forward_{n}"
                self.__write_state(self.current_state, self.allowedCharsForMove, "→", "", next_move_state)
                self.current_state = next_move_state
            # final move transitions into next state
            self.__write_state(self.current_state, self.allowedCharsForMove, "→", "", next_state)
            self.current_state = next_state
        else:
            raise Exception("Steps must be > 0 when moving forward n")

    def move_backward_n(self, steps: int, next_state: str) -> None:
        if steps > 0:
            # move
            for n in range(steps-1, 0, -1):
                next_move_state = f"move_backward_{n}"
                self.__write_state(self.current_state, self.allowedCharsForMove, "←", "", next_move_state)
                self.current_state = next_move_state
            # final move transitions into next state
            self.__write_state(self.current_state, self.allowedCharsForMove, "←", "", next_state)
            self.current_state = next_state
        else:
            raise Exception("Steps must be > 0 when moving backward n")
        

    def move_forward_n_remember_x(self, steps: int, remember: str, next_state: str) -> str:
        if steps > 0:
            # move
            for n in range(steps-1, 0, -1):
                next_move_state = f"move_forward_{n}_remember_{remember}"
                self.__write_state(self.current_state, self.allowedCharsForMove, "→", "", next_move_state)
                self.current_state = next_move_state
            # final move transitionts into next state
            self.__write_state(self.current_state, self.allowedCharsForMove, "→", "", next_state)
            self.current_state = next_state
        else:
            raise Exception("Steps must be > 0 when moving forward n and remembering x")
        

    def move_backward_n_remember_x(self, steps: int, remember: str, next_state: str) -> str:
        if steps > 0:
            # move
            for n in range(steps-1, 0, -1):
                next_move_state = f"move_backward_{n}_remember_{remember}"
                self.__write_state(self.current_state, self.allowedCharsForMove, "←", "", next_move_state)
                self.current_state = next_move_state
            # final move transitionts into next state
            self.__write_state(self.current_state, self.allowedCharsForMove, "←", "", next_state)
            self.current_state = next_state
        else:
            raise Exception("Steps must be > 0 when moving")
            

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