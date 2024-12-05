def prepare_data(file="input.txt"):
    with open(file) as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]

    rules = {}
    for i, line in enumerate(lines):
        if line == "":
            break
        a, b = line.split("|")
        a = int(a)
        b = int(b)

        rules[b] = rules.get(b, []) + [a]

    nums = []
    for j in range(i + 1, len(lines)):
        nums.append(lines[j].split(","))
        nums[-1] = [int(n) for n in nums[-1]]

    return {"rules": rules, "nums": nums}


def check_line(line, rules):
    line_set = set(line)
    seen = set()

    for i, n in enumerate(line):
        seen.add(n)
        for k in rules.get(n, []):
            if k not in seen and k in line_set:
                return False
    return True


def solve1(rules, nums, **kwargs):
    ans = 0
    for line in nums:
        if check_line(line, rules):
            ans += line[len(line) // 2]

    return ans


def fix_line_once(line, rules):
    line_set = set(line)
    seen = set()

    for i, n in enumerate(line):
        seen.add(n)
        for k in rules.get(n, []):
            if k not in seen and k in line_set:
                ki = line.index(k)
                line[ki], line[i] = line[i], line[ki]
                return line, False

    return line, True


def solve2(rules, nums, **kwargs):
    ans = 0
    for line in nums:
        correct = check_line(line, rules)
        if correct:
            continue
        while not correct:
            line, correct = fix_line_once(line, rules)

        ans += line[len(line) // 2]
    return ans
