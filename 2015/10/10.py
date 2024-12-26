# input = 111221 # 312211 (test)
orig_input = str(1113222113) # (real input)

# PART I

def split_runs(input):
    seq = input[0]
    split = []
    for next in input[1:]:
        if next == seq[-1]:
            seq += next
        else:
            split.append(seq)
            seq = next
    if len(seq) > 0:
        split.append(seq)
    return split

input = orig_input

for _ in range(40):
    split = split_runs(input)
    input = [str(len(s)) + str(s[0]) for s in split]
    input = ''.join(input)

print(len(input))

# PART II

input = orig_input

for i in range(50):
    print(i)
    split = split_runs(input)
    input = [str(len(s)) + str(s[0]) for s in split]
    input = ''.join(input)

print(len(input))
