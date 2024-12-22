from copy import deepcopy
from collections import defaultdict
from functools import lru_cache
import csv

# Open and read the file
inputs = []
with open('21/input.txt', 'r') as file:
    reader = csv.reader(file) 
    for row in reader:
        inputs.append([r for r in row[0]])

@lru_cache(maxsize=None)
def get_numpad_moves(curr, targ):

    lookup = {
        '00': 'A', '01': '^<A', '02': '^A', '03': '^>A', '04': '^^<A', '05': '^^A', '06': '^^>A',
        '07': '^^^<A', '08': '^^^A', '09': '^^^>A', '0A': '>A',
        '10': '>vA', '11': 'A', '12': '>A', '13': '>>A', '14': '^A', '15': '^>A',
        '16': '^>>A', '17': '^^A', '18': '^^>A', '19': '^^>>A', '1A': '>>vA',
        '20': 'vA', '21': '<A', '22': 'A', '23': '>A', '24': '<^A', '25': '^A',
        '26': '^>A', '27': '<^^A', '28': '^^A', '29': '^^>A', '2A': 'v>A',
        '30': '<vA', '31': '<<A', '32': '<A', '33': 'A', '34': '<<^A', '35': '<^A',
        '36': '^A', '37': '<<^^A', '38': '<^^A', '39': '^^A', '3A': 'vA',
        '40': '>vvA', '41': 'vA', '42': 'v>A', '43': 'v>>A', '44': 'A', '45': '>A',
        '46': '>>A', '47': '^A', '48': '^>A', '49': '^>>A', '4A': '>>vvA',
        '50': 'vvA', '51': '<vA', '52': 'vA', '53': 'v>A', '54': '<A', '55': 'A',
        '56': '>A', '57': '<^A', '58': '^A', '59': '^>A', '5A': 'vv>A',
        '60': '<vvA', '61': '<<vA', '62': '<vA', '63': 'vA', '64': '<<A', '65': '<A',
        '66': 'A', '67': '<<^A', '68': '<^A', '69': '^A', '6A': 'vvA',
        '70': '>vvvA', '71': 'vvA', '72': 'vv>A', '73': 'vv>>A', '74': 'vA', '75': 'v>A',
        '76': 'v>>A', '77': 'A', '78': '>A', '79': '>>A', '7A': '>>vvvA',
        '80': 'vvvA', '81': '<vvA', '82': 'vvA', '83': 'vv>A', '84': '<vA', '85': 'vA',
        '86': 'v>A', '87': '<A', '88': 'A', '89': '>A', '8A': 'vvv>A',
        '90': '<vvvA', '91': '<<vvA', '92': '<vvA', '93': 'vvA', '94': '<<vA', '95': '<vA',
        '96': 'vA', '97': '<<A', '98': '<A', '99': 'A', '9A': 'vvvA',
        'A0': '<A', 'A1': '^<<A', 'A2': '<^A', 'A3': '^A', 'A4': '^^<<A', 'A5': '<^^A',
        'A6': '^^A', 'A7': '^^^<<A', 'A8': '<^^^A', 'A9': '^^^A', 'AA': 'A'
    }

    key = curr + targ
    return ''.join(lookup[key])

@lru_cache(maxsize=None)
def get_dirpad_moves(curr, targ):

    lookup = {
        '<<': 'A', '<>': '>>A', '<^': '>^A', '<v': '>A', '<A': '>>^A',
        '><': '<<A', '>>': 'A', '>^': '<^A', '>v': '<A', '>A': '^A',
        '^<': 'v<A', '^>': 'v>A', '^^': 'A', '^v': 'vA', '^A': '>A',
        'v<': '<A', 'v>': '>A', 'v^': '^A', 'vv': 'A', 'vA': '^>A',
        'A<': 'v<<A', 'A>': 'vA', 'A^': '<A', 'Av': '<vA', 'AA': 'A',
    }
    key = curr + targ
    return ''.join(lookup[key])

dirpad = {
    '<<': 'A', '<>': '>>A', '<^': '>^A', '<v': '>A', '<A': '>>^A',
    '><': '<<A', '>>': 'A', '>^': '<^A', '>v': '<A', '>A': '^A',
    '^<': 'v<A', '^>': 'v>A', '^^': 'A', '^v': 'vA', '^A': '>A',
    'v<': '<A', 'v>': '>A', 'v^': '^A', 'vv': 'A', 'vA': '^>A',
    'A<': 'v<<A', 'A>': 'vA', 'A^': '<A', 'Av': '<vA', 'AA': 'A',
}

output = 0
n_start = 'A'
rm1_start = 'A'
rm2_start = 'A'
for code in inputs:
    final_moves = []
    for c in code:
        robot1_moves = get_numpad_moves(n_start, c)
        for rm1 in robot1_moves:
            robot2_moves = get_dirpad_moves(rm1_start, rm1)
            for rm2 in robot2_moves:
                me_moves = get_dirpad_moves(rm2_start, rm2)
                for m in me_moves:
                    final_moves.append(m)
                rm2_start = rm2
            rm1_start = rm1
        n_start = c
    print(int(''.join(code)[:-1]), len(final_moves))
    output += (int(''.join(code)[:-1]) * len(final_moves))

print(output)

# PART II

# At each layer we keep track of all the unique moves needed from the layer
# above and how many times each one occurs
# Then we only need to work out the next level of that move once but can
# update the total count for as many that occur as needed

output = 0
for code in inputs:
    final_moves = 0
    moves = ''.join(get_numpad_moves(a, b) for (a, b) in zip(['A'] + code, code))
    count = defaultdict(int)
    for (m, n) in zip('A' + moves, moves):
        count[m + n] += 1
    for _ in range(25):
        count2 = defaultdict(int)
        for k in count.keys():
            for (p, q) in zip('A' + dirpad[k], dirpad[k]):
                count2[p + q] += count[k]
        count = deepcopy(count2)
    final_moves = sum(count.values())
    print(int(''.join(code)[:-1]), final_moves)
    output += (int(''.join(code)[:-1]) * final_moves)

print(output)
