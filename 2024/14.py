def prepare_data(file="input.txt"):
    with open(file) as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines]

    positions = []
    velocities = []
    for i in range(len(lines)):
        p, v = lines[i].split()
        p = tuple([int(i) for i in p[2:].split(",")])
        v = tuple([int(i) for i in v[2:].split(",")])
        positions.append(p)
        velocities.append(v)

    return {"positions": positions, "velocities": velocities}


def make_n_steps(positions, velocities, h, w, n=1):
    positions = positions.copy()
    for _ in range(n):
        for i, (p, v) in enumerate(zip(positions, velocities)):
            positions[i] = ((p[0] + v[0]) % w, (p[1] + v[1]) % h)

    return positions


def solve1(positions, velocities, h, w, **kwargs):
    positions = make_n_steps(positions, velocities, h, w, n=100)

    q = [0, 0, 0, 0]
    midx = w // 2
    midy = h // 2
    for p in positions:
        x = (p[0] > midx) - (p[0] < midx)
        y = (p[1] > midy) - (p[1] < midy)
        if x * y != 0:
            q[(x + 1) + (y + 1) // 2] += 1

    ans = 1
    for n in q:
        ans *= n

    return ans


def print_map(h, w, positions, empty="_", robot="H"):
    matrix = [[empty for __ in range(w)] for _ in range(h)]
    for p in positions:
        matrix[p[1]][p[0]] = robot
    print("\n".join(["".join(line) for line in matrix]))


def print_first_n(n, h, w, positions, velocities, empty="_", robot="H"):
    # I printed first 100 positions to find some horizontal and vertical patterns
    for i in range(n):
        print(i)
        print_map(h, w, positions, empty, robot)
        positions = make_n_steps(positions, velocities, n=1)


def solve2(positions, velocities, h, w, horizontal_pattern=12, vertical_pattern=69, **kwargs):
    # It is a very input specific solution
    # I printed first 100 positions to find first horizontal and vertical patterns
    # print_first_n(100, h,w, positions, velocities, empty = '_', robot = 'H')

    while horizontal_pattern != vertical_pattern:
        if horizontal_pattern < vertical_pattern:
            horizontal_pattern += h
        else:
            vertical_pattern += w

    positions = make_n_steps(positions, velocities, h, w, n=vertical_pattern)
    print_map(h, w, positions)

    return vertical_pattern
