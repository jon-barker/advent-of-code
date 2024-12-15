from copy import deepcopy
import csv
import numpy as np

# Open and read the file
grid = []
moves = ''
with open('15/input.txt', 'r') as file:
    reader = csv.reader(file) 
    for row in reader:
        if len(row) == 0:
            pass
        elif row[0][0] in ['^', '>', 'v', '<']:
            moves += row[0]
        else:
            grid.append([r for r in row[0]])
grid = np.array(grid)

deltas = {'^': (-1, 0),
          '>': (0, 1),
          'v': (1, 0),
          '<': (0, -1)}

chars = np.unique(grid)
chars = {c.item(): i for i, c in enumerate(chars)}

new_grid = np.zeros_like(grid, dtype=np.int8)
for j in range(grid.shape[0]):
    for i in range(grid.shape[1]):
       new_grid[j, i] = chars[grid[j, i].item()] 
grid = new_grid

orig_grid = deepcopy(grid)

print("Initial setup:")
print(grid, moves, deltas, chars)

def in_bounds(grid, y, x):
    if y < 0:
        return False
    if y >= grid.shape[0]:
        return False
    if x < 0:
        return False
    if x >= grid.shape[1]:
        return False
    return True

def try_move(grid, dy, dx):
    j_s, i_s = (grid == chars['@']).nonzero()
    j_s, i_s = j_s.item(), i_s.item()
    j_f, i_f = j_s + dy, i_s + dx
    # Count how many Os are ahead
    while grid[j_f, i_f] not in [chars['.'], chars['#']]:
        j_f, i_f = j_f + dy, i_f + dx
    # If there's a string of Os (including zero Os) and space to move them into
    # then we move them
    if in_bounds(grid, j_f + dy, i_f + dx) and grid[j_f, i_f] != chars['#'] and (grid[j_f + dy, i_f + dx] == chars['.'] or grid[j_f, i_f] == chars['.']):
        if j_f == j_s:
            j_f += 1
        if i_f == i_s:
            i_f += 1
        if j_f < j_s:
            j_step = -1
        else:
            j_step = 1
        if i_f < i_s:
            i_step = -1
        else:
            i_step = 1
        tmp = np.copy(grid[j_s : j_f : j_step, i_s : i_f : i_step])
        grid[j_s : j_f : j_step, i_s : i_f : i_step] = chars['.']
        grid[j_s + dy : j_f + dy : j_step, i_s + dx : i_f + dx : i_step] = np.copy(tmp)
    return grid

for move in moves:
    dy, dx = deltas[move]
    grid = try_move(grid, dy, dx)

def sum_coords(grid):
    boxes = (grid == chars['O']).nonzero()
    output = 0
    for j, i in zip(boxes[0], boxes[1]):
        output += 100 * j + i
    return output

print(sum_coords(grid))

# PART II
# basically a re-write as it's better handled with an entity-component setup

chars['['] = len(chars.keys()) + 1
chars[']'] = len(chars.keys()) + 1

def expand_grid(grid):
    rows, cols = grid.shape
    inter = np.empty((rows, 2 * cols), dtype=grid.dtype)
    filler = np.ones_like(grid) * -1
    inter[:, ::2] = grid
    inter[:, 1::2] = grid
    inter[:, 1::2] = filler
    for j in range(inter.shape[0] - 1, -1, -1):
        for i in range(inter.shape[1] - 1, -1, -1):
            if inter[j, i] == chars['.']:
                inter[j, i+1] = chars['.']
            elif inter[j, i] == chars['@']:
                inter[j, i+1] = chars['.']
            elif inter[j, i] == chars['#']:
                inter[j, i+1] = chars['#']
            elif inter[j, i] == chars['O']:
                inter[j, i] = chars['[']
                inter[j, i+1] = chars[']']
    return inter


grid = expand_grid(orig_grid)

from dataclasses import dataclass
@dataclass
class Entity:
    y: int
    x1: int
    x2: int
    type: int

robot_y, robot_x = (grid == chars['@']).nonzero()
robot = Entity(int(robot_y.item()), int(robot_x.item()), int(robot_x.item()), chars['@'])
entities = [robot]

walls = (grid == chars['#']).nonzero()
for y, x in zip(walls[0], walls[1]):
    e = Entity(int(y), int(x), int(x), chars['#'])
    entities.append(e)

boxes = (grid == chars['[']).nonzero()
for y, x in zip(boxes[0], boxes[1]):
    e = Entity(int(y), int(x), int(x) + 1, chars['['])
    entities.append(e)

def collides(e1, e2, dy, dx):
    if e1 == e2:
        return False
    if dy != 0:
        if e1.y + dy == e2.y and (e1.x1 == e2.x1 or e1.x1 == e2.x2 or e1.x2 == e2.x1 or e1.x2 == e2.x2):
            return True
    if dx == 1:
        if e1.y == e2.y and e1.x2 + dx == e2.x1:
            return True
    if dx == -1:
        if e1.y == e2.y and e1.x1 + dx == e2.x2:
            return True
    return False

def make_move(entities, dy, dx):
    e1 = entities[0]
    to_move = [0]
    stack = []
    for i, e2 in enumerate(entities):
        collision = collides(e1, e2, dy, dx)
        if collision and e2.type != chars['#']:
            stack.append(e2)
            if i not in to_move:
                to_move.append(i)
        elif collision and e2.type == chars['#']: 
            return entities
    while len(stack) > 0:
        e1 = stack.pop()
        for i, e2 in enumerate(entities):
            collision = collides(e1, e2, dy, dx)
            if collision and e2.type != chars['#']:
                stack.append(e2)
                if i not in to_move:
                    to_move.append(i)
            elif collision and e2.type == chars['#']:
                return entities
    for i in to_move:
        entities[i].y += dy
        entities[i].x1 += dx
        entities[i].x2 += dx
    return entities

for m_idx, move in enumerate(moves):
    dy, dx = deltas[move]
    entities = make_move(entities, dy, dx)
    print(m_idx, len(moves))

final_sum = 0
for e in entities:
    if e.type == chars['[']:
        final_sum += (100 * e.y + e.x1)
print(final_sum)
