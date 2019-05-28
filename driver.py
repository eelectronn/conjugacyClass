import operation
import time as t
import math as m

before = t.time_ns()
obj = operation.get_conj_class([3, 3, 4])
after = t.time_ns()
print('%.20f' % ((after - before)*m.pow(10, -9)))
