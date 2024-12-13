def prepare_data(file="input.txt"):
    with open(file) as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines]
    return {"lines": lines}


def parse_input(lines):
    a = [int(n[1:]) for n in lines[0][10:].split(", ")]
    b = [int(n[1:]) for n in lines[1][10:].split(", ")]
    t = [int(n[2:]) for n in lines[2][7:].split(", ")]

    return a, b, t


def compute_cost(a, b, target):
    denom = b[1] * a[0] - a[1] * b[0]
    num_b = target[1] * a[0] - a[1] * target[0]
    num_a = target[1] * b[0] - b[1] * target[0]

    if num_b % denom == 0 and num_a % denom == 0:
        steps_a = -num_a // denom
        steps_b = num_b // denom
        return 3 * steps_a + steps_b
    return 0


def solve1(lines, **kwargs):
    ans = 0

    for i in range(len(lines) // 4 + 1):
        ans += compute_cost(*parse_input(lines[i * 4 : i * 4 + 3]))
    return ans


def solve2(lines, **kwargs):
    ans = 0

    for i in range(len(lines) // 4 + 1):
        a, b, target = parse_input(lines[i * 4 : i * 4 + 3])
        ans += compute_cost(a, b, (target[0] + 10_000_000_000_000, target[1] + 10_000_000_000_000))
    return ans
