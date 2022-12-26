import re


def prepare_data(file="input.txt"):
    # data preparation
    with open(file) as file:
        lines = [line.strip() for line in file.readlines()]

    data = []
    for line in lines:
        nums = re.split("Sensor at x=|, y=|: closest beacon is at x=|, y=", line)[1:]
        data.append([int(n) for n in nums])

    data = {"data": data}
    return data


def get_free_intervals(data, y):
    # get the intervals without a beacon for a given y
    intervals = []
    for sx, sy, bx, by in data:
        dy = abs(y - sy)
        dist = abs(by - sy) + abs(bx - sx)
        if dy <= dist:
            intervals.append([sx - (dist - dy), sx + (dist - dy)])
        intervals.sort()

    if len(intervals) == 0:
        return []

    i = 0
    ans = [intervals[0]]
    for i in range(1, len(intervals)):
        if ans[-1][1] >= intervals[i][0] - 1:
            ans[-1][1] = max(ans[-1][1], intervals[i][1])
        else:
            ans.append(intervals[i])
        i += 1
    return ans


def solve1(data, y=2000000):
    ans = 0
    intervals = get_free_intervals(data, y)
    for interval in intervals:
        ans += interval[1] - interval[0] + 1
    occupied = set()
    for sx, sy, bx, by in data:
        if sy == y:
            occupied.add((y, sx))
        elif by == y:
            occupied.add((y, bx))

    return ans - len(occupied)


def solve2(data, limit=4000000):
    for y in range(0, limit + 1):
        intervals = get_free_intervals(data, y)

        if len(intervals) > 1 or intervals[0][0] > 0 or intervals[0][1] < limit:
            return y + (intervals[0][1] + 1) * 4000000

    return None
