import csv
import numpy as np

# Open and read the file
input_text = []
with open('12/input.txt', 'r') as file:
    reader = csv.reader(file) 
    for row in reader:
        input_text.append([r for r in row[0]])
array = np.array(input_text)

letters = np.unique(array)
new_array = np.zeros_like(array, dtype=np.int32)
for i, l in enumerate(letters):
    new_array[array == l] = i
array = new_array

max_y, max_x = array.shape

def grow_group(arr, y, x, value, in_group, visited):
    visited.add((y, x))
    if arr[y, x] == value:
        in_group[y, x] = 1
        # up
        if y - 1 >= 0 and (y - 1, x) not in visited:
            in_group = grow_group(arr, y - 1, x, value, in_group, visited)
        # right
        if x + 1 < max_x and (y, x + 1) not in visited:
            in_group = grow_group(arr, y, x + 1, value, in_group, visited)
        # down
        if y + 1 < max_y and (y + 1, x) not in visited:
            in_group = grow_group(arr, y + 1, x, value, in_group, visited)
        # left
        if x - 1 >= 0 and (y, x - 1) not in visited:
            in_group = grow_group(arr, y, x - 1, value, in_group, visited)
    return in_group

def count_neighbors(group, y, x):
        count = 0
        # up
        if y - 1 >= 0 and group[y - 1, x] == 1:
            count += 1
        # right
        if x + 1 < max_x and group[y, x + 1] == 1:
            count += 1
        # down
        if y + 1 < max_y and group[y + 1, x] == 1:
            count += 1
        # left
        if x - 1 >= 0 and group[y, x - 1] == 1:
            count += 1
        return count

def get_perimeter(group):
    perimeter = 0
    yx = (group == 1).nonzero()
    for y, x in zip(yx[0], yx[1]):
        count = count_neighbors(group, y, x)
        if count == 0:
            perimeter += 4
        elif count == 1:
            perimeter += 3
        elif count == 2:
            perimeter += 2
        elif count == 3:
            perimeter += 1
    return perimeter

master_visited = np.zeros_like(array, dtype=np.int8)
total_perimeter = 0
for y in range(max_y):
    for x in range(max_x):
        if master_visited[y, x] == 0:
            group = grow_group(array, y, x, array[y, x], np.zeros_like(array), set())
            master_visited = master_visited + group
            perimeter = get_perimeter(group)
            total_perimeter += (group.sum() * perimeter)

print(total_perimeter)

# PART II

def count_corners(group):
    corners = 0
    group = np.pad(group, (1, 1))
    new_max_y, new_max_x = group.shape
    for y in range(new_max_y - 1):
        for x in range(new_max_x - 1):
            window = group[y:y+2, x:x+2]
            if window.sum() == 1:
                corners += 1
            elif window.sum() == 3:
                corners += 1
            elif window[0, 0] == 1 and window[1, 1] == 1 and window.sum() == 2:
                corners += 2
            elif window[1, 0] == 1 and window[0, 1] == 1 and window.sum() == 2:
                corners += 2
    return corners
            
master_visited = np.zeros_like(array, dtype=np.int8)
total_corners = 0
for y in range(max_y):
    for x in range(max_x):
        if master_visited[y, x] == 0:
            group = grow_group(array, y, x, array[y, x], np.zeros_like(array), set())
            master_visited = master_visited + group
            corners = count_corners(group)
            total_corners += (group.sum() * corners)

print(total_corners)
