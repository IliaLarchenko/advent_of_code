from functools import cache


def get_pos_dict(matrix):
    pos_dict = {}
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            pos_dict[matrix[i][j]] = (i, j)
    return pos_dict


def prepare_data(file="input.txt"):
    with open(file) as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]

    return {"lines": lines, "pos_dict_num": pos_dict_num, "pos_dict_dir": pos_dict_dir}


pos_dict_num = get_pos_dict(["789", "456", "123", "#0A"])
pos_dict_dir = get_pos_dict(["#^A", "<v>"])


@cache
def get_path(a, b, nums=True):
    path = []

    pos_dict = pos_dict_num if nums else pos_dict_dir

    ia, ja = pos_dict[a]
    ib, jb = pos_dict[b]

    if nums:
        if ib == 3 and ja == 0:
            path = path + [">"] * (jb - ja)
            ja = jb
        if jb == 0 and ia == 3:
            path = path + ["^"] * (ia - ib)
            ia = ib
    else:
        if b == "<":
            path = path + ["v"] * (ib - ia)
            ia = ib

        if a == "<":
            path = path + [">"] * (jb - ja)
            ja = jb

    if jb < ja:
        path = path + ["<"] * (ja - jb)
    if ib > ia:
        path = path + ["v"] * (ib - ia)
    if ib < ia:
        path = path + ["^"] * (ia - ib)
    if jb > ja:
        path = path + [">"] * (jb - ja)

    path.append("A")

    return "".join(path)


def get_sec_num(password):
    seq_dict = {}
    a = "A"
    for i in range(len(password)):
        b = password[i]
        seq = get_path(a, b)
        seq_dict[seq] = seq_dict.get(seq, 0) + 1
        a = b
    return seq_dict


def get_sec_dir(seq_dict):
    new_seq_dict = {}
    for prev_seq, num in seq_dict.items():
        a = "A"
        for b in prev_seq:
            seq = get_path(a, b, False)
            new_seq_dict[seq] = new_seq_dict.get(seq, 0) + num
            a = b
    return new_seq_dict


def get_answer(lines, num_int_dir):
    ans = 0
    for line in lines:
        seq_dict = get_sec_num(line)
        for _ in range(num_int_dir):
            seq_dict = get_sec_dir(seq_dict)
        ans += sum([len(k) * v for k, v in seq_dict.items()]) * int(line[:-1])
    return ans


def solve1(lines, **kwargs):
    return get_answer(lines, 2)


def solve2(lines, **kwargs):
    return get_answer(lines, 25)
