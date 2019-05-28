def get_list_structure(partition):
    cyc = []
    part = []
    if len(partition) == 0:
        return cyc
    cyc.append([[None] * partition[0]])
    index = 0
    part.append(partition[0])
    for i in range(1, len(partition)):
        if partition[i] == partition[i - 1]:
            cyc[index].append([None] * partition[i])
        else:
            index += 1
            cyc.append([[None]*partition[i]])
            part.append(partition[i])
    return {'list_structure': cyc, 'parts': part}


def get_conj_class(partition):
    n = sum(partition)
    partition.sort()
    obj = get_list_structure(partition)
    cyc = obj['list_structure']
    part = obj['parts']
    used = [False]*n
    create_con_class(cyc, used, 0)


def create_con_class(cyc, used, count):
    no_empty_spot = True
    x = y = z = 0
    for i in range(len(cyc)):
        for j in range(len(cyc[i])):
            for k in range(len(cyc[i][j])):
                if cyc[i][j][k] is None:
                    no_empty_spot = False
                    x = i
                    y = j
                    z = k
                    break
            if not no_empty_spot:
                break
        if not no_empty_spot:
            break
    if no_empty_spot:
        count += 1
        print(count)
        print(cyc)
        return
    start = 0
    for a in range(start, len(used)):
        if not used[a]:
            if z == 0:
                if y == 0:
                    cyc[x][y][z] = a+1
                    used[a] = True
                    create_con_class(cyc, used, count)
                    cyc[x][y][z] = None
                    used[a] = False
                else:
                    if a+1 > cyc[x][y-1][0]:
                        cyc[x][y][z] = a + 1
                        used[a] = True
                        create_con_class(cyc, used, count)
                        cyc[x][y][z] = None
                        used[a] = False
            else:
                if a+1 > cyc[x][y][0]:
                    cyc[x][y][z] = a + 1
                    used[a] = True
                    create_con_class(cyc, used, count)
                    cyc[x][y][z] = None
                    used[a] = False
    return
