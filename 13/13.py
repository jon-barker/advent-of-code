import csv
from functools import lru_cache

# Open and read the file
input_data = []
with open('13/input.txt', 'r') as file:
    reader = csv.reader(file, delimiter = ' ') 
    for row in reader:
        if len(row) > 0:
            if row[1] == 'A:':
                deltaxA = int(row[2].split('+')[-1].strip(','))
                deltayA = int(row[3].split('+')[-1])
            if row[1] == 'B:':
                deltaxB = int(row[2].split('+')[-1].strip(','))
                deltayB = int(row[3].split('+')[-1])
            if row[0] == 'Prize:':
                xt = int(row[1].split('=')[-1].strip(','))
                yt = int(row[2].split('=')[-1])
                input_data.append([yt, xt, deltayA, deltaxA, deltayB, deltaxB])

# @lru_cache(maxsize=None)
# def push_buttons_recursive(cost, ys, xs, yt, xt, deltayA, deltaxA, deltayB, deltaxB, depthA, depthB, max_depth):
#     if max_depth is not None:
#         if (depthA > max_depth or depthB > max_depth):
#             return False, None

#     # Found target
#     if ys == yt and xs == xt:
#         return True, cost

#     # Overshot
#     if ys > yt or xs > xt: return False, None

#     # Try A
#     valid_seq_A, downstream_cost_A = push_buttons_recursive(3, ys + deltayA, xs + deltaxA, yt, xt, deltayA, deltaxA, deltayB, deltaxB, depthA + 1, depthB, max_depth)
#     # Try B
#     valid_seq_B, downstream_cost_B = push_buttons_recursive(1, ys + deltayB, xs + deltaxB, yt, xt, deltayA, deltaxA, deltayB, deltaxB, depthA, depthB + 1, max_depth)

#     if valid_seq_A and valid_seq_B:
#         this_cost = min(downstream_cost_A, downstream_cost_B) + cost
#         return True, this_cost
#     elif valid_seq_A and not valid_seq_B:
#         this_cost = downstream_cost_A + cost
#         return True, this_cost
#     elif not valid_seq_A and valid_seq_B:
#         this_cost = downstream_cost_B + cost
#         return True, this_cost
#     else:
#         return False, None

# total_cost = 0
# for input in input_data[:1]:
#     valid_seq, cost = push_buttons_recursive(0, 0, 0, *input, 0, 0, max_depth=99)
#     if valid_seq:
#         total_cost += cost

# print(total_cost)

# PART II
# [yt, xt, deltayA, deltaxA, deltayB, deltaxB]

# PART I solution exceed maximum recursive depth for such large targets
# We will try an iterative solution

# def push_buttons_iterative(yt, xt, deltayA, deltaxA, deltayB, deltaxB):
#     stack = [(0, 0, 0)] # last_y, last_y, cost
#     global_min = [float('inf')]

#     seen = set()

#     while stack:
#         curr_y, curr_x, cost = stack.pop()

#         # Found target
#         if curr_y == yt and curr_x == xt:
#             if cost < global_min[0]:
#                 global_min[0] = cost
#             continue

#         if cost > global_min[0]:
#             continue

#         # Overshot
#         if curr_y > yt or curr_x > xt:
#             continue

#         # Add next choices to the stack
#         if (curr_y, curr_x) not in seen:
#             stack.append((curr_y + deltayA, curr_x + deltaxA, cost + 3))
#             stack.append((curr_y + deltayB, curr_x + deltaxB, cost + 1))
#             seen.add((curr_y, curr_x))
    
#     return global_min[0]

# Iterative solution is too slow! We will try an optimization solution
# Brute force optimization is too slow
# import math
# def brute_force_optimize_button_mashing(yt, xt, deltayA, deltaxA, deltayB, deltaxB):
#     global_min = float('inf')
#     M_max = min(math.ceil(xt / deltaxA), math.ceil(yt / deltayA))
#     N_max = min(math.ceil(xt / deltaxB), math.ceil(yt / deltayB))
#     for N in range(N_max):
#         for M in range(M_max):
#             xs = N * deltaxA + M * deltaxB
#             ys = N * deltayA + M * deltayB
#             if xs == xt and ys == yt:
#                cost = 3 * N + M 
#                if cost < global_min:
#                    global_min = cost
#     return global_min

# see if we can just linearly solve the equations... 
import numpy as np
from math import floor, ceil
def linear_solve_button_mashing(yt, xt, deltayA, deltaxA, deltayB, deltaxB):
    a = np.array([[deltaxA, deltaxB], [deltayA, deltayB]])
    b = np.array([xt, yt])
    # This will find a float solution if one exists
    x = np.linalg.solve(a, b) 
    global_min = float('inf')
    cost = -1
    # Now we need to search around for an integer solution
    max_deltaN = max(int(deltaxA), int(deltayA)) 
    max_deltaM = max(int(deltaxB), int(deltayB)) 
    for N in range(int(x[0]) - max_deltaN, int(x[0]) + max_deltaN):
        for M in range(int(x[1]) - max_deltaM, int(x[1]) + max_deltaM):
            xs = N * deltaxA + M * deltaxB
            ys = N * deltayA + M * deltayB
            if xs == xt and ys == yt:
                cost = 3 * N + M 
                if cost < global_min:
                    global_min = cost
    return cost

from math import gcd

total_cost = 0
counter = 0
for input in input_data:
    # comment these out for PART I
    input[0] += 10000000000000
    input[1] += 10000000000000

    # We can divide all the x terms and y terms by any GCD
    gcdx = gcd(gcd(input[0], input[2]), input[4]) 
    input[0] /= gcdx
    input[2] /= gcdx
    input[4] /= gcdx
    gcdy = gcd(gcd(input[1], input[3]), input[5]) 
    input[1] /= gcdy
    input[3] /= gcdy
    input[5] /= gcdy

    # cost = push_buttons_iterative(*input)
    # cost = brute_force_optimize_button_mashing(*input)
    cost = linear_solve_button_mashing(*input)
    if cost > -1:
        total_cost += cost
    counter += 1

print(total_cost)
