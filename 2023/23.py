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
    adj_dict = {}
    for i in range(len(lines)):
        for j in range(len(lines[0])):
            if lines[i][j] != "#":
                adj_dict[(i, j)] = {x: 1 for x in get_adj2(i, j, lines)}

    # simplify the graph
    for k, v in list(adj_dict.items()):
        if len(v) == 2:
            items = list(v.items())
            prev = items[0]
            nxt = items[1]

            adj_dict[prev[0]][nxt[0]] = nxt[1] + adj_dict[prev[0]][k]
            adj_dict[nxt[0]][prev[0]] = prev[1] + adj_dict[nxt[0]][k]

            adj_dict[prev[0]].pop(k)
            adj_dict[nxt[0]].pop(k)
            adj_dict.pop(k)

    max_len = 0
    routes = [(set([S]), S, 0)]

    while len(routes) > 0:
        visited, current, total_len = routes.pop()

        if current == F:
            max_len = max(max_len, total_len)

        for (i, j), weight in adj_dict[(current[0], current[1])].items():
            if (i, j) not in visited:
                new_visited = visited.copy()
                new_visited.add((i, j))
                routes.append((new_visited, (i, j), total_len + weight))

    return max_len
