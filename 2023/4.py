def prepare_data(file="input.txt"):
    with open(file) as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines]

    cards = []
    for line in lines:
        numbers = line.split(":")[1]
        w_numbers, y_numbers = numbers.split("|")
        w_numbers, y_numbers = w_numbers.strip(), y_numbers.strip()
        w_numbers, y_numbers = w_numbers.split(), y_numbers.split()
        cards.append((set(w_numbers), set(y_numbers)))

    return {"cards": cards}


def solve1(cards, **kwargs):
    ans = 0
    for card in cards:
        p = 0
        w_numbers, y_numbers = card
        for n in w_numbers:
            if n in y_numbers:
                p += 1
        if p > 0:
            ans += 2 ** (p - 1)
    return ans


def solve2(cards, **kwargs):
    nums = [1] * len(cards)

    for i, card in enumerate(cards):
        p = 0
        w_numbers, y_numbers = card
        for n in w_numbers:
            if n in y_numbers:
                p += 1
        for j in range(p):
            nums[i + j + 1] += nums[i]

    return sum(nums)
