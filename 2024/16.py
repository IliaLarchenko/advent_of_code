def prepare_data(file="input.txt"):
    with open(file) as f:
        lines = f.readlines()
    matrix = [list(x.strip()) for x in lines]

    return {"matrix": matrix}


def find_c(matrix, c):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == c:
                return i, j
    return None, None


def solve_maze(matrix):
    start = find_c(matrix, "S")
    end = find_c(matrix, "E")

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    direction = 0

    reached = {
        0: set([(start, direction)])  # s:set(positions), all positions achieved with score s
    }

    best_previous = {
        (start, direction): (0, []),  # (position,direction):(score, list(previous(position,direction)))
    }

    reached_end = False
    s = 0

    while not reached_end:
        if s not in reached:
            s += 1
            continue
        frontier = reached.pop(s)
        for (i, j), d in frontier:
            if matrix[i][j] == "E":
                reached_end = True
            for ni, nj, nd, ns in [
                (i + directions[d][0], j + directions[d][1], d, s + 1),
                (i, j, (d + 1) % 4, s + 1000),
                (i, j, (d - 1) % 4, s + 1000),
            ]:
                if matrix[ni][nj] == "#":
                    continue

                if ((ni, nj), nd) in best_previous:
                    if ns > best_previous[((ni, nj), nd)][0]:
                        continue
                    elif ns == best_previous[((ni, nj), nd)][0]:
                        best_previous[((ni, nj), nd)][1].add(((i, j), d))
                        continue

                best_previous[((ni, nj), nd)] = (ns, set([((i, j), d)]))
                reached[ns] = reached.get(ns, set())
                reached[ns].add(((ni, nj), nd))
        s += 1

    good_seats = set()
    to_check = set()

    to_check = {(end, d) for (pos, d) in frontier if pos == end}

    while len(to_check) > 0:
        (i, j), d = to_check.pop()
        good_seats.add((i, j))
        if ((i, j), d) in best_previous:
            for x in best_previous[((i, j), d)][1]:
                to_check.add(x)
    return s - 1, len(good_seats)
