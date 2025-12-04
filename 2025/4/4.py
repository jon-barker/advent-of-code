import numpy as np

with open("input.txt", "r") as f:
    lines = [line.rstrip("\n") for line in f if line.strip() != ""]

# PART I

arr = np.array([[1 if ch == "@" else 0 for ch in line] for line in lines], dtype=np.int8)
arr = np.pad(arr, ((1, 1), (1, 1)), constant_values=0)
arr2 = arr.copy()

S = 0
for row in range(0, arr.shape[0]):
    for col in range(0, arr.shape[1]):
        if arr[row, col] == 1:
            adjacent = arr[row-1:row+2, col-1:col+2]
            adjacent = adjacent.sum() - 1
            if adjacent < 4:
                arr2[row, col] = 0
                S += 1
print(S)

# PART II
arr = arr2.copy()
total_removals = S
while S > 0:
    S = 0
    for row in range(0, arr.shape[0]):
        for col in range(0, arr.shape[1]):
            if arr[row, col] == 1:
                adjacent = arr[row-1:row+2, col-1:col+2]
                adjacent = adjacent.sum() - 1
                if adjacent < 4:
                    arr2[row, col] = 0
                    S += 1
    total_removals += S
    arr = arr2.copy()
print(total_removals)
