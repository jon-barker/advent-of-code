# PART I

with open("input.txt", "r") as f:
    input = f.read()

parsed = ""
new = False
for i, c in enumerate(input):
    if c in '-0123456789':
        if new:
            parsed += " "
            new = False
        parsed += c
    else:
        new = True   

num_list = [int(p) for p in parsed.split(" ")[1:]]
print(sum(num_list))

# PART II
