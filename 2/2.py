import csv
import numpy as np

def is_safe(levels: np.array) -> bool:
    diff = levels[1:] - levels[0:-1]    
    # check all increasing or decreasing
    if (diff < 0).all() or (diff > 0).all():
        if (np.abs(diff) > 0).all() and (np.abs(diff) < 4).all():
            return True
    return False

# Open and read the file
safe_count_1 = 0
extras = 0
with open('2/input.txt', 'r') as file:
    reader = csv.reader(file, delimiter='\t')  # Specify tab as the delimiter
    for row in reader:
        levels = np.array([int(r) for r in row[0].split(' ')])
        if is_safe(levels):
            safe_count_1 += 1
        else:
            for i in range(len(levels)):
                if is_safe(np.concatenate((levels[:i], levels[i+1:]), -1)):
                    extras += 1
                    break

print(safe_count_1)
print(safe_count_1 + extras)
