def prepare_data(file="input.txt"):
    with open(file) as file:
        lines = [line.strip() for line in file.readlines()]

    pairs = []

    for line in lines:
        left, right = tuple([x for x in line.split(",")])
        a1, b1 = tuple([int(x) for x in left.split("-")])
        a2, b2 = tuple([int(x) for x in right.split("-")])
        pairs.append((a1, b1, a2, b2))

    data = {"pairs": pairs}

    return data


def solve1(pairs, **kwargs):
    return sum([(a <= x and b >= y) or (a >= x and b <= y) for a, b, x, y in pairs])


def solve2(pairs, **kwargs):
    return sum([(a <= y) and (b >= x) for a, b, x, y in pairs])
