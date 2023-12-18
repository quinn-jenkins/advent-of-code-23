import time
from heapq import heappop, heappush

def main(filename: str, partOne : bool):
    with open(filename) as file:
        lines = [line.rstrip() for line in file]
        if partOne:
            minheat = djikstra(lines, 1, 3)
            print(f"Part One: {minheat}")
        else:
            minheat = djikstra(lines, 4, 10)
            print(f"Part Two: {minheat}")

def djikstra(lines, minMoves : int, maxMoves : int):
    startNode = (0, 0, 0, -1)
    endRow = len(lines) - 1
    endCol = len(lines[endRow]) - 1
    openList = [startNode]
    closedList = set()

    directionOptions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    while len(openList) > 0:
        currentHeat, curRow, curCol, prevDir = heappop(openList)

        if curRow == endRow and curCol == endCol:
            return currentHeat
        if (curRow, curCol, prevDir) in closedList:
            continue

        closedList.add((curRow, curCol, prevDir))
        
        for direction in range(4):
            # can't go back the way we came, but also can't continue in the same direction
            if direction == prevDir or (direction + 2) % 4 == prevDir:
                continue
            
            heatIncrease = 0
            for i in range(1, maxMoves+1):
                newRow = curRow + directionOptions[direction][0] * i
                newCol = curCol + directionOptions[direction][1] * i
                if isPositionInLines(lines, (newRow, newCol)):
                    heatIncrease += int(lines[newRow][newCol])
                    if i < minMoves:
                        continue
                    totalHeat = currentHeat + heatIncrease
                    heappush(openList, (totalHeat, newRow, newCol, direction))

def isPositionInLines(lines, position):
    if position[0] >= 0 and position[1] >= 0 and position[0] < len(lines) and position[1] < len(lines[position[0]]):
        return True
    return False     

if __name__ == "__main__":
    filename = "day17/input.txt"
    startTime = time.time()
    main(filename, True)
    print(f"Part One time: {time.time() - startTime:.3f} sec")
    startTime = time.time()
    main(filename, False)
    print(f"Part Two time: {time.time() - startTime:.3f} sec")