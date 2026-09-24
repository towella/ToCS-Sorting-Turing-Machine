from random import randint

def generate_hex_num(length: int):
    characters = "0123456789ABCDEF"
    num = ""
    for i in range(length):
        num += characters[randint(0, len(characters)-1)]
    return num


num = int(input("How many items in the list? "))

output = []
for i in range(num):
    output.append(generate_hex_num(16))

print(f"Unsorted: [{",".join(output)}]")
output.sort()
print(f"Sorted:   [{",".join(output)}]")


'''
old failing test cases:
[]  <- edge case (resolved)
[ABA0904C15399F42,C3EBFFFC09189593,7A0D72AA72F64EF3]  <- programming bug (resolved)
[8935D7F144F3F3E0,D87F4551DA17DB4C,3121E14D7DCE1F3C,089679F20570C007,49C1A4B80A21AFFC,E60868A1035193B9,3DDDC9E654B4E6F1,27ED214EB7619026,43FA4897AB7D907B,0471F41E09E4283A]  <- takes a long time but succeeds (21527 steps)
'''
