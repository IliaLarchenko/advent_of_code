def prepare_data(file="input.txt"):
    with open(file) as file:
        lines = [line.strip() for line in file.readlines()]

    jet = lines[0]

    data = {"jet": jet}

    return data


def print_matrix(matrix):
    for i in range(len(matrix) - 1, -1, -1):
        print("".join(matrix[i]))


def clean_matrix(matrix):
    while len(matrix) > 0 and len(set(matrix[-1])) == 1:
        matrix.pop()
    return matrix


def add_object(matrix, shape):
    clean_matrix(matrix)

    for _ in range(3):
        matrix.append(["."] * 7)

    if shape == "-":
        matrix.append([".", ".", "@", "@", "@", "@", "."])
        lines = (len(matrix) - 1, len(matrix) - 1)

    elif shape == "+":
        matrix.append([".", ".", ".", "@", ".", ".", "."])
        matrix.append([".", ".", "@", "@", "@", ".", "."])
        matrix.append([".", ".", ".", "@", ".", ".", "."])
        lines = (len(matrix) - 3, len(matrix) - 1)

    elif shape == "|":
        matrix.append([".", ".", "@", ".", ".", ".", "."])
        matrix.append([".", ".", "@", ".", ".", ".", "."])
        matrix.append([".", ".", "@", ".", ".", ".", "."])
        matrix.append([".", ".", "@", ".", ".", ".", "."])
        lines = (len(matrix) - 4, len(matrix) - 1)

    elif shape == "0":
        matrix.append([".", ".", "@", "@", ".", ".", "."])
        matrix.append([".", ".", "@", "@", ".", ".", "."])
        lines = (len(matrix) - 2, len(matrix) - 1)

    elif shape == "L":
        matrix.append([".", ".", "@", "@", "@", ".", "."])
        matrix.append([".", ".", ".", ".", "@", ".", "."])
        matrix.append([".", ".", ".", ".", "@", ".", "."])

        lines = (len(matrix) - 3, len(matrix) - 1)

    return matrix, lines


def move_down(matrix, lines):
    can_move = True
    if lines[0] == 0:
        can_move = False

    for i in range(lines[0], lines[1] + 1):
        for j in range(7):
            if matrix[i][j] == "@" and matrix[i - 1][j] not in [".", "@"]:
                can_move = False
    if can_move:
        for i in range(lines[0], lines[1] + 1):
            for j in range(7):
                if matrix[i][j] == "@":
                    matrix[i - 1][j] = "@"
                    matrix[i][j] = "."

        return matrix, True, (lines[0] - 1, lines[1] - 1)

    else:
        for i in range(lines[1], lines[0] - 1, -1):
            for j in range(7):
                if matrix[i][j] == "@":
                    matrix[i][j] = "#"
        return matrix, False, None


def move_side(matrix, lines, side):
    can_move = True
    if side == "<":
        for i in range(lines[0], lines[1] + 1):
            for j in range(7):
                if matrix[i][j] == "@" and (
                    j == 0 or matrix[i][j - 1] not in [".", "@"]
                ):
                    can_move = False
                    break
        if can_move:
            for i in range(lines[1], lines[0] - 1, -1):
                for j in range(7):
                    if matrix[i][j] == "@":
                        matrix[i][j - 1] = "@"
                        matrix[i][j] = "."

    elif side == ">":
        for i in range(lines[0], lines[1] + 1):
            for j in range(7):
                if matrix[i][j] == "@" and (
                    j == 6 or matrix[i][j + 1] not in [".", "@"]
                ):
                    can_move = False
                    break
        if can_move:
            for i in range(lines[1], lines[0] - 1, -1):
                for j in range(6, -1, -1):
                    if matrix[i][j] == "@":
                        matrix[i][j + 1] = "@"
                        matrix[i][j] = "."

    return matrix, (lines[0], lines[1])


def get_height(num_shapes, jet):
    matrix = []
    shapes = "-+L|0"
    shape_i = 0
    jet_i = 0

    shapes_stopped = 0
    moved = False
    lines = [0, 0]

    while shapes_stopped < num_shapes:
        if moved:
            matrix, lines = move_side(matrix, lines, jet[jet_i])
            jet_i = (jet_i + 1) % len(jet)
            matrix, moved, lines = move_down(matrix, lines)
            if not moved:
                shapes_stopped += 1
        else:
            matrix, lines = add_object(matrix, shapes[shape_i])
            shape_i = (shape_i + 1) % len(shapes)
            moved = True

    clean_matrix(matrix)
    return len(matrix)


def solve1(jet, **kwargs):
    return get_height(2022, jet)


def find_cycle(max_shapes, jet):
    matrix = []
    shapes = "-+L|0"
    shape_i = 0
    jet_i = 0

    shapes_stopped = 0
    moved = False
    lines = [0, 0]

    statuses = set()
    first_point = None

    while shapes_stopped < max_shapes:
        if moved:
            matrix, lines = move_side(matrix, lines, jet[jet_i])
            jet_i = (jet_i + 1) % len(jet)
            matrix, moved, lines = move_down(matrix, lines)
            if not moved:
                shapes_stopped += 1
        else:
            if len(matrix) > 10:
                # if shape_i, jet_i ans the last 10 layers are the same
                # we call it a cycle
                status = (
                    shape_i,
                    jet_i,
                    "".join(["".join(matrix[-i]) for i in range(10)]),
                )
                if status in statuses:
                    clean_matrix(matrix)
                    if first_point is None:
                        first_point = {
                            "shapes_stopped": shapes_stopped,
                            "height": len(matrix),
                        }
                        statuses = set()
                    else:
                        second_point = {
                            "shapes_stopped": shapes_stopped,
                            "height": len(matrix),
                        }

                        cycle_shapes = (
                            second_point["shapes_stopped"]
                            - first_point["shapes_stopped"]
                        )
                        cycle_height = second_point["height"] - first_point["height"]

                        return cycle_shapes, cycle_height, first_point["shapes_stopped"]

                statuses.add(status)
            matrix, lines = add_object(matrix, shapes[shape_i])
            shape_i = (shape_i + 1) % len(shapes)
            moved = True

    return None, None, None


def solve2(jet, **kwargs):
    shapes_num = 1000000000000
    cycle_shapes, cycle_height, cycle_start = find_cycle(shapes_num, jet)

    before_cycle_shapes = (shapes_num - cycle_start) % cycle_shapes + cycle_start
    cycles = (shapes_num - cycle_start) // cycle_shapes

    return get_height(before_cycle_shapes, jet) + cycles * cycle_height
