from copy import copy

# Open and read the file
with open('9/input.txt', 'r') as file:
    input = file.read()
input = list(input)[:-1]
input = [int(i) for i in input]

# Convert to individual block representation
block_rep = [0] * input[0]
block_or_empty = 1 # 0 = block, 1 = empty
idx = 0
for digit in input[1:]:
    if block_or_empty == 1:
        block_rep += ['.'] * digit
    else:
        block_rep += [idx] * digit
    block_or_empty = (block_or_empty + 1) % 2
    if block_or_empty == 0:
        idx += 1

orig_block_rep = copy(block_rep)

# compact the block representation
left_idx, right_idx = 0, len(block_rep) - 1
while block_rep[left_idx] != '.':
    left_idx +=1
while block_rep[right_idx] == '.':
    right_idx -= 1
while right_idx > left_idx:
    block_rep[left_idx] = block_rep[right_idx]
    block_rep[right_idx] = '.'
    while block_rep[left_idx] != '.':
        left_idx +=1
    while block_rep[right_idx] == '.':
        right_idx -= 1

# calculate sum product of block ids and block rep indices
output = 0
for block_rep_idx, block_id in zip(range(len(block_rep)), block_rep):
    if block_id != '.':
        output += (block_rep_idx * block_id)

print(output)

# PART II

def count_seq(block_rep, idx):
    ch1 = ch2 = block_rep[idx]
    count = 1
    while ch2 == ch1 and idx <= len(block_rep) - 2:
        idx += 1
        ch2 = block_rep[idx]
        if ch2 == ch1:
            count += 1
    return count
        
def find_first(block_rep, ch):
    for i in range(len(block_rep)):
        if block_rep[i] == ch:
            return i

def find_next(block_rep, ch, idx):
    for i in range(idx + 1, len(block_rep)):
        if block_rep[i] == ch:
            return i

block_rep = orig_block_rep

# get highest block ID
block_id = block_rep[-1]

left_idx = find_first(block_rep, '.')
right_idx = find_first(block_rep, block_id)
while block_id > 0:
    allocated = False
    space_needed = count_seq(block_rep, right_idx)
    while not allocated and (left_idx < right_idx):
        space_available = count_seq(block_rep, left_idx)
        if space_available >= space_needed:
            block_rep[left_idx:left_idx + space_needed] = block_rep[right_idx:right_idx + space_needed]
            for i in range(right_idx, right_idx + space_needed):
                block_rep[i] = '.'
            allocated = True
        else:
            left_idx = find_next(block_rep, '.', left_idx)
    left_idx = find_first(block_rep, '.')
    block_id -= 1
    right_idx = find_first(block_rep, block_id)
    if block_id % 100 == 0:
        print(block_id)


output = 0
for block_rep_idx, block_id in zip(range(len(block_rep)), block_rep):
    if block_id != '.':
        output += (block_rep_idx * block_id)

print(output)
