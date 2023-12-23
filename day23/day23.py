import time
import sys
from collections import deque

sys.setrecursionlimit(10**6)


def main(filename: str, part_two: bool):
    with open(filename) as file:
        lines = [line.rstrip() for line in file]
    num_rows = len(lines)
    num_cols = len(lines[num_rows - 1])
    start = (0, 1)
    end = (len(lines) - 1, len(lines[len(lines) - 1]) - 2)
    nodes = [start]
    for i, line in enumerate(lines):
        for j, sym in enumerate(line):
            num_choices = 0
            for drow, dcol in [
                (-1, 0),
                (1, 0),
                (0, 1),
                (0, -1),
            ]:
                choice_row = i + drow
                choice_col = j + dcol
                if (
                    0 <= choice_row < num_rows
                    and 0 <= choice_col < num_cols
                    and lines[choice_row][choice_col] != "#"
                ):
                    num_choices += 1
            if num_choices > 2 and lines[i][j] != "#":
                nodes.append((i, j))
    nodes.append(end)

    edges = {}
    for node_row, node_col in nodes:
        edges[(node_row, node_col)] = []
        queue = deque([(node_row, node_col, 0)])
        visited = set()
        while queue:
            row, col, distance = queue.popleft()
            if (row, col) in visited:
                continue
            visited.add((row, col))
            if (row, col) in nodes and (row, col) != (node_row, node_col):
                edges[(node_row, node_col)].append(((row, col), distance))
                continue
            for sym, drow, dcol in [
                ("^", -1, 0),
                ("v", 1, 0),
                (">", 0, 1),
                ("<", 0, -1),
            ]:
                if (
                    0 <= row + drow < num_rows
                    and 0 <= col + dcol < num_cols
                    and lines[row + drow][col + dcol] != "#"
                ):
                    if (
                        not part_two
                        and lines[row][col] in ["<", ">", "^", "v"]
                        and lines[row][col] != sym
                    ):
                        continue
                    queue.append((row + drow, col + dcol, distance + 1))

    count = 0
    max_distance = 0
    visited = [[False for _ in range(num_cols)] for _ in range(num_rows)]

    def dfs(node, distance):
        nonlocal count
        nonlocal max_distance
        count += 1
        row, col = node
        if visited[row][col]:
            return
        visited[row][col] = True
        if row == num_rows - 1:
            max_distance = max(max_distance, distance)
        for next_node, dist_to_next in edges[node]:
            dfs(next_node, distance + dist_to_next)
        visited[row][col] = False

    dfs(start, 0)

    if part_two:
        print(f"Part Two: {max_distance}")
    else:
        print(f"Part One: {max_distance}")


if __name__ == "__main__":
    filename = "day23/input.txt"
    startTime = time.time()
    main(filename, False)
    print(f"Part One time: {time.time() - startTime:.3f} sec")
    startTime = time.time()
    main(filename, True)
    print(f"Part Two time: {time.time() - startTime:.3f} sec")
