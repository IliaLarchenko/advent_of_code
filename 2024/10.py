def prepare_data(file="input.txt"):
    with open(file) as f:
        lines = f.readlines()
    matrix = [[int(i) for i in x.strip()] for x in lines]
    return {"matrix": matrix}


def get_adj(i, j, matrix):
    for i1, j1 in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
        if 0 <= i1 < len(matrix) and 0 <= j1 < len(matrix[0]):
            yield (i1, j1)


def count_trails(matrix, count_duplicates):
    ans = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == 0:
                last_reached = {(i, j): 1}
                for n in range(1, 10):
                    reached = {}
                    for (i1, j1), count in last_reached.items():
                        for i2, j2 in get_adj(i1, j1, matrix):
                            if matrix[i2][j2] == n:
                                reached[(i2, j2)] = reached.get((i2, j2), 0) + count
                    last_reached = reached

                if count_duplicates:
                    ans += sum(reached.values())
                else:
                    ans += len(reached)
    return ans


def solve1(matrix, **kwargs):
    return count_trails(matrix, False)


def solve2(matrix, **kwargs):
    return count_trails(matrix, True)
