from copy import deepcopy
import csv
from functools import lru_cache
from math import floor

# Open and read the file
with open('17/input.txt', 'r') as file:
    reader = csv.reader(file, delimiter=' ') 
    for row in reader:
        if len(row) == 0:
            continue
        elif row[0] == 'Register':
            if row[1] == 'A:':
                rA = int(row[2])
            elif row[1] == 'B:':
                rB = int(row[2])
            elif row[1] == 'C:':
                rC = int(row[2])
        elif row[0] == 'Program:':
            ins = [int(i) for i in row[1].split(',')]

# PART I

@lru_cache(1000000)
def get_combo(opr, rA, rB, rC):
    if opr < 4:
        return opr
    elif opr == 4:
        return rA
    elif opr == 5:
        return rB
    elif opr == 6:
        return rC

output = []
inst_p = 0
while inst_p < len(ins):
    opc = ins[inst_p]
    opr = ins[inst_p + 1]
    if opc == 0:
        num = rA
        den = 2 ** get_combo(opr, rA, rB, rC)
        rA = floor(num / den) 
        inst_p += 2
    elif opc == 1:
        rB = rB ^ opr
        inst_p += 2
    elif opc == 2:
        rB = get_combo(opr, rA, rB, rC) % 8
        inst_p += 2
    elif opc == 3:
        if rA != 0:
            inst_p = opr
        else:
            inst_p += 2
    elif opc == 4:
        rB = rB ^ rC
        inst_p += 2
    elif opc == 5:
        output.append(get_combo(opr, rA, rB, rC) % 8)
        inst_p += 2
    elif opc == 6:
        num = rA
        den = 2 ** get_combo(opr, rA, rB, rC)
        rB = floor(num / den) 
        inst_p += 2
    elif opc == 7:
        num = rA
        den = 2 ** get_combo(opr, rA, rB, rC)
        rC = floor(num / den) 
        inst_p += 2

print(output)
print(','.join([str(o) for o in output]))

# PART II

working_bits = 0
rA_base = int(working_bits)
for i in range(len(ins)):
    found = False
    while not found and rA_base >= 0:
        rA = rA_base << 3 * (len(ins) - i - 1)
        rB = 0
        rC = 0
        output = []
        inst_p = 0
        while inst_p < len(ins):
            opc = ins[inst_p]
            opr = ins[inst_p + 1]
            if opc == 0:
                num = rA
                den = 2 ** get_combo(opr, rA, rB, rC)
                rA = floor(num / den) 
                inst_p += 2
            elif opc == 1:
                rB = rB ^ opr
                inst_p += 2
            elif opc == 2:
                rB = get_combo(opr, rA, rB, rC) % 8
                inst_p += 2
            elif opc == 3:
                if rA != 0:
                    inst_p = opr
                else:
                    inst_p += 2
            elif opc == 4:
                rB = rB ^ rC
                inst_p += 2
            elif opc == 5:
                output.append(get_combo(opr, rA, rB, rC) % 8)
                inst_p += 2
            elif opc == 6:
                num = rA
                den = 2 ** get_combo(opr, rA, rB, rC)
                rB = floor(num / den) 
                inst_p += 2
            elif opc == 7:
                num = rA
                den = 2 ** get_combo(opr, rA, rB, rC)
                rC = floor(num / den) 
                inst_p += 2
        if len(output) == len(ins) and output[len(output) - i - 1:] == ins[len(ins) - i - 1:]:
            rA_base = rA_base << 3
            break
        else:
            rA_base += 1
    print(i, len(ins))
print(rA_base >> 3)
