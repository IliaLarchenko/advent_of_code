import re


def prepare_data(file="input.txt"):
    with open(file) as file:
        lines = [line for line in file.readlines()]

    num = len(lines[0]) // 4
    blocks = [[] for _ in range(num)]
    moves = []

    for line in lines:
        if line[0] == "[" or line[:2] == "  ":
            for i in range(num):
                if line[i * 4 + 1] != " ":
                    blocks[i].append(line[i * 4 + 1])
        elif line[0] == "m":
            moves.append(
                [int(re.split("move | from | to |\n", line)[i + 1]) for i in range(3)]
            )

    data = {"init_blocks": blocks, "moves": moves}

    return data


def solve1(init_blocks, moves, **kwargs):
    blocks = [init_blocks[i].copy() for i in range(len(init_blocks))]

    for m, f, t in moves:
        blocks[t - 1] = blocks[f - 1][:m][::-1] + blocks[t - 1]
        blocks[f - 1] = blocks[f - 1][m:]

    return "".join([x[0] for x in blocks])


def solve2(init_blocks, moves, **kwargs):
    blocks = [init_blocks[i].copy() for i in range(len(init_blocks))]

    for m, f, t in moves:
        blocks[t - 1] = blocks[f - 1][:m] + blocks[t - 1]
        blocks[f - 1] = blocks[f - 1][m:]

    return "".join([x[0] for x in blocks])
