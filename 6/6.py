import csv
import numpy as np

# Open and read the file
input_text = []
with open('6/input.txt', 'r') as file:
    reader = csv.reader(file) 
    for row in reader:
        input_text.append([r for r in row[0]])

array = np.array(input_text)

MOVES = {
    '^': 0,
    '>': 1,
    'v': 2,
    '<': 3,
    '.': 4,
    '#': 5,
    'X': 6,
    'O': 7,
}

int_array = np.zeros_like(array, dtype=np.int8)
for row in range(array.shape[0]):
    for col in range(array.shape[1]):
        int_array[row, col] = MOVES[str(array[row, col][0])]

array = np.copy(int_array)

MAX_Y, MAX_X = array.shape

def make_move(array, y, x, ps=None, check_if_seen=False):
    """Simple logic to make the next correct move given current state
    and update the record of previously seen states"""

    item = array[y, x].item()
    if check_if_seen:
        if ps[y, x, item] == 1:
            return array, ps, y, x, True, True

        ps[y, x, item] = 1

    if array[y, x] == MOVES['^']:
        if y - 1 < 0:
            array[y, x] = MOVES['X']
            return array, ps, y - 1, x, False, False
        elif array[y - 1, x] == MOVES['#']:
            array[y, x] = MOVES['>']
            return array, ps, y, x, True, False
        else:
            array[y, x] = MOVES['X']
            array[y - 1, x] = MOVES['^']
            return array, ps, y - 1, x, True, False
    elif array[y, x] == MOVES['>']:
        if x + 1 == MAX_X:
            array[y, x] = MOVES['X']
            return array, ps, y, x + 1, False, False
        elif array[y, x + 1] == MOVES['#']:
            array[y, x] = MOVES['v']
            return array, ps, y, x, True, False
        else:
            array[y, x] = MOVES['X']
            array[y, x + 1] = MOVES['>']
            return array, ps, y, x + 1, True, False
    elif array[y, x] == MOVES['v']:
        if y + 1 == MAX_Y:
            array[y, x] = MOVES['X']
            return array, ps, y + 1, x, False, False
        elif array[y + 1, x] == MOVES['#']:
            array[y, x] = MOVES['<']
            return array, ps, y, x, True, False
        else:
            array[y, x] = MOVES['X']
            array[y + 1, x] = MOVES['v']
            return array, ps, y + 1, x, True, False
    elif array[y, x] == MOVES['<']:
        if x - 1 < 0:
            array[y, x] = MOVES['X']
            return array, ps, y, x - 1, False, False
        elif array[y, x - 1] == MOVES['#']:
            array[y, x] = MOVES['^']
            return array, ps, y, x, True, False
        else:
            array[y, x] = MOVES['X']
            array[y, x - 1] = MOVES['<']
            return array, ps, y, x - 1, True, False

def get_hypothetical_obstacle(array, y, x):

    if array[y, x] == MOVES['^']:
        if y - 1 < 0:
            return None, None
        elif array[y - 1, x] == MOVES['#']:
            return None, None
        else:
            return y - 1, x
    elif array[y, x] == MOVES['>']:
        if x + 1 == MAX_X:
            return None, None
        elif array[y, x + 1] == MOVES['#']:
            return None, None
        else:
            return y, x + 1
    elif array[y, x] == MOVES['v']:
        if y + 1 == MAX_Y:
            return None, None
        elif array[y + 1, x] == MOVES['#']:
            return None, None
        else:
            return y + 1, x
    elif array[y, x] == MOVES['<']:
        if x - 1 < 0:
            return None, None
        elif array[y, x - 1] == MOVES['#']:
            return None, None
        else:
            return y, x - 1

# array to mark valid part 2 obstacles
obstacles = np.copy(array)

# initial position
y, x = (array < 4).nonzero()
y = y.item()
x = x.item()

in_bounds = True
count = 0
tested_positions = set()
while in_bounds:
    tmp_y, tmp_x = get_hypothetical_obstacle(array, y, x)
    if tmp_y is not None and (tmp_y, tmp_x) not in tested_positions:
        tested_positions.add((tmp_y, tmp_x))
        hyp_array = np.copy(array)
        hyp_array[tmp_y, tmp_x] = MOVES['#']
        # previously seen states
        hyp_ps = np.zeros((array.shape[0], array.shape[1], 4), dtype=np.int8)
        seen = False
        hyp_in_bounds = True
        hyp_y = y
        hyp_x = x
        while hyp_in_bounds and not seen:
            hyp_array, hyp_ps, hyp_y, hyp_x, hyp_in_bounds, seen = make_move(hyp_array, hyp_y, hyp_x, hyp_ps, check_if_seen=True)
        if seen:
            obstacles[tmp_y, tmp_x] = MOVES['O']
    array, _, y, x, in_bounds, _ = make_move(array, y, x)
    count += 1

# part 1 output
print((array == MOVES['X']).sum())

# part 2 output
print((obstacles == MOVES['O']).sum())
