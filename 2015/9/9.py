import csv
from itertools import permutations

cities = set()
dists = {}
with open("2015/9/input.txt", "r") as f:
    reader = csv.reader(f, delimiter=' ')
    for row in reader:
        cities.add(row[0])
        cities.add(row[2])
        dists[(row[0], row[2])] = int(row[-1])
        dists[(row[2], row[0])] = int(row[-1])

# PART I 

shortest_path = float('inf')
for perm in permutations(cities):
    path = sum([dists[(a, b)] for (a, b) in zip(perm[:-1], perm[1:])])
    shortest_path = min(path, shortest_path) 

print(shortest_path)

# PART II

longest_path = 0
for perm in permutations(cities):
    path = sum([dists[(a, b)] for (a, b) in zip(perm[:-1], perm[1:])])
    longest_path = max(path, longest_path) 

print(longest_path)

