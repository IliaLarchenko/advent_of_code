from functools import cache


def prepare_data(file="input.txt"):
    with open(file) as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines]
    conditions = [x.split()[0] for x in lines]
    nums = [tuple([int(y) for y in x.split()[1].split(",")]) for x in lines]

    return {"conditions": conditions, "nums": nums}


def num_arr(condition, num):
    @cache
    def rec(i, num):
        if i >= len(condition) and len(num) == 0:
            return 1
        elif i >= len(condition):
            return 0
        elif condition[i] == ".":
            return rec(i + 1, num)
        else:
            n = 0
            if condition[i] == "?":
                n = rec(i + 1, num)

            if len(num) == 0:
                pass
            elif "." not in set(condition[i : i + num[0]]) and (
                i + num[0] == len(condition)
                or (i + num[0] < len(condition) and condition[i + num[0]] in "?.")
            ):
                n += rec(i + num[0] + 1, num[1:])
            else:
                pass

            return n

    return rec(0, num)


def solve1(conditions, nums, **kwargs):
    return sum([num_arr(c, n) for c, n in zip(conditions, nums)])


def solve2(conditions, nums, **kwargs):
    return sum([num_arr("?".join([c] * 5), n * 5) for c, n in zip(conditions, nums)])
