def prepare_data(file="input.txt"):
    with open(file) as file:
        lines = [line.strip() for line in file.readlines()]

    return {"lines": lines}


def check_adj_symbols(lines, line_n, start, end):
    for i in range(max(0, line_n - 1), min(line_n + 2, len(lines))):
        for j in range(max(start - 1, 0), min(len(lines[0]), end + 1)):
            if lines[i][j] != "." and not lines[i][j].isnumeric():
                return True
    return False


def solve1(lines, **kwargs):
    nums = []

    for i, line in enumerate(lines):
        n = -1
        for j, c in enumerate(line):
            if n == -1 and not c.isnumeric():
                continue
            elif n == -1 and c.isnumeric():
                n = int(c)
                start = j
            elif n > -1 and c.isnumeric():
                n = n * 10 + int(c)
            elif c == ".":
                end = j
                if check_adj_symbols(lines, i, start, end):
                    nums.append(n)
                n = -1
            else:
                nums.append(n)
                n = -1
        if n > -1 and check_adj_symbols(lines, i, start, len(line)):
            nums.append(n)
    return sum(nums)


def fins_adj_gear(lines, line_n, start, end):
    gears = []
    for i in range(max(0, line_n - 1), min(line_n + 2, len(lines))):
        for j in range(max(start - 1, 0), min(len(lines[0]), end + 1)):
            if lines[i][j] == "*":
                gears.append((i, j))
    return gears


def solve2(lines, **kwargs):
    gears_dict = {}

    for i, line in enumerate(lines):
        n = -1
        for j, c in enumerate(line):
            if n == -1 and not c.isnumeric():
                continue
            elif n == -1 and c.isnumeric():
                n = int(c)
                start = j
            elif n > -1 and c.isnumeric():
                n = n * 10 + int(c)
            else:
                end = j
                for g in fins_adj_gear(lines, i, start, end):
                    if g in gears_dict:
                        gears_dict[g].append(n)
                    else:
                        gears_dict[g] = [n]
                n = -1
        if n > -1:
            for g in fins_adj_gear(lines, i, start, len(line)):
                if g in gears_dict:
                    gears_dict[g].append(n)
                else:
                    gears_dict[g] = [n]
    ans = 0
    for k, v in gears_dict.items():
        if len(v) == 2:
            ans += v[0] * v[1]
    return ans
