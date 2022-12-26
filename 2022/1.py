def prepare_data(file="input.txt"):
    with open(file) as file:
        lines = [line.strip() for line in file.readlines()]

    food = [[]]

    for line in lines:
        if line == "":
            food.append([])
        else:
            food[-1].append(int(line))

    data = {"food": food}

    return data


def solve1(food, **kwargs):
    return max([sum(x) for x in food])


def solve2(food, **kwargs):
    return sum(sorted([sum(x) for x in food])[-3:])
