from collections import defaultdict
from itertools import product
import csv

# Open and read the file
graph = defaultdict(list)
with open('23/input.txt', 'r') as file:
    reader = csv.reader(file) 
    for row in reader:
        n1, n2 = row[0].split('-')
        graph[n1].append(n2)
        graph[n2].append(n1)

# PART I - brute force - way too slow...
# finds all possible triples and then checks if they're a clique
# triples = (tuple(sorted(t)) for t in product(graph.keys(), repeat=3) if len(set(t)) == len(t))
# unique_triples = set()
# from tqdm import tqdm
# for t in tqdm(triples):
#     unique_triples.add(t)

# cliques = set()
# seen = set()
# for t in tqdm(unique_triples):
#     t = tuple(t)
#     if t in seen:
#         continue
#     else:
#         seen.add(t)
#         if (
#             t[1] in graph[t[0]] and
#             t[2] in graph[t[0]] and
#             t[2] in graph[t[1]] 
#         ):
#             cliques.add(t)

# cliques = [c for c in cliques if (c[0][0] == 't' or c[1][0] == 't' or c[2][0] == 't')]
# print(len(cliques))

# second attempt using the algorithm of Chiba & Nishizeki (1985) described here:
# https://en.wikipedia.org/wiki/Clique_problem#Cliques_of_fixed_size

# no need to sort vertices by degree as they all have the same degree
cliques = set()
keys = graph.keys()
for v in keys:
    for n1 in graph[v]:
        for n2 in graph[n1]:
            if n2 in graph[v]:
                cliques.add(tuple(sorted([v, n1, n2])))

cliques = [c for c in cliques if (c[0][0] == 't' or c[1][0] == 't' or c[2][0] == 't')]
print(len(cliques))

# PART II - https://en.wikipedia.org/wiki/Bron–Kerbosch_algorithm
# implementation pretty much exactly follows the pseudocode from wikipedia

def bron_kerbosch(graph, R, P, X, cliques):
    if not P and not X:
        # Found a maximal clique
        cliques.append(R)
    else:
        for v in list(P):
            bron_kerbosch(
                graph,
                R.union({v}),
                P.intersection(graph[v]),
                X.intersection(graph[v]),
                cliques,
            )
            P.remove(v)
            X.add(v)

def largest_clique(graph):
    cliques = []
    bron_kerbosch(graph, set(), set(graph.keys()), set(), cliques)
    # Find the largest clique
    largest = 0
    for c in cliques:
        if len(c) > largest:
            largest_clique = ','.join(sorted(c))
            largest = len(c)
    return largest_clique

largest = largest_clique(graph)
print(largest)

