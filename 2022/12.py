def prepare_data(file="input.txt"):
    # data preparation

    with open(file) as file:
        lines = [line.strip() for line in file.readlines()]

    matrix = [[None] * len(lines[0]) for _ in range(len(lines))]
    start2 = []
    for i in range(len(lines)):
        for j in range(len(lines[0])):
            if lines[i][j] == "S":
                start1 = [(i, j)]
                start2.append((i, j))
                matrix[i][j] = 0
            elif lines[i][j] == "E":
                end = [(i, j)]
                matrix[i][j] = ord("z") - ord("a")
            else:
                matrix[i][j] = ord(lines[i][j]) - ord("a")
                if matrix[i][j] == 0:
                    start2.append((i, j))

    data = {"matrix": matrix, "start1": start1, "start2": start2, "end": end}
    return data


def get_adj(i, j, size):
    for i1, j1 in [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]:
        if 0 <= i1 < size[0] and 0 <= j1 < size[1]:
            yield (i1, j1)


def search(start, end, matrix):
    steps = 0

    visited_end = {e for e in end}
    queue_end = {e for e in end}

    visited_start = {s for s in start}
    queue_start = {s for s in start}

    while len(queue_end) > 0 and len(queue_start) > 0:

        # will still work if you remove this block
        new_queue_start = set()
        while len(queue_start) > 0:
            i, j = queue_start.pop()
            for i1, j1 in get_adj(i, j, (len(matrix), len(matrix[0]))):
                if matrix[i1][j1] - matrix[i][j] <= 1 and (i1, j1) not in visited_start:
                    if (i1, j1) in visited_end:
                        return steps + 1
                    new_queue_start.add((i1, j1))
                    visited_start.add((i1, j1))
        steps += 1
        queue_start = new_queue_start

        # will still work if you remove this block
        new_queue_end = set()
        while len(queue_end) > 0:
            i, j = queue_end.pop()
            for i1, j1 in get_adj(i, j, (len(matrix), len(matrix[0]))):
                if matrix[i1][j1] - matrix[i][j] >= -1 and (i1, j1) not in visited_end:
                    if (i1, j1) in visited_start:
                        return steps + 1
                    new_queue_end.add((i1, j1))
                    visited_end.add((i1, j1))
        steps += 1
        queue_end = new_queue_end

    return None


def solve1(start1, end, matrix, **kwargs):
    return search(start1, end, matrix)


def solve2(start2, end, matrix, **kwargs):
    return search(start2, end, matrix)
