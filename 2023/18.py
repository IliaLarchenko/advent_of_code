def prepare_data(file="input.txt"):
    with open(file) as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines]
    directoins = [x[0] for x in lines]
    dist = [int(x.split()[1]) for x in lines]
    colors = [x.split()[2] for x in lines]

    colors_dist = [int(c[2:7], 16) for c in colors]
    d = "RDLU"
    colors_directoins = [d[int(c[7])] for c in colors]

    return {
        "directoins": directoins,
        "dist": dist,
        "colors_dist": colors_dist,
        "colors_directoins": colors_directoins,
    }


def get_next(i, j, direct, dist):
    if direct == "R":
        return i, j + dist
    elif direct == "L":
        return i, j - dist
    elif direct == "U":
        return i - dist, j
    elif direct == "D":
        return i + dist, j


def get_corners(directoins, dist):
    corners = [(0, 0)]
    for direct, d in zip(directoins, dist):
        i, j = get_next(corners[-1][0], corners[-1][1], direct, d)
        corners.append((i, j))

    i_min, i_max = min([x[0] for x in corners]), max([x[0] for x in corners])
    j_min, j_max = min([x[1] for x in corners]), max([x[1] for x in corners])

    corners_new = [(i - i_min, j - j_min) for i, j in corners]

    return corners_new


def get_blocks(corners, index=0):
    all_i = sorted(list(set([x[index] for x in corners])))
    i_blocks = []  # (start, len)
    i_to_block = {}
    i_blocks.append((all_i[0], 1))
    i_to_block[all_i[0]] = 0
    for i in range(len(all_i) - 1):
        i_blocks.append((all_i[i] + 1, all_i[i + 1] - all_i[i] - 1))
        i_blocks.append((all_i[i + 1], 1))
        i_to_block[all_i[i + 1]] = 2 * i + 2

    return i_blocks, i_to_block


def get_matrix(corners, i_blocks, i_to_block, j_blocks, j_to_block):
    matrix = [["." for __ in range(len(j_blocks))] for _ in range(len(i_blocks))]

    matrix[i_to_block[corners[0][0]]][j_to_block[corners[0][1]]] = "#"
    i, j = corners[0]
    for k in range(len(corners) - 1):
        i1, j1 = corners[k + 1]
        if i1 == i:
            i_m = i_to_block[i1]
            j2 = min(j1, j)
            j_m = min(j_to_block[j1], j_to_block[j])
            while j2 <= max(j1, j):
                matrix[i_m][j_m] = "#"
                j2 += j_blocks[j_m][1]
                j_m += 1

        if j1 == j:
            j_m = j_to_block[j1]
            i2 = min(i1, i)
            i_m = min(i_to_block[i1], i_to_block[i])
            while i2 <= max(i1, i):
                matrix[i_m][j_m] = "#"
                i2 += i_blocks[i_m][1]
                i_m += 1

        i, j = corners[k + 1]

    return matrix


def get_adj(i, j, size):
    for i1, j1 in [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]:
        if 0 <= i1 < size[0] and 0 <= j1 < size[1]:
            yield (i1, j1)


def fill_matrix(matrix, start=None, mode="outer", empty=".", filled="O"):
    if start:
        next_iter = start
    else:
        next_iter = []
        if mode == "outer":
            for i in range(len(matrix)):
                next_iter.append((i, -1))
                next_iter.append((i, len(matrix[0])))
            for j in range(len(matrix[0])):
                next_iter.append((-1, j))
                next_iter.append((len(matrix), j))

    while len(next_iter) > 0:
        i, j = next_iter.pop()
        for i1, j1 in get_adj(i, j, (len(matrix), len(matrix[0]))):
            if matrix[i1][j1] == empty:
                next_iter.append((i1, j1))
                matrix[i1][j1] = filled

    return matrix


def solve1(directoins, dist, **kwargs):
    # just a straightforward solution with no tricks
    corners = get_corners(directoins, dist)
    i_blocks, i_to_block = get_blocks(corners, index=0)
    j_blocks, j_to_block = get_blocks(corners, index=1)
    matrix = get_matrix(corners, i_blocks, i_to_block, j_blocks, j_to_block)
    matrix = fill_matrix(matrix, start=None, mode="outer", empty=".", filled="O")

    n = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] in "#.":
                n += i_blocks[i][1] * j_blocks[j][1]
    return n


def solve2(colors_directoins, colors_dist, **kwargs):
    return solve1(colors_directoins, colors_dist)
