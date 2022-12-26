from collections import deque


def prepare_data(file="input.txt"):
    # data preparation

    with open(file) as file:
        lines = [line.strip() for line in file.readlines()]

    rocks = set()
    for line in lines:
        edges = [e.split(",") for e in line.split(" -> ")]
        edges = [(int(e[0]), int(e[1])) for e in edges]

        for i in range(len(edges) - 1):
            if edges[i][0] == edges[i + 1][0]:
                for y in range(
                    min(edges[i][1], edges[i + 1][1]),
                    max(edges[i][1], edges[i + 1][1]) + 1,
                ):
                    rocks.add((edges[i][0], y))
            elif edges[i][1] == edges[i + 1][1]:
                for x in range(
                    min(edges[i][0], edges[i + 1][0]),
                    max(edges[i][0], edges[i + 1][0]) + 1,
                ):
                    rocks.add((x, edges[i][1]))

    abyss = max([x[1] for x in rocks])
    floor = abyss + 2

    data = {"abyss": abyss, "floor": floor, "rocks": rocks}
    return data


def solve1(rocks, abyss, **kwargs):
    # 1st question DFS
    visited = set()
    stack = [(500, 0)]
    while len(stack) > 0:
        x, y = stack[-1]
        if y == abyss:
            break
        else:
            stop = True
            for nx, ny in [(x + 1, y + 1), (x - 1, y + 1), (x, y + 1)]:
                if ((nx, ny) not in rocks) and ((nx, ny) not in visited):
                    stack.append((nx, ny))
                    stop = False
        if stop:
            visited.add((x, y))
            stack.pop()
    return len(visited)


def solve2(rocks, floor, **kwargs):
    # 2nd question BFS
    visited = set((500, 0))
    stack = deque([(500, 0)])
    while len(stack) > 0:
        x, y = stack.popleft()
        for nx, ny in [(x + 1, y + 1), (x - 1, y + 1), (x, y + 1)]:
            if ((nx, ny) not in rocks) and ((nx, ny) not in visited) and (ny < floor):
                stack.append((nx, ny))
                visited.add((nx, ny))
    return len(visited) - 1
