import re
from functools import cache


def prepare_data(file="input.txt"):
    with open(file) as file:
        lines = [line.strip() for line in file.readlines()]

    valves_dict = {}

    for line in lines:
        split = re.split(
            """Valve | has flow rate=|; tunnels lead to valves |
            ; tunnel leads to valve |; tunnel leads to valve |, """,
            line,
        )[1:]
        name = split[0]
        pressure = int(split[1])
        paths_to = split[2:]

        valves_dict[name] = {"pressure": pressure, "paths_to": paths_to, "costs": {}}

    names = [k for k in valves_dict]

    for k, v in valves_dict.items():
        for name in names:
            v["costs"][name] = float("+inf")
        for name in v["paths_to"]:
            v["costs"][name] = 1
        v["costs"][k] = 0
        del v["paths_to"]

    for inter in names:
        for name1 in names:
            for name2 in names:
                valves_dict[name1]["costs"][name2] = min(
                    valves_dict[name1]["costs"][name2],
                    valves_dict[name1]["costs"][inter]
                    + valves_dict[inter]["costs"][name2],
                )

    zero_pressure = [k for k, v in valves_dict.items() if v["pressure"] == 0]
    non_zero_pressure = [k for k, v in valves_dict.items() if v["pressure"] > 0]

    for name in zero_pressure:
        if name != "AA":
            del valves_dict[name]
    for k, v in valves_dict.items():
        for name in zero_pressure:
            del v["costs"][name]

    for i, name in enumerate(non_zero_pressure):
        valves_dict[name]["num"] = i

    init_costs = [None] * len(non_zero_pressure)

    for name, cost in valves_dict["AA"]["costs"].items():
        init_costs[valves_dict[name]["num"]] = cost

    cost_matrix = [
        [None] * len(non_zero_pressure) for _ in range(len(non_zero_pressure))
    ]

    for name1 in non_zero_pressure:
        for name2 in non_zero_pressure:
            cost_matrix[valves_dict[name1]["num"]][
                valves_dict[name2]["num"]
            ] = valves_dict[name1]["costs"][name2]

    pressure = [None] * len(non_zero_pressure)

    for name in non_zero_pressure:
        pressure[valves_dict[name]["num"]] = valves_dict[name]["pressure"]

    data = {"init_costs": init_costs, "pressure": pressure, "cost_matrix": cost_matrix}

    return data


def set_status(status, n):
    return (1 << n) | status


def get_status(status, n):
    return (status >> n) & 1


def solve1(init_costs, pressure, cost_matrix, **kwarg):
    @cache
    def recursion_step(valve, time_left, status, opened):
        if time_left == 0:
            return 0

        best = time_left * opened
        for i in range(len(cost_matrix)):
            if (
                i != valve
                and get_status(status, i) == 0
                and time_left > cost_matrix[valve][i] + 1
            ):
                best = max(
                    best,
                    recursion_step(
                        i,
                        time_left - cost_matrix[valve][i] - 1,
                        set_status(status, i),
                        opened + pressure[i],
                    )
                    + (cost_matrix[valve][i] + 1) * opened,
                )
        return best

    time = 30
    best = 0
    for i in range(len(cost_matrix)):
        if init_costs[i] < time:
            best = max(
                best,
                recursion_step(
                    i, time - init_costs[i] - 1, set_status(0, i), pressure[i]
                ),
            )
    return best


def solve2(init_costs, pressure, cost_matrix, verbose=False, **kwarg):
    @cache
    def first_recursion_step(valve1, cost1, valve2, cost2, time_left, status, opened):
        if time_left == 0:
            return 0

        if valve1 > valve2:
            return first_recursion_step(
                valve2, cost2, valve1, cost1, time_left, status, opened
            )

        if cost1 == 0 and get_status(status, valve1) == 0:
            return (
                second_recursion_step(
                    valve1,
                    0,
                    valve2,
                    cost2,
                    time_left,
                    set_status(status, valve1),
                    opened + pressure[valve1],
                )
                + opened
            )

        if cost1 > 0:
            return (
                second_recursion_step(
                    valve1, cost1 - 1, valve2, cost2, time_left, status, opened
                )
                + opened
            )

        best = 0
        for i in range(len(cost_matrix)):
            if (
                i != valve1
                and get_status(status, i) == 0
                and time_left > cost_matrix[valve1][i] + 1
                and ((i != valve2) or (cost_matrix[valve1][i] < cost2))
            ):
                best = max(
                    best,
                    second_recursion_step(
                        i,
                        cost_matrix[valve1][i] - 1,
                        valve2,
                        cost2,
                        time_left,
                        set_status(status, valve1),
                        opened,
                    )
                    + opened,
                )
        if best == 0:
            best = (
                second_recursion_step(
                    valve1, 0, valve2, cost2, time_left, status, opened
                )
                + opened
            )
        return best

    @cache
    def second_recursion_step(valve1, cost1, valve2, cost2, time_left, status, opened):
        if time_left == 0:
            return 0

        if cost2 == 0 and get_status(status, valve2) == 0:
            return first_recursion_step(
                valve1,
                cost1,
                valve2,
                0,
                time_left - 1,
                set_status(status, valve2),
                opened + pressure[valve2],
            )

        if cost2 > 0:
            return first_recursion_step(
                valve1, cost1, valve2, cost2 - 1, time_left - 1, status, opened
            )

        best = 0
        for i in range(len(cost_matrix)):
            if (
                i != valve2
                and get_status(status, i) == 0
                and time_left > cost_matrix[valve2][i] + 1
                and ((i != valve1) or (cost_matrix[valve2][i] <= cost1))
            ):
                best = max(
                    best,
                    first_recursion_step(
                        valve1,
                        cost1,
                        i,
                        cost_matrix[valve2][i] - 1,
                        time_left - 1,
                        set_status(status, valve2),
                        opened,
                    ),
                )
        if best == 0:
            best = first_recursion_step(
                valve1, cost1, valve2, cost2, time_left - 1, status, opened
            )
        return best

    time = 26
    best = 0
    for i in range(len(cost_matrix) - 1):
        for j in range(i + 1, len(cost_matrix)):
            if init_costs[i] < time and init_costs[j] < time:
                best = max(
                    best,
                    first_recursion_step(
                        i, init_costs[i], j, init_costs[j], time, 0, 0
                    ),
                )
                if verbose:
                    print(best, i, j)
    return best
