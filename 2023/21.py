def prepare_data(file="input.txt"):
    with open(file) as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines]

    return {"lines": lines}


def get_matrix(lines):
    matrix = [list(x.strip()) for x in lines]
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == "S":
                S = (i, j)
                matrix[i][j] = "."
    return matrix, S


def get_adj(i, j, size):
    for i1, j1 in [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]:
        if 0 <= i1 < size[0] and 0 <= j1 < size[1]:
            yield (i1, j1)


def fill_matrix_step(matrix, next_iter):
    new_next_iter = set()
    for i, j in next_iter:
        for i1, j1 in get_adj(i, j, (len(matrix), len(matrix[0]))):
            if matrix[i1][j1] == ".":
                new_next_iter.add((i1, j1))
    return new_next_iter


def fill_matrix(matrix, next_iter, steps=64):
    for _ in range(steps):
        next_iter = fill_matrix_step(matrix, next_iter=next_iter)
    return next_iter


def solve1(lines, steps=64, **kwargs):
    matrix, S = get_matrix(lines)
    return len(fill_matrix(matrix, [S], steps=steps))


def fill_full(matrix, next_iter):
    even = len(next_iter)
    odd = 0
    prev = None
    for i in range(1, len(matrix[0]) * len(matrix[1])):
        next_iter = fill_matrix_step(matrix, next_iter=next_iter)
        if i % 2 == 1:
            odd = len(next_iter)
            if odd == prev:
                return i, odd, even
            prev = even

        else:
            even = len(next_iter)
            if even == prev:
                return i - 1, odd, even
            prev = odd
    return i, odd, even


def get_corners_dict(matrix, S):
    corners = [
        (0, 0),
        (0, len(matrix[1]) - 1),
        (len(matrix[0]) - 1, len(matrix[1]) - 1),
        (len(matrix[0]) - 1, 0),
    ]
    corners_dict = {}
    for corner in corners:
        i, odd, even = fill_full(matrix, [corner])
        corners_dict[corner] = {"steps": i, "odd": odd, "even": even}

    next_iter = [S]
    for i in range(300):
        next_iter = fill_matrix_step(matrix, next_iter=next_iter)
        for corner in corners:
            if corner in next_iter and "first_reach" not in corners_dict[corner]:
                corners_dict[corner]["first_reach"] = i + 1
    return corners_dict


def get_result(matrix, N, steps_to_corners, size, odd_full, even_full):
    # number of full blocks covered to the farthest corner
    n = (N - steps_to_corners) // size + 1

    # steps with full coverage
    k = steps_to_corners + (n - 1) * size

    steps_left = N - k

    even_blocks = n**2
    odd_blocks = (n - 1) ** 2

    diagonal_steps_left = steps_left + (size - 2)

    val = 0

    val += len(fill_matrix(matrix, [(0, 0)], steps=diagonal_steps_left)) * (n - 1)
    val += len(fill_matrix(matrix, [(0, len(matrix[0]) - 1)], steps=diagonal_steps_left)) * (n - 1)
    val += len(fill_matrix( matrix, [(len(matrix) - 1, len(matrix[0]) - 1)], steps=diagonal_steps_left)) * (n - 1)
    val += len(fill_matrix(matrix, [(len(matrix) - 1, 0)], steps=diagonal_steps_left)) * (n - 1)

    l = (size - 1) // 2
    val += len(fill_matrix(matrix, [(0, l)], steps=steps_left + l - 1))
    val += len(fill_matrix(matrix, [(l, 0)], steps=steps_left + l - 1))
    val += len(fill_matrix(matrix, [(l, len(matrix[0]) - 1)], steps=steps_left + l - 1))
    val += len(fill_matrix(matrix, [(len(matrix) - 1, l)], steps=steps_left + l - 1))

    if steps_left >= 2:
        val += len(fill_matrix(matrix, [(0, 0)], steps=steps_left - 2)) * n
        val += (len(fill_matrix(matrix, [(0, len(matrix[0]) - 1)], steps=steps_left - 2)) * n)
        val += (len(fill_matrix(matrix, [(len(matrix) - 1, len(matrix[0]) - 1)], steps=steps_left - 2)) * n)
        val += (len(fill_matrix(matrix, [(len(matrix) - 1, 0)], steps=steps_left - 2)) * n)

    if steps_left % 2 == 0:
        return odd_blocks * odd_full + even_blocks * even_full + val
    else:
        return odd_blocks * even_full + even_blocks * odd_full + val


def solve2(lines, **kwargs):
    # This solution is specifc to the input
    # But I tried to make it more generic and with small changes it can
    # be used for other inputs (with limitaion)
    # It can be simplified more for the given input

    matrix, S = get_matrix(lines)
    N = 26501365

    corners_dict = get_corners_dict(matrix, S)
    odd_full = corners_dict[(0, 0)]["odd"]
    even_full = corners_dict[(0, 0)]["even"]
    steps_to_corners = corners_dict[(0, 0)]["first_reach"]

    size = len(matrix)

    return get_result(
        matrix, N, steps_to_corners, size, odd_full, even_full, debug=True
    )
