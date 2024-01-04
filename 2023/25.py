import graphviz
import random


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


def get_node_dict(lines, ignore_edges=None):
    nodes_dict = {}
    for line in lines:
        node1, nodes = line.split(": ")
        for node2 in nodes.split(" "):
            if ignore_edges is None or node1 + node2 not in ignore_edges:
                nodes_dict[node1] = nodes_dict.get(node1, set())
                nodes_dict[node1].add(node2)

                nodes_dict[node2] = nodes_dict.get(node2, set())
                nodes_dict[node2].add(node1)
    return nodes_dict


def count_nodes(nodes_dict, start):
    visited = set()
    to_visit = set([start])
    while len(to_visit) > 0:
        next_node = to_visit.pop()
        visited.add(next_node)
        for node in nodes_dict[next_node]:
            if node not in visited:
                to_visit.add(node)

    return len(visited)


def solve1(lines, remove_edges=["lrdqpg", "xsltpb", "zlvbmx"], **kwargs):
    # I just found the edges to remove using graphviz
    # This solution is not universal
    # Below is the function that finds the edges to remove automatically
    nodes_dict = get_node_dict(lines, remove_edges)
    start = lines[0].split(": ")[0]
    num_nodes = count_nodes(nodes_dict, start)

    return num_nodes * (len(nodes_dict) - num_nodes)


def get_3_nodes_to_remove(nodes_dict):
    candidates = None

    while candidates is None or len(candidates) > 6:
        start = random.choice(list(nodes_dict.keys()))
        end = random.choice(list(nodes_dict.keys()))

        restrictions = set()
        n_path = 0
        for _ in range(4):
            backtracking = {start: None}
            current_steps = [start]
            while len(current_steps) > 0:
                node = current_steps.pop(0)
                if node == end:
                    while backtracking[node]:
                        restrictions.add(node + backtracking[node])
                        restrictions.add(backtracking[node] + node)
                        node = backtracking[node]
                    n_path += 1
                    break

                for next_node in nodes_dict[node]:
                    if (
                        next_node not in backtracking
                        and node + next_node not in restrictions
                    ):
                        backtracking[next_node] = node
                        current_steps.append(next_node)

        if n_path == 3:
            if candidates is None:
                candidates = restrictions
            else:
                candidates = candidates.intersection(restrictions)

    return candidates


def solve1_auto(lines, **kwargs):
    # The proper solution
    nodes_dict = get_node_dict(lines)
    remove_edges = get_3_nodes_to_remove(get_node_dict(lines))
    for edge in remove_edges:
        nodes_dict[edge[:3]].remove(edge[3:])
    start = lines[0].split(": ")[0]

    num_nodes = count_nodes(nodes_dict, start)

    return num_nodes * (len(nodes_dict) - num_nodes)
