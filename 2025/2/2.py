# PART I

def has_repeat(n):
    l = len(str(n))
    if l % 2 == 1:
        return False
    if str(n)[:l//2] == str(n)[l//2:]:
        return True
    return False

with open("input.txt", "r") as f:
    ranges = f.read().split(',')

S = 0
for r in ranges:
    s, e = r.split('-')
    for i in range(int(s), int(e) + 1):
        if has_repeat(i):
            S += i

print(S)

## PART II
def has_repeat_2(n):
    l = len(str(n))
    # iterate over possible chunk sizes
    for i in range((l//2), 0, -1):
        # check the number of digits has no residual mod chunk size
        if l % i == 0:
            # split the number into chunks
            chunks = [str(n)[j*i:(j*i)+i] for j in range(l//i)]
            # check all chunks are the same
            equal = all([c == chunks[0] for c in chunks])
            if equal:
                return True
    return False

with open("input.txt", "r") as f:
    ranges = f.read().split(',')

S = 0
for r in ranges:
    s, e = r.split('-')
    for i in range(int(s), int(e) + 1):
        if has_repeat_2(i):
            S += i

print(S)
