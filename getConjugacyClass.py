import sys
import operation

a = sys.argv
partition = []

output = 'pattern'

for i in range(1, len(a)-1):
    partition.append(int(a[i]))

f = open(a[len(a)-1], 'wt')

operation.get_conj_class(partition, f, output)
