def prepare_data(file="input.txt"):
    with open(file) as file:
        lines = [line.strip() for line in file.readlines()]

    data = [line.split(" ") for line in lines]
    data = [(k, int(v)) for k, v in data]

    data = {"data": data}
    return data


def update(tx, ty, hx, hy):
    if tx == hx:
        if ty > hy + 1:
            ty -= 1
        elif ty < hy - 1:
            ty += 1
    elif ty == hy:
        if tx > hx + 1:
            tx -= 1
        elif tx < hx - 1:
            tx += 1
    elif abs(ty - hy) == 1 and abs(tx - hx) == 1:
        pass
    else:
        if tx > hx:
            tx -= 1
        elif tx < hx:
            tx += 1

        if ty > hy:
            ty -= 1
        elif ty < hy:
            ty += 1

    return tx, ty


def solve_n(data, num):
    visited = {(0, 0)}
    knots = [[0, 0] for _ in range(num)]

    for d, l in data:
        for _ in range(l):
            if d == "R":
                knots[0][0] += 1
            elif d == "U":
                knots[0][1] += 1
            elif d == "L":
                knots[0][0] -= 1
            else:
                knots[0][1] -= 1

            for i in range(1, num):
                knots[i][0], knots[i][1] = update(
                    knots[i][0], knots[i][1], knots[i - 1][0], knots[i - 1][1]
                )

            visited.add((knots[num - 1][0], knots[num - 1][1]))
    return len(visited)


def solve1(data, **kwargs):
    return solve_n(data, 2)


def solve2(data, **kwargs):
    return solve_n(data, 10)
