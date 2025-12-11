from functools import lru_cache

@lru_cache(None)
def dfs(child, fft=False, dac=False, part2=False):
    if child == 'out':
        return 1 if ((not part2) or (fft and dac)) else 0
    new_dac = dac or (child == 'dac')
    new_fft = fft or (child == 'fft')
    total = 0
    for c in edges[child]:
        total += dfs(c, new_fft, new_dac, part2=part2)
    return total


# PART I
with open("input.txt", "r") as f:
    data = f.readlines()
    data = [d.strip('\n').split(' ') for d in data]

global edges
edges = {}
for d in data:
    edges[d[0][:-1]] = d[1:]

found = dfs('you')
print(found)

# PART II
with open("input.txt", "r") as f:
    data = f.readlines()
    data = [d.strip('\n').split(' ') for d in data]


edges = {}
for d in data:
    edges[d[0][:-1]] = d[1:]
found = dfs('svr', part2=True)
print(found)

            