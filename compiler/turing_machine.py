import os

class TuringMachine:
    def __init__(self, first_state: str):
        # allows duplicate states to be created with different transitions out
        # e.g. id2_move_forward_4 transitions eventually into <compare2>
        #      id3_move_forward_4 transitions eventually into <swap3>
        # without a unique id to differentiate, they would conflict, breaking the DFA
        self.unique_state_id = 0
        self.states = []  # list of all the rows in the turing machine
        self.current_state = "⎆"  # keep track of the current TM state (for writing etc)
        self.all_chars = "0 1 2 3 4 5 6 7 8 9 A B C D E F [ ] ,"
        self.hex_chars = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
        self.__write_start_state(first_state)  # start state

# -- high level methods --
    
    def compare(self):
        '''
        Start at A0 (word A, index 0):
        For i in (0 to 15)
            Remember Ai
            Move -> 17 - (i + 1)
                char == ]
                    end of list (break/loop)
                char != ]
                    Move -> 1 to Bi
                Bi <= Ai
                    Move <- 17 - (i + 1) to A(i+1)
                    next i
                Bi > Ai
                    Move <- 17 - i to Ai
                    Break and swap from this char onwards through the word
        '''
        # loop_state_id = self.__get_state_id()
        # for i in range(15):
        #     loop_state = f"id{loop_state_id}_compare_loop_{i}"
        #     self.move(17 - (i + 1), loop_state, True)
        pass

    def swap(self):
        pass

# -- helper macros --

     # next state is the state to go into after moving is complete
    def move(self, steps: int, next_state: str) -> None:
        if steps != 0:
            move_char = "→" if steps > 0 else "←"
            state_direction = "forward" if steps > 0 else "backward"
            state_id = self.__get_state_id()
            steps = abs(steps)

            # move on any character
            for n in range(steps-1, 0, -1):  # decrememnt loop
                next_move_state = f"id{state_id}_move_{state_direction}_{n}"
                self.__write_state(self.current_state, self.all_chars, move_char, "", next_move_state)
                self.current_state = next_move_state
            # final move transitions into next state
            self.__write_state(self.current_state, self.all_chars, move_char, "", next_state)
            self.current_state = next_state

        else:
            raise Exception("0 steps is not allowed when moving. Must be some positive or negative number of steps")

    # returns all states that should be accounted for (one for each character in format <next_state>_<char>)
    # current state transitions/diverges into 16 variants of next_state
    # current state must be handled outside method as it could be one of 16 states
    def move_and_remember(self, steps: int, next_state: str) -> list[str]:
        if steps != 0:
            start_state = self.current_state
            state_id = self.__get_state_id()
            move_char = "→" if steps > 0 else "←"
            state_direction = "forward" if steps > 0 else "backward"
            steps = abs(steps)

            # make duplicate states for each possible char (since we don't know what char we'll get and must account for all)
            for char in self.hex_chars:
                state_tail = f"remember_{char}"

                # single step: move only on given character straight into next state
                if steps == 1:
                    self.__write_state(start_state, char, move_char, "", f"{next_state}_{char}")

                # any other number of states
                else:
                    for n in range(steps-1, 0, -1):  # decrememnt loop
                        next_move_state = f"id{state_id}_move_{state_direction}_{n}_{state_tail}"

                        if n == steps-1:  # for the first step
                            # only accept char we're remembering at start
                            self.__write_state(start_state, char, move_char, "", next_move_state)
                        else:
                            # continue to move on any char now we know what car we're remembering
                            self.__write_state(self.current_state, self.all_chars, move_char, "", next_move_state)
                        self.current_state = next_move_state
                    # final move transitions into next state
                    self.__write_state(self.current_state, self.all_chars, move_char, "", f"{next_state}_{char}")

            self.current_state = next_state  # current state must be updated outside method
            return [f"{next_state}_{char}" for char in self.hex_chars]
        
        else:
            raise Exception("0 steps is not allowed when moving and remembering. Must be some positive or negative number of steps")

    # the turing machine writes to the input string tape
    # does not move the head unit. Only writes to the tape and changes to next given state
    # creates variant of current state for every possible writable character (since we don't know what we're writing)
    # they all transition/converge to the same state (next_state)
    def stationary_tape_write(self, next_state: str) -> None:
        state_id = self.__get_state_id()
        for char in self.hex_chars:
            temp_state = f"id{state_id}_{self.current_state}_write_{char}"
            # write to tape and move (must move)
            self.__write_state(f"{self.current_state}_{char}, self.all_chars, "→", char, temp_state)
            # undo move from previous step
            self.__write_state(temp_state, self.all_chars, "←", "", next_state)
        self.current_state = next_state

    # returns to cell 0 and returns accept state
    def end_as_sort_completed(self) -> None:
        '''
        if char == [
            halt accept
        else
            loop -- halt and accept if [
                move backwards
        '''
        all_chars_exclude_open_square_bracket = "0 1 2 3 4 5 6 7 8 9 A B C D E F ] ,"
        # already cell 0
        self.__write_state(self.current_state, "[", "⏹", "", "✔")

        # loop move backward
        self.__write_state(self.current_state, all_chars_exclude_open_square_bracket, "←", "", "end_and_accept")
        self.__write_state("end_and_accept", all_chars_exclude_open_square_bracket, "←", "", "end_and_accept")

        # end loop at cell 0
        self.__write_state("end_and_accept", "[", "⏹", "", "✔")

# -- private methods --

    # internal class method just for writing to the output file
    def __write_state(self, current_state: str, current_symbol: str, move: str, next_symbol: str, next_state: str) -> None:
        self.states.append([current_state, current_symbol, move, next_symbol, next_state])

    # moves to first digit of first hex number in list
    def __write_start_state(self, next_state: str) -> None:
        self.__write_state("⎆", "[", "→", "", next_state)
        self.current_state = next_state

    def __get_state_id(self) -> int:
        self.unique_state_id += 1
        return self.unique_state_id - 1

# -- out to file --

    def output_to_file(self) -> None:
        output_path = os.path.join(os.path.dirname(__file__), "..", "turing-machine-output.tsv")
        with open(output_path, "w", encoding="utf-8") as f:
            for state in self.states:
                f.write("\t".join(state))
                f.write("\n")