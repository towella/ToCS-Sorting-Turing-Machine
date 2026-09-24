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