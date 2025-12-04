inp = open("input.txt", "r").readlines()

# PART I - naive brute force

S = 0
for row in inp:
    largest = 0
    l_idx = 0
    for i, c in enumerate(row):
        if c == '\n' or i == len(row) - 2:
            continue
        if int(c) > largest:
            largest = int(c)
            l_idx = i
    second = 0
    s_idx = l_idx + 1
    for i in range(s_idx, len(row) - 1):
        if int(row[i]) > second:
            second = int(row[i])
    S += int(str(largest) + str(second))
print(S)

# PART II
S = 0
for row in inp:
    if row[-1] == '\n':
        row = row[:-1]
    left = 0
    R = ''
    while (left < len(row)) and len(R) < 12:
        largest = int(row[left])
        l_idx = left
        right = len(row) - (12 - (len(R) + 1))
        if right > len(row): right = len(row)
        for i in range(left, right):
            if int(row[i]) > largest:
                largest = int(row[i])
                l_idx = i
        R += str(largest)
        left = l_idx + 1
    S += int(R)
print(S)