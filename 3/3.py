import csv
import re

# Open and read the file
total = 0
with open('3/input.txt', 'r') as file:
    reader = csv.reader(file, delimiter='\t')  # Specify tab as the delimiter
    for row in reader:
        pattern = r"mul\(\d{1,3},\d{1,3}\)"
        matches = re.findall(pattern, str(row))
        for m in matches:
            m = m.strip("mul(").strip(")").split(",")
            total += (int(m[0]) * int(m[1]))

print(total)

total = 0
with open('3/input.txt', 'r') as file:
    reader = csv.reader(file, delimiter='\t')  # Specify tab as the delimiter
    enabled = True
    for row in reader:
        pattern = r"mul\(\d{1,3},\d{1,3}\)|do\(\)|don't\(\)"
        matches = re.findall(pattern, str(row))
        for m in matches:
            if m == "do()":
                enabled = True
            elif m == "don't()":
                enabled = False
            elif enabled:
                m = m.strip("mul(").strip(")").split(",")
                total += (int(m[0]) * int(m[1]))

print(total)
