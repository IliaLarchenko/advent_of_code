def prepare_data(file="input.txt"):
    with open(file) as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines]
    for j in range(len(lines[0])):
        if lines[0][j] == ".":
            S = (0, j)
        if lines[-1][j] == ".":
            F = (len(lines) - 1, j)

    return {"lines": lines, "S": S, "F": F}


def get_adj(i, j, size):
    adj = []
    for i1, j1 in [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]:
        if 0 <= i1 < size[0] and 0 <= j1 < size[1]:
            adj.append((i1, j1))
    return adj


def solve1(lines, S, F, **kwargs):
    max_len = 0
    routes = [(set([S]), S)]

    while len(routes) > 0:
        visited, current = routes.pop()
        options = []

        if current == F:
            max_len = max(max_len, len(visited))
        if lines[current[0]][current[1]] == ".":
            next_steps = get_adj(current[0], current[1], (len(lines), len(lines[0])))
        elif lines[current[0]][current[1]] == ">":
            next_steps = [(current[0], current[1] + 1)]
        elif lines[current[0]][current[1]] == "<":
            next_steps = [(current[0], current[1] - 1)]
        elif lines[current[0]][current[1]] == "^":
            next_steps = [(current[0] - 1, current[1])]
        elif lines[current[0]][current[1]] == "v":
            next_steps = [(current[0] + 1, current[1])]

        for i, j in next_steps:
            if (i, j) not in visited and lines[i][j] != "#":
                new_visited = visited.copy()
                new_visited.add((i, j))
                routes.append((new_visited, (i, j)))

    return max_len - 1


def get_adj2(i, j, lines):
    size = (len(lines), len(lines[0]))
    adj = []
    for i1, j1 in [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]:
        if 0 <= i1 < size[0] and 0 <= j1 < size[1] and lines[i1][j1] != "#":
            adj.append((i1, j1))
    return adj


def solve2(lines, S, F, **kwargs):
    # it is not an efficient solution, just a bruteforce, but it works in reasonable time
    adj_dict = {}
    for i in range(len(lines)):
        for j in range(len(lines[0])):
            if lines[i][j] != "#":
                adj_dict[(i, j)] = get_adj2(i, j, lines)

    max_len = 0
    routes = [(set([S, (S[0] + 1, S[1])]), (S[0] + 1, S[1]))]

    while len(routes) > 0:
        # this one lets you get the correct answer before it goes through all options
        # need to import random
        # if random.random() < 0.0001:
        #     print(len(routes),max_len)
        visited, current = routes.pop()
        next_steps = adj_dict[current[0], current[1]]

        while len(next_steps) == 2:
            if next_steps[0] in visited:
                i, j = next_steps[1]
            else:
                i, j = next_steps[0]
            next_steps = []
            if (i, j) == F:
                max_len = max(max_len, len(visited))
            elif (i, j) not in visited:
                visited.add((i, j))
                current = (i, j)
                next_steps = adj_dict[i, j]

        if len(next_steps) == 1:
            continue

        if len(next_steps) > 2:
            for i, j in next_steps:
                if (i, j) == F:
                    max_len = max(max_len, len(visited))
                if (i, j) not in visited:
                    dub_visited = visited.copy()
                    dub_visited.add((i, j))
                    routes.append((dub_visited, (i, j)))

    return max_len
