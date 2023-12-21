def prepare_data(file="input.txt"):
    with open(file) as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines]
    return {"lines": lines}


directions = {
    "R": (0, +1),
    "L": (0, -1),
    "D": (1, 0),
    "U": (-1, 0),
}

reflections = {
    "\\": {
        "R": "D",
        "L": "U",
        "D": "R",
        "U": "L",
    },
    "/": {
        "R": "U",
        "L": "D",
        "D": "L",
        "U": "R",
    },
}


def count_energized(lines, beams):
    energized = {}
    while len(beams) > 0:
        i, j, d = beams.pop()
        if not (0 <= i < len(lines)) or not (0 <= j < len(lines[0])):
            continue
        if (i, j) not in energized:
            energized[(i, j)] = set()
        if d in energized[(i, j)]:
            continue
        else:
            energized[(i, j)].add(d)
            if (
                lines[i][j] == "."
                or (d in "RL" and lines[i][j] == "-")
                or (d in "UD" and lines[i][j] == "|")
            ):
                beams.append((i + directions[d][0], j + directions[d][1], d))
            elif lines[i][j] == "|":
                beams.append((i + 1, j, "D"))
                beams.append((i - 1, j, "U"))
            elif lines[i][j] == "-":
                beams.append((i, j + 1, "R"))
                beams.append((i, j - 1, "L"))
            else:
                new_d = reflections[lines[i][j]][d]
                beams.append(
                    (i + directions[new_d][0], j + directions[new_d][1], new_d)
                )
    return len(energized)


def solve1(lines, **kwargs):
    return count_energized(lines, beams=[(0, 0, "R")])


def solve2(lines, **kwargs):
    max_e = 0

    for i in range(len(lines)):
        max_e = max(count_energized(lines, [(i, 0, "R")]), max_e)
        max_e = max(count_energized(lines, [(i, len(lines[0]) - 1, "L")]), max_e)

    for j in range(len(lines[0])):
        max_e = max(count_energized(lines, [(0, j, "D")]), max_e)
        max_e = max(count_energized(lines, [(len(lines) - 1, j, "U")]), max_e)

    return max_e
