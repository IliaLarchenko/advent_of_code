def prepare_data(file="input.txt"):
    with open(file) as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines]

    instruction = lines[0]
    nodes = {l[:3]: (l[7:10], l[12:15]) for l in lines[2:]}

    return {"instruction": instruction, "nodes": nodes}


def solve1(instruction, nodes, **kwargs):
    i = 0
    node = "AAA"
    while True:
        s = instruction[i % len(instruction)]
        i += 1
        if s == "R":
            node = nodes[node][1]
        else:
            node = nodes[node][0]
        if node == "ZZZ":
            return i


def solve2(instruction, nodes, **kwargs):
    # preprocessing to work with cycles
    all_ends = {}
    for k in nodes.keys():
        all_ends[k] = [set(), None]
        node = k
        for i in range(len(instruction) * len(nodes)):
            s = instruction[i % len(instruction)]
            # for i,s in enumerate(instruction):
            if node[-1] == "Z":
                all_ends[k][0].add(i)
            if s == "R":
                node = nodes[node][1]
            else:
                node = nodes[node][0]
        if node[-1] == "Z":
            all_ends[k][0].add(i + 1)
        all_ends[k][1] = node

    # solution, quite a bruteforce but works good enough
    current_nodes = []
    for node in nodes.keys():
        if node[-1] == "A":
            current_nodes.append(node)
    current_nodes

    n = 0
    while True:
        ends = all_ends[current_nodes[0]][0]
        for node in current_nodes[1:]:
            ends = ends.intersection(all_ends[node][0])
            if len(ends) == 0:
                break
        if len(ends) > 0:
            return min(ends) + len(instruction) * len(nodes) * n
            break
        for j in range(len(current_nodes)):
            current_nodes[j] = all_ends[current_nodes[j]][1]
        n += 1
