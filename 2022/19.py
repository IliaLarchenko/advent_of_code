import re
from functools import cache


def parse_line(line):
    split = re.split(
        "Blueprint |: Each ore robot costs | ore. Each clay robot costs "
        "| ore. Each obsidian robot costs | ore and "
        "| clay. Each geode robot costs | ore and | obsidian.",
        line,
    )[1:-1]
    data = {
        "num": int(split[0]),
        "ore": int(split[1]),
        "clay": int(split[2]),
        "obsidian": (int(split[3]), int(split[4])),
        "geode": (int(split[5]), int(split[6])),
    }

    return data


def prepare_data(file="input.txt"):
    with open(file) as file:
        lines = [line.strip() for line in file.readlines()]

    blueprints = [parse_line(line) for line in lines]

    data = {"blueprints": blueprints}

    return data


def evaluate_blueprint(num, ore, clay, obsidian, geode, time):

    # robot_nums = (ore, clay, obsidian)
    # resources = (ore, clay, obsidian)

    @cache
    def rec_step(robot_nums, time_left, resources):
        if time_left <= 1:
            return 0

        # idle only if you can't build at least 1 type of robots that needed
        idle = False

        # from some point it does't make sense to build some types of robots
        make_sense = [False, False, False]

        best = 0

        # build a geode robot if it makes sense
        if resources[0] >= geode[0] and resources[2] >= geode[1]:
            make_sense[2] = True
            best = max(
                best,
                rec_step(
                    (robot_nums[0], robot_nums[1], robot_nums[2]),
                    time_left - 1,
                    (
                        resources[0] - geode[0] + robot_nums[0],
                        resources[1] + robot_nums[1],
                        resources[2] - geode[1] + robot_nums[2],
                    ),
                )
                + (time_left - 1),
            )
        elif robot_nums[2] > 0:
            idle = True

        # build an obsidian robot if it makes sense
        if (
            robot_nums[2] < geode[1]  # max useful quanitily is not reached
            and time_left > 3  # there is time to collect and use obsidian
        ):
            make_sense[1] = True
            if resources[0] >= obsidian[0] and resources[1] >= obsidian[1]:
                best = max(
                    best,
                    rec_step(
                        (robot_nums[0], robot_nums[1], robot_nums[2] + 1),
                        time_left - 1,
                        (
                            resources[0] - obsidian[0] + robot_nums[0],
                            resources[1] - obsidian[1] + robot_nums[1],
                            resources[2] + robot_nums[2],
                        ),
                    ),
                )
            elif robot_nums[1] > 0:
                idle = True

        # build a clay robot if it makes sense
        if (
            robot_nums[1] < obsidian[1]  # max useful quanitily is not reached
            and time_left > 5  # there is time to collect and use clay -> obsidian
        ):
            make_sense[0] = True
            if resources[0] >= clay:
                best = max(
                    best,
                    rec_step(
                        (robot_nums[0], robot_nums[1] + 1, robot_nums[2]),
                        time_left - 1,
                        (
                            resources[0] - clay + robot_nums[0],
                            resources[1] + robot_nums[1],
                            resources[2] + robot_nums[2],
                        ),
                    ),
                )
            else:
                idle = True

        # build an ore robot if it makes sense
        if time_left > 3 and robot_nums[0] < max(
            (a * b for a, b in zip(make_sense, [clay, obsidian[0], geode[0]]))
        ):
            if resources[0] >= ore:
                best = max(
                    best,
                    rec_step(
                        (robot_nums[0] + 1, robot_nums[1], robot_nums[2]),
                        time_left - 1,
                        (
                            resources[0] - ore + robot_nums[0],
                            resources[1] + robot_nums[1],
                            resources[2] + robot_nums[2],
                        ),
                    ),
                )
            else:
                idle = True

        # if we have robots that still make sense to build
        # but don't have resources, let's wait
        if idle:
            best = max(
                best,
                rec_step(
                    (robot_nums[0], robot_nums[1], robot_nums[2]),
                    time_left - 1,
                    (
                        resources[0] + robot_nums[0],
                        resources[1] + robot_nums[1],
                        resources[2] + robot_nums[2],
                    ),
                ),
            )

        return best

    return rec_step((1, 0, 0), time, (0, 0, 0))


def solve1(blueprints, **kwargs):
    ans = 0
    for blueprint in blueprints:
        res = evaluate_blueprint(**blueprint, time=24)
        ans += blueprint["num"] * res
    return ans


def solve2(blueprints, **kwargs):
    ans = 1
    for blueprint in blueprints[:3]:
        res = evaluate_blueprint(**blueprint, time=32)
        ans *= res
    return ans
