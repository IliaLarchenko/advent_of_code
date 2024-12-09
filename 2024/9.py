def prepare_data(file="input.txt"):
    with open(file) as f:
        raw = f.readline().strip()
    raw = [int(i) for i in raw]

    disk = []
    files = []
    empty = []

    file_id = 0
    pos = 0
    is_file = True
    
    for i in range(len(raw)):
        if is_file:
            disk.append((file_id, raw[i], pos))  # id, len, pos
            files.append((file_id, raw[i], pos))  # id, len, pos
            file_id += 1
        else:
            disk.append((-1, raw[i], pos))  # id = -1 for empty space
            empty.append((raw[i], pos))  # len, pos

        pos += raw[i]
        is_file = not is_file

    return {"disk": disk, "files": files, "empty": empty}


def get_checksum(file_id, mem, pos):
    return file_id * ((pos + pos + mem - 1) * mem // 2)


def solve1(disk, **kwargs):
    i = 0
    j = len(disk) - 1

    ans = 0

    empty_memory = 0
    file_memory = 0

    while j > i:
        if empty_memory == 0:
            if disk[i][0] != -1:
                ans += get_checksum(*disk[i])
                i += 1
                continue
            else:
                _, empty_memory, empty_pos = disk[i]

        if file_memory == 0:
            if disk[j][0] == -1:
                j -= 1
                continue
            else:
                file_id, file_memory, file_pos = disk[j]

        to_move = min(file_memory, empty_memory)
        ans += get_checksum(file_id, to_move, empty_pos)

        empty_memory -= to_move
        file_memory -= to_move
        empty_pos += to_move

        if empty_memory == 0:
            i += 1
        if file_memory == 0:
            j -= 1

    ans += get_checksum(file_id, file_memory, file_pos)

    return ans


def solve2(files, empty, **kwargs):
    ans = 0
    empty = empty.copy()

    for j in range(len(files) - 1, -1, -1):
        file_id, file_memory, file_pos = files[j]

        for i in range(len(empty) + 1):
            if i == len(empty) or empty[i][1] > file_pos:
                ans += get_checksum(file_id, file_memory, file_pos)
                break

            empty_memory, empty_pos = empty[i]

            if file_memory <= empty_memory:
                ans += get_checksum(file_id, file_memory, empty_pos)
                empty[i] = (empty_memory - file_memory, empty_pos + file_memory)
                break

        j -= 1

        # Not necessary but speeds the process up a lot
        # Useful when you use list instead of proper data structure with O(1) element removal
        if j % 200 == 0:
            empty = [el for el in empty if el[0] > 0]

    return ans
