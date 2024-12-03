def prepare_data(file="input.txt"):
    with open(file) as f:
        lines = f.readlines()
    memory = "\n".join(lines)

    return {"memory": memory}


def solve1(memory, **kwargs):
    ans = 0
    for i in range(len(memory) - 3):
        if memory[i : i + 4] == "mul(":
            for j in range(i + 4, len(memory)):
                if memory[j] == ")":
                    nums = memory[i + 4 : j].split(",")
                    if len(nums) == 2 and nums[0].isnumeric() and nums[1].isnumeric():
                        ans += int(nums[0]) * int(nums[1])
                    break

    return ans


def solve2(memory, **kwargs):
    ans = 0
    do = True
    for i in range(len(memory) - 3):
        if memory[i : i + 4] == "do()":
            do = True
        elif memory[i : i + 7] == "don't()":
            do = False
        elif do and memory[i : i + 4] == "mul(":
            for j in range(i + 4, len(memory)):
                if memory[j] == ")":
                    nums = memory[i + 4 : j].split(",")
                    if len(nums) == 2 and nums[0].isnumeric() and nums[1].isnumeric():
                        ans += int(nums[0]) * int(nums[1])
                    break

    return ans
