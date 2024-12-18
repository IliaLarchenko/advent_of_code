def prepare_data(file="input.txt"):
    with open(file) as f:
        lines = f.readlines()

    space = {}
    for i, line in enumerate(lines):
        x, y = [int(x) for x in line.strip().split(",")]
        space[(x, y)] = i + 1

    return {"space": space}


def check_position(x, y, n, space, size):
    if x < 0 or y < 0 or x >= size[0] or y >= size[1]:
        return False
    if (x, y) in space:
        return n < space[(x, y)]
    else:
        return True


def find_shortest_path(space, n_bytes, size):
    start = (0, 0)
    end = (
        size[0] - 1,
        size[1] - 1,
    )
    directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]

    visited = set([start])
    front = [start]

    steps = 0
    while len(front) > 0:
        steps += 1
        next_front = []
        for x, y in front:
            for dx, dy in directions:
                if check_position(x + dx, y + dy, n_bytes, space, size) and (x + dx, y + dy) not in visited:
                    visited.add((x + dx, y + dy))
                    next_front.append((x + dx, y + dy))
                    if (x + dx, y + dy) == end:
                        return steps

        front = next_front
    return None


def solve1(space, bytes=1024, size=(71, 71), **kwargs):
    return find_shortest_path(space, bytes, size)


def solve2(space, size=(71, 71), **kwargs):
    search_range = [0, 1_000_000]

    while True:
        n = sum(search_range) // 2
        result = find_shortest_path(space, n, size)
        if result is None:
            search_range[1] = n
        else:
            search_range[0] = n + 1
        if search_range[0] == search_range[1]:
            n = search_range[0]
            break

    return ",".join([str(x) for x in list(space.keys())[list(space.values()).index(n)]])
