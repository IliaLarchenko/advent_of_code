def prepare_data(file="input.txt"):
    with open(file) as f:
        lines = f.readlines()
    lines = [list(x.strip()) for x in lines]

    for i in range(len(lines)):
        for j in range(len(lines[0])):
            if lines[i][j] in "^v<>":
                i0, j0 = i, j
                break

    return {"lines": lines, "i0": i0, "j0": j0}


dir_dict = {
    # (y direction, x direction, next rotation)
    "^": (-1, 0, ">"),
    "v": (1, 0, "<"),
    ">": (0, 1, "v"),
    "<": (0, -1, "^"),
}


def explore(lines, i0, j0, dir_dict):
    # returns visited coordinates, and flag if the map is left
    i, j = i0, j0
    direction = lines[i0][j0]
    visited = set()
    visited.add((i, j))
    hit_guard = set()

    while True:
        d = dir_dict[direction]
        i += d[0]
        j += d[1]
        while 0 <= i < len(lines) and 0 <= j < len(lines[0]) and lines[i][j] != "#":
            visited.add((i, j))
            i += d[0]
            j += d[1]
        if not (0 <= i < len(lines) and 0 <= j < len(lines[0])):
            return visited, True
        if lines[i][j] == "#":
            hit = (i, j, i - d[0], j - d[1])
            if hit in hit_guard:
                return visited, False
            hit_guard.add(hit)
            i -= d[0]
            j -= d[1]
            direction = d[2]


def solve1(lines, i0, j0, **kwargs):
    visited, _ = explore(lines, i0, j0, dir_dict)
    return len(visited)


def solve2(lines, i0, j0, **kwargs):
    # Not optimal but fast enough
    # Takes ~5 seconds
    ans = 0
    v, b = explore(lines, i0, j0, dir_dict)

    for i, j in v:
        if (i, j) == (i0, j0):
            continue
        lines[i][j] = "#"
        _, b = explore(lines, i0, j0, dir_dict)
        ans += not b
        lines[i][j] = "."
    return ans
