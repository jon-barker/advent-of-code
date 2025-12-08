import numpy as np
from scipy.sparse.csgraph import connected_components

# PART I 

jboxes = np.loadtxt("input.txt", delimiter=',')
N = 1000

# work out the euclidean distance between each pair of 3D coords
distances = np.sqrt(np.sum((jboxes[:, None, :] - jboxes[None, :, :])**2, axis=-1))
distances[np.where(distances == 0)] = np.inf

affinity = np.zeros_like(distances)

# perform N iterations of:
for i in range(N):
    # find closest pair of coords
    c_idx = np.where(distances == distances.min())
    rows, cols = c_idx
    # set that connection (and it's transpose) to a large number in pairwise distances
    distances[rows, cols] = np.inf
    distances[cols, rows] = np.inf
    # update affinity matrix
    affinity[rows, cols] = 1

# we only need the non-directed graph
affinity = (affinity + affinity.T).clip(0, 1)

# find the connected components
components = connected_components(affinity, directed=False)
# multiply the size of the 3 largest non-zero components together to get final answer
sizes = sorted([(components[1] == i).sum() for i in range(components[0])])
out = np.prod(sizes[-3:])
print(out)

# PART II
jboxes = np.loadtxt("input.txt", delimiter=',')

# work out the euclidean distance between each pair of 3D coords
distances = np.sqrt(np.sum((jboxes[:, None, :] - jboxes[None, :, :])**2, axis=-1))
distances[np.where(distances == 0)] = np.inf

affinity = np.zeros_like(distances)

biggest_component = 0

# perform N iterations of:
while biggest_component < affinity.shape[0]:
    # find closest pair of coords
    c_idx = np.where(distances == distances.min())
    rows, cols = c_idx
    # set that connection (and it's transpose) to a large number in pairwise distances
    distances[rows, cols] = np.inf
    distances[cols, rows] = np.inf
    # update affinity matrix
    affinity[rows, cols] = 1

    # we only need the non-directed graph
    affinity = (affinity + affinity.T).clip(0, 1)

    # find the connected components
    components = connected_components(affinity, directed=False)
    csize = max(np.array([(components[1] == i).sum() for i in range(components[0])]))
    if csize > biggest_component:
        biggest_component = csize
        print(f"New biggest component found of size: {biggest_component}")
print(int(jboxes[c_idx[0][0]][0] * jboxes[c_idx[0][1]][0]))