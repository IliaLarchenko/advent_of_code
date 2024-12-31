import random


def parse_data(lines):
    values = {}
    for i, line in enumerate(lines):
        if line == "":
            break
        name, value = line.split(": ")
        values[name] = int(value)

    operations = {}
    impact = {}
    for j in range(i + 1, len(lines)):
        line = lines[j]
        op, tgt = line.split(" -> ")
        a1, op, a2 = op.split(" ")
        operations[tgt] = (op, a1, a2)
        for a in (a1, a2):
            impact[a] = impact.get(a, set())
            impact[a].add(tgt)
    return values, operations, impact


def prepare_data(file="input.txt"):
    with open(file) as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]

    values, operations, impact = parse_data(lines)
    all_wires = set(values.keys())
    all_wires.update(set(operations.keys()))

    return {"values": values, "operations": operations, "impact": impact, "all_wires": all_wires}


def fill_values(values, operations, impact):
    to_check = set([y for x in values.keys() for y in impact[x]])
    while len(to_check) > 0:
        x = to_check.pop()
        op, a1, a2 = operations[x]
        if a1 in values and a2 in values:
            if op == "AND":
                values[x] = values[a1] and values[a2]
            elif op == "OR":
                values[x] = values[a1] or values[a2]
            else:
                values[x] = values[a1] ^ values[a2]
            to_check.update(impact.get(x, set()))
    return values


def solve1(values, operations, impact, **kwargs):
    z_wires = sorted([w for w in operations.keys() if w[0] == "z"])
    values = fill_values(values, operations, impact)
    ans = 0
    m = 1
    for w in z_wires:
        ans += m * values[w]
        m *= 2
    return ans


def swap_wires(wires, operations, impact):
    for i in (0, 1):
        impact[operations[wires[i]][1]].remove(wires[i])
        impact[operations[wires[i]][2]].remove(wires[i])
    operations[wires[0]], operations[wires[1]] = operations[wires[1]], operations[wires[0]]

    for i in (0, 1):
        _, a1, a2 = operations[wires[i]]
        impact[a1].add(wires[i])
        impact[a2].add(wires[i])


def num_to_values(values, wires, num):
    for i in range(len(wires)):
        values[wires[i]] = num % 2
        num = num // 2
    return values


def values_to_binary(values, wires):
    return "".join([str(values[w]) for w in wires])


def find_best_replacement(wire, all_wires, operations, impact, n=1000):
    x_wires = sorted([w for w in all_wires if w[0] == "x"])
    y_wires = sorted([w for w in all_wires if w[0] == "y"])
    z_wires = sorted([w for w in all_wires if w[0] == "z"])
    best_error = float("inf")
    best_replacement = None
    for w in all_wires:
        if w[0] in "xy" or w == wire:
            continue

        swap_wires((wire, w), operations, impact)
        error_count = 0

        for _ in range(n):
            x = random.randint(0, 2 ** len(x_wires))
            y = random.randint(0, 2 ** len(y_wires))

            values = {}
            num_to_values(values, x_wires, x)
            num_to_values(values, y_wires, y)
            values = fill_values(values, operations, impact)

            if all([z_w in values for z_w in z_wires]):
                actual_result = values_to_binary(values, z_wires)
                expected_result = values_to_binary(num_to_values(values, z_wires, x + y), z_wires)

                for i in range(len(expected_result)):
                    error_count += expected_result[i] != actual_result[i]
            else:
                error_count = float("inf")
                break

        swap_wires((wire, w), operations, impact)

        if error_count < best_error:
            best_error = error_count
            best_replacement = w
    return best_replacement, best_error


def solve2(operations, impact, all_wires, **kwargs):
    # wires that have strange operations and should be swapped
    candidates = []

    z_wires = [w for w in operations.keys() if w[0] == "z"]

    for k in z_wires:
        v = operations[k]
        if k[0] == "z" and v[0] != "XOR" and k != "z45":
            candidates.append(k)

    for k, v in operations.items():
        if v[0] == "XOR" and k[0] != "z":
            if v[1][0] not in "xy" or v[2][0] not in "xy":
                candidates.append(k)

            elif v[1][1:] == v[2][1:]:
                z = f"z{v[1][1:]}"
                if k not in operations[f"z{v[1][1:]}"] and z not in candidates:
                    candidates.append(k)

    error = 1
    while error > 0:
        # usually 1 iteration is enough but need to retry if accidentally swapped a wire that should not be swapped
        answer = []
        pairs = []
        for wire in candidates:
            if wire in answer:
                continue
            pair, error = find_best_replacement(wire, all_wires, operations, impact, n=30)
            print(wire, pair, error)
            swap_wires((wire, pair), operations, impact)
            answer.append(wire)
            answer.append(pair)
            pairs.append((wire, pair))
        if error > 0:
            for pair in pairs:
                swap_wires(pair, operations, impact)

    return ",".join(sorted(answer))
