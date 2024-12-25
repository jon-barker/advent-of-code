from copy import copy
from functools import lru_cache
import csv

# Open and read the file
targets = []
with open('19/input.txt', 'r') as file:
    reader = csv.reader(file, delimiter=',') 
    for i, row in enumerate(reader):
        if i == 0:
            avail = row
        elif i > 1:
            targets.append(row[0])
avail = [a.strip(' ') for a in avail]

# PART I
# you can't just use a greedy approach as you can end up at a dead-end
# for a case that is solvable with a different sequence of choices

@lru_cache(1000000)
def match_pattern(t):
    if t in avail:
        return True
    possible = False
    for a in avail:
        if t[:len(a)] == a:
            possible = possible or match_pattern(t[len(a):])
    return possible

possible = 0
for i, target in enumerate(targets):
    if match_pattern(target):
        possible += 1

print(possible)

# PART II
# now we need to keep track of all ways to make the pattern

@lru_cache(1000000)
def match_pattern_2(t):
    if len(t) == 0:
        return True, 1
    below = 0
    for a in avail:
        if t[:len(a)] == a:
            path_below, count = match_pattern_2(t[len(a):])
            if path_below:
                below += count
    if below == 0:
        return False, None
    else:
        return True, below

solutions = 0
for i, target in enumerate(targets):
    print(i)
    possible, paths = match_pattern_2(target)
    if possible:
        solutions += paths

print(solutions)
