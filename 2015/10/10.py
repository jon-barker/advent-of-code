# input = 111221 # 312211 (test)
input = 1113222113 # (real input)

input = str(input)

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

for _ in range(40):
    split = split_runs(input)
    input = ''
    for s in split:
        input += str(len(s))
        input += s[0]

print(len(input))
