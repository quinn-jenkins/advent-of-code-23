import time
from collections import deque

move_set = ((1, 0), (-1, 0), (0, 1), (0, -1))

num_steps = 64


def main(filename: str, partTwo: bool):
    with open(filename) as file:
        lines = [line.rstrip() for line in file]
        start = find_start(lines)

        tiles_visited_at_max_steps = walk(num_steps, start, lines)
        print(f"Part One: {len(tiles_visited_at_max_steps)}")


def walk(max_dist, start, lines):
    size_rows = len(lines)
    size_cols = len(lines[0])

    queue = deque([(start, 0)])
    closed = set()
    exactly_64 = set()
    while queue:
        pos, dist = queue.popleft()

        if (pos, dist) in closed:
            continue

        closed.add((pos, dist))

        if dist == max_dist:
            exactly_64.add(pos)
            continue

        for move in move_set:
            new_pos = (pos[0] + move[0], pos[1] + move[1])
            # if (
            #     new_pos[0] >= 0
            #     and new_pos[0] < size_rows
            #     and new_pos[1] >= 0
            #     and new_pos[1] < size_cols
            #     and lines[new_pos[0]][new_pos[1]] != "#"
            # ):
            if lines[new_pos[0] % size_rows][new_pos[1] % size_cols] != "#":
                queue.append((new_pos, dist + 1))
    return exactly_64


def find_start(lines):
    for row, line in enumerate(lines):
        col = line.find("S")
        if col > 0:
            return (row, col)


if __name__ == "__main__":
    filename = "day21/input.txt"
    start_time = time.time()
    main(filename, False)
    print(f"Part One time: {time.time() - start_time:.3f} sec")
    # start_time = time.time()
    # main(filename, True)
    # print(f"Part Two time: {time.time() - start_time:.3f} sec")
