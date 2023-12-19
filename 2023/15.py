def prepare_data(file="input.txt"):
    with open(file) as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines]
    steps = lines[0].split(",")
    return {"steps": steps}


def get_hash(string):
    n = 0
    for c in string:
        n += ord(c)
        n *= 17
        n = n % 256
    return n


def solve1(steps, **kwargs):
    return sum([get_hash(step) for step in steps])


def decode_step(step):
    if step[-2] == "=":
        code = step[:-2]
        op = step[-2]
        num = int(step[-1])
    else:
        code = step[:-1]
        op = step[-1]
        num = None
    return code, op, num


def solve2(steps, **kwargs):
    hashmap = [([], []) for _ in range(256)]
    for step in steps:
        code, op, num = decode_step(step)
        h = get_hash(code)
        if op == "-":
            i = 0
            while i < len(hashmap[h][0]):
                if hashmap[h][0][i] == code:
                    hashmap[h][0].pop(i)
                    hashmap[h][1].pop(i)
                else:
                    i += 1
        else:
            found = False
            for i in range(len(hashmap[h][0])):
                if hashmap[h][0][i] == code:
                    hashmap[h][1][i] = num
                    found = True
                    break
            if not found:
                hashmap[h][0].append(code)
                hashmap[h][1].append(num)

    ans = 0
    for i, box in enumerate(hashmap):
        for j, l in enumerate(box[1]):
            ans += l * (i + 1) * (j + 1)
    return ans
