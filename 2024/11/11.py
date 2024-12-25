from copy import copy
import math

# Open and read the file
with open('11/input.txt', 'r') as file:
    input = file.readline().split(' ')
orig_input = [int(i) for i in input]

def count_digits(n):
    count = 0
    while n >= 1:
        n = n / 10
        count += 1
    return count

# PART 1
input = copy(orig_input)
for blink in range(25):
    output = []
    for i, stone in enumerate(input):
        len_stone = count_digits(stone)
        if stone == 0:
            output.append(1)
        elif stone != 0 and len_stone % 2 == 0:
            left_part = math.floor(stone / (10 ** (len_stone // 2)))
            output.append(left_part)
            right_part = stone - left_part * 10 ** (len_stone // 2)
            output.append(right_part)
        else:
            output.append(stone * 2024)
    input = copy(output)

print(len(output))
            
# PART 2
from functools import lru_cache
@lru_cache(maxsize = 10000000) 
def process_stone(stone, depth):
    if depth == 75:
        return 1
    else:
        len_stone = count_digits(stone)
        if stone == 0:
            count = process_stone(1, depth + 1)
        elif stone != 0 and len_stone % 2 == 0:
            left_part = math.floor(stone / (10 ** (len_stone // 2)))
            right_part = stone - left_part * 10 ** (len_stone // 2)
            count = process_stone(left_part, depth + 1) + process_stone(right_part, depth + 1)
        else:
            count = process_stone(stone * 2024, depth + 1)
        return count

count = 0
for stone in orig_input:
    count += process_stone(stone, 0)
print(count)
