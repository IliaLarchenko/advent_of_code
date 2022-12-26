def prepare_data(file="input.txt"):
    with open(file) as f:
        lines = [line.strip() for line in f.readlines()]

    elf_list = []

    for i in range(len(lines)):
        for j in range(len(lines[0])):
            if lines[i][j] == "#":
                elf_list.append((i, j))

    data = {"elf_list": elf_list}

    return data


def get_rev_elf_dict(elf_list):
    rev_elf_dict = {}
    for i, elf in enumerate(elf_list):
        rev_elf_dict[elf] = i

    return rev_elf_dict


def make_step(elf_list, moves, rev_elf_dict):
    proposed_moves = {}

    for elf, (i, j) in enumerate(elf_list):
        if not (
            (i - 1, j) not in rev_elf_dict
            and (i - 1, j + 1) not in rev_elf_dict
            and (i - 1, j - 1) not in rev_elf_dict
            and (i + 1, j) not in rev_elf_dict
            and (i + 1, j + 1) not in rev_elf_dict
            and (i + 1, j - 1) not in rev_elf_dict
            and (i, j - 1) not in rev_elf_dict
            and (i, j + 1) not in rev_elf_dict
        ):
            for d in moves:
                if d == "N":
                    if (
                        (i - 1, j) not in rev_elf_dict
                        and (i - 1, j + 1) not in rev_elf_dict
                        and (i - 1, j - 1) not in rev_elf_dict
                    ):
                        proposed_moves[(i - 1, j)] = proposed_moves.get(
                            (i - 1, j), []
                        ) + [elf]
                        break
                elif d == "S":
                    if (
                        (i + 1, j) not in rev_elf_dict
                        and (i + 1, j + 1) not in rev_elf_dict
                        and (i + 1, j - 1) not in rev_elf_dict
                    ):
                        proposed_moves[(i + 1, j)] = proposed_moves.get(
                            (i + 1, j), []
                        ) + [elf]
                        break
                elif d == "W":
                    if (
                        (i - 1, j - 1) not in rev_elf_dict
                        and (i, j - 1) not in rev_elf_dict
                        and (i + 1, j - 1) not in rev_elf_dict
                    ):
                        proposed_moves[(i, j - 1)] = proposed_moves.get(
                            (i, j - 1), []
                        ) + [elf]
                        break
                elif d == "E":
                    if (
                        (i - 1, j + 1) not in rev_elf_dict
                        and (i, j + 1) not in rev_elf_dict
                        and (i + 1, j + 1) not in rev_elf_dict
                    ):
                        proposed_moves[(i, j + 1)] = proposed_moves.get(
                            (i, j + 1), []
                        ) + [elf]
                        break

    n_moves = 0
    for k, v in proposed_moves.items():
        if len(v) == 1:
            del rev_elf_dict[elf_list[v[0]]]
            elf_list[v[0]] = k
            rev_elf_dict[k] = v[0]
            n_moves += 1

    moves = moves[1:] + moves[:1]

    return elf_list, moves, rev_elf_dict, n_moves


def solve1(elf_list, **kwargs):
    elf_list = elf_list.copy()
    rev_elf_dict = get_rev_elf_dict(elf_list)
    moves = ["N", "S", "W", "E"]
    for _ in range(10):
        elf_list, moves, rev_elf_dict, _ = make_step(elf_list, moves, rev_elf_dict)

    x_min = min([x[0] for x in elf_list])
    x_max = max([x[0] for x in elf_list])
    y_min = min([x[1] for x in elf_list])
    y_max = max([x[1] for x in elf_list])

    return (x_max - x_min + 1) * (y_max - y_min + 1) - len(elf_list)


def solve2(elf_list, **kwargs):
    elf_list = elf_list.copy()
    rev_elf_dict = get_rev_elf_dict(elf_list)
    moves = ["N", "S", "W", "E"]
    n_moves = 1
    i = 0
    while n_moves > 0:
        elf_list, moves, rev_elf_dict, n_moves = make_step(
            elf_list, moves, rev_elf_dict
        )
        i += 1

    return i
