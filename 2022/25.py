def prepare_data(file="input.txt"):
    with open(file) as f:
        lines = [line.strip() for line in f.readlines()]

    data = {"lines": lines}

    return data


def snafu_to_dec(num):
    n = 0
    for i, c in enumerate(num[::-1]):
        if c == "-":
            n += 5**i * -1
        elif c == "=":
            n += 5**i * -2
        else:
            n += 5**i * int(c)
    return n


def dec_to_snafu(num):
    ans = []

    while num > 0:
        ans.append(num % 5)
        num = num // 5
    ans.append(0)

    for i, n in enumerate(ans):
        if n >= 5:
            n -= 5
            ans[i + 1] += 1

        if n <= 2:
            ans[i] = str(n)
        elif n >= 3:
            ans[i + 1] += 1
            if n == 3:
                ans[i] = "="
            elif n == 4:
                ans[i] = "-"

    if ans[-1] == "0":
        ans.pop()
    return "".join(ans[::-1])


def solve1(lines, **kwargs):
    return dec_to_snafu(sum([snafu_to_dec(line) for line in lines]))
