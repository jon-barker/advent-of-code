from copy import deepcopy
import csv

# Open and read the file
# hash table where before_rules[item] returns a list of all items that should preceed item
before_rules = {}
# hash table where after_rules[item] returns a list of all items that should succeed item
after_rules = {}
with open('5/input.txt', 'r') as file:
    reader = csv.reader(file) 
    count_1 = 0
    count_2 = 0
    for row in reader:
        if len(row) > 0 and '|' in row[0]:
            first, second = row[0].split('|')
            first = int(first)
            second = int(second)
            if first in after_rules:
                after_rules[first].append(second)
            else:
                after_rules[first] = [second]
            if second in before_rules:
                before_rules[second].append(first)
            else:
                before_rules[second] = [first]

        # Part 1 case
        invalid = False
        if len(row) > 1:
            row = [int(r) for r in row]
            for i, r in enumerate(row):
                for b in range(0, i):
                    if r in after_rules and row[b] in after_rules[r]:
                        invalid = True
                        break
                if not invalid:
                    for a in range(i+1, len(row)-1):
                        if r in before_rules and row[a] in before_rules[r]:
                            invalid = True
                            break
            if not invalid:
                middle = row[len(row) // 2]
                count_1 += middle
            else:
                # Part 2 case
                row_len = len(row)
                while invalid:
                    skip = False
                    for i in range(len(row)):
                        r = row[i]
                        for b in range(0, i):
                            if r in after_rules and row[b] in after_rules[r]:
                                row = row[:b] + row[b+1:i+1] + row[b:b+1] + row[i+1:] 
                                skip = True
                                break
                        if not skip:
                            for a in range(i+1, len(row)-1):
                                if r in before_rules and row[a] in before_rules[r]:
                                    row = row[:i] + row[a:a+1] + row[i:a] + row[a+1:] 
                                    skip = True
                                    break
                        if skip:
                            break
                    if not skip:
                        invalid = False
                middle = row[len(row) // 2]
                count_2 += middle

print(count_1)
print(count_2)
