def prepare_data(file="input.txt"):
    with open(file) as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines]

    matrix = []
    for i in range(len(lines)):
        if lines[i] == "":
            break
        matrix.append(list(lines[i]))

    moves = "".join(lines[i + 1 :])

    return {"matrix": matrix, "moves": moves}


def expand_matrix(matrix):
    new_matrix = []
    replace_dict = {
        "@": "@.",
        ".": "..",
        "#": "##",
        "O": "[]",
    }

    for i in range(len(matrix)):
        new_matrix.append([])
        for j in range(len(matrix[0])):
            new_matrix[i] += list(replace_dict[matrix[i][j]])

    return new_matrix


def find_start(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == "@":
                return i, j
    return None, None


moves_dict = {
    "^": (-1, 0),
    "v": (1, 0),
    ">": (0, 1),
    "<": (0, -1),
}


def move_boxes(matrix, moves):
    matrix = [line.copy() for line in matrix]
    position = find_start(matrix)

    for move in moves:
        di, dj = moves_dict[move]
        movable = [[position]]
        replacement = {position: "."}
        while len(movable) > 0:
            new_level = []
            for i, j in movable[-1]:
                if matrix[i + di][j + dj] == "#":
                    movable = []
                    break
                elif matrix[i + di][j + dj] == "[":
                    new_level.append((i + di, j + dj))
                    new_level.append((i + di, j + dj + 1))
                elif matrix[i + di][j + dj] == "]":
                    new_level.append((i + di, j + dj))
                    new_level.append((i + di, j + dj - 1))
                elif matrix[i + di][j + dj] == "O":
                    new_level.append((i + di, j + dj))

            if len(movable) > 0 and len(new_level) > 0:
                movable.append([(i, j) for (i, j) in new_level if (i, j) not in movable[-1]])
                for i, j in movable[-1]:
                    if (i - di, j - dj) not in movable[-2] and (i - di, j - dj) not in new_level:
                        replacement[(i, j)] = "."

            if len(movable) == 0 or len(new_level) == 0 or len(movable[-1]) == 0:
                break

        if len(movable) > 0:
            for level in movable:
                for i, j in level:
                    replacement[(i + di, j + dj)] = matrix[i][j]
            for (i, j), v in replacement.items():
                matrix[i][j] = v
            position = (position[0] + di, position[1] + dj)
    return matrix


def count_coordinates(matrix):
    ans = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] in "[O":
                ans += 100 * i + j
    return ans


def solve1(matrix, moves, **kwargs):
    final_matrix = move_boxes(matrix, moves)
    return count_coordinates(final_matrix)


def solve2(matrix, moves, **kwargs):
    expanded_matrix = expand_matrix(matrix)
    final_matrix = move_boxes(expanded_matrix, moves)
    return count_coordinates(final_matrix)
