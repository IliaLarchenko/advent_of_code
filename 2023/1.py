def prepare_data(file="input.txt"):
    with open(file) as file:
        lines = [line.strip() for line in file.readlines()]

    return {"lines": lines}

def get_num(line):
    n = []
    for c in line:
        if c.isnumeric():
            n.append(c)
            
    return int(n[0])*10 + int(n[-1])

def solve1(lines, **kwargs):
    return sum([get_num(line) for line in lines])

def get_num2(line, d):
    nums = []
    for i,c in enumerate(line):
        if c.isnumeric():
            nums.append(int(c))
        else:
            for k,v in d.items():
                if line[i: i + len(k)] == k:
                    nums.append(v)
                continue
    return int(nums[0])*10 + int(nums[-1])

def solve2(lines, **kwargs):
    d = {
        "one":1, 
        "two":2, 
        "three":3, 
        "four":4, 
        "five":5, 
        "six":6, 
        "seven":7, 
        "eight":8, 
        "nine": 9
    }
    return sum([get_num2(line, d) for line in lines])
