from copy import copy
import csv
import numpy as np

# Open and read the file
mazes = []
maze = np.zeros((71, 71), dtype =np.str_)
maze[:, :] = '.'
bites = []
with open('18/input.txt', 'r') as file:
    reader = csv.reader(file, delimiter=',') 
    for i, row in enumerate(reader):
        maze[int(row[1]), int(row[0])] = '#'
        mazes.append(copy(maze))
        bites.append((row[0], row[1]))
        

chars = np.unique(mazes[0])
chars = {c.item(): i for i, c in enumerate(chars)}

print(chars)

new_mazes = []
count = 0
for maze in mazes:
    new_maze = np.zeros_like(maze, dtype=np.int8)
    for j in range(maze.shape[0]):
        for i in range(maze.shape[1]):
            new_maze[j, i] = chars[maze[j, i].item()] 
    new_mazes.append(new_maze)
    count += 1
    print(count)
mazes = new_mazes

def add_pos(a, b):
    return [a[0] + b[0], a[1] + b[1]]

import heapq

def dijkstra(maze, start_pos, end_pos):
    # Each state: (cost, r, c)
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
            return cost

        # If blockage, skip
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

start = [0, 0]
end = [70, 70]
lowest_cost = dijkstra(mazes[1023], start, end)

# PART I answer:
print("Cost: ", lowest_cost)

# PART II answer:
lowest_cost = 0
m_idx = 1023
while lowest_cost is not None:
    lowest_cost = dijkstra(mazes[m_idx], start, end)
    print(m_idx, lowest_cost)
    m_idx += 1

print(bites[m_idx -1])
