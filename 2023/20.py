from collections import deque
import math


def prepare_data(file="input.txt"):
    with open(file) as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines]

    return {"lines": lines}


def parseline(line):
    name, connections = line.split(" -> ")
    if name[0] == "b":
        t = "b"
    else:
        t = name[0]
        name = name[1:]
    connections = connections.split(", ")
    return t, name, connections


def get_modules(lines):
    modules = {}
    for line in lines:
        t, name, connections = parseline(line)
        modules[name] = {"type": t, "outs": connections}
        if t == "%":
            modules[name]["status"] = False
        elif t == "&":
            modules[name]["inputs"] = {}  # high = True

    out_modules = {}
    for name, module in modules.items():
        for out in module["outs"]:
            if out not in modules:
                out_modules[out] = {"type": "output", "status": True}
            else:
                if modules[out]["type"] == "&":
                    modules[out]["inputs"][name] = False
    modules.update(out_modules)
    return modules


def press_button(modules, n=None):
    low = 1
    high = 0
    actions = deque([("broadcaster", False, None)])  # target, signal, source

    def send_signals(outs, signal, name):
        nonlocal high, low
        for out in outs:
            actions.append((out, signal, name))
            if signal:
                high += 1
            else:
                low += 1

    while len(actions) > 0:
        name, signal, source = actions.popleft()
        if name == "broadcaster":
            send_signals(modules[name]["outs"], signal, name)
        elif modules[name]["type"] == "%":
            if not signal:
                modules[name]["status"] = not modules[name]["status"]
                send_signals(modules[name]["outs"], modules[name]["status"], name)
        elif modules[name]["type"] == "&":
            modules[name]["inputs"][source] = signal
            if signal and min(modules[name]["inputs"].values()):
                send_signals(modules[name]["outs"], False, name)
            else:
                send_signals(modules[name]["outs"], True, name)
        else:
            modules[name]["status"] = signal

    return low, high


def solve1(lines, **kwargs):
    modules = get_modules(lines)

    high = 0
    low = 0
    for i in range(1000):
        lowi, highi = press_button(modules)
        high += highi
        low += lowi

    return high * low


def press_and_track(modules, check_name=None):
    actions = deque([("broadcaster", False, None)])

    def send_signals(outs, signal, name):
        for out in outs:
            actions.append((out, signal, name))

    while len(actions) > 0:
        name, signal, source = actions.popleft()
        if name == "broadcaster":
            send_signals(modules[name]["outs"], signal, name)
        elif modules[name]["type"] == "%":
            if not signal:
                modules[name]["status"] = not modules[name]["status"]
                send_signals(modules[name]["outs"], modules[name]["status"], name)
        elif modules[name]["type"] == "&":
            modules[name]["inputs"][source] = signal
            if signal and min(modules[name]["inputs"].values()):
                send_signals(modules[name]["outs"], False, name)
            else:
                send_signals(modules[name]["outs"], True, name)
        else:
            modules[name]["status"] = signal
        if name == "lx":
            if modules["lx"]["inputs"][check_name]:
                return True
    else:
        return False


def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)


def solve2(lines, **kwargs):
    # a very non generic solution specific for the input
    cycle_steps = []
    modules = get_modules(lines)
    for name in modules["lx"]["inputs"]:
        modules = get_modules(lines)
        n = 1
        while not press_and_track(modules, name):
            n += 1
        cycle_steps.append(n)

    n = cycle_steps[0]
    for i in range(1, len(cycle_steps)):
        n = lcm(n, cycle_steps[i])

    return n
