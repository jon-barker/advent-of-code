import csv
import itertools
import numpy as np

# Open and read the file
input_text = []
with open('8/input.txt', 'r') as file:
    reader = csv.reader(file) 
    for row in reader:
        input_text.append([r for r in row[0]])
array = np.array(input_text)

antenna_ids = np.unique(array)

new_array = np.zeros_like(array, dtype=np.int8)
for idx, antenna_id in enumerate(antenna_ids):
    new_array[array == antenna_id] = idx
array = new_array

max_y, max_x = array.shape

def in_bounds(y, x):
    if (y >= 0) and (y < max_y) and (x >=0) and (x < max_x):
        return True
    else:
        return False

antinodes = set()
for id in range(1, len(antenna_ids)):
    # Get the coords of each antenna matching id 
    ant_ys, ant_xs = (array == id).nonzero()
    # Get all pairs of antennas (ignoring order)
    ant_combos = set(tuple(sorted(p)) for p in itertools.product(range(len(ant_ys)), repeat=2))
    for combo in ant_combos:
        # Antennas don't create valid pairs with themselves
        if combo[0] == combo[1]:
            continue
        y1, x1 = ant_ys[combo[0]], ant_xs[combo[0]]
        y2, x2 = ant_ys[combo[1]], ant_xs[combo[1]]
        # These equations compute the coordinates of the two antinodes for a pair
        y3 = 2*y1 - y2
        x3 = 2*x1 - x2
        y4 = 2*y2 - y1 
        x4 = 2*x2 - x1
        # The antinode is only valid if it's in bounds
        if in_bounds(y3, x3):
            antinodes.add((y3, x3))
        if in_bounds(y4, x4):
            antinodes.add((y4, x4))

print(len(antinodes))

antinodes = set()
for id in range(1, len(antenna_ids)):
    # Get the coords of each antenna matching id 
    ant_ys, ant_xs = (array == id).nonzero()
    # Get all pairs of antennas (ignoring order)
    ant_combos = set(tuple(sorted(p)) for p in itertools.product(range(len(ant_ys)), repeat=2))
    for combo in ant_combos:
        # Antennas don't create valid pairs with themselves
        if combo[0] == combo[1]:
            continue
        y1, x1 = ant_ys[combo[0]], ant_xs[combo[0]]
        y2, x2 = ant_ys[combo[1]], ant_xs[combo[1]]
        # calculate the slope of the line through the pair
        m = (y2 - y1) / (x2 - x1)
        # for each row in the area calculate the corresponding x coord on the line
        for y3 in range(max_y):
            x3 = ((y3 - y2) / m) + x2
            # if the x coord is in bounds and is an integer then it's an antinode
            if (x3 >= 0) and (x3 < max_x) and x3.is_integer():
                antinodes.add((y3, x3))
        # for each row in the area calculate the corresponding y coord on the line
        for x3 in range(max_x):
            y3 = (m * (x3 - x2)) + y2
            # if the y coord is in bounds and is an integer then it's an antinode
            if (y3 >= 0) and (y3 < max_y) and y3.is_integer():
                antinodes.add((y3, x3))
        
print(len(antinodes))
