from collections import defaultdict
from pprint import pprint

def partOne(filename: str):
    with open(filename) as file:
        lines = file.read().splitlines()

        numRows = len(lines)
        numCols = len(lines[0])

        grid = []
        for i in range(numRows):
            grid.append([-1] * numCols)
        
        startingRow, startingCol = findStartingPoint(lines)
        grid[startingRow][startingCol] = 0

        print("Input")
        pprint(lines)
        # print("Grid")
        # pprint(grid)
        print(f'Starting Point : {startingRow}, {startingCol}')

        # from the starting point, we can go in any of 4 directions, 
        # but only if the connecting pipe has an end 'facing' us
        done = False
        currentPoint = (startingRow, startingCol)
        steps = 1
        while not done:
            if canGoNorth(lines, currentPoint[0], currentPoint[1]):
                currentPoint = currentPoint[0] - 1, currentPoint[1]
                grid[currentPoint[0]][currentPoint[1]] = steps
            elif canGoEast(lines, currentPoint[0], currentPoint[1]):
                currentPoint = currentPoint[0], currentPoint[1] + 1
                grid[currentPoint[0]][currentPoint[1]] = steps
            elif canGoSouth(lines, currentPoint[0], currentPoint[1]):
                currentPoint = currentPoint[0] + 1, currentPoint[1]
                grid[currentPoint[0]][currentPoint[1]] = steps
            elif canGoWest(lines, currentPoint[0], currentPoint[1]):
                currentPoint = currentPoint[0], currentPoint[1] - 1
                grid[currentPoint[0]][currentPoint[1]] = steps
            else:
                done = True

            steps += 1

        pprint(grid)

        # graph = defaultdict(list)
        # for i in range(numRows):
        #     for j in range(numCols):
        #         char = lines[i][j]
        #         if 

def canGoNorth(lines, curRow : int, curCol : int) -> bool:
    currentSymbol = lines[curRow][curCol]
    if (curRow == 0):
        return False
    northSymbol = lines[curRow - 1][curCol]
    if currentSymbol == "|" or currentSymbol == "L" or currentSymbol == "J" or currentSymbol == "S":
        #can't go back to "S", because that means we're done
        if northSymbol == "|" or northSymbol == "7" or northSymbol == "F":
            return True
    return False

def canGoEast(lines, curRow : int, curCol : int) -> bool:
    currentSymbol = lines[curRow][curCol]
    if (curCol == (len(lines[0]) - 1)):
        return False
    eastSymbol = lines[curRow - 1][curCol]
    if currentSymbol == "-" or currentSymbol == "L" or currentSymbol == "F" or currentSymbol == "S":
        #can't go back to "S", because that means we're done
        if eastSymbol == "-" or eastSymbol == "J" or eastSymbol == "7":
            return True
    return False

def canGoSouth(lines, curRow : int, curCol : int) -> bool:
    currentSymbol = lines[curRow][curCol]
    if (curRow == (len(lines) - 1)):
        return False
    southSymbol = lines[curRow - 1][curCol]
    if currentSymbol == "|" or currentSymbol == "7" or currentSymbol == "F" or currentSymbol == "S":
        #can't go back to "S", because that means we're done
        if southSymbol == "|" or southSymbol == "L" or southSymbol == "J":
            return True
    return False

def canGoWest(lines, curRow : int, curCol : int) -> bool:
    currentSymbol = lines[curRow][curCol]
    if (curCol == 0):
        return False
    westSymbol = lines[curRow - 1][curCol]
    if currentSymbol == "-" or currentSymbol == "J" or currentSymbol == "7" or currentSymbol == "S":
        #can't go back to "S", because that means we're done
        if westSymbol == "-" or westSymbol == "L" or westSymbol == "F":
            return True
    return False

def findStartingPoint(lines):
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char == 'S':
                return row, col

partOne("day9/ex1.txt")