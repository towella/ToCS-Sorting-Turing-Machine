from turing_machine import TuringMachine

tm = TuringMachine("<first state here (state to move into first), e.g. compare>")


tm.move_forward_n(4, "test1")
tm.move_backward_n(1, "test2")





# Once program is finished, write to file
tm.output_to_file()
