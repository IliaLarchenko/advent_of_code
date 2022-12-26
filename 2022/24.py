from collections import deque


def prepare_data(file="input.txt"):
    with open(file) as f:
        lines = [line.strip() for line in f.readlines()]

    data = {"lines": lines}

    return data


class Map:
    def __init__(self, lines):
        self.blizards_dirs = []
        blizards_pos = []
        self.start = None
        self.end = None

        for i in range(len(lines)):
            for j in range(len(lines[0])):
                if lines[i][j] == ">":
                    self.blizards_dirs.append((0, 1))
                    blizards_pos.append((i - 1, j - 1))
                elif lines[i][j] == "<":
                    self.blizards_dirs.append((0, -1))
                    blizards_pos.append((i - 1, j - 1))
                elif lines[i][j] == "v":
                    self.blizards_dirs.append((1, 0))
                    blizards_pos.append((i - 1, j - 1))
                elif lines[i][j] == "^":
                    self.blizards_dirs.append((-1, 0))
                    blizards_pos.append((i - 1, j - 1))
                elif lines[i][j] == "." and i == 0:
                    self.start = (i - 1, j - 1)
                elif lines[i][j] == "." and i == len(lines) - 1:
                    self.end = (i - 1, j - 1)

        self.height = len(lines) - 2
        self.width = len(lines[0]) - 2
        self.maps = [(tuple(blizards_pos), set(blizards_pos))]

    def get_blizards(self, t):
        t = t % (self.height * self.width)
        if t >= len(self.maps):
            bliz_map = []
            last_bliz, _ = self.get_blizards(t - 1)
            for i, bliz_pos in enumerate(last_bliz):
                bliz_map.append(
                    (
                        (bliz_pos[0] + self.blizards_dirs[i][0]) % self.height,
                        (bliz_pos[1] + self.blizards_dirs[i][1]) % self.width,
                    )
                )
            self.maps.append((tuple(bliz_map), set(bliz_map)))
        return self.maps[t]


def get_path(start, end, t, game_map):
    if start[0] > end[0]:
        direction = -1
    else:
        direction = 1

    queue = deque([(start, t, None)])
    cache = {}

    while len(queue) > 0:
        pos, t, prev_pos = queue.popleft()
        if (pos, t % (game_map.height * game_map.width)) in cache:
            continue
        cache[(pos, t % (game_map.height * game_map.width))] = prev_pos
        _, blizards = game_map.get_blizards(t)
        if pos not in blizards:
            if (pos[0] + direction, pos[1]) == end:
                ans = t + 1
                break

            if pos[0] - 1 >= 0:
                queue.append(((pos[0] - 1, pos[1]), t + 1, pos))
            if pos[0] + 1 < game_map.height:
                queue.append(((pos[0] + 1, pos[1]), t + 1, pos))
            if pos[1] + 1 < game_map.width and game_map.height > pos[0] >= 0:
                queue.append(((pos[0], pos[1] + 1), t + 1, pos))
            if pos[1] - 1 >= 0 and game_map.height > pos[0] >= 0:
                queue.append(((pos[0], pos[1] - 1), t + 1, pos))
            queue.append(((pos[0], pos[1]), t + 1, pos))
    return ans


def solve1(lines, **kwargs):
    game_map = Map(lines)
    return get_path(game_map.start, game_map.end, 0, game_map)


def solve2(lines, **kwargs):
    game_map = Map(lines)
    t1 = get_path(game_map.start, game_map.end, 0, game_map)
    t2 = get_path(game_map.end, game_map.start, t1, game_map)
    t3 = get_path(game_map.start, game_map.end, t2, game_map)
    return t3
