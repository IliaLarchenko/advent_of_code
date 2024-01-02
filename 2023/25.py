import graphviz


def prepare_data(file="input.txt"):
    with open(file) as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines]

    return {"lines": lines}


def show_graph(lines):
    # I used this function to play with the graph
    # You can add some determenistic or random filters and found
    # the edges to remove in a few iterations
    dot = graphviz.Digraph()
    for line in lines:
        node1, nodes = line.split(": ")
        dot.node(node1)
        for node2 in nodes.split(" "):
            dot.node(node2)
            dot.edge(node1, node2, node1 + node2, constraint="true")

    dot.render("graph", format="png", view=True)


def solve1(lines, remove_edges=["lrdqpg", "xsltpb", "zlvbmx"], **kwargs):
    # I just found the edges to remove using graphviz
    # This solution is not universal
    nodes_dict = {}
    for line in lines:
        node1, nodes = line.split(": ")
        for node2 in nodes.split(" "):
            if node1 + node2 not in remove_edges:
                nodes_dict[node1] = nodes_dict.get(node1, set())
                nodes_dict[node1].add(node2)

                nodes_dict[node2] = nodes_dict.get(node2, set())
                nodes_dict[node2].add(node1)
    start = node1

    visited = set()
    to_visit = set([start])
    while len(to_visit) > 0:
        next_node = to_visit.pop()
        visited.add(next_node)
        for node in nodes_dict[next_node]:
            if node not in visited:
                to_visit.add(node)

    return len(visited) * (len(nodes_dict) - len(visited))
