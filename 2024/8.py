def prepare_data(file="input.txt"):
    with open(file) as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines]
    size = (len(lines), len(lines[0]))

    symbols = {}
    for i in range(len(lines)):
        for j in range(len(lines[0])):
            if lines[i][j] != ".":
                symbols[lines[i][j]] = symbols.get(lines[i][j], [])
                symbols[lines[i][j]].append((i, j))

    return {"size": size, "symbols": symbols}


def solve1(size, symbols, **kwargs):
    anti = set()
    for c in symbols:
        for k in range(len(symbols[c])):
            for n in range(len(symbols[c])):
                if k == n:
                    continue
                i1, j1 = symbols[c][k]
                i2, j2 = symbols[c][n]

                if 0 <= i1 + (i1 - i2) < size[0] and 0 <= j1 + (j1 - j2) < size[1]:
                    anti.add((i1 + (i1 - i2), j1 + (j1 - j2)))

    return len(anti)


def solve2(size, symbols, **kwargs):
    anti = set()
    for c in symbols:
        for k in range(len(symbols[c])):
            for n in range(len(symbols[c])):
                if k == n:
                    continue
                i1, j1 = symbols[c][k]
                i2, j2 = symbols[c][n]

                m = 0
                while 0 <= i1 + m * (i1 - i2) < size[0] and 0 <= j1 + m * (j1 - j2) < size[1]:
                    anti.add((i1 + m * (i1 - i2), j1 + m * (j1 - j2)))
                    m += 1

    return len(anti)
