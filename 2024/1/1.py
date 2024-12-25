import csv

list1 = []
list2 = []

with open('1/input.txt', 'r') as file:
    reader = csv.reader(file, delimiter=' ')  # Specify tab as the delimiter
    for row in reader:
        list1.append(row[0])  # Append first column to list1
        list2.append(row[-1])  # Append second column to list2

list1 = sorted(list1) 
list2 = sorted(list2) 

answer = 0
for i1, i2 in zip(list1, list2):
    answer += abs(int(i1) - int(i2))

print(answer)

counts = {}
for i2 in list2:
    if i2 in counts:
        counts[i2] += 1
    else:
        counts[i2] = 1

answer = 0
for i1 in list1:
    if i1 in counts:
        answer += (int(i1) * counts[i1])

print(answer)
