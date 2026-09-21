from turing_machine import TuringMachine

tm = TuringMachine("<first state here (state to move into first), e.g. compare>")


tm.move(4, "test1")
tm.move(-1, "test2")
tm.move(6, "test3", "0")
tm.move(-2, "test4", "bingbong")
tm.stationary_tape_write("b", "test5")




# Once program is finished, write to file
tm.output_to_file()
