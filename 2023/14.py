def prepare_data(file="input.txt"):
    with open(file) as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines]
    return {"lines": lines}


def solve1(lines, **kwargs):
    n = 0
    for j in range(len(lines[0])):
        w = len(lines)
        for i in range(len(lines)):
            if lines[i][j] == "O":
                n += w
                w -= 1
            elif lines[i][j] == "#":
                w = len(lines) - i - 1
    return n


def cycle(matrix):
    for _ in range(4):
        for j in range(len(matrix[0])):
            start_i = 0
            n = 0
            for i in range(len(matrix) + 1):
                if i == len(matrix) or matrix[i][j] == "#":
                    for i1 in range(start_i, start_i + n):
                        matrix[i1][j] = "O"
                    for i1 in range(start_i + n, i):
                        matrix[i1][j] = "."
                    start_i = i + 1
                    n = 0
                elif matrix[i][j] == "O":
                    n += 1

        matrix = [
            [matrix[-i - 1][j] for i in range(len(matrix))]
            for j in range(len(matrix[0]))
        ]
    return matrix


def encode(matrix):
    mirrors = []
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == "O":
                mirrors.append((i, j))
    return tuple(mirrors)


def solve2(lines, **kwargs):
    matrix = [list(x) for x in lines]

    i = 0
    results = {}
    while True:
        i += 1
        matrix = cycle(matrix)
        state = encode(matrix)
        if state not in results:
            results[state] = i
        else:
            last_i = results[state]
            cycle_lenght = i - last_i
            break
    for _ in range((1000000000 - i) % cycle_lenght):
        matrix = cycle(matrix)

    n = 0
    for j in range(len(matrix[0])):
        for i in range(len(matrix)):
            if matrix[i][j] == "O":
                n += len(matrix) - i

    return n
