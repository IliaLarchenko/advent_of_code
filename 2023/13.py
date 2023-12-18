def prepare_data(file="input.txt"):
    with open(file) as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines]
    notes = [[]]
    for line in lines:
        if len(line) == 0:
            notes.append([])
        else:
            notes[-1].append(list(line))

    return {"notes": notes}


def compare_lists(l1, l2):
    for i in range(min(len(l1), len(l2))):
        if l1[i] != l2[i]:
            return False
    return True


def find_mirror(h_line, ignore=None):
    for i in range(1, len(h_line)):
        if compare_lists(h_line[:i][::-1], h_line[i:]) and i != ignore:
            return i
    return 0


def solve1(notes, **kwargs):
    n = 0
    for note in notes:
        h_line_vert = [hash("".join(x)) for x in note]
        n += find_mirror(h_line_vert) * 100

        h_line_hor = [
            hash("".join([note[i][j] for i in range(len(note))]))
            for j in range(len(note[0]))
        ]
        n += find_mirror(h_line_hor)
    return n


def solve2(notes, **kwargs):
    n = 0
    for note in notes:
        h_line_vert = [hash("".join(x)) for x in note]
        h_line_hor = [
            hash("".join([note[i][j] for i in range(len(note))]))
            for j in range(len(note[0]))
        ]
        vert = find_mirror(h_line_vert)
        hor = find_mirror(h_line_hor)

        ans = []
        for i in range(len(note)):
            for j in range(len(note[0])):
                if note[i][j] == ".":
                    note[i][j] = "#"
                else:
                    note[i][j] = "."

                h_line_vert = [hash("".join(x)) for x in note]
                h_line_hor = [
                    hash("".join([note[i][j] for i in range(len(note))]))
                    for j in range(len(note[0]))
                ]
                vert1 = find_mirror(h_line_vert, vert)
                hor1 = find_mirror(h_line_hor, hor)

                if vert != vert1 and vert1 != 0:
                    n += vert1 * 100
                    ans.append(("v", i, j, vert1, vert))
                if hor1 != hor and hor1 != 0:
                    n += hor1
                    ans.append(("h", i, j, hor1, hor))

                if note[i][j] == ".":
                    note[i][j] = "#"
                else:
                    note[i][j] = "."

    return n // 2
