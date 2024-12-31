def prepare_data(file="input.txt"):
    with open(file) as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]

    keys = []
    locks = []

    i = 0
    for line in lines:
        if line == "":
            i += 1
            continue
        if len(keys) + len(locks) == i:
            to_update = [0] * 5
            if line[0][0] == "#":
                keys.append(to_update)
            else:
                locks.append(to_update)
        for j, c in enumerate(line):
            if c == "#":
                to_update[j] += 1

    return {"keys": keys, "locks": locks}


def solve1(keys, locks, **kwargs):
    ans = 0
    for key in keys:
        for lock in locks:
            ans += all([i + j <= 7 for i, j in zip(key, lock)])
    return ans
