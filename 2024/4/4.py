import csv
import numpy as np

# Open and read the file
input_text = []
with open('4/input.txt', 'r') as file:
    reader = csv.reader(file) 
    for row in reader:
        input_text.append([r for r in row[0]])

array = np.array(input_text)

def check_neighbor(array, r, c, delta_r, delta_c, target_letter='M'):
    found = False
    next_letter = {'M':'A', 'A':'S'}
    if (r + delta_r >= array.shape[0]) or (r + delta_r < 0) or (c + delta_c >= array.shape[1]) or (c + delta_c < 0):
        return False
    if array[r + delta_r, c + delta_c] == target_letter:
        if target_letter == 'S':
            found = True
        else:
            found = check_neighbor(array, r + delta_r, c + delta_c, delta_r, delta_c, target_letter=next_letter[target_letter])
    return found

count = 0
for r in range(array.shape[0]):
    for c in range(array.shape[1]):
        if array[r][c] == 'X':
            if check_neighbor(array, r, c, 0, 1):
                count += 1
            if check_neighbor(array, r, c, 1, 1):
                count += 1
            if check_neighbor(array, r, c, 1, 0):
                count += 1
            if check_neighbor(array, r, c, 1, -1):
                count += 1
            if check_neighbor(array, r, c, 0, -1):
                count += 1
            if check_neighbor(array, r, c, -1, -1):
                count += 1
            if check_neighbor(array, r, c, -1, 0):
                count += 1
            if check_neighbor(array, r, c, -1, 1):
                count += 1

print(count)

"""
Possible cases:

M . M
. A .
S . S

M . S
. A . 
M . S

S . M
. A .
S . M

S . S
. A .
M . M
"""

count = 0
for r in range(array.shape[0]):
    for c in range(array.shape[1]):
        if array[r][c] == 'M':
            # check down and left plus either up-right or down-right
            if check_neighbor(array, r, c, 1, 1, target_letter="A"):
                if array[r][c + 2] == "M" and check_neighbor(array, r, c + 2, 1, -1, target_letter="A"):
                    count += 1
                elif array[r + 2][c] == "M" and check_neighbor(array, r + 2, c, -1, 1, target_letter="A"):
                    count += 1
            # check up and left plus either up-right or down-left
            if check_neighbor(array, r, c, -1, -1, target_letter="A"):
                if array[r][c - 2] == "M" and check_neighbor(array, r, c - 2, -1, 1, target_letter="A"):
                    count += 1
                elif array[r - 2][c] == "M" and check_neighbor(array, r - 2, c, 1, -1, target_letter="A"):
                    count += 1

print(count)
