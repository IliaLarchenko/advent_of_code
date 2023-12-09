def prepare_data(file="input.txt"):
    with open(file) as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines]

    nums_all = []
    for line in lines:
        line.split()[1:]
        nums_all.append([int(x) for x in line.split()])

    return {"nums_all": nums_all}


def get_diff(nums):
    diff = []
    for i in range(1, len(nums)):
        diff.append(nums[i] - nums[i - 1])
    return diff


def next_num(nums):
    if min(nums) == 0 and max(nums) == 0:
        return 0
    else:
        nums_2 = get_diff(nums)
        next_diff = next_num(nums_2)
        return nums[-1] + next_diff


def solve1(nums_all, **kwargs):
    ans = 0
    for nums in nums_all:
        ans += next_num(nums)
    return ans


def solve2(nums_all, **kwargs):
    ans = 0
    for nums in nums_all:
        ans += next_num(nums[::-1])
    return ans
