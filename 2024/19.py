from functools import cache


def prepare_data(file="input.txt"):
    with open(file) as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]

    towels = lines[0].split(", ")
    designs = lines[2:]

    return {"towels": towels, "designs": designs}


def get_answer(designs, towels, get_sum=True):
    @cache
    def count_arrangements(design):
        if len(design) == 0:
            return 1
        return sum([count_arrangements(design[len(t) :]) for t in towels if design[: len(t)] == t])

    if get_sum:
        return sum([count_arrangements(d) for d in designs])
    else:
        return sum([count_arrangements(d) > 0 for d in designs])


def solve1(designs, towels, **kwargs):
    return get_answer(designs, towels, False)


def solve2(designs, towels, **kwargs):
    return get_answer(designs, towels, True)
