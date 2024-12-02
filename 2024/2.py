def prepare_data(file="input.txt"):
    with open(file) as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines]
    reports = []

    for line in lines:
        reports.append([int(i) for i in line.split()])

    return {"reports": reports}


def check_order(nums, asc=True):
    for i in range(len(nums) - 1):
        if asc and nums[i] > nums[i + 1]:
            return False
        elif not asc and nums[i] < nums[i + 1]:
            return False
    return True


def check_diff(nums):
    for i in range(len(nums) - 1):
        if abs(nums[i] - nums[i + 1]) < 1 or abs(nums[i] - nums[i + 1]) > 3:
            return False
    return True


def check_valid(nums):
    return (check_order(nums, True) or check_order(nums, False)) and check_diff(nums)


def solve1(reports, **kwargs):
    return sum([1 for report in reports if check_valid(report)])


def check_valid_drop_one(nums):
    if check_valid(nums):
        return True
    for i in range(len(nums)):
        if check_valid(nums[:i] + nums[i + 1 :]):
            return True
    return False


def solve2(reports, **kwargs):
    return sum([1 for report in reports if check_valid_drop_one(report)])
