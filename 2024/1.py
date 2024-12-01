def prepare_data(file="input.txt"):
    with open(file) as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines]
    la, lb = [], []
    for l in lines:
        a,b = l.split('   ')
        la.append(int(a))
        lb.append(int(b))

    return {"la": la, "lb": lb}


def solve1(la, lb, **kwargs):
    la.sort()
    lb.sort()

    ans = 0
    for i in range(len(la)):
        ans += abs(la[i] - lb[i])

    return ans


def solve2(la, lb, **kwargs):
    ans = 0
    db = {}

    for b in lb:
        db[b] = db.get(b, 0) + 1

    for a in la:
        ans += a * db.get(a, 0)

    return ans