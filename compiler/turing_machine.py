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

    def sort(self):
        pass

# -- high level methods --
    
    # compares a pair of characters between two hex numbers A and B and forwards on to another pair comparison,
    # either between (A and B) or (B and C), or otherwise breaks to continue bubble sorting
    def compare(self):
        '''
        Start comparing from given position
        For all possible values of An
            Move -> 17 to Bn
                for each step check if on ]
                    char == ]
                        break and return to start of list to bubble again
                    char != ]
                        continue moving
                An > Bn
                    Move <- 17 - i to An
                    Swap from this char onwards through the word
                An == Bn
                    Move <- 17 - (n + 1) to A(n+1)
                    Next comparison (recursive call)
                An < Bn
                    Move <- to B0
                    Next comparison (recursive call)  
        '''

        # consider any possible character
        for char in self.hex_chars:
            self.current_state = "compare"
            state_id = self.__get_state_id()

            # move 17 from An to Bn remembering An for comparison
            # check every step whether we're at the end of the list (in which case we do something else)
            for i in range(16, 0, -1):
                new_state = f"id{state_id}_move_forward_{i}_remember_{char}"
                self.__write_state(self.current_state, "0 1 2 3 4 5 6 7 8 9 A B C D E F ,", "→", "", new_state)
                self.__write_state(self.current_state, "]", "←", "", "<BREAK/LOOP> ------------------- TODO ----------------------")
                self.current_state = new_state

            remembered_char = self.current_state[-1]  # char final char of state by our established convention
            remembered_char_state = self.current_state  # cache current state for following branching decisions

            # - compare -
            # An > Bn
            # don't want blank accepted chars (none less than 0)
            if remembered_char != "0":
                new_state = f"id{state_id}_swap_required"
                self.__write_state(remembered_char_state, self.get_less_than_hex_char(remembered_char), "←", "", new_state)
                self.current_state = new_state
                # move <- to Ai (already moved back one in prev step so 16 not 17)
                self.move(-16, "swap")

            # An < Bn
            # don't want blank accepted chars (none greater than F)
            if remembered_char != "F":
                new_state = f"id{state_id}_no_swap_required"
                self.__write_state(remembered_char_state, self.get_greater_than_hex_char(remembered_char), "→", "", new_state)
                self.current_state = new_state
                # move <- B0 for next comparison
                self.move(-i - 1, "compare")

            # Ai == Bi
            new_state = f"id{state_id}_compare_next_char_pair"
            self.__write_state(remembered_char_state, remembered_char, "←", "", new_state)
            self.current_state = new_state
            # move <- to A(i+1)
            self.move(-15, "compare")

    # swaps a pair of characters between two hex numbers A and B and forwards on to another pair swap or 
    # on to the next comparison of hex nums B and C
    def swap(self):
        '''
        Assume current char is first swap
        Loop until , or ]
            Remember Ai
            Move -> 17 to Bi
            Remember Bi and write Ai
            Move <- 17 to Ai
            Write Bi
            Move -> 1 to Ai+1
            Ai+1 == , (will never be ] since we know there is a B number)
                Move -> 1 to B0
                Begin next comparison of B and C (recursion base case)
            Ai+1 != ,
                Begin next swap recursively
        '''

        self.current_state = "swap"

        # remember Ai, Move -> 17 to Bi
        loop_state = f"swap_loop"
        A_variant_states = self.move_and_remember(17, f"{loop_state}_remember_A_and_overwrite_B")

        # Remember Bi and write Ai
        # account for all possible Bi chars to remember
        for char in self.hex_chars:
            for A_state in A_variant_states:
                remembered_A_char = A_state[-1]
                self.current_state = f"{loop_state}_overwrote_B_remember_B_{char}"
                self.__write_state(A_state, char, "→", remembered_A_char, self.current_state)

            # move <- 17 to Ai (and compensate for write move hence 18)
            self.move(-18, f"{loop_state}_overwrite_A_with_B_{char}")

            # overwrite Ai as Bi and move -> 1 to Ai+1
            self.__write_state(f"{loop_state}_overwrite_A_with_B_{char}", " ".join(self.hex_chars), "→", char, f"{loop_state}_check_for_separator")

        # Ai+1 == ,  Move -> 1 to B0, begin next comparison
        self.__write_state(f"{loop_state}_check_for_separator", ",", "→", "", "compare")
        # Ai+1 != ,  Begin next char pair swap from here
        self.__write_state(f"{loop_state}_check_for_separator", " ".join(self.hex_chars), "→", "", f"{loop_state}_setup_next_swap")
            # undo previous move forward when checking no comma
        self.__write_state(f"{loop_state}_setup_next_swap", self.all_chars, "←", "", "swap")

            

# -- macros --

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

# -- helper methods --

    # returns space separated string of hex characters greater than give char
    def get_greater_than_hex_char(self, char: str) -> str:
        i = self.hex_chars.index(char)
        return " ".join(self.hex_chars[i+1:])

    def get_less_than_hex_char(self, char: str) -> str:
        i = self.hex_chars.index(char)
        return " ".join(self.hex_chars[:i])

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