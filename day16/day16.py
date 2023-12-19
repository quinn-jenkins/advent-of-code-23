from enum import Enum
from dataclasses import dataclass
import time
from collections import defaultdict


class Direction(Enum):
    UP = (1,)
    RIGHT = 2
    DOWN = (3,)
    LEFT = 4


@dataclass
class Beam:
    row: int
    col: int
    dir: Direction


def main(filename: str, partOne: bool):
    with open(filename) as file:
        lines = [line.rstrip() for line in file]

        if partOne:
            numEnergizedTiles = getNumberOfEnergizedTiles(lines, 0, 0, Direction.RIGHT)
            print(f"Part One: {numEnergizedTiles}")
        else:
            maxEnergizedTiles = 0
            for row in range(len(lines)):
                numEnergizedTiles = getNumberOfEnergizedTiles(
                    lines, row, 0, Direction.RIGHT
                )
                maxEnergizedTiles = max(maxEnergizedTiles, numEnergizedTiles)
                numEnergizedTiles = getNumberOfEnergizedTiles(
                    lines, row, len(lines[row]) - 1, Direction.LEFT
                )
                maxEnergizedTiles = max(maxEnergizedTiles, numEnergizedTiles)
                print(f"Completed iterating over row {row} of {len(lines)}")
            for col in range(len(lines[0])):
                numEnergizedTiles = getNumberOfEnergizedTiles(
                    lines, 0, col, Direction.DOWN
                )
                maxEnergizedTiles = max(maxEnergizedTiles, numEnergizedTiles)
                numEnergizedTiles = getNumberOfEnergizedTiles(
                    lines, len(lines) - 1, col, Direction.UP
                )
                maxEnergizedTiles = max(maxEnergizedTiles, numEnergizedTiles)
                print(f"Completed iterating over col {col} of {len(lines[0])}")
            print(f"Part Two {maxEnergizedTiles}")

        # visited = []
        # for i, line in enumerate(lines):
        #     visited.append([])
        #     for letter in line:
        #         visited[i].append(letter)

        # for coord in allVisitedCoords:
        #     visited[coord[1]][coord[0]] = "#"

        # for line in visited:
        #     print(' '.join(line))


def getNumberOfEnergizedTiles(lines, startRow, startCol, startDir):
    beams = [Beam(startRow, startCol, startDir)]
    allVisitedCoords = defaultdict(list)
    while len(beams) > 0:
        beam = beams.pop()
        currentCoord = (beam.col, beam.row)
        if (
            currentCoord in allVisitedCoords
            and beam.dir in allVisitedCoords[currentCoord]
        ):
            # we've already explored this path, so make sure we don't loop through it again
            continue
        allVisitedCoords[currentCoord].append(beam.dir)
        # print(f"Visited {beam.row}, {beam.col}")
        next, nextRow, nextCol = getNextChar(lines, beam.row, beam.col, beam.dir)
        # print(f"Next char to the {beam.dir} is: {next} at coord {nextRow}, {nextCol}")
        if next is None:
            continue
        if (beam.dir == Direction.RIGHT or beam.dir == Direction.LEFT) and next == "|":
            # print("Split up/down")
            beams.append(Beam(nextRow, nextCol, Direction.UP))
            beams.append(Beam(nextRow, nextCol, Direction.DOWN))
        elif (beam.dir == Direction.UP or beam.dir == Direction.DOWN) and next == "-":
            # print("Split left/right")
            beams.append(Beam(nextRow, nextCol, Direction.LEFT))
            beams.append(Beam(nextRow, nextCol, Direction.RIGHT))
        elif next == "/":
            if beam.dir == Direction.RIGHT:
                # print("Redirect up")
                beams.append(Beam(nextRow, nextCol, Direction.UP))
            elif beam.dir == Direction.LEFT:
                # print("Redirect down")
                beams.append(Beam(nextRow, nextCol, Direction.DOWN))
            elif beam.dir == Direction.UP:
                # print("Redirect right")
                beams.append(Beam(nextRow, nextCol, Direction.RIGHT))
            elif beam.dir == Direction.DOWN:
                # print("Redirect left")
                beams.append(Beam(nextRow, nextCol, Direction.LEFT))
        elif next == "\\":
            if beam.dir == Direction.RIGHT:
                # print("Redirect down")
                beams.append(Beam(nextRow, nextCol, Direction.DOWN))
            elif beam.dir == Direction.LEFT:
                # print("Redirect up")
                beams.append(Beam(nextRow, nextCol, Direction.UP))
            elif beam.dir == Direction.UP:
                # print("Redirect left")
                beams.append(Beam(nextRow, nextCol, Direction.LEFT))
            elif beam.dir == Direction.DOWN:
                # print("Redirect right")
                beams.append(Beam(nextRow, nextCol, Direction.RIGHT))
        elif next in ".-|":
            # print("Continue")
            beams.append(Beam(nextRow, nextCol, beam.dir))
    return len(allVisitedCoords)


def getNextChar(lines, row, col, dir: Direction):
    if dir == Direction.UP and row > 0:
        return lines[row - 1][col], row - 1, col
    elif dir == Direction.DOWN and row < (len(lines) - 1):
        return lines[row + 1][col], row + 1, col
    elif dir == Direction.LEFT and col > 0:
        return lines[row][col - 1], row, col - 1
    elif dir == Direction.RIGHT and col < (len(lines[row]) - 1):
        return lines[row][col + 1], row, col + 1
    return None, None, None


if __name__ == "__main__":
    filename = "day16/input.txt"
    startTime = time.time()
    main(filename, True)
    print(f"Part One time: {time.time() - startTime:.3f} sec")
    startTime = time.time()
    main(filename, False)
    print(f"Part Two time: {time.time() - startTime:.3f} sec")
