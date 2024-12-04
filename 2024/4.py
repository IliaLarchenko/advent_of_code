def prepare_data(file="input.txt"):
    with open(file) as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]

    return {"lines": lines}


def solve1(lines, **kwargs):
    ans = 0
    for i in range(len(lines)):
        for j in range(len(lines[0])):
            if lines[i][j] != "X":
                continue
            for di in range(-1, 2):
                for dj in range(-1, 2):
                    if di == 0 and dj == 0:
                        continue
                    if i + di * 3 < 0 or i + di * 3 >= len(lines) or j + dj * 3 < 0 or j + dj * 3 >= len(lines[0]):
                        continue
                    if lines[i + di][j + dj] + lines[i + di * 2][j + dj * 2] + lines[i + di * 3][j + dj * 3] == "MAS":
                        ans += 1

    return ans


def solve2(lines, **kwargs):
    ans = 0
    for i in range(1, len(lines) - 1):
        for j in range(1, len(lines[0]) - 1):
            ans += (
                lines[i][j] == "A"
                and lines[i - 1][j - 1] != lines[i + 1][j + 1]
                and "".join(sorted([lines[i + di][j + dj] for di in (-1, 1) for dj in (-1, 1)])) == "MMSS"
            )

    return ans
