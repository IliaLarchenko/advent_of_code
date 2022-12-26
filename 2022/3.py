def prepare_data(file="input.txt"):
    with open(file) as file:
        lines = [line.strip() for line in file.readlines()]

    data = {"lines": lines}

    return data


def get_letter(line):
    a = set(line[: len(line) // 2])
    b = set(line[(len(line) // 2) :])
    return list(a.intersection(b))[0]


def letter_to_num(c):
    if c <= "Z":
        return ord(c) - ord("A") + 27
    else:
        return ord(c) - ord("a") + 1


def solve1(lines, **kwargs):
    return sum([letter_to_num(get_letter(line)) for line in lines])


def get_letter3(a, b, c):
    return list(set(a).intersection(set(b)).intersection(set(c)))[0]


def solve2(lines, **kwargs):
    return sum(
        [
            letter_to_num(get_letter3(lines[i * 3], lines[i * 3 + 1], lines[i * 3 + 2]))
            for i in range(len(lines) // 3)
        ]
    )
