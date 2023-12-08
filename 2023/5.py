def prepare_data(file="input.txt"):
    with open(file) as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines]

    cur_nums = [int(x) for x in lines[0].split()[1:]]

    blocks = []
    for l in lines[2:]:
        if len(l) == 0:
            pass
        elif not l[0].isnumeric():
            blocks.append([])
        else:
            blocks[-1].append([int(x) for x in l.split()])
    blocks = [sorted(x, key=lambda y: y[1]) for x in blocks]

    ranges = []
    for i in range(len(cur_nums) // 2):
        ranges.append([cur_nums[i * 2], cur_nums[i * 2 + 1]])

    return {"cur_nums": cur_nums, "ranges": ranges, "blocks": blocks}


def solve1(cur_nums, blocks, **kwargs):
    min_num = float("inf")
    for num in cur_nums:
        for block in blocks:
            for m in block:
                if m[1] + m[2] > num >= m[1]:
                    num = m[0] - m[1] + num
                    break
        min_num = min(num, min_num)
    return min_num


def solve2(ranges, blocks, **kwargs):
    for block in blocks:
        new_r = []
        for r in ranges:
            for m in block:
                if m[1] + m[2] > r[0] >= m[1]:
                    len_r = min(r[1], m[1] + m[2] - r[0])
                    new_r.append([m[0] - m[1] + r[0], len_r])
                    r[0] += len_r
                    r[1] -= len_r

                elif m[1] > r[0] and r[0] + r[1] > m[1]:
                    len_r = min(m[2] + m[1], r[0] + r[1]) - m[1]
                    new_r.append([m[0], len_r])
                    new_r.append([r[0], m[1] - r[0]])
                    r[1] = r[1] + r[0] - m[1] - len_r
                    r[0] = m[1] + len_r

        ranges = [x for x in sorted(new_r + ranges) if x[1] != 0]

    return ranges[0][0]
