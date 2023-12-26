import time
from collections import defaultdict
import random
from collections import deque


def main(filename: str, partTwo: bool):
    with open(filename) as file:
        lines = [line.rstrip() for line in file]

    wires = defaultdict(set)
    for line in lines:
        source, connections = line.split(": ")
        connections = connections.split(" ")
        for connection in connections:
            # the data only has wire connections in 1 direction, so lets add the links to be bi-directional
            wires[source].add(connection)
            wires[connection].add(source)

    # monte-carlo traversal of the graph to find the most commonly used edges to connect random pairs of nodes
    # the 3 most used edges are likely to be the 3 we need to remove to separate the graph into 2 portions
    edge_use_count = {}
    for _ in range(1000):
        node_start, node_end = random.sample(list(wires.keys()), 2)
        path = get_path(wires, node_start, node_end)
        if path is None:
            continue
        for i in range(len(path) - 1):
            edge = tuple(sorted([path[i], path[i + 1]]))
            edge_use_count[edge] = edge_use_count.get(edge, 0) + 1

    most_used_edges = sorted(edge_use_count.items(), key=lambda x: x[1], reverse=True)
    edges_to_remove = [p[0] for p in most_used_edges[:3]]
    print(f"Removing edges: {edges_to_remove}")

    size_group_1 = get_comp_size(wires, edges_to_remove[0][0], edges_to_remove)
    size_group_2 = get_comp_size(wires, edges_to_remove[0][1], edges_to_remove)

    # if our 2 groups don't combine to be the same size as the original, then our monte carlo didn't work
    print(size_group_1 + size_group_2 == len(wires))
    print(size_group_1 * size_group_2)


def get_comp_size(wires, node, removed_nodes):
    nodes = [node]
    seen = {node}
    while nodes:
        new_nodes = []
        for node in nodes:
            for neighbor in wires[node]:
                if (
                    neighbor in seen
                    or (node, neighbor) in removed_nodes
                    or (neighbor, node) in removed_nodes
                ):
                    continue
                seen.add(neighbor)
                new_nodes.append(neighbor)
        nodes = new_nodes
    return len(seen)


def get_path(wires, node_start, node_end):
    prev = {node_start: node_start}
    nodes = [node_start]
    seen = set(node_start)
    while nodes:
        neighbors = set()
        for node in nodes:
            for neighbor in wires[node]:
                if neighbor in seen:
                    continue
                seen.add(neighbor)
                prev[neighbor] = node
                neighbors.add(neighbor)
        nodes = neighbors

    if prev.get(node_end) is None:
        return None

    path = []
    node = node_end
    while node != node_start:
        path.append(node)
        node = prev[node]
    path.append(node_start)
    return path[::-1]


if __name__ == "__main__":
    filename = "day25/input.txt"
    startTime = time.time()
    main(filename, False)
    print(f"Part One time: {time.time() - startTime:.3f} sec")
    # startTime = time.time()
    # main(filename, True)
    # print(f"Part Two time: {time.time() - startTime:.3f} sec")
