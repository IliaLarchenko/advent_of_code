def prepare_data(file="input.txt"):
    with open(file) as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]

    space = {}
    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            space[(i, j)] = c
            if c == "S":
                start = (i, j)
            elif c == "E":
                end = (i, j)

    return {"space": space, "start": start, "end": end}


def check_position(x, y, space):
    return (x, y) in space and space[(x, y)] != "#"


def get_dist_to_end(space, start, end):
    x, y = end
    dist_to_end = {end: 0}

    dist = 1
    while (x, y) != start:
        for dx, dy in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
            if check_position(x + dx, y + dy, space) and (x + dx, y + dy) not in dist_to_end:
                x, y = x + dx, y + dy
                dist_to_end[(x, y)] = dist
                break
        dist += 1

    return dist_to_end


def get_all_cheats(x, y, space, time):
    for dx in range(-time, time + 1):
        max_dy = time - abs(dx)
        for dy in range(-max_dy, max_dy + 1):
            if (dx, dy) != (0, 0) and check_position(x + dx, y + dy, space):
                yield (x + dx, y + dy)


def get_answer(space, cheat_time, dist_to_end, save=100):
    ans = 0

    for x, y in dist_to_end.keys():
        for nx, ny in get_all_cheats(x, y, space, cheat_time):
            if dist_to_end[(x, y)] - dist_to_end[(nx, ny)] - abs(x - nx) - abs(y - ny) >= save:
                ans += 1
    return ans


def solve1(space, start, end, save=100, **kwargs):
    dist_to_end = get_dist_to_end(space, start, end)
    return get_answer(space, 2, dist_to_end, save)


def solve2(space, start, end, save=100, **kwargs):
    dist_to_end = get_dist_to_end(space, start, end)
    return get_answer(space, 20, dist_to_end, save)
