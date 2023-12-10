def prepare_data(file="input.txt"):
    with open(file) as f:
        lines = f.readlines()
    lines = [list(x.strip()) for x in lines]

    return {"lines": lines}


class Node:
    # it was probably too much to do it like this
    # and I should have worked with the original data structure
    # but this is how I actually solved it
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.left = None
        self.right = None
        self.top = None
        self.bottom = None


def create_graph(lines):
    nodes_dict = {}

    for i in range(len(lines)):
        for j in range(len(lines[0])):
            if lines[i][j] == "S":
                S = (i, j)
            node = Node(i, j)
            nodes_dict[(i, j)] = node

    for i in range(len(lines)):
        for j in range(len(lines[0])):
            if lines[i][j] in "S|-LJ7F":
                node = nodes_dict[(i, j)]
            if lines[i][j] == "|":
                node.top = nodes_dict.get((i - 1, j), None)
                node.bottom = nodes_dict.get((i + 1, j), None)
            elif lines[i][j] == "-":
                node.left = nodes_dict.get((i, j - 1), None)
                node.right = nodes_dict.get((i, j + 1), None)
            elif lines[i][j] == "L":
                node.top = nodes_dict.get((i - 1, j), None)
                node.right = nodes_dict.get((i, j + 1), None)
            elif lines[i][j] == "J":
                node.top = nodes_dict.get((i - 1, j), None)
                node.left = nodes_dict.get((i, j - 1), None)
            elif lines[i][j] == "7":
                node.bottom = nodes_dict.get((i + 1, j), None)
                node.left = nodes_dict.get((i, j - 1), None)
            elif lines[i][j] == "F":
                node.bottom = nodes_dict.get((i + 1, j), None)
                node.right = nodes_dict.get((i, j + 1), None)

            if abs(i - S[0]) + abs(j - S[1]) == 1:
                if node.right is nodes_dict[S]:
                    nodes_dict[S].left = node
                elif node.left is nodes_dict[S]:
                    nodes_dict[S].right = node
                elif node.top is nodes_dict[S]:
                    nodes_dict[S].bottom = node
                elif node.bottom is nodes_dict[S]:
                    nodes_dict[S].top = node

    return nodes_dict, S


def get_distances(nodes_dict, S):
    dist = {}

    next_items = [(-1, nodes_dict[S])]

    while len(next_items) > 0:
        n, node = next_items.pop(0)
        dist[node] = min(dist.get(node, float("inf")), n + 1)
        if node.right is not None and (
            node.right not in dist or dist[node.right] > n + 1
        ):
            next_items.append((n + 1, node.right))
        if node.left is not None and (node.left not in dist or dist[node.left] > n + 1):
            next_items.append((n + 1, node.left))
        if node.top is not None and (node.top not in dist or dist[node.top] > n + 1):
            next_items.append((n + 1, node.top))
        if node.bottom is not None and (
            node.bottom not in dist or dist[node.bottom] > n + 1
        ):
            next_items.append((n + 1, node.bottom))
    return dist


def solve1(lines, **kwargs):
    nodes_dict, S = create_graph(lines)
    dist = get_distances(nodes_dict, S)
    return max(dist.values())


def solve2(lines, **kwargs):
    nodes_dict, S = create_graph(lines)
    dist = get_distances(nodes_dict, S)

    # create a map with gaps
    map_with_gaps = [
        ["I"] * (len(lines[0]) * 2 - 1) for _ in range((len(lines) * 2 - 1))
    ]

    # mark the loop nodes
    for node in dist.keys():
        map_with_gaps[node.i * 2][node.j * 2] = "L"
        if node.right in dist:
            map_with_gaps[node.i * 2][node.j * 2 + 1] = "L"
        if node.left in dist:
            map_with_gaps[node.i * 2][node.j * 2 - 1] = "L"
        if node.top in dist:
            map_with_gaps[node.i * 2 - 1][node.j * 2] = "L"
        if node.bottom in dist:
            map_with_gaps[node.i * 2 + 1][node.j * 2] = "L"

    # mark the walls
    next_iter = []
    for i in range(len(map_with_gaps)):
        for j in range(len(map_with_gaps[0])):
            if (
                i == 0
                or j == 0
                or i == len(map_with_gaps) - 1
                or j == len(map_with_gaps[0]) - 1
            ):
                if map_with_gaps[i][j] != "L":
                    map_with_gaps[i][j] = "O"
                    next_iter.append((i, j))

    # get the inner nodes
    while len(next_iter) > 0:
        i, j = next_iter.pop()
        map_with_gaps[i][j] = "O"
        for i1, j1 in [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]:
            if (
                0 <= i1 < len(map_with_gaps)
                and 0 <= j1 < len(map_with_gaps[0])
                and map_with_gaps[i1][j1] == "I"
            ):
                next_iter.append((i1, j1))

    # count the inner nodes in the original map
    ans = 0
    for i in range(len(map_with_gaps)):
        for j in range(len(map_with_gaps[0])):
            if map_with_gaps[i][j] == "I" and i % 2 == 0 and j % 2 == 0:
                ans += 1

    return ans


# No graph solution
def fix_s_tile(lines):
    # No checks for edge cases
    # In practice you could just do it mannualy in the input file for speed
    for i in range(len(lines)):
        for j in range(len(lines[0])):
            if lines[i][j] == "S":
                S = (i, j)
                break

    i, j = S
    connections = [False, False, False, False]  # left, right, top, bottom
    if lines[i + 1][j] in "|LJ":
        connections[3] = True
    if lines[i - 1][j] in "|F7":
        connections[2] = True
    if lines[i][j + 1] in "-J7":
        connections[1] = True
    if lines[i][j - 1] in "-LF":
        connections[0] = True

    if connections[0] and connections[1]:
        lines[i][j] = "-"
    elif connections[0] and connections[2]:
        lines[i][j] = "J"
    elif connections[0] and connections[3]:
        lines[i][j] = "7"
    elif connections[1] and connections[2]:
        lines[i][j] = "L"
    elif connections[1] and connections[3]:
        lines[i][j] = "F"
    elif connections[2] and connections[3]:
        lines[i][j] = "|"

    return S


def find_cycle(lines):
    # No checks for edge cases

    S = fix_s_tile(lines)

    cycle = set()
    to_visit = set()
    to_visit.add(S)

    while len(to_visit) > 0:
        i, j = to_visit.pop()
        cycle.add((i, j))

        if lines[i][j] == "|":
            to_add = [(i + 1, j), (i - 1, j)]
        elif lines[i][j] == "-":
            to_add = [(i, j + 1), (i, j - 1)]
        elif lines[i][j] == "L":
            to_add = [(i - 1, j), (i, j + 1)]
        elif lines[i][j] == "J":
            to_add = [(i - 1, j), (i, j - 1)]
        elif lines[i][j] == "F":
            to_add = [(i + 1, j), (i, j + 1)]
        elif lines[i][j] == "7":
            to_add = [(i + 1, j), (i, j - 1)]

        for i, j in to_add:
            if (i, j) not in cycle and (i, j) not in to_visit:
                to_visit.add((i, j))

    # fix the input back
    lines[S[0]][S[1]] = "S"

    return S, cycle


def solve1_no_graph(lines, **kwargs):
    _, cycle = find_cycle(lines)
    return len(cycle) // 2


def solve2_no_graph(lines, **kwargs):
    S, cycle = find_cycle(lines)

    # create a map with gaps
    map_with_gaps = [
        ["I"] * (len(lines[0]) * 2 - 1) for _ in range((len(lines) * 2 - 1))
    ]

    # mark the cycle 
    # everyhting esle is the same as before
    for i, j in cycle:
        map_with_gaps[i * 2][j * 2] = "L"
        if lines[i][j] == "|":
            map_with_gaps[i * 2 + 1][j * 2] = "L"
            map_with_gaps[i * 2 - 1][j * 2] = "L"
        elif lines[i][j] == "-":
            map_with_gaps[i * 2][j * 2 + 1] = "L"
            map_with_gaps[i * 2][j * 2 - 1] = "L"
        elif lines[i][j] == "L":
            map_with_gaps[i * 2][j * 2 + 1] = "L"
            map_with_gaps[i * 2 - 1][j * 2] = "L"
        elif lines[i][j] == "J":
            map_with_gaps[i * 2][j * 2 - 1] = "L"
            map_with_gaps[i * 2 - 1][j * 2] = "L"
        elif lines[i][j] == "7":
            map_with_gaps[i * 2][j * 2 - 1] = "L"
            map_with_gaps[i * 2 + 1][j * 2] = "L"
        elif lines[i][j] == "F":
            map_with_gaps[i * 2][j * 2 + 1] = "L"
            map_with_gaps[i * 2 + 1][j * 2] = "L"

    # mark the walls
    next_iter = []
    for i in range(len(map_with_gaps)):
        for j in range(len(map_with_gaps[0])):
            if (
                i == 0
                or j == 0
                or i == len(map_with_gaps) - 1
                or j == len(map_with_gaps[0]) - 1
            ):
                if map_with_gaps[i][j] != "L":
                    map_with_gaps[i][j] = "O"
                    next_iter.append((i, j))

    # get the inner nodes
    while len(next_iter) > 0:
        i, j = next_iter.pop()
        map_with_gaps[i][j] = "O"
        for i1, j1 in [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]:
            if (
                0 <= i1 < len(map_with_gaps)
                and 0 <= j1 < len(map_with_gaps[0])
                and map_with_gaps[i1][j1] == "I"
            ):
                next_iter.append((i1, j1))

    # count the inner nodes in the original map
    ans = 0
    for i in range(len(map_with_gaps)):
        for j in range(len(map_with_gaps[0])):
            if map_with_gaps[i][j] == "I" and i % 2 == 0 and j % 2 == 0:
                ans += 1

    return ans
