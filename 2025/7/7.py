# PART I 

with open("input.txt", "r") as f:
    grid = [l.rstrip('\n') for l in f.readlines()]
    grid = [[c for c in line] for line in grid]

prev = grid[0]
splits = 0
for row in grid[1:]:
    for c_idx in range(len(row)):
        if prev[c_idx] in ['S', '|'] and row[c_idx] == '.':
            row[c_idx] = '|'
        elif prev[c_idx] == '|' and row[c_idx] =='^':
            row[c_idx - 1] = '|'
            row[c_idx + 1] = '|'
            splits += 1
    prev = row
print(splits)

# PART II

with open("input.txt", "r") as f:
    grid = [l.rstrip('\n') for l in f.readlines()]

from functools import lru_cache

@lru_cache(None)
def new_timeline(curr, rest, cols):
    if rest == '.' * cols:
        return 1
    children = 0
    for c in range(cols):
        if curr[c] in ('S','|') and rest[c] == '.':
            newrest = rest[:c] + '|' + rest[c+1:]
            children += new_timeline(newrest[:cols], newrest[cols:], cols)
        elif curr[c] == '|' and rest[c] == '^':
            if c-1 >= 0 and rest[c-1] == '.':
                newrest = rest[:c-1] + '|' + rest[c:]
                children += new_timeline(newrest[:cols], newrest[cols:], cols)
            if c+1 < cols and rest[c+1] == '.':
                newrest = rest[:c+1] + '|' + rest[c+2:]
                children += new_timeline(newrest[:cols], newrest[cols:], cols)
    return children

total_worlds = new_timeline(grid[0], ''.join(grid[1:]), len(grid[0]))
print(total_worlds)