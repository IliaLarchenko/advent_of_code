def prepare_data(file="input.txt"):
    with open(file) as file:
        lines = [line.strip() for line in file.readlines()]

    data = {"lines": lines}

    return data


class Monkey:
    def __init__(self, data, divider=1):
        self.n = int(data[0][7:-1])
        self.items = [int(x) for x in data[1][16:].split(", ")]
        self.insp_count = 0
        self.operation = lambda old: eval(data[2][17:])
        self.test = (
            lambda x: int(data[4][25:])
            if x % int(data[3][19:]) == 0
            else int(data[5][26:])
        )
        self.divider = divider
        self.base = None
        self.div = int(data[3][19:])

    def set_base(self, base):
        self.base = base

    def inspect_item(self, i, monkeys):
        self.items[i] = self.operation(self.items[i]) // self.divider
        n = self.test(self.items[i])

        if self.base:
            self.items[i] = self.items[i] % self.base

        monkeys[n].items.append(self.items[i])
        del self.items[i]
        self.insp_count += 1

    def inspect(self, monkeys):
        while len(self.items) > 0:
            self.inspect_item(0, monkeys)


def solve_n(lines, div, steps):
    monkeys = []

    for i in range(len(lines) // 7 + 1):
        data = lines[i * 7 : (i + 1) * 7]
        monkeys.append(Monkey(data, div))

    base = 1
    for m in monkeys:
        base *= m.div

    for m in monkeys:
        m.set_base(base)

    for r in range(steps):
        for m in monkeys:
            m.inspect(monkeys)
    top = [x.insp_count for x in monkeys]
    top.sort()

    return top[-1] * top[-2]


def solve1(lines, **kwargs):
    return solve_n(lines, 3, 20)


def solve2(lines, **kwargs):
    return solve_n(lines, 1, 10000)
