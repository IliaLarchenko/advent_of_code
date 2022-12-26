def prepare_data(file="input.txt"):
    with open(file) as file:
        lines = [line.strip() for line in file.readlines()]

    pixels = set()
    for line in lines:
        x, y, z = [int(x) for x in line.split(",")]
        pixels.add((x, y, z))

    data = {"pixels": pixels}

    return data


def get_adj(x, y, z):
    return [
        (x + 1, y, z),
        (x - 1, y, z),
        (x, y + 1, z),
        (x, y - 1, z),
        (x, y, z + 1),
        (x, y, z - 1),
    ]


def solve1(pixels, **kwargs):
    ans = 0
    for p in pixels:
        for adj_p in get_adj(*p):
            if adj_p not in pixels:
                ans += 1

    return ans


def solve2(pixels, **kwargs):
    steam = set()
    step = set()
    x_lim = min([p[0] for p in pixels]), max([p[0] for p in pixels])
    y_lim = min([p[1] for p in pixels]), max([p[1] for p in pixels])
    z_lim = min([p[2] for p in pixels]), max([p[2] for p in pixels])

    # initial steam is outside the limits
    for x in range(x_lim[0], x_lim[1]):
        for y in range(y_lim[0], y_lim[1]):
            for z in (z_lim[0] - 1, z_lim[1] + 1):
                steam.add((x, y, z))
                step.add((x, y, z))

    for x in range(x_lim[0], x_lim[1]):
        for y in (y_lim[0] - 1, y_lim[1] + 1):
            for z in range(z_lim[0], z_lim[1]):
                steam.add((x, y, z))
                step.add((x, y, z))

    for x in (x_lim[0] - 1, x_lim[1] + 1):
        for y in range(y_lim[0], y_lim[1]):
            for z in range(z_lim[0], z_lim[1]):
                steam.add((x, y, z))
                step.add((x, y, z))

    # expand the steam to all possible cells
    while len(step) > 0:
        p = step.pop()
        for adj_p in get_adj(*p):
            x, y, z = adj_p
            if (
                x_lim[0] <= x <= x_lim[1]
                and y_lim[0] <= y <= y_lim[1]
                and z_lim[0] <= z <= z_lim[1]
                and ((x, y, z) not in pixels)
                and ((x, y, z) not in steam)
            ):
                steam.add((x, y, z))
                step.add((x, y, z))

    ans = 0
    for p in pixels:
        for adj_p in get_adj(*p):
            if adj_p in steam:
                ans += 1

    return ans
