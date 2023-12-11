from pprint import pprint
import math

def partOne(filename: str):
    with open(filename) as file:
        lines = file.read().splitlines()

        galaxyLocations = getGalaxyLocations(lines)
        pprint(galaxyLocations)

        emptyRows = getEmptyRows(galaxyLocations, len(lines))
        print(f'Empty rows: {emptyRows}')

        emptyCols = getEmptyColumns(galaxyLocations, len(lines[0]))
        print(f'Empty cols: {emptyCols}')

        galaxyDistances = getShortestGalaxyDistancePairs(galaxyLocations, emptyRows, emptyCols)
        print(f'Galaxy Distances Dict: {galaxyDistances}')

        pair = 1
        totalDistance = 0
        for galaxy in galaxyDistances:
            for otherGalaxyDistance in galaxyDistances[galaxy]:
                # print(f'Pair {pair} - {galaxy} and {otherGalaxyDistance[0]} - Distance {otherGalaxyDistance[1]}')
                totalDistance += otherGalaxyDistance[1]
                # print(f'Total distance is now: {totalDistance}')
                pair+=1

def getShortestGalaxyDistancePairs(galaxyLocations, emptyRows : [], emptyCols : []) -> {}:
    galaxyPairsDistance = {}
    for i, galaxy in enumerate(galaxyLocations):
        galaxyPairsDistance[galaxy] = []
        for otherGalaxy in galaxyLocations[i+1:]:
            distance = getDistanceBetweenGalaxies(galaxy, otherGalaxy, emptyRows, emptyCols)
            galaxyPairsDistance[galaxy].append((otherGalaxy, distance))
    return galaxyPairsDistance

def getDistanceBetweenGalaxies(startGalaxy, endGalaxy, emptyRows, emptyCols):
    deltaX = getDeltaXWithExpansion(startGalaxy, endGalaxy, emptyRows)
    deltaY = getDeltaYWithExpansion(startGalaxy, endGalaxy, emptyCols)

    return deltaX + deltaY

def getDeltaXWithExpansion(startGalaxy, endGalaxy, emptyRows) -> int:
    startX = 0
    endX = 0
    if startGalaxy[0] > endGalaxy[0]:
        startX = endGalaxy[0]
        endX = startGalaxy[0]
    else:
        startX = startGalaxy[0]
        endX = endGalaxy[0]

    rowsCrossed = []
    for emptyRow in emptyRows:
        if startX < emptyRow and endX > emptyRow:
            rowsCrossed.append(emptyRow)

    deltaX = endX - startX + len(rowsCrossed)
    return deltaX

def getDeltaYWithExpansion(startGalaxy, endGalaxy, emptyCols) -> int:
    startY = 0
    endY = 0
    if startGalaxy[1] > endGalaxy[1]:
        startY = endGalaxy[1]
        endY = startGalaxy[1]
    else:
        startY = startGalaxy[1]
        endY = endGalaxy[1]

    colsCrossed = []
    for emptyCol in emptyCols:
        if startY < emptyCol and endY > emptyCol:
            colsCrossed.append(emptyCol)

    deltaY = endY - startY + len(colsCrossed)
    return deltaY

# any row in the input that doesn't have a galaxy should actually be 2 rows
def getGalaxyLocations(lines) -> []:
    galaxyLocations = []
    for i, row in enumerate(lines):
        for j, char in enumerate(row):
            if char in "#":
                galaxyLocations.append((i, j))
    return galaxyLocations

def getEmptyRows(galaxyLocations : [], maxRows) -> []:
    emptyRows = []
    for i in range(maxRows):
        atLeastOneGalaxy = False
        for galaxyLoc in galaxyLocations:
            if galaxyLoc[0] == i:
                atLeastOneGalaxy = True
                break
        if not atLeastOneGalaxy:
            emptyRows.append(i)
    return emptyRows

def getEmptyColumns(galaxyLocations : [], maxCols) -> []:
    emptyCols = []
    for j in range(maxCols):
        atLeastOneGalaxy = False
        for galaxyLoc in galaxyLocations:
            if galaxyLoc[1] == j:
                atLeastOneGalaxy = True
                break
        if not atLeastOneGalaxy:
            emptyCols.append(j)
    return emptyCols

if __name__ == "__main__":
    filename = "day11/example.txt"
    partOne(filename)
    # partTwo(filename)
    filename = "day11/input.txt"
    partOne(filename)