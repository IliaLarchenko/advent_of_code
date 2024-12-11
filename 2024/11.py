from functools import cache


def prepare_data(file="input.txt"):
    with open(file) as f:
        line = f.readline().strip()
    stones = [x for x in line.split()]
    return {"stones": stones}


@cache
def count_stones(stone, blinks):
    if blinks == 0:
        return 1
    if stone == "0":
        return count_stones("1", blinks - 1)
    elif len(stone) % 2 == 0:
        mid = len(stone) // 2
        return count_stones(stone[:mid], blinks - 1) + count_stones(str(int(stone[mid:])), blinks - 1)
    else:
        return count_stones(str(int(stone) * 2024), blinks - 1)


def solve1(stones, **kwargs):
    return sum([count_stones(stone, 25) for stone in stones])


def solve2(stones, **kwargs):
    return sum([count_stones(stone, 75) for stone in stones])
