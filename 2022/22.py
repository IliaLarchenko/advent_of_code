def prepare_data(file="input.txt"):
    with open(file) as f:
        lines = f.readlines()

    map0 = [line[:-1] for line in lines[:-2]]
    rotations = ">v<^"
    movements = lines[-1].strip()

    move = []
    n = 0
    for x in movements:
        if x in ["R", "L"]:
            move.append(n)
            move.append(x)
            n = 0
        else:
            n = n * 10 + int(x)
    if x not in ["R", "L"]:
        move.append(n)

    data = {"map0": map0, "rotations": rotations, "move": move}

    return data


class Node:
    def __init__(self, t):
        self.t = t
        self.left = None
        self.right = None
        self.up = None
        self.down = None


def generate_grid(map0):
    max_width = max([len(line) for line in map0])
    grid = [[None] * max_width for _ in range(len(map0))]
    start = None
    nodes_dict = {}
    for row in range(len(map0)):
        for column in range(len(map0[row])):
            if map0[row][column] != " ":
                grid[row][column] = Node(map0[row][column])
                nodes_dict[grid[row][column]] = (row, column)
                if start is None and grid[row][column] != " ":
                    start = grid[row][column]
    return grid, nodes_dict, start


def connect_plain(grid):
    for row in range(len(grid)):
        last = None
        for column in range(len(grid[row])):
            if grid[row][column] is None:
                continue
            last = grid[row][column]

        for column in range(len(grid[row])):
            if grid[row][column] is None:
                continue
            grid[row][column].left = last
            last.right = grid[row][column]
            last = grid[row][column]

    for column in range(len(grid[0])):
        last = None
        for row in range(len(grid)):
            if grid[row][column] is None:
                continue
            last = grid[row][column]

        for row in range(len(grid)):
            if grid[row][column] is None:
                continue
            grid[row][column].up = last
            last.down = grid[row][column]
            last = grid[row][column]

    return grid


def connect_cube(grid):
    # hardcoded for the task input
    # can be done automatically but it is more complex
    for i in range(50):
        grid[i][149].right = grid[149 - i][99]
        grid[149 - i][99].right = grid[i][149]

        grid[i][50].left = grid[149 - i][0]
        grid[149 - i][0].left = grid[i][50]

        grid[0][50 + i].up = grid[150 + i][0]
        grid[150 + i][0].left = grid[0][50 + i]

        grid[0][100 + i].up = grid[199][i]
        grid[199][i].down = grid[0][100 + i]

        grid[49][100 + i].down = grid[50 + i][99]
        grid[50 + i][99].right = grid[49][100 + i]

        grid[50 + i][50].left = grid[100][i]
        grid[100][i].up = grid[50 + i][50]

        grid[149][50 + i].down = grid[150 + i][49]
        grid[150 + i][49].right = grid[149][50 + i]
    return grid


def solve(start, nodes_dict, move):
    direction = 0
    position = start

    for x in move:
        if x == "R":
            direction = (direction + 1) % 4
        elif x == "L":
            direction = (direction - 1) % 4
        else:
            for _ in range(x):
                if direction == 0:
                    next_pos = position.right
                elif direction == 2:
                    next_pos = position.left
                elif direction == 3:
                    next_pos = position.up
                elif direction == 1:
                    next_pos = position.down

                if next_pos.t == "#":
                    break
                else:
                    if next_pos.right == position:
                        direction = 2
                    elif next_pos.left == position:
                        direction = 0
                    elif next_pos.up == position:
                        direction = 1
                    elif next_pos.down == position:
                        direction = 3
                    position = next_pos

    return (
        (nodes_dict[position][0] + 1) * 1000
        + (nodes_dict[position][1] + 1) * 4
        + direction
    )


def solve1(map0, move, **kwargs):
    grid, nodes_dict, start = generate_grid(map0)
    grid = connect_plain(grid)
    return solve(start, nodes_dict, move)


def solve2(map0, move, **kwargs):
    grid, nodes_dict, start = generate_grid(map0)
    grid = connect_plain(grid)
    grid = connect_cube(grid)
    return solve(start, nodes_dict, move)
