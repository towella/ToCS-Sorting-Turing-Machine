from turing_machine import TuringMachine

tm = TuringMachine("compare")
tm.compare()
tm.swap()

tm.move(4, "test1")
tm.move(2, "test1-5")
tm.move(-1, "test2")
tm.move_and_remember(1, "test3")
tm.move_and_remember(-3, "test4")
tm.stationary_tape_write("test5")
tm.end_as_sort_completed()

print(tm.get_greater_than_hex_char("0"))
print(tm.get_less_than_hex_char("0"))



# Once program is finished, write to file
tm.output_to_file()
