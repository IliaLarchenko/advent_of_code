def prepare_data(file="input.txt"):
    d = {
        "T": 10,
        "J": 11,
        "Q": 12,
        "K": 13,
        "A": 14,
    }

    def had_to_list(hand):
        t = []
        for c in hand:
            if c.isnumeric():
                t.append(int(c))
            else:
                t.append(d[c])
        return t

    with open(file) as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines]

    hands = []
    for line in lines:
        split = line.split()
        hands.append([had_to_list(split[0]), int(split[1])])

    return {"hands": hands}


def get_type(hand):
    res = {}
    for i in set(hand):
        for n in hand:
            if n == i:
                res[i] = res.get(i, 0) + 1
    if 5 in res.values():
        return 7
    elif 4 in res.values():
        return 6
    elif 3 in res.values() and 2 in res.values():
        return 5
    elif 3 in res.values():
        return 4
    elif sum([1 for x in res.values() if x == 2]) == 2:
        return 3
    elif 2 in res.values():
        return 2
    else:
        return 1


def solve1(hands, **kwargs):
    hands_with_type = []
    for hand in hands:
        hands_with_type.append((get_type(hand[0]), hand[0], hand[1]))
    hands_with_type.sort()

    ans = 0
    for i, hand in enumerate(hands_with_type):
        ans += (i + 1) * hand[2]
    return ans


def get_type_j(hand):
    if 1 not in hand:
        return get_type(hand)

    res = {}
    j_num = 0
    for i in set(hand):
        for n in hand:
            if n == 1:
                j_num += 1
            elif n == i:
                res[i] = res.get(i, 0) + 1
    j_num = j_num // len(set(hand))

    if j_num == 5 or max(res.values()) + j_num == 5:
        return 7
    elif max(res.values()) + j_num == 4:
        return 6
    elif sum([1 for x in res.values() if x == 2]) == 2 and j_num == 1:
        return 5
    elif j_num == 2 or (j_num == 1 and 2 in res.values()):
        return 4
    else:
        return 2


def solve2(hands, **kwargs):
    for hand in hands:
        for i, c in enumerate(hand[0]):
            if c == 11:
                hand[0][i] = 1
    hands

    hands_with_type = []
    for hand in hands:
        hands_with_type.append((get_type_j(hand[0]), hand[0], hand[1]))
    hands_with_type.sort()

    ans = 0
    for i, hand in enumerate(hands_with_type):
        ans += (i + 1) * hand[2]
    return ans
