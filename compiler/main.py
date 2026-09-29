from turing_machine import TuringMachine

tm = TuringMachine("compare")

# create program states
tm.compare() # kim's todo: i think this needs to be adjusted if im passing in a swap/no swap state
tm.swap()
tm.advance_sorted_boundary()
tm.sort_completed_reset_list_and_end()

# Once program is finished, write to file
tm.output_to_file()
