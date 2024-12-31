def prepare_data(file="input.txt"):
    with open(file) as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]

    connections = {}
    for line in lines:
        a, b = line.split("-")
        connections[a] = connections.get(a, set())
        connections[a].add(b)
        connections[b] = connections.get(b, set())
        connections[b].add(a)

    return {"connections": connections}


def solve1(connections, **kwargs):
    sets = set()
    for k in connections.keys():
        if k[0] == "t":
            connected = list(connections[k])
            for i, c1 in enumerate(connected):
                for c2 in connected[i + 1 :]:
                    if c1 in connections[c2]:
                        sets.add(tuple(sorted([k, c1, c2])))
    return len(sets)


def solve2(connections, **kwargs):
    biggest_cluster = []
    checked = set()

    for k in connections.keys():
        if len(connections[k]) + 1 < len(biggest_cluster):
            checked.add(k)
            continue
        valid_connections = [
            c for c in connections[k] if c not in checked and len(connections[c]) + 1 > len(biggest_cluster)
        ]
        clusters = set([tuple([c]) for c in valid_connections])

        while len(clusters) > 0:
            new_clusters = set()
            for cluster in clusters:
                for c in valid_connections:
                    if c not in cluster and set(cluster).issubset(connections[c]):
                        new_cluster = tuple(sorted(list((*cluster, c))))
                        new_clusters.add(new_cluster)
            clusters = new_clusters
            if len(clusters) == 0:
                break

        if len(new_cluster) > len(biggest_cluster) - 1:
            biggest_cluster = list((*new_cluster, k))
        checked.add(k)

    return ",".join(sorted(biggest_cluster))
