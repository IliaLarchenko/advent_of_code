def prepare_data(file="input.txt"):
    with open(file) as file:
        lines = [line.strip() for line in file.readlines()]
    games = []
    for line in lines:
        _, resutls = line.split(":")
        results = resutls.split(";")
        turn = []
        for result in results:
            raw_result = result.split()
            final_results = {"red": 0, "green": 0, "blue": 0}
            for i in range(len(raw_result) // 2):
                key = raw_result[2 * i + 1]
                if key[-1] == ",":
                    key = key[:-1]
                final_results[key] = int(raw_result[2 * i])
            turn.append(final_results)
        games.append(turn)

    return {"games": games}


def solve1(games, **kwargs):
    possible = {"red": 12, "green": 13, "blue": 14}

    ans = []
    for i, game in enumerate(games):
        is_possible = True
        for turn in game:
            for c in ["red", "green", "blue"]:
                if turn[c] > possible[c]:
                    is_possible = False
        if is_possible:
            ans.append(i + 1)
    return sum(ans)


def solve2(games, **kwargs):
    ans = []
    for i, game in enumerate(games):
        min_possible = {"red": 0, "green": 0, "blue": 0}
        for turn in game:
            for c in ["red", "green", "blue"]:
                min_possible[c] = max(min_possible[c], turn[c])
        n = 1
        for k, v in min_possible.items():
            n *= v
        ans.append(n)
    return sum(ans)
