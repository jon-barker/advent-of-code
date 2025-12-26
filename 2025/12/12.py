import numpy as np


with open("input.txt", "r") as f:
    data = f.readlines()

shapes = []
bins = []
bin_reqs = []

new_shape = False
shape = []
for d in data:
    d = d.strip('\n')
    if d == '':
        if len(shape) > 0 and new_shape:
            shapes.append(np.array(shape))
            new_shape = False
        continue
    elif ':' in d and 'x' not in d:
        new_shape = True
        shape = []
    elif ':' not in d:
        d = [1 if c == '#' else 0 for c in d]
        shape.append(d)
    elif 'x' in d:
        bins.append(d.split(' ')[0].split('x'))
        bin_reqs.append([int(c) for c in d.split(' ')[1:]])
bins = [[int(b[0]), int(b[1][:-1])] for b in bins]

shape_areas = [s.sum() for s in shapes]

print(shapes)
print(bins)
print(bin_reqs)
print(shape_areas)

# Dumb check for part 1 - just iterate over the problems and throw out those
# where the total required area would exceed what's available even
# if the shapes were perfectly packed
#
# This works!!!
count = 0
for b_idx, bin in enumerate(bins):
    bin_area = bin[0] * bin[1]
    required_area = 0
    for s_idx, repeats in enumerate(bin_reqs[b_idx]):
        required_area += (shape_areas[s_idx] * repeats)
    if required_area <= bin_area:
        count += 1
        print(f"{count} found, {b_idx + 1} checked out of {len(bins)}\n")

