def prepare_data(file="input.txt"):
    with open(file) as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines]

    times = [int(x) for x in lines[0].split()[1:]]
    distances = [int(x) for x in lines[1].split()[1:]]

    return {"times": times, "distances": distances}


def get_options(time, distance):
    D = time**2 - 4 * distance
    x1 = int((time - (D) ** (1 / 2)) / 2 + 1.0000000000000001)
    x2 = int((time + (D) ** (1 / 2)) / 2 - 0.000000000001)
    return x1, x2


def solve1(times, distances, **kwargs):
    n = 1
    for t, d in zip(times, distances):
        x1, x2 = get_options(t, d)
        n *= x2 - x1 + 1
    return n


def solve2(times, distances, **kwargs):
    time = int("".join([str(x) for x in times]))

    distance = int("".join([str(x) for x in distances]))

    x1, x2 = get_options(time, distance)

    return x2 - x1 + 1
