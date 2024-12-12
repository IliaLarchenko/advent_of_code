def prepare_data(file="input.txt"):
    with open(file) as f:
        lines = f.readlines()
    garden = [["."] + [n for n in x.strip()] + ["."] for x in lines]
    padding = [["."] * (len(garden) + 2)]
    garden = padding + garden + padding
    return {"garden": garden}


def compute_price(garden, apply_discount=False):
    price = 0
    seen = set()

    for i in range(1, len(garden) - 1):
        for j in range(1, len(garden[0]) - 1):
            if (i, j) in seen:
                continue

            perimeter = 0
            area = 0

            to_check = set([(i, j)])
            plant = garden[i][j]

            while len(to_check) > 0:
                i1, j1 = to_check.pop()
                area += 1

                for i2, j2 in ((i1 + 1, j1), (i1 - 1, j1), (i1, j1 + 1), (i1, j1 - 1)):
                    if garden[i2][j2] != plant:
                        perimeter += 1
                        if apply_discount:
                            if (i1 == i2 and garden[i1 - 1][j1] == plant and garden[i1 - 1][j2] != plant) or (
                                j1 == j2 and garden[i1][j1 - 1] == plant and garden[i2][j1 - 1] != plant
                            ):
                                perimeter -= 1
                    elif (i2, j2) not in seen:
                        to_check.add((i2, j2))
                seen.add((i1, j1))
            price += area * perimeter
    return price


def solve1(garden, **kwargs):
    return compute_price(garden, apply_discount=False)


def solve2(garden, **kwargs):
    return compute_price(garden, apply_discount=True)
