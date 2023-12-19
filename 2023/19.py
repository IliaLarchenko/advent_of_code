def part_to_dict(part):
    return {x.split("=")[0]: int(x.split("=")[1]) for x in part[1:-1].split(",")}


def wf_to_dict(wf):
    wfo = {}
    name = wf.split("{")[0]
    ops = wf[:-1].split("{")[1].split(",")

    wfo["ops"] = []

    for op in ops[:-1]:
        check, redirect = op.split(":")
        wfo["ops"].append(
            {
                "var": check[0],
                "sign": check[1] == ">",
                "num": int(check[2:]),
                "redirect": redirect,
            }
        )

    wfo["else"] = ops[-1]

    return name, wfo


def prepare_data(file="input.txt"):
    with open(file) as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines]

    wfs = []
    parts = []
    i = 0
    while len(lines[i]) > 0:
        wfs.append(lines[i])
        i += 1
    i += 1
    while i < len(lines):
        parts.append(lines[i])
        i += 1

    parts_list = [part_to_dict(part) for part in parts]

    wfs_dict = {}
    for wf in wfs:
        name, wfo = wf_to_dict(wf)
        wfs_dict[name] = wfo

    return {"parts_list": parts_list, "wfs_dict": wfs_dict}


def evaluate(part, wf_name, wfs_dict):
    wf = wfs_dict[wf_name]
    res = None

    for op in wf["ops"]:
        if (op["sign"] and part[op["var"]] > op["num"]) or (
            not op["sign"] and part[op["var"]] < op["num"]
        ):
            res = op["redirect"]
            break
    if res is None:
        res = wf["else"]
    if res in "AR":
        return res
    else:
        return evaluate(part, res, wfs_dict)


def solve1(parts_list, wfs_dict, **kwargs):
    ans = 0
    for part in parts_list:
        if evaluate(part, "in", wfs_dict) == "A":
            ans += sum([v for v in part.values()])
    return ans


def evaluate_range(part, wf_name, wfs_dict):
    wf = wfs_dict[wf_name]
    res = None
    for op in wf["ops"]:
        if (op["sign"] and part[op["var"]][0] > op["num"]) or (
            not op["sign"] and part[op["var"]][1] < op["num"]
        ):
            res = op["redirect"]
            break
        elif (op["sign"] and part[op["var"]][1] <= op["num"]) or (
            not op["sign"] and part[op["var"]][0] >= op["num"]
        ):
            pass
        else:
            if op["sign"]:
                part_left = {k: v for k, v in part.items()}
                part_left[op["var"]] = (part[op["var"]][0], op["num"])
                part_right = {k: v for k, v in part.items()}
                part_right[op["var"]] = (op["num"] + 1, part[op["var"]][1])
            else:
                part_left = {k: v for k, v in part.items()}
                part_left[op["var"]] = (part[op["var"]][0], op["num"] - 1)
                part_right = {k: v for k, v in part.items()}
                part_right[op["var"]] = (op["num"], part[op["var"]][1])
            return evaluate_range(part_left, wf_name, wfs_dict) + evaluate_range(
                part_right, wf_name, wfs_dict
            )

    if res is None:
        res = wf["else"]

    if res == "A":
        return (
            (part["x"][1] - part["x"][0] + 1)
            * (part["m"][1] - part["m"][0] + 1)
            * (part["a"][1] - part["a"][0] + 1)
            * (part["s"][1] - part["s"][0] + 1)
        )
    elif res == "R":
        return 0
    else:
        return evaluate_range(part, res, wfs_dict)


def solve2(wfs_dict, **kwargs):
    return evaluate_range(
        {"x": (1, 4000), "m": (1, 4000), "a": (1, 4000), "s": (1, 4000)}, "in", wfs_dict
    )
