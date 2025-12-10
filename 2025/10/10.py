import itertools
import pulp
import numpy as np

with open("input.txt", "r") as f:
    data = f.readlines()

data = [d.strip('\n').split(' ') for d in data]

# PART I 
total = 0
for i, d in enumerate(data):
    # get target vector
    target = d[0][1:-1]
    target = [1 if c == '#' else 0 for c in target]
    target = np.array(target)
    # get switches
    switches = []
    for s in d[1:-1]:
        switch = np.zeros((target.shape[0]))
        for t in s[1:-1].split(','):
            switch[int(t)] = 1
        switches.append(switch)
    switches = np.array(switches)
    found = False
    length = 1
    while not found:
        for chosen in itertools.product(list(range(switches.shape[0])), repeat=length):
            mult = np.zeros((switches.shape[0]))
            for c in chosen:
                mult[c] = 1
            out = np.matmul(mult, switches)
            out = out % 2
            if (out == target).all():
                found = True
                total += length
                break
        length += 1
    print(f"{i} of {len(data)}")

print(total)

# PART II 
total = 0
for i, d in enumerate(data):
    # get target vector
    target = d[-1][1:-1].split(',')
    target = [int(t) for t in target]
    target = np.array(target)
    # get switches
    switches = []
    for s in d[1:-1]:
        switch = np.zeros((target.shape[0]))
        for t in s[1:-1].split(','):
            switch[int(t)] = 1
        switches.append(switch)
    switches = np.array(switches)

    # used an off-the-shelf ILP solver because I don't want to write that myself
    model = pulp.LpProblem('Ax=b', pulp.LpMinimize)

    # integer nonnegative variables
    x_vars = [pulp.LpVariable(f'x{i}', lowBound=0, cat='Integer')
            for i in range(switches.shape[0])]

    # objective: minimize sum of x_vars
    model += pulp.lpSum(x_vars)

    # constraints: for each row r of switches, sum_j switches[j, r]*x_j == target[r]
    for r in range(switches.shape[1]):
        model += (pulp.lpSum(switches[j, r] * x_vars[j]
                            for j in range(switches.shape[0])) == target[r])

    model.solve()
    solution = [int(v.value()) for v in x_vars]
    total += sum(solution)

    print(f"{i} of {len(data)}")

print(total)
