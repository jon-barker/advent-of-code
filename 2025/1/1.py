# PART I
position = 50
zeros = 0

with open("input.txt", "r") as f:
    for line in f.readlines():
        steps = int(line[1:])
        position = (position - steps) if line[0] == 'L' else (position + steps) 
        position = position % 100
        if position == 0:
            zeros += 1
print(zeros)

# PART II
position = 50
zeros = 0

with open("input.txt", "r") as f:
    for line in f.readlines():
        steps = int(line[1:])
        for _ in range(steps):
            position = (position - 1) if line[0] == 'L' else (position + 1) 
            position = position % 100
            if position == 0:
                zeros += 1
print(zeros)
