import sys
import operation

a = sys.argv
partition = []
index = 1
fileName = 'file.txt'
output = 'cycle'
count = False

# print(a)

for i in range(1, len(a)):
    if a[i].isdigit():
        partition.append(int(a[i]))
    else:
        index = i
        break

if index < len(a) and index != 1:
    fileName = a[index]
    index += 1

if index < len(a) and index != 1:
    output = a[index]
    index += 1

if index < len(a):
    if a[index] == 'y' and index != 1:
        count = True

f = open(fileName, 'wt')

operation.get_conj_class(partition, f, output, count)
