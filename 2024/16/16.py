from copy import deepcopy
import csv
import numpy as np

# Open and read the file
maze = []
with open('16/input.txt', 'r') as file:
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

import heapq

def dijkstra(maze, start_pos, start_dir, end_pos):
    # Each state: (cost, (r, c, d))
    start_state = (0, start_pos[0], start_pos[1], start_dir)
    visited = {}
    prev_nodes = {}  # state -> [list_of_predecessors]
    pq = [start_state]

    while pq:
        cost, r, c, d = heapq.heappop(pq)

        state = (r, c, d)

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

        # Explore neighbors: forward, turn right, turn left
        moves = []
        # forward
        fr, fc = r + directions[d][0], c + directions[d][1]
        if 0 <= fr < maze.shape[0] and 0 <= fc < maze.shape[1]:
            moves.append((cost+1, fr, fc, d, state))

        # turn right
        rd = (d + 1) % 4
        rr, rc = r + directions[rd][0], c + directions[rd][1]
        if 0 <= rr < maze.shape[0] and 0 <= rc < maze.shape[1]:
            moves.append((cost+1001, rr, rc, rd, state))

        # turn left
        ld = (d - 1) % 4
        lr, lc = r + directions[ld][0], c + directions[ld][1]
        if 0 <= lr < maze.shape[0] and 0 <= lc < maze.shape[1]:
            moves.append((cost+1001, lr, lc, ld, state))

        for new_cost, nr, nc, nd, prev_state in moves:
            new_state = (nr, nc, nd)
            if new_state not in visited or visited[new_state] > new_cost:
                visited[new_state] = new_cost
                prev_nodes[new_state] = [prev_state]
                heapq.heappush(pq, (new_cost, nr, nc, nd))
            elif visited[new_state] == new_cost:
                # Found another shortest path to the same state
                prev_nodes[new_state].append(prev_state)

    # Find the minimum cost end state and reconstruct all shortest paths
    end_states = [(r, c, d) for (r, c, d) in visited.keys() if (r, c) == tuple(end_pos)]
    if not end_states:
        return None, []

    # Pick the direction at end with minimal cost
    best_end_state = min(end_states, key=lambda s: visited[s])
    best_cost = visited[best_end_state]

    # Reconstruct all shortest paths
    all_paths = []

    def backtrack(state):
        if state == (start_pos[0], start_pos[1], start_dir):
            return [[state]]
        paths = []
        for p in prev_nodes.get(state, []):
            for subpath in backtrack(p):
                paths.append(subpath + [state])
        return paths

    all_paths = backtrack(best_end_state)
    return best_cost, all_paths

start = get_pos(maze, 'S')
end = get_pos(maze, 'E')
lowest_cost, shortest_paths = dijkstra(maze, start, 0, end)

# PART I answer:
print("Cost: ", lowest_cost)

# PART II answer:
# Find the unique nodes across all shortest paths
print("Number of shortest paths: ", len(shortest_paths))
on_shortest_path = set()
for path in shortest_paths:
    for node in path:
       if (node[0], node[1]) not in on_shortest_path:
           on_shortest_path.add((node[0], node[1]))
print("Number of unique nodes on shortest paths: ", len(on_shortest_path))
