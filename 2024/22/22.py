from collections import defaultdict
from functools import lru_cache
from copy import deepcopy
import csv

# Open and read the file
ins = []
with open('22/input.txt', 'r') as file:
    reader = csv.reader(file) 
    for row in reader:
        ins.append(int(row[0]))


@lru_cache(maxsize=None)
def mix_and_prune(x, y):
    x = x ^ y
    x = x % 16777216
    return x        

@lru_cache(maxsize=None)
def next_secret(s):

    s1 = s * 64
    s = mix_and_prune(s, s1)

    s1 = s // 32
    s = mix_and_prune(s, s1)

    s1 = s * 2048
    s = mix_and_prune(s, s1)

    return s

# Test next_secret
# s = 123
# for i in range(10):
#     s = next_secret(s)
#     print(s)

# PART I
# total = 0
# for i in ins:
#     s = i
#     for _ in range(2000):
#         s = next_secret(s)
#     total += s

# print(total)

# PART II
seqs = []
diffs = []
for idx, this_s in enumerate(ins):
    seqs.append([])
    diffs.append([])
    seqs[idx] = [this_s % 10]
    diffs[idx] = [0]
    s = this_s
    for _ in range(2001):
        s_new = next_secret(s)
        seqs[idx].append(s_new % 10)
        diffs[idx].append((s_new % 10) - (s % 10))
        s = s_new

test_diffs = defaultdict(int)
for diff, seq in zip(diffs, seqs):
    seen = set()
    for i in range(0, len(diff) - 3):
        if tuple(diff[i:i+4]) not in seen:
            profit = seq[i + 3]
            seen.add(tuple(diff[i:i+4]))
            test_diffs[tuple(diff[i:i+4])] += profit

print(max(test_diffs.values()))
