import csv
from itertools import product
import numpy as np

chars = {'.': 0, '#': 1}

# Open and read the file
locks = []
keys = []
with open('25/input.txt', 'r') as file:
    reader = csv.reader(file) 
    grid = []
    for row in reader:
        if len(row) == 0:
            if grid[0][0] == 1:
                locks.append(np.array(grid))
            elif grid[0][0] == 0: 
                keys.append(np.array(grid))
            grid = []
            continue
        else:
            grid.append([chars[r] for r in row[0]])
if grid[0][0] == 1:
    locks.append(np.array(grid))
elif grid[0][0] == 0: 
    keys.append(np.array(grid))

valid_combos = 0
for combo in product(locks, keys):
    if not ((combo[0] + combo[1]) == 2).any():
        valid_combos += 1
print(valid_combos)
