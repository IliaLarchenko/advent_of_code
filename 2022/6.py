def prepare_data(file="input.txt"):
    with open(file) as file:
        lines = [line.strip() for line in file.readlines()]

    data = {"line": lines[0]}
    return data


def solve_n(line, n):
    chars = []
    for i, c in enumerate(line):
        if len(chars) == n:
            chars = chars[1:]
        if c in chars:
            chars += [c]
        else:
            if len(set(chars)) == n - 1:
                return i + 1
            chars += [c]
    return None


def solve1(line, **kwargs):
    return solve_n(line, 4)


def solve2(line, **kwargs):
    return solve_n(line, 14)
