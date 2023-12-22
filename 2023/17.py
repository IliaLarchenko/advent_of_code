def prepare_data(file="input.txt"):
    with open(file) as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines]
    matrix = [[int(x) for x in line] for line in lines]
    matrix[0][0] = 0

    return {"matrix": matrix}


d_dict = {"R": (0, 1, "UD"), "L": (0, -1, "UD"), "U": (-1, 0, "LR"), "D": (1, 0, "LR")}


def solve1(matrix, **kwargs):
    memo = {}
    min_loss = float("+inf")

    memo[(0, 0, "R", 0)] = float("+inf")
    memo[(0, 0, "D", 0)] = float("+inf")

    next_steps = set()
    next_steps.add((0, 0, 0, "R", 0))
    next_steps.add((0, 0, 0, "D", 0))

    while len(next_steps) > 0:
        loss, i, j, d, steps = next_steps.pop()

        if i < 0 or i > len(matrix) - 1 or j < 0 or j > len(matrix[0]) - 1:
            continue

        loss = loss + matrix[i][j]

        if loss >= min_loss:
            continue

        if (i, j, d, steps) not in memo:
            memo[(i, j, d, steps)] = loss
        elif (
            memo[(i, j, d, steps)] <= loss
            or memo.get((i, j, d, steps - 1), float("+inf")) <= loss
            or memo.get((i, j, d, steps - 1), float("+inf")) <= loss
        ):
            continue
        elif loss < memo[(i, j, d, steps)]:
            memo[(i, j, d, steps)] = loss

        if i == len(matrix) - 1 and j == len(matrix[0]) - 1:
            min_loss = min(min_loss, loss)
            continue

        for new_d in d_dict[d][2]:
            next_steps.add((loss, i + d_dict[new_d][0], j + d_dict[new_d][1], new_d, 1))

        if steps < 3:
            next_steps.add((loss, i + d_dict[d][0], j + d_dict[d][1], d, steps + 1))

    return min_loss


def solve2(matrix, **kwargs):
    memo = {}
    min_loss = float("+inf")

    next_steps = set()
    next_steps.add((0, 0, 0, "R", 0))
    next_steps.add((0, 0, 0, "D", 0))

    while len(next_steps) > 0:
        loss, i, j, d, steps = next_steps.pop()

        if i < 0 or i > len(matrix) - 1 or j < 0 or j > len(matrix[0]) - 1:
            continue

        loss = loss + matrix[i][j]
        if loss >= min_loss:
            continue

        if (i, j, d, steps) not in memo:
            memo[(i, j, d, steps)] = loss
        elif memo[(i, j, d, steps)] <= loss:
            continue
        elif loss < memo[(i, j, d, steps)]:
            memo[(i, j, d, steps)] = loss

        if i == len(matrix) - 1 and j == len(matrix[0]) - 1 and 10 >= steps >= 4:
            min_loss = min(min_loss, loss)
            continue

        if steps < 10:
            next_steps.add((loss, i + d_dict[d][0], j + d_dict[d][1], d, steps + 1))

        if steps >= 4:
            for new_d in d_dict[d][2]:
                next_steps.add(
                    (loss, i + d_dict[new_d][0], j + d_dict[new_d][1], new_d, 1)
                )
    return min_loss
