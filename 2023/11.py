def prepare_data(file="input.txt"):
    with open(file) as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines]

    return {"lines": lines}


def get_expansion(lines):
    rows_to_expand = {
        i for i in range(len(lines)) if len(set(lines[i])) == 1 and lines[i][0] == "."
    }
    columns_to_expand = {
        j
        for j in range(len(lines[0]))
        if len(set([lines[i][j] for i in range(len(lines))])) == 1
        and lines[0][j] == "."
    }

    return rows_to_expand, columns_to_expand


def get_galaxies(lines):
    galaxies = []
    for i in range(len(lines)):
        for j in range(len(lines[0])):
            if lines[i][j] == "#":
                galaxies.append((i, j))

    return galaxies


def get_distances(lines, exp_coeff):
    rows_to_expand, columns_to_expand = get_expansion(lines)
    galaxies = get_galaxies(lines)

    rows_counter = [0] * len(lines)
    columns_counter = [0] * len(lines[0])

    for k, g1 in enumerate(galaxies):
        for l, g2 in enumerate(galaxies[k + 1 :]):
            rows_counter[min(g1[0], g2[0])] += 1
            rows_counter[max(g1[0], g2[0])] -= 1
            columns_counter[min(g1[1], g2[1])] += 1
            columns_counter[max(g1[1], g2[1])] -= 1

    ans = 0
    m = 0
    for i, n in enumerate(rows_counter):
        ans += m * (1 + int(i in rows_to_expand) * (exp_coeff - 1))
        m += n
    m = 0
    for i, n in enumerate(columns_counter):
        ans += m * (1 + int(i in columns_to_expand) * (exp_coeff - 1))
        m += n
    return ans


def solve1(lines, **kwargs):
    return get_distances(lines, 2)


def solve2(lines, **kwargs):
    return get_distances(lines, 1000000)
