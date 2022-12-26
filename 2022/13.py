def prepare_data(file="input.txt"):
    # data preparation

    with open(file) as file:
        lines = [line.strip() for line in file.readlines()]

    pairs = []
    for i in range((len(lines) + 1) // 3):
        pairs.append((eval(lines[i * 3]), eval(lines[i * 3 + 1])))

    data = {"pairs": pairs}
    return data


def compare(l1, l2):
    i = 0

    while i < len(l1) and i < len(l2):
        if isinstance(l1[i], list) and isinstance(l2[i], list):
            order = compare(l1[i], l2[i])
        elif isinstance(l2[i], list):
            order = compare([l1[i]], l2[i])
        elif isinstance(l1[i], list):
            order = compare(l1[i], [l2[i]])
        else:
            if l1[i] < l2[i]:
                order = 1
            elif l1[i] > l2[i]:
                order = -1
            else:
                order = 0
        if order == 0:
            i += 1
        else:
            return order

    if i == len(l1) and i == len(l2):
        return 0
    elif i == len(l1):
        return 1
    else:
        return -1


def solve1(pairs, **kwargs):
    true_ind = []
    for i in range(len(pairs)):
        order = compare(*pairs[i])
        if order == 1:
            true_ind.append(i + 1)

    return sum(true_ind)


def solve2(pairs, **kwargs):
    pos = [1, 2]

    for pair in pairs:
        for el in pair:
            if compare(el, [[6]]) == 1:
                pos[1] += 1
                if compare(el, [[2]]) == 1:
                    pos[0] += 1

    return pos[0] * pos[1]
