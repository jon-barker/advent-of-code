import csv
import itertools
from math import floor, log10

# Open and read the file
test_values = []
operands = []
count = 0
with open('7/input.txt', 'r') as file:
    reader = csv.reader(file) 
    for row in reader:
        row = row[0].split(':')
        test_value = int(row[0])
        operands = [int(r) for r in row[1].split(' ')[1:]]
        for ops in itertools.product((0,1), repeat=len(operands)-1):
            total = operands[0]
            for op_idx, op in enumerate(ops):
                if op == 0:
                    total += operands[op_idx + 1] 
                elif op == 1:
                    total *= operands[op_idx + 1]
                if total > test_value:
                    break
            if total == test_value:
                count += total
                break

print(count)

# Pre-read file
with open('7/input.txt') as f:
    lines = f.readlines()

# Open and read the file
count = 0
step = 0
for line in lines:
    print(step)
    step += 1
    parts = line.strip().split(':')
    test_value = int(parts[0])
    operands = list(map(int, parts[1].split()))
    for ops in itertools.product((0,1,2), repeat=len(operands)-1):
        total = operands[0]
        valid = True
        for op, val in zip(ops, operands[1:]):
            if op == 0:
                total += val
            elif op == 1:
                total *= val
            elif op == 2:
                total = total * (10 ** (floor(log10(val))+1)) + val
            if total > test_value:
                valid = False
                break

        if valid and total == test_value:
            count += total
            break

print(count)
