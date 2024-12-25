import csv
import numpy as np

# Open and read the file
input_text = []
with open('10/input.txt', 'r') as file:
    reader = csv.reader(file) 
    for row in reader:
        input_text.append([int(r) for r in row[0]])
array = np.array(input_text)

maxy, maxx = array.shape

trailheads = (array == 0).nonzero()
peaks = (array == 9).nonzero()

def find_path(arr, ya, xa, yb, xb, ha):
    if ya == yb and xa == xb:
        return True
    up = right = down = left = False
    # up
    if ya - 1 >= 0 and arr[ya - 1, xa] == ha + 1:
        up = find_path(arr, ya - 1, xa, yb, xb, ha + 1)
    # right
    if xa + 1 < maxx and arr[ya, xa + 1] == ha + 1:
        right = find_path(arr, ya, xa + 1, yb, xb, ha + 1)
    # down
    if ya + 1 < maxy and arr[ya + 1, xa] == ha + 1:
        down = find_path(arr, ya + 1, xa, yb, xb, ha + 1)
    # left
    if xa - 1 >= 0 and arr[ya, xa - 1] == ha + 1:
        left = find_path(arr, ya, xa - 1, yb, xb, ha + 1)

    if up or down or right or left:
        return True
    else:
        return False

count = 0
for y_th, x_th in zip(trailheads[0], trailheads[1]):
    trailhead_tally = np.zeros_like(array)
    for y_b, x_b in zip(peaks[0], peaks[1]):
        path = find_path(array, y_th, x_th, y_b, x_b, 0)
        if path:
            trailhead_tally[y_b, x_b] = 1
    count += trailhead_tally.sum()

print(count)

# PART 2

def find_path_2(arr, ya, xa, yb, xb, ha, count = 0):
    if ya == yb and xa == xb:
        return 1
    up = right = down = left = 0
    # up
    if ya - 1 >= 0 and arr[ya - 1, xa] == ha + 1:
        up = find_path_2(arr, ya - 1, xa, yb, xb, ha + 1, count)
    # right
    if xa + 1 < maxx and arr[ya, xa + 1] == ha + 1:
        right = find_path_2(arr, ya, xa + 1, yb, xb, ha + 1, count)
    # down
    if ya + 1 < maxy and arr[ya + 1, xa] == ha + 1:
        down = find_path_2(arr, ya + 1, xa, yb, xb, ha + 1, count)
    # left
    if xa - 1 >= 0 and arr[ya, xa - 1] == ha + 1:
        left = find_path_2(arr, ya, xa - 1, yb, xb, ha + 1, count)
    count += (up + right + down + left)
    return count

count = 0
for y_th, x_th in zip(trailheads[0], trailheads[1]):
    for y_b, x_b in zip(peaks[0], peaks[1]):
        path_count = find_path_2(array, y_th, x_th, y_b, x_b, 0)
        count += path_count

print(count)
