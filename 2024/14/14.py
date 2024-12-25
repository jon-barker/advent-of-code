from copy import deepcopy
import csv
import numpy as np

# Open and read the file
positions = []
velocities = []
with open('14/input.txt', 'r') as file:
    reader = csv.reader(file, delimiter = ' ') 
    for row in reader:
        x, y = row[0].split('=')[-1].split(',')
        positions.append([int(y), int(x)])
        dx, dy = row[1].split('=')[-1].split(',')
        velocities.append([int(dy), int(dx)])

height, width = 103, 101

for step in range(100):
    for robot in range(len(positions)):
        positions[robot][0] = (positions[robot][0] + velocities[robot][0]) % height
        positions[robot][1] = (positions[robot][1] + velocities[robot][1]) % width

orig_positions = deepcopy(positions)

def get_count_grid(positions, height, width):
    count_grid = np.zeros((height, width))
    for p in positions:
        count_grid[p[0], p[1]] += 1
    return count_grid

count_grid = get_count_grid(orig_positions, height, width)

safety_factor = count_grid[:(height // 2), :(width // 2)].sum() * \
                count_grid[(height // 2 + 1):, :(width // 2)].sum() * \
                count_grid[(height // 2 + 1):, (width // 2 + 1):].sum() * \
                count_grid[:(height // 2):, (width // 2 + 1):].sum()

print(int(safety_factor))

# PART II

def grow_trees(count_grid):
    p = count_grid.nonzero()
    _, width = count_grid.shape
    largest_tree = 0 
    for t in zip(p[0], p[1]):
        if t[1] > 0 and count_grid[t[0], t[1] - 1] > 0:
            continue
        elif t[1] < width - 1 and count_grid[t[0], t[1] + 1] > 0:
            continue
        in_tree = True
        row = 1
        tree_size = count_grid[t[0], t[1]]
        while in_tree:
            test_points = count_grid[row, t[1] - row : t[1] + row + 1]
            if (test_points > 0).all():
                tree_size += test_points.sum()
                row += 1
            else:
                in_tree = False
        if tree_size > largest_tree:
            largest_tree = tree_size
    return largest_tree
        
import matplotlib.pyplot as plt

# NOTE: this works but it's a little unsatisfying
# the tree is more complicated than just a triangle (which I was assuming)
# it does have a triangle at the top though and in my case that happens to have
# 13 robots in it, hence the magic number
# TODO: re-write this using something like a connected components search

is_tree = False
steps = 0
num_robots = count_grid.sum()
global_largest = 0
while not is_tree:
    for robot in range(len(positions)):
        positions[robot][0] = (positions[robot][0] + velocities[robot][0]) % height
        positions[robot][1] = (positions[robot][1] + velocities[robot][1]) % width
    steps += 1
    count_grid = get_count_grid(positions, height, width)
    largest_tree = grow_trees(count_grid)
    if largest_tree == 13:
        is_tree = True
    if largest_tree > global_largest:
        global_largest = largest_tree
        plt.imsave('im.png', count_grid)
    print(steps, largest_tree, global_largest)
