def prepare_data(file="input.txt"):
    with open(file) as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines]

    bricks = [
        (
            [int(x) for x in line.split("~")[0].split(",")],
            [int(x) for x in line.split("~")[1].split(",")],
        )
        for line in lines
    ]

    return {"bricks": bricks}


def get_brick_vecels(brick):
    vex = []
    x1, y1, z1 = brick[0]
    x2, y2, z2 = brick[1]
    vex.append((x1, y1, z1))
    if x1 != x2:
        for x in range(min(x1, x2), max(x1, x2) + 1):
            vex.append((x, y1, z1))
    if y1 != y2:
        for y in range(min(y1, y2), max(y1, y2) + 1):
            vex.append((x1, y, z1))
    if z1 != z2:
        for z in range(min(z1, z2), max(z1, z2) + 1):
            vex.append((x1, y1, z))
    return vex


def init_space(bricks):
    max_x, max_y, max_z = 0, 0, 0

    for brick in bricks:
        max_x = max(max_x, brick[0][0])
        max_x = max(max_x, brick[1][0])
        max_y = max(max_y, brick[0][1])
        max_y = max(max_y, brick[1][1])
        max_z = max(max_z, brick[0][2])
        max_z = max(max_z, brick[1][2])

    space = [
        [[-1 for _ in range(max_z + 1)] for __ in range(max_y + 1)]
        for ___ in range(max_z + 1)
    ]

    for i, brick in enumerate(bricks):
        for v in get_brick_vecels(brick):
            space[v[0]][v[1]][v[2]] = i

    return space


def move_all(space, bricks, skip=None):
    moved = True
    moved_bricks = set()
    while moved:
        moved = False
        for i, brick in enumerate(bricks):
            if i == skip:
                continue
            vex = get_brick_vecels(brick)
            can_move = True
            for x, y, z in vex:
                if z == 0:
                    can_move = False
                    break
                if space[x][y][z - 1] not in (i, -1):
                    can_move = False
                    break
            if can_move:
                for x, y, z in vex:
                    space[x][y][z] = -1
                for x, y, z in vex:
                    space[x][y][z - 1] = i
                bricks[i][0][2] -= 1
                bricks[i][1][2] -= 1
                moved = True
                moved_bricks.add(i)

    return len(moved_bricks)


def solve1(bricks, **kwargs):
    bricks = [(b[0].copy(), b[1].copy()) for b in bricks]
    space = init_space(bricks)
    move_all(space, bricks, skip=None)

    n = 0
    for i, brick in enumerate(bricks):
        vex = get_brick_vecels(brick)

        to_check = set()
        for x, y, z in vex:
            if space[x][y][z + 1] not in (i, -1):
                to_check.add(space[x][y][z + 1])

        supported = 0
        for check_i in to_check:
            check_b = bricks[check_i]
            check_vex = get_brick_vecels(check_b)
            for x, y, z in check_vex:
                if z == 0 or space[x][y][z - 1] not in (i, -1, check_i):
                    supported += 1
                    break

        if len(to_check) == supported:
            n += 1

    return n


def solve2(bricks, **kwargs):
    # bruteforce works just fine
    bricks = [(b[0].copy(), b[1].copy()) for b in bricks]
    space = init_space(bricks)
    move_all(space, bricks, skip=None)

    n = 0
    for j in range(len(bricks)):
        new_space = [
            [
                [space[x][y][z] for z in range(len(space[0][0]))]
                for y in range(len(space[0]))
            ]
            for x in range(len(space))
        ]
        new_bricks = [(b[0].copy(), b[1].copy()) for b in bricks]
        vex = get_brick_vecels(bricks[j])

        for x, y, z in vex:
            new_space[x][y][z] = -1

        n += move_all(new_space, new_bricks, skip=j)

    return n
