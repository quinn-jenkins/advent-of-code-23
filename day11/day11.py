from pprint import pprint

partTwoExpansionFactor = 1000000

def main(filename: str):
    with open(filename) as file:
        lines = file.read().splitlines()

        galaxyLocations = getGalaxyLocations(lines)
        emptyRows = getEmptyRows(galaxyLocations, len(lines))
        emptyCols = getEmptyColumns(galaxyLocations, len(lines[0]))
        galaxyDistances = getShortestGalaxyDistancePairs(galaxyLocations, emptyRows, emptyCols, True)

        totalDistance = 0
        for galaxy in galaxyDistances:
            for otherGalaxyDistance in galaxyDistances[galaxy]:
                totalDistance += otherGalaxyDistance[1]
        print(f'Part One: {totalDistance}')

        # Start Part Two
        galaxyDistances = getShortestGalaxyDistancePairs(galaxyLocations, emptyRows, emptyCols, False)
        totalDistance = 0
        for galaxy in galaxyDistances:
            for otherGalaxyDistance in galaxyDistances[galaxy]:
                totalDistance += otherGalaxyDistance[1]
        print(f'Part Two: {totalDistance}')

def getShortestGalaxyDistancePairs(galaxyLocations, emptyRows : [], emptyCols : [], partOne : bool) -> {}:
    galaxyPairsDistance = {}
    for i, galaxy in enumerate(galaxyLocations):
        galaxyPairsDistance[galaxy] = []
        for otherGalaxy in galaxyLocations[i+1:]:
            distance = getDistanceBetweenGalaxies(galaxy, otherGalaxy, emptyRows, emptyCols, partOne)
            galaxyPairsDistance[galaxy].append((otherGalaxy, distance))
    return galaxyPairsDistance

def getDistanceBetweenGalaxies(startGalaxy, endGalaxy, emptyRows, emptyCols, partOne : bool):
    deltaX = getDeltaXWithExpansion(startGalaxy, endGalaxy, emptyRows, partOne)
    deltaY = getDeltaYWithExpansion(startGalaxy, endGalaxy, emptyCols, partOne)

    return deltaX + deltaY

def getDeltaXWithExpansion(startGalaxy, endGalaxy, emptyRows, partOne : bool) -> int:
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

    expansion = 0
    if len(rowsCrossed) > 0:
        expansion = len(rowsCrossed) if partOne else (partTwoExpansionFactor - 1) * len(rowsCrossed)
    deltaX = endX - startX + expansion
    return deltaX

def getDeltaYWithExpansion(startGalaxy, endGalaxy, emptyCols, partOne : bool) -> int:
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
    
    expansion = 0
    if len(colsCrossed) > 0:
        expansion = len(colsCrossed) if partOne else (partTwoExpansionFactor - 1) * len(colsCrossed)
    deltaY = endY - startY + expansion
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
    # main(filename)
    filename = "day11/input.txt"
    main(filename)