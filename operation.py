def get_conj_class(partition, f, output, print_count):
    n = sum(partition)
    partition.sort()
    cyc = get_list_structure(partition)
    used = [False]*n
    create_con_class(cyc, used, 0, f, output, print_count)
    if output == 'pattern':
        write_pattern_file(f)


def get_list_structure(partition):
    cyc = []
    if len(partition) == 0:
        return cyc
    cyc.append([[None]*partition[0]])
    index = 0
    for i in range(1, len(partition)):
        if partition[i] == partition[i - 1]:
            cyc[index].append([None]*partition[i])
        else:
            index += 1
            cyc.append([[None]*partition[i]])
    return cyc


def create_con_class(cyc, used, count, f, output, print_count, position=None):
    obj = get_next_slot(position, cyc)
    no_empty_spot, position = obj['no_more_spot'], obj['array']
    if no_empty_spot:
        count += 1
        if output in switch:
            switch[output](len(used), cyc, count, print_count, f)
        else:
            write_cycle_file(len(used), cyc, count, print_count, f)
        return count
    x, y, z = position[0], position[1], position[2]
    start, end = 0, len(used)
    if z == 0:
        end = len(used) - len(cyc[x]) + y + 1
    if y != 0:
        start = cyc[x][y-1][0]
    for a in range(start, end):
        if not used[a]:
            if z == 0:
                if y == 0:
                    obj = rec_call(cyc, used, count, position, output, print_count, x, y, z, a, f)
                    count, position = obj['count'], obj['position']
                else:
                    if a+1 > cyc[x][y-1][0]:
                        obj = rec_call(cyc, used, count, position, output, print_count, x, y, z, a, f)
                        count, position = obj['count'], obj['position']
            else:
                if a+1 > cyc[x][y][0]:
                    obj = rec_call(cyc, used, count, position, output, print_count, x, y, z, a, f)
                    count, position = obj['count'], obj['position']
    return count


def get_next_slot(array, cyc):
    if array is None:
        return {'array': [0, 0, 0], 'no_more_spot': False}
    if len(cyc[array[0]][array[1]]) > array[2] + 1:
        array[2] += 1
        return {'array': array, 'no_more_spot': False}
    if len(cyc[array[0]]) > array[1] + 1:
        array[1] += 1
        array[2] = 0
        return {'array': array, 'no_more_spot': False}
    if len(cyc) > array[0] + 1:
        array[0] += 1
        array[1] = array[2] = 0
        return {'array': array, 'no_more_spot': False}
    return {'array': None, 'no_more_spot': True}


def rec_call(cyc, used, count, position, output, print_count, x, y, z, a, f):
    cyc[x][y][z] = a + 1
    used[a] = True
    count = create_con_class(cyc, used, count, f, output, print_count, position)
    position = [x, y, z]
    cyc[x][y][z] = None
    used[a] = False
    return {'position': position, 'count': count}


def write_cycle_file(n, cyc, count, print_count, f):
    if print_count:
        f.write(str(count)+'\n')
    s = ''
    for block in cyc:
        for cycle in block:
            s += str(cycle) + ' '
    f.write(s+'\n')


def write_inline_file(n, cyc, count, print_count, f):
    if print_count:
        f.write(str(count)+'\n')
    inline = to_inline(n, cyc)
    f.write(str(inline)+'\n')


def to_inline(n, cyc):
    inline = [None] * n
    for block in cyc:
        for cycle in block:
            for i in range(len(cycle)):
                inline[cycle[i] - 1] = cycle[(i + 1) % len(cycle)]
    return inline


def pattern_frequency(n, cyc, count=None, print_count=None, f=None):
    if n < 2:
        return
    inline = to_inline(n, cyc)
    s = ''
    for i in range(1, n):
        if inline[i] > inline[i-1]:
            s += 'u'
        else:
            s += 'd'
    if s in pattern:
        pattern[s] += 1
    else:
        pattern[s] = 1


pattern = {}


def write_pattern_file(f):
    for seq in sorted(pattern.keys()):
        f.write(str(seq) + '  :  ' + str(pattern[seq]) + '\n')


switch = {
    'inline': write_inline_file,
    'cycle': write_cycle_file,
    'pattern': pattern_frequency
}
