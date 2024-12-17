def prepare_data(file="input.txt"):
    with open(file) as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines]

    a = int(lines[0][12:])
    b = int(lines[1][12:])
    c = int(lines[2][12:])

    program = [int(x) for x in lines[4][9:].split(",")]

    return {"program": program, "a": a, "b": b, "c": c}


def get_output(program, a, b, c):
    pointer = 0
    output = []

    while 0 <= pointer < len(program):
        inst = program[pointer]
        literal = program[pointer + 1]

        if literal < 4:
            combo = literal
        elif literal < 7:
            combo = [a, b, c][literal - 4]

        if inst == 0:
            a = a // (2**combo)
        elif inst == 1:
            b = b ^ literal
        elif inst == 2:
            b = combo % 8
        elif inst == 3:
            if a != 0:
                pointer = literal
                continue
        elif inst == 4:
            b = b ^ c
        elif inst == 5:
            output.append(combo % 8)
        elif inst == 6:
            b = a // (2**combo)
        elif inst == 7:
            c = a // (2**combo)

        pointer += 2

    return output


def solve1(program, a, b, c, **kwargs):
    return ",".join([str(x) for x in get_output(program, a, b, c)])


def get_rest(program, pos, a):
    # Finds `a` that generate a program up to the `pos` position
    # given starting `a` that generates the rest of the program
    if pos == -1:
        return a

    for i in range(8):
        if get_output(program, a * 8 + i, 0, 0)[0] == program[pos]:
            res = get_rest(program, pos - 1, a * 8 + i)
            if res is not None:
                return res

    return None


def solve2(program, **kwargs):
    return get_rest(program, len(program) - 1, 0)
