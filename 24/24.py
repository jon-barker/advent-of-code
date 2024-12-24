from copy import deepcopy
import csv

# Open and read the file
wires = {}
gates = []
with open('24/input.txt', 'r') as file:
    reader = csv.reader(file, delimiter=' ') 
    for row in reader:
        if len(row) == 0:
            continue
        elif ':' in row[0]:
            wires[row[0][:-1]] = int(row[1])
        elif '->' in row:
            w1 = row[0]
            gtype = row[1]
            w2 = row[2]
            wo = row[-1]
            gates.append((w1, w2, gtype, wo))
print(len(gates))

orig_gates = deepcopy(gates)
orig_wires = deepcopy(wires)

# PART I

while gates:
    for g in gates:
        if g[0] in wires and g[1] in wires:
            if g[2] == 'AND':
                wires[g[3]] = int(wires[g[0]] and wires[g[1]])
            elif g[2] == 'OR':
                wires[g[3]] = int(wires[g[0]] or wires[g[1]])
            elif g[2] == 'XOR':
                wires[g[3]] = int(wires[g[0]] ^ wires[g[1]])
            gates.remove(g)

z_wires = {w:wires[w] for w in wires if w[0] == 'z'}
binary = ''
for i in range(len(z_wires) - 1, -1, -1):
    binary += str(z_wires[f"z{i:02}"])
print(binary)
print(int(binary, 2))

# PART II
# I believe the solution is that the correct circuit is
# ripple-carry adder made from full adders
# so the question is how to automatically find where
# it's wrong without just drawing the whole thing out
# on paper...

# I believe the first half-adder is correct, so we
# just need to search the full-adders
        
# For each full adder we will initialize the input wires
# Then for each truth-table entry we'll run the gates
# but this time we'll remove wires from the output if they
# get used in a subsequent rule.
# If we find a truth-table entry with an error then we
# know 

TRUTH_TABLE = {
    (0, 0, 0): (0, 0),
    (0, 0, 1): (0, 1),
    (0, 1, 0): (0, 1),
    (0, 1, 1): (1, 0),
    (1, 0, 0): (0, 1),
    (1, 0, 1): (1, 0),
    (1, 1, 0): (1, 0),
    (1, 1, 1): (1, 1),
}

# Figured out manually from half-adder
C = 'fhd'
for i in range(1, 45):
    for t in TRUTH_TABLE:
        wires = {w:orig_wires[w] for w in deepcopy(orig_wires) if (f'y{i:02}' in w or 'x{i:02}' in w or C in w)}
        wires[f'x{i:02}'] = t[0]
        wires[f'y{i:02}'] = t[1]
        wires[C] = t[2]
        gates = deepcopy(orig_gates)
        while len(wires) < 8:
            for g in gates:
                if g[0] in wires and g[1] in wires:
                    if g[2] == 'AND':
                        wires[g[3]] = int(wires[g[0]] and wires[g[1]])
                    elif g[2] == 'OR':
                        wires[g[3]] = int(wires[g[0]] or wires[g[1]])
                        C1 = g[3]
                    elif g[2] == 'XOR':
                        wires[g[3]] = int(wires[g[0]] ^ wires[g[1]])
                    gates.remove(g)
        c_out = wires[C1]
        s_out = wires[[w for w in wires if 'z' in w][0]]
        assert (c_out, s_out) == TRUTH_TABLE[t], f"Error in adder {i}"
    C = C1

# Swaps manually applied:
# adder 6: dhg <-> z06
# adder 11: dpd <-> brk
# adder 23: z23 <-> bhd
# adder 38: nbf <-> z38

output = ','.join(sorted(['dhg', 'z06', 'dpd', 'brk', 'z23', 'bhd', 'nbf', 'z38']))
print(output)
