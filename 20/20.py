from functools import lru_cache
from itertools import product
import csv
import numpy as np

# Open and read the file
maze = []
with open('20/input.txt', 'r') as file:
    reader = csv.reader(file) 
    for row in reader:
        maze.append([r for r in row[0]])
maze = np.array(maze)

chars = np.unique(maze)
chars = {c.item(): i for i, c in enumerate(chars)}

print(chars)

new_maze = np.zeros_like(maze, dtype=np.int8)
for j in range(maze.shape[0]):
    for i in range(maze.shape[1]):
       new_maze[j, i] = chars[maze[j, i].item()] 
maze = new_maze

directions = [[0, 1], [1, 0], [0, -1], [-1, 0]]

def get_pos(maze, ch):
    pos = (maze == chars[ch]).nonzero()
    return [pos[0].item(), pos[1].item()]

def add_pos(a, b):
    return [a[0] + b[0], a[1] + b[1]]

import sys
sys.setrecursionlimit(1000000)

import heapq

def dijkstra(maze, start_pos, end_pos, return_paths = False):
    # Each state: (cost, (r, c))
    start_state = (0, start_pos[0], start_pos[1])
    visited = {}
    prev_nodes = {}  # state -> [list_of_predecessors]
    pq = [start_state]

    while pq:
        cost, r, c = heapq.heappop(pq)

        state = (r, c)

        if state in visited:
            # If we already have a better or equal cost, skip
            if visited[state] < cost:
                continue
            elif visited[state] == cost:
                # Same best cost, do nothing special here
                pass
        else:
            visited[state] = cost

        # Check if we reached the end
        if (r, c) == tuple(end_pos):
            # Shortest distance found but don't stop since we want all shortest paths
            pass

        # If wall, skip
        if maze[r, c] == chars['#']:
            continue

        # Explore neighbors: up, down, left, right
        moves = []
        # up
        fr, fc = r - 1, c
        if 0 <= fr < maze.shape[0] and 0 <= fc < maze.shape[1]:
            moves.append((cost+1, fr, fc, state))
        # right
        fr, fc = r, c + 1
        if 0 <= fr < maze.shape[0] and 0 <= fc < maze.shape[1]:
            moves.append((cost+1, fr, fc, state))
        # down
        fr, fc = r + 1, c
        if 0 <= fr < maze.shape[0] and 0 <= fc < maze.shape[1]:
            moves.append((cost+1, fr, fc, state))
        # left
        fr, fc = r, c - 1
        if 0 <= fr < maze.shape[0] and 0 <= fc < maze.shape[1]:
            moves.append((cost+1, fr, fc, state))

        for new_cost, nr, nc, prev_state in moves:
            new_state = (nr, nc)
            if new_state not in visited or visited[new_state] > new_cost:
                visited[new_state] = new_cost
                prev_nodes[new_state] = [prev_state]
                heapq.heappush(pq, (new_cost, nr, nc))
            elif visited[new_state] == new_cost:
                # Found another shortest path to the same state
                prev_nodes[new_state].append(prev_state)

    # Find the minimum cost end state and reconstruct all shortest paths
    end_states = [(r, c) for (r, c) in visited.keys() if (r, c) == tuple(end_pos)]
    if not end_states:
        return None, []

    # Pick the direction at end with minimal cost
    best_end_state = min(end_states, key=lambda s: visited[s])
    best_cost = visited[best_end_state]

    # Reconstruct all shortest paths
    all_paths = []

    def backtrack(state):
        if state == (start_pos[0], start_pos[1]):
            return [[state]]
        paths = []
        for p in prev_nodes.get(state, []):
            for subpath in backtrack(p):
                paths.append(subpath + [state])
        return paths

    if return_paths:
        all_paths = backtrack(best_end_state)
    return best_cost, all_paths

start = (maze == chars['S']).nonzero()
start = [s.item() for s in start]
end = (maze == chars['E']).nonzero()
end = [e.item() for e in end]

lowest_cost, shortest_paths = dijkstra(maze, start, end, return_paths = True)
print(lowest_cost)

# PART I

cheats_found = 0

cost_limit = lowest_cost - 100
seen = set()
for i, node in enumerate(shortest_paths[0]):
    if i % 100 == 0:
        print(i, len(shortest_paths[0]))
    # up
    if maze[node[0] - 1, node[1]] == chars['#']:
        if (node[0] - 1, node[1]) not in seen:
            new_maze = np.copy(maze)
            new_maze[node[0] - 1, node[1]] = chars['.']
            seen.add((node[0] - 1, node[1]))
            lowest_cost, _ = dijkstra(new_maze, start, end)
            if lowest_cost <= cost_limit:
                cheats_found += 1
    # down
    if maze[node[0] + 1, node[1]] == chars['#']:
        if (node[0] + 1, node[1]) not in seen:
            new_maze = np.copy(maze)
            new_maze[node[0] + 1, node[1]] = chars['.']
            seen.add((node[0] + 1, node[1]))
            lowest_cost, _ = dijkstra(new_maze, start, end)
            if lowest_cost <= cost_limit:
                cheats_found += 1
    # left
    if maze[node[0], node[1] - 1] == chars['#']:
        if (node[0], node[1] - 1) not in seen:
            new_maze = np.copy(maze)
            new_maze[node[0], node[1] - 1] = chars['.']
            seen.add((node[0], node[1] - 1))
            lowest_cost, _ = dijkstra(new_maze, start, end)
            if lowest_cost <= cost_limit:
                cheats_found += 1
    # right
    if maze[node[0], node[1] + 1] == chars['#']:
        if (node[0], node[1] + 1) not in seen:
            new_maze = np.copy(maze)
            new_maze[node[0], node[1] + 1] = chars['.']
            seen.add((node[0], node[1] + 1))
            lowest_cost, _ = dijkstra(new_maze, start, end)
            if lowest_cost <= cost_limit:
                cheats_found += 1

print(cheats_found)

# PART II

positions = {val: i for i, val in enumerate(shortest_paths[0])}
cost_limit = lowest_cost - 100

cheats_found = 0
for i, (x, y) in enumerate(product(shortest_paths[0], repeat=2)):
    if positions[x] > positions[y] or positions[x] + (lowest_cost - positions[y]) > cost_limit:
        continue
    d = sum(abs(a - b) for a, b in zip(x, y))
    if d > 20:
        continue
    start_cost = positions[x]
    end_cost = lowest_cost - positions[y]
    if start_cost + d + end_cost <= cost_limit:
        cheats_found += 1
    if i % 1000 == 0:
        print('cheats', i)

print(cheats_found)
