from copy import deepcopy
import csv
import numpy as np

# Open and read the file
input_text = []
with open('6/input.txt', 'r') as file:
    reader = csv.reader(file) 
    for row in reader:
        input_text.append([r for r in row[0]])

array = np.array(input_text)

global deltas
deltas = {'^': (-1, 0),
          '>': (0, 1),
          'v': (1, 0),
          '<': (0, -1)}

def make_move(array):
    """Simple logic to make the next correct move given current state"""

    y, x = np.where((array == '^') | (array == '>') | (array == 'v') | (array == '<'))

    max_y, max_x = array.shape

    if array[y, x] == '^':
        if y-1 < 0:
            array[y, x] = 'X'
            return array, False
        elif array[y - 1, x] == '#':
            array[y, x] = '>'
            return array, True
        else:
            array[y, x] = 'X'
            array[y - 1, x] = '^'
            return array, True
    elif array[y, x] == '>':
        if x + 1 == max_x:
            array[y, x] = 'X'
            return array, False
        elif array[y, x + 1] == '#':
            array[y, x] = 'v'
            return array, True
        else:
            array[y, x] = 'X'
            array[y, x + 1] = '>'
            return array, True
    elif array[y, x] == 'v':
        if y + 1 == max_y:
            array[y, x] = 'X'
            return array, False
        elif array[y + 1, x] == '#':
            array[y, x] = '<'
            return array, True
        else:
            array[y, x] = 'X'
            array[y, x] = 'X'
            array[y + 1, x] = 'v'
            return array, True
    elif array[y, x] == '<':
        if x - 1 < 0:
            array[y, x] == 'X'
            return array, False
        elif array[y, x - 1] == '#':
            array[y, x] = '^'
            return array, True
        else:
            array[y, x] = 'X'
            array[y, x - 1] = '<'
            return array, True

in_bounds = True
while in_bounds:
    array, in_bounds = make_move(array)

# part 1 output
print((array == 'X').sum())
