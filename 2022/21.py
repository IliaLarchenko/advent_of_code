import re


def prepare_data(file="input.txt"):
    with open(file) as file:
        lines = [line.strip() for line in file.readlines()]

    monkeys = {}
    for line in lines:
        name = line[:4]
        names = re.split(" \+ | - | \* | / ", line[6:])
        if len(names) == 1:
            monkeys[name] = int(names[0])
        else:
            # (name1, name2, operation)
            monkeys[name] = (names[0], names[1], line[11])

    data = {"monkeys": monkeys}

    return data


def get_monkey(name, monkeys, var_name=None):
    if name == var_name:
        return (None, None, None)
    if isinstance(monkeys[name], tuple):
        num0 = get_monkey(monkeys[name][0], monkeys)
        num1 = get_monkey(monkeys[name][1], monkeys)
        if isinstance(num0, tuple) or isinstance(num1, tuple):
            monkeys[name] = (monkeys[name][0], monkeys[name][1], monkeys[name][2])
        else:
            monkeys[name] = eval(f"{num0}{monkeys[name][2]}{num1}")
    return monkeys[name]


def solve1(monkeys, **kwargs):
    return int(get_monkey("root", monkeys.copy()))


def get_diff(monkeys, var_name, var_val):
    monkeys = monkeys.copy()
    monkeys[var_name] = var_val
    return get_monkey("root", monkeys)


def descent(num, step, monkeys):
    # it will work only with monotonous functions
    # but for this problem it is enough
    left = get_diff(monkeys, "humn", num - step) ** 2
    res = get_diff(monkeys, "humn", num) ** 2
    right = get_diff(monkeys, "humn", num + step) ** 2

    if res == 0:
        return num
    if res <= min(right, left):
        return descent(num, max(step // 2, 1), monkeys)

    if right < res:
        return descent(num + step, step, monkeys)
    if left < res:
        return descent(num - step, step, monkeys)


def solve2(monkeys, **kwargs):
    monkeys_new = monkeys.copy()
    monkeys_new["root"] = (monkeys_new["root"][0], monkeys_new["root"][1], "-")
    monkeys_new["humn"] = (None, None, None)
    return descent(0, 1000000000000000000, monkeys_new)
