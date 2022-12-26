def prepare_data(file="input.txt"):
    with open(file) as file:
        lines = [line.strip() for line in file.readlines()]

    data = {"lines": lines}

    return data


def get_score1(line):
    op = ord(line[0]) - ord("A")
    you = ord(line[-1]) - ord("X")
    return ((you - op + 1) % 3) * 3 + you + 1


def solve1(lines, **kwargs):
    return sum([get_score1(line) for line in lines])


def get_score2(line):
    op = ord(line[0]) - ord("A")
    you = (op + ord(line[-1]) - ord("X") - 1) % 3
    return ((you - op + 1) % 3) * 3 + you + 1


def solve2(lines, **kwargs):
    return sum([get_score2(line) for line in lines])
