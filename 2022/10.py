def prepare_data(file="input.txt"):
    with open(file) as file:
        lines = [tuple(line.strip().split(" ")) for line in file.readlines()]

    steps = []
    for line in lines:
        if line[0][0] == "n":
            steps.append(0)
        else:
            steps.append(0)
            steps.append(int(line[1]))

    data = {"steps": steps}
    return data


def solve1(steps, **kwargs):
    ans = 0
    x = 1
    for i, n in enumerate(steps):
        if (i - 19) % 40 == 0:
            ans += x * (i + 1)
        x += n
    return ans


def solve2(steps, **kwargs):
    ans = []
    x = 1

    line = []
    for i, n in enumerate(steps):

        if abs(i % 40 - x) <= 1:
            line.append("#")
        else:
            # if should be "." but it is easier to read like this
            line.append(" ")

        x += n
        if (i + 1) % 40 == 0:
            ans.append("".join(line))
            line = []

    return "\n".join(ans)
