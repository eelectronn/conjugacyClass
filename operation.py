def get_conj_class(partition, f):
    n = sum(partition)
    partition.sort()
    cyc = get_list_structure(partition)
    used = [False]*n
    create_con_class(cyc, used, 0, f)


def get_list_structure(partition):
    cyc = []
    if len(partition) == 0:
        return cyc
    cyc.append([[None] * partition[0]])
    index = 0
    for i in range(1, len(partition)):
        if partition[i] == partition[i - 1]:
            cyc[index].append([None] * partition[i])
        else:
            index += 1
            cyc.append([[None]*partition[i]])
    return cyc


def create_con_class(cyc, used, count, f, position=None):
    obj = get_next_slot(position, cyc)
    no_empty_spot, position = obj['no_more_spot'], obj['array']
    if no_empty_spot:
        count += 1
        write_in_file(cyc, count, f)
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
                    obj = rec_call(cyc, used, count, position, x, y, z, a, f)
                    count, position = obj['count'], obj['position']
                else:
                    if a+1 > cyc[x][y-1][0]:
                        obj = rec_call(cyc, used, count, position, x, y, z, a, f)
                        count, position = obj['count'], obj['position']
            else:
                if a+1 > cyc[x][y][0]:
                    obj = rec_call(cyc, used, count, position, x, y, z, a, f)
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


def rec_call(cyc, used, count, position, x, y, z, a, f):
    cyc[x][y][z] = a + 1
    used[a] = True
    count = create_con_class(cyc, used, count, f, position)
    position = [x, y, z]
    cyc[x][y][z] = None
    used[a] = False
    return {'position': position, 'count': count}


def write_in_file(cyc, count, f):
    # f.write(str(count)+'\n')
    s = ''
    for block in cyc:
        for cycle in block:
            s += str(cycle) + ' '
    f.write(s+'\n')
    