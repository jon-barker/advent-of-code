fresh_ranges = []
available = []

with open("input.txt", "r") as f:
    blank = False
    for row in f.readlines():
        if row == "\n": 
            blank = True 
            continue
        if not blank:
            fresh_ranges.append([int(i) for i in row[:-1].split('-')])
        else:
            available.append(int(row[:-1]))

# print(fresh_ranges)
# print(available)

# PART I

total = 0
for a in available:
    found = False
    for r in fresh_ranges:
        if a >= r[0] and a <= r[1]:
            found = True
            break
    if found:
        total += 1

print(total)

# PART II
more_merges = True
while more_merges:
    merged_ranges = [fresh_ranges[0]]
    for r in fresh_ranges[1:]:
        found_merge = False
        for i, s in enumerate(merged_ranges):
            if r[0] <= s[1] and r[1] >= s[0]:
                found_merge = True
                merged_ranges[i] = [min(r[0], s[0]), max(r[1], s[1])]
                break
        if not found_merge:
            merged_ranges.append(r)
    if len(merged_ranges) == len(fresh_ranges):
        more_merges = False
    fresh_ranges = merged_ranges

total = 0
for m in merged_ranges:
    total += m[1] - m[0] + 1
print(total)