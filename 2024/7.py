def prepare_data(file="input.txt"):
    with open(file) as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines]

    results = []
    inputs = []
    for line in lines:
        r, i = line.split(":")
        i = i.strip()
        results.append(int(r))
        inputs.append([int(n) for n in i.split(" ")])

    return {"results": results, "inputs": inputs}


def check(inputs, i, num, target, check_concat):
    if num > target:
        return False
    if len(inputs) == i:
        return target == num

    return (
        check(inputs, i + 1, num * inputs[i], target, check_concat)
        or check(inputs, i + 1, num + inputs[i], target, check_concat)
        or (check_concat and check(inputs, i + 1, num * 10 ** (len(str(inputs[i]))) + inputs[i], target, check_concat))
    )


def solve1(results, inputs, **kwargs):
    ans = 0
    for r, inp in zip(results, inputs):
        if check(inp, 0, 0, r, False):
            ans += r
    return ans


def solve2(results, inputs, **kwargs):
    ans = 0
    for r, inp in zip(results, inputs):
        if check(inp, 0, 0, r, True):
            ans += r
    return ans
