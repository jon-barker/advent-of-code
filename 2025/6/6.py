import numpy as np

# PART I

with open("input.txt", "r") as f:
    lines = [line.rstrip("\n") for line in f if line.strip() != ""]
    lines = [l.split(' ') for l in lines]
    lines = [[ch for ch in line if ch != ''] for line in lines]
    nums = lines[:-1]
    nums = np.array([[int(n) for n in line] for line in nums])
    ops = lines[-1]

grand_total = 0
for i, op in enumerate(ops):
    if op == '*':
        total = 1
        for n in nums[:, i]:
            total *= n
    elif op == '+':
        total = 0
        for n in nums[:, i]:
            total += n
    grand_total += total

print(grand_total)

# PART II

with open("input.txt", "r") as f:
    lines = [line.rstrip("\n") for line in f if line.strip() != ""]
    lines = [[ch for ch in line if ch != ''] for line in lines]
    current_op = None
    grand_total = 0
    op_total = 0
    new_problem = False
    for i in range(len(lines[0])):
        if new_problem or i == 0:
            if current_op is not None:
                grand_total += op_total
            current_op = lines[-1][i]
            if current_op == '*':
                op_total = 1
            elif current_op == '+':
                op_total = 0
            new_problem = False
        if all([row[i] == ' ' for row in lines]):
            new_problem = True
        else:
            if current_op == '*':
                nums = []
                for row in lines[:-1]:
                    if row[i] not in ['', ' ']:
                        nums.append(row[i])
                if len(nums) > 0:
                    num = int(''.join(nums))
                    op_total *= num
            elif current_op == '+':
                nums = []
                for row in lines[:-1]:
                    if row[i] not in ['', ' ']:
                        nums.append(row[i])
                if len(nums) > 0:
                    num = int(''.join(nums))
                    op_total += num
grand_total += op_total
print(grand_total)
