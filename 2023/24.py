import numpy as np
from scipy.optimize import minimize


def prepare_data(file="input.txt"):
    with open(file) as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines]

    return {"lines": lines}


def line_to_2d(line):
    coord, speed = line.split(" @ ")
    coord = [int(x) for x in coord.split(", ")]
    speed = [int(x) for x in speed.split(", ")]

    # a is never 0 in the test data
    a = speed[1]
    b = -speed[0]
    c = -coord[0] * speed[1] + coord[1] * speed[0]

    return (b / a, c / a, coord[0], speed[0] > 0)  # x + by + c = 0


def get_intersect(line1, line2):
    b1, c1, x01, dir1 = line1
    b2, c2, x02, dir2 = line2

    if b1 == b2:
        return None

    y = (c2 - c1) / (b1 - b2)
    x = (c1 * b2 - c2 * b1) / (b1 - b2)

    return (x, y)


def solve1(lines, lim=(200000000000000, 400000000000000), **kwargs):
    lines_2d = [line_to_2d(x) for x in lines]

    ans = 0
    for i, line1 in enumerate(lines_2d):
        for j, line2 in enumerate(lines_2d[i + 1 :]):
            intersect = get_intersect(line1, line2)
            if (
                intersect
                and lim[0] <= intersect[0] <= lim[1]
                and lim[0] <= intersect[1] <= lim[1]
                and ((intersect[0] > line1[2]) == line1[3])
                and ((intersect[0] > line2[2]) == line2[3])
            ):
                ans += 1
    return ans


def line_to_coord(line):
    coord, speed = line.split(" @ ")
    coord = [int(x) for x in coord.split(", ")]
    speed = [int(x) for x in speed.split(", ")]

    return coord, speed


def solve2(lines, **kwargs):
    lines_coord = [line_to_coord(x) for x in lines]
    coords = np.stack([np.array(x[0]) for x in lines_coord])
    speeds = np.stack([np.array(x[1]) for x in lines_coord])

    def min_loss(arr):
        ts = arr[6:]
        return (
            ((coords - arr[:3]) + (speeds - arr[3:6]) * ts.reshape(len(ts), 1)) ** 2
        ).sum()

    x0 = np.array([0, 0, 0, 0, 0, 0] + [0] * len(lines_coord))
    res = minimize(min_loss, x0, method="Powell")

    return round(res["x"][:3].sum())


def solve2_alt(lines, **kwargs):
    lines_coord = [line_to_coord(x) for x in lines]
    coords = np.stack([np.array(x[0]) for x in lines_coord])
    speeds = np.stack([np.array(x[1]) for x in lines_coord])

    # Initial guess
    c = np.random.rand(3)
    s = np.random.rand(3)
    ts = np.random.rand(len(lines_coord), 1)

    # Iterative optimization
    for i in range(20000):
        # analytical solution for the local optimums
        # each of the following lines returns the optimal value of the corresponding variable
        # given the values of the other variables
        # it works even faster than scipy.optimize for this porblem

        ts = -((coords - c) * (speeds - s)).sum(1) / ((speeds - s) ** 2).sum(1)
        ts = ts.reshape(len(ts), 1)
        c = (coords + (speeds - s) * ts.reshape(len(ts), 1)).mean(0)
        s = (((coords - c) + speeds * ts) * ts).mean(0) / (ts**2).mean()

    return int(c.sum().round())
