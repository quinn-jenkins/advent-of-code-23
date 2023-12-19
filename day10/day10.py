import math
from pprint import pprint
from enum import Enum
from matplotlib.path import Path


class Direction(Enum):
    NORTH = (1,)
    EAST = (2,)
    SOUTH = (3,)
    WEST = 4


def main(filename: str):
    with open(filename) as file:
        lines = file.read().splitlines()

        numRows = len(lines)
        numCols = len(lines[0])

        grid = []
        for i in range(numRows):
            grid.append([-1] * numCols)

        startingRow, startingCol = findStartingPoint(lines)
        grid[startingRow][startingCol] = 0

        print(f"Starting Point : {startingRow}, {startingCol}")

        # from the starting point, we can go in any of 4 directions,
        # but only if the connecting pipe has an end 'facing' us
        done = False
        currentPoint = (startingRow, startingCol)
        steps = 1
        lastDirection = None
        path = []
        path.append((startingRow, startingCol))
        while not done:
            if canGoNorth(lines, currentPoint[0], currentPoint[1], lastDirection):
                currentPoint = currentPoint[0] - 1, currentPoint[1]
                grid[currentPoint[0]][currentPoint[1]] = steps
                lastDirection = Direction.NORTH
            elif canGoEast(lines, currentPoint[0], currentPoint[1], lastDirection):
                currentPoint = currentPoint[0], currentPoint[1] + 1
                grid[currentPoint[0]][currentPoint[1]] = steps
                lastDirection = Direction.EAST
            elif canGoSouth(lines, currentPoint[0], currentPoint[1], lastDirection):
                currentPoint = currentPoint[0] + 1, currentPoint[1]
                grid[currentPoint[0]][currentPoint[1]] = steps
                lastDirection = Direction.SOUTH
            elif canGoWest(lines, currentPoint[0], currentPoint[1], lastDirection):
                currentPoint = currentPoint[0], currentPoint[1] - 1
                grid[currentPoint[0]][currentPoint[1]] = steps
                lastDirection = Direction.WEST
            else:
                done = True
            steps += 1
            path.append(currentPoint)

        # steps is now the total length of the loop, so the furthest point should be the midpoint away
        mostSteps = math.floor(steps / 2)

        # Start Part Two
        # remove everything that isn't ground or a pipe in our path
        pathOnlyGrid = []
        for row in range(len(lines)):
            pathOnlyGrid.append([])
            for col in range(len(lines[row])):
                if (row, col) not in path:
                    pathOnlyGrid[row].append(".")
                else:
                    pathOnlyGrid[row].append(lines[row][col])

        # can determine if we're "inside" or "outside" the loop based on the number of times we cross the path on our way out
        # however, symbols that run parallel to our direction don't count as crossing
        enclosedPoints = 0
        for row in range(len(pathOnlyGrid)):
            for col in range(len(pathOnlyGrid[row])):
                if pathOnlyGrid[row][col] == ".":
                    pathIntersections = 0
                    cornerPiecesSeen = []
                    for nextCol in range(col + 1, len(pathOnlyGrid[row])):
                        if pathOnlyGrid[row][nextCol] in "|S":
                            pathIntersections += 1
                        if pathOnlyGrid[row][nextCol] in "FL":
                            cornerPiecesSeen.append(pathOnlyGrid[row][nextCol])
                        if len(cornerPiecesSeen) > 0:
                            if (
                                cornerPiecesSeen[-1] == "F"
                                and pathOnlyGrid[row][nextCol] == "J"
                            ):
                                pathIntersections += 1
                                cornerPiecesSeen.pop(-1)
                            elif (
                                cornerPiecesSeen[-1] == "L"
                                and pathOnlyGrid[row][nextCol] == "7"
                            ):
                                pathIntersections += 1
                                cornerPiecesSeen.pop(-1)

                    if pathIntersections % 2 == 1:
                        enclosedPoints += 1
                        pathOnlyGrid[row][col] = "I"
                    else:
                        pathOnlyGrid[row][col] = "0"

        for row in pathOnlyGrid:
            print("".join(row))
        print(f"Part 1: {mostSteps}")
        print(f"Part 2: {enclosedPoints}")


def canGoNorth(lines, curRow: int, curCol: int, lastDirection: Direction) -> bool:
    currentSymbol = lines[curRow][curCol]
    if curRow == 0 or lastDirection == Direction.SOUTH:
        return False
    northSymbol = lines[curRow - 1][curCol]
    if (
        currentSymbol == "|"
        or currentSymbol == "L"
        or currentSymbol == "J"
        or currentSymbol == "S"
    ):
        # can't go back to "S", because that means we're done
        if northSymbol == "|" or northSymbol == "7" or northSymbol == "F":
            return True
    return False


def canGoEast(lines, curRow: int, curCol: int, lastDirection: Direction) -> bool:
    currentSymbol = lines[curRow][curCol]
    if (curCol == (len(lines[0]) - 1)) or lastDirection == Direction.WEST:
        return False
    eastSymbol = lines[curRow][curCol + 1]
    if (
        currentSymbol == "-"
        or currentSymbol == "L"
        or currentSymbol == "F"
        or currentSymbol == "S"
    ):
        # can't go back to "S", because that means we're done
        if eastSymbol == "-" or eastSymbol == "J" or eastSymbol == "7":
            return True
    return False


def canGoSouth(lines, curRow: int, curCol: int, lastDirection: Direction) -> bool:
    currentSymbol = lines[curRow][curCol]
    if (curRow == (len(lines) - 1)) or lastDirection == Direction.NORTH:
        return False
    southSymbol = lines[curRow + 1][curCol]
    if (
        currentSymbol == "|"
        or currentSymbol == "7"
        or currentSymbol == "F"
        or currentSymbol == "S"
    ):
        # can't go back to "S", because that means we're done
        if southSymbol == "|" or southSymbol == "L" or southSymbol == "J":
            return True
    return False


def canGoWest(lines, curRow: int, curCol: int, lastDirection: Direction) -> bool:
    currentSymbol = lines[curRow][curCol]
    if curCol == 0 or lastDirection == Direction.EAST:
        return False
    westSymbol = lines[curRow][curCol - 1]
    if (
        currentSymbol == "-"
        or currentSymbol == "J"
        or currentSymbol == "7"
        or currentSymbol == "S"
    ):
        # can't go back to "S", because that means we're done
        if westSymbol == "-" or westSymbol == "L" or westSymbol == "F":
            return True
    return False


def findStartingPoint(lines):
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char == "S":
                return row, col


main("day10/input.txt")
