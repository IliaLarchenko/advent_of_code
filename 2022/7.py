class Dir:
    def __init__(self, name, prefix="", parent=None):
        self.name = name
        self.full_name = prefix + name
        self.size = None
        self.files = {}
        self.dirs = {}
        self.parent = parent


def fill_dirs(lines):
    root = Dir("/", "")
    current_dir = root
    i = 0
    while i < len(lines):
        if lines[i][0] == "$":
            if lines[i] == "$ ls":
                i += 1
                while i < len(lines) and lines[i][0] != "$":
                    if lines[i][0] == "d":
                        name = lines[i][4:]
                        if name not in current_dir.dirs:
                            current_dir.dirs[name] = Dir(
                                name + "/", current_dir.full_name, current_dir
                            )
                    else:
                        size, name = tuple(lines[i].split(" "))
                        current_dir.files[name] = int(size)
                    i += 1
                i -= 1
            else:
                arg = lines[i].split(" ")[-1]
                if arg == "/":
                    current_dir = root
                elif arg == "..":
                    if current_dir.parent:
                        current_dir = current_dir.parent
                else:
                    if arg not in current_dir.dirs:
                        current_dir.dirs[arg] = Dir(
                            arg + "/", current_dir.full_name, current_dir
                        )
                    current_dir = current_dir.dirs[arg]

        i += 1
    return root


def prepare_data(file="input.txt"):
    with open(file) as file:
        lines = [line.strip() for line in file.readlines()]

    root = fill_dirs(lines)

    data = {"root": root}
    return data


def get_dir_size(d, memo):
    d.size = 0
    for f in d.files:
        d.size += d.files[f]
    for sd in d.dirs:
        d.size += get_dir_size(d.dirs[sd], memo)
    memo[d.full_name] = d.size
    return d.size


def solve1(root, **kwargs):
    memo = {}
    get_dir_size(root, memo)

    ans = 0
    for _, s in memo.items():
        if s < 100000:
            ans += s

    return ans


def solve2(root, **kwargs):
    memo = {}
    get_dir_size(root, memo)

    to_free = 30000000 - (70000000 - memo["/"])
    ans = 70000000
    for m, s in memo.items():
        if s >= to_free and s < ans:
            ans = s

    return ans
