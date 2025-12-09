with open("input.txt", "r") as f:
    coords = f.readlines()
coords = [c.strip('\n').split(',') for c in coords]
coords = [[int(c) for c in point] for point in coords]

# PART I

max_area = 0
for i, a in enumerate(coords):
    for b in coords[i:]:
        area = (abs(a[0]-b[0])+1) * (abs(a[1]-b[1])+1)
        if area > max_area:
            max_area = area
print(max_area)

# PART II

import numpy as np

max0 = 0
max1 = 1
for c in coords:
    if c[0] > max0:
        max0 = c[0]
    if c[1] > max1:
        max1 = c[1]

print("Marking corners...")
grid = np.zeros((max1 + 1, max0 + 1), dtype=np.bool)
for c in coords:
    grid[c[1], c[0]] = 1

# draw outline
# there are only ever two corners per row or column of the grid
print("Drawing outline...")
for a in coords:
    for b in coords:
        x, y = None, None
        if (a[0] == b[0]):
            x = a[0]
        if (a[1] == b[1]):
            y = a[1]
        if x is not None:
            for y in range(min(a[1], b[1]), max(a[1], b[1])):
                grid[y, x] = 1
        if y is not None:
            for x in range(min(a[0], b[0]), max(a[0], b[0])):
                grid[y, x] = 1

# flood fill
print("Flood filling...")
p = [coords[0][1], coords[0][0]]
u = grid[p[0]-1, p[1]]
r = grid[p[0], p[1]+1]
l = grid[p[0], p[1]-1]
d = grid[p[0]+1, p[1]]
start = [0, 0]
if u:
    start[0] = p[0]-1
if r:
    start[1] = p[1]+1
if l:
    start[1] = p[1]-1
if d:
    start[0] = p[0]+1


from collections import deque
def flood_fill_bfs(grid, start):
    rows, cols = grid.shape
    sr, sc = start
    if not (0 <= sr < rows and 0 <= sc < cols):
        return grid
    if grid[sr, sc]:
        return grid

    visited = np.zeros_like(grid, dtype=bool)
    q = deque()
    q.append((sr, sc))
    visited[sr, sc] = True

    while q:
        print(len(q))
        r, c = q.popleft()
        if grid[r, c] == 0:
            grid[r, c] = 1
        for nr, nc in ((r-1,c), (r+1,c), (r,c-1), (r,c+1)):
            if 0 <= nr < rows and 0 <= nc < cols and not visited[nr, nc] and grid[nr, nc] == 0:
                visited[nr, nc] = True
                q.append((nr, nc))

    return grid

print(flood_fill_bfs(grid, start))

# test areas
print("Finding largest area...")
max_area = 0
counter = 0
for i, a in enumerate(coords):
    for b in coords[i+1:]:
        if counter % 100 == 0:
            print(f"{counter} of {(len(coords) ** 2) // 2 }")
        if a[0]**2 + a[1]**2 > b[0]**2 + b[1]**2:
            tl = b
            br = a
        else:
            tl = a
            br = b
        area = (br[0] - tl[0] + 1) * (br[1] - tl[1] + 1)
        if (area > max_area):
            if grid[tl[1]:br[1]+1, tl[0]:br[0]+1].all():
                max_area = area
        counter += 1

print(max_area)
        