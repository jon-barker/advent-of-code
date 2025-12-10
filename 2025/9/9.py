with open("input.txt", "r") as f:
    coords = f.readlines()
coords = [reversed(c.strip('\n').split(',')) for c in coords]
# coords are (col, row) pairs with zero indexing
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

maxc = 0
maxr = 1
for c in coords:
    if c[0] > maxc:
        maxc = c[0]
    if c[1] > maxr:
        maxr = c[1]

print("Marking corners...")
grid = np.zeros((maxc + 1, maxr + 1), dtype=np.bool)
for c in coords:
    grid[c[0], c[1]] = 1
print(grid.sum(0).max(), grid.sum(1).max())
print(grid)

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
            for y in range(min(a[1], b[1]), max(a[1], b[1]) + 1):
                grid[x, y] = 1
        if y is not None:
            for x in range(min(a[0], b[0]), max(a[0], b[0]) + 1):
                grid[x, y] = 1
print(grid)

# get indices of nonzero values in each row
bounds = [grid[r, :].nonzero()[0] for r in range(grid.shape[0])]
bounds = [[min(b), max(b)] if len(b) > 0 else [] for b in bounds]

# fill in the outline
def in_bounds(bounds, p):
    x, y = p
    row = bounds[y]
    if not row: return False
    return row[0] <= x <= row[1]

print("Filling outline...")
for i, b in enumerate(bounds):
    if len(b) > 0:
        grid[i, b[0]:b[1]+1] = 1
print(grid)

# test areas
print("Finding largest area...")

# given tl = (x0, y0), br = (x1, y1)
def check_rect_edges(grid, tl, br):
    x0, y0 = tl
    x1, y1 = br
    # width/height
    if x0 > x1 or y0 > y1:
        return False

    # left col
    if not grid[x0, y0:y1+1].all():
        return False
    # right col (skip if same as left)
    if y1 != y0:
        if not grid[x1, y0:y1+1].all():
            return False
    # top row (exclude corners already checked)
    if y1 - y0 > 1:
        if not grid[x0+1:x1, y0].all():
            return False
    # bottom row (skip if same row)
    if x1 != x0 and y1 - y0 > 1:
        if not grid[x0+1:x1, y1].all():
            return False

    return True

max_area = 0
counter = 0
for i, a in enumerate(coords):
    for b in coords[i+1:]:
        if counter % 100 == 0:
            print(f"{counter} of {(len(coords) ** 2) // 2 }")
        if (a[0] != b[0]):
            if (a[1] != b[1]):
                x0 = min(a[0], b[0])
                x1 = max(a[0], b[0])
                y0 = min(a[1], b[1])
                y1 = max(a[1], b[1])
                area = (x1 - x0 + 1) * (y1 - y0 + 1)
                if (area > max_area):
                    if check_rect_edges(grid, (x0, y0), (x1, y1)):
                        # if edges are all valid do a final check on the whole rectangle
                        if grid[x0:x1+1, y0:y1+1].all():
                            max_area = area
        counter += 1

print(max_area)