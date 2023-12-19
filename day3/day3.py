import re


def createSearchRegion(
    rowNum: int, numStartIndex: int, numEndIndex: int, maxRows: int, rowLength: int
):
    # print(f'Row num {rowNum} Max rows {maxRows}')
    vertRegion = max(rowNum - 1, 0), min(rowNum + 1, maxRows - 1)
    horizRegion = max(numStartIndex - 1, 0), min(numEndIndex + 1, rowLength)
    return vertRegion, horizRegion


def isPartNumber(lines, searchRegion):
    for row in range(searchRegion[0][0], searchRegion[0][1] + 1):
        for col in range(searchRegion[1][0], searchRegion[1][1]):
            if not lines[row][col].isdigit() and lines[row][col] != ".":
                # print(f'Found symbol {lines[row][col]}')
                return True
    return False


def calculatePartNumber(lines, searchRegion):
    allMatchesByRow = {}
    allMatches = []
    numMatches = 0
    for row in range(searchRegion[0][0], searchRegion[0][1] + 1):
        matchesInRow = [
            match
            for match in re.finditer(
                r"\d+", lines[row][searchRegion[1][0] : searchRegion[1][1] + 1]
            )
        ]
        if len(matchesInRow) > 0:
            allMatchesByRow[row] = matchesInRow
            allMatches.append(matchesInRow)
            numMatches = numMatches + len(matchesInRow)

    partNumber = 1
    if numMatches == 2:
        for rowWithDigit in allMatchesByRow.keys():
            allDigitMatchesInRow = [
                match for match in re.finditer(r"\d+", lines[rowWithDigit])
            ]
            for match in allDigitMatchesInRow:
                for knownGearRatioLocation in allMatchesByRow[rowWithDigit]:
                    if (
                        match.span()[0]
                        <= knownGearRatioLocation.span()[0] + searchRegion[1][0]
                        and match.span()[1]
                        >= knownGearRatioLocation.span()[1] + searchRegion[1][0]
                    ):
                        partNumber = partNumber * int(match.group())
        print(f"Gear ratio is {partNumber}")
        return partNumber
    else:
        return 0


def partOne():
    with open("day3/day3input.txt") as file:
        lines = file.read().splitlines()
        numLines = len(lines)
        sum = 0
        for i in range(numLines):
            line = lines[i]
            line.strip()
            # print(line)
            numberMatches = [match for match in re.finditer(r"\d+", line)]
            for number in numberMatches:
                startingLoc = number.span()[0]
                # print(f'start: {startingLoc}')
                endLoc = number.span()[1]
                # print(f'end: {endLoc}')
                searchRegion = createSearchRegion(
                    i, startingLoc, endLoc, numLines, len(line)
                )
                # print(f'Search Region: {searchRegion}')
                if isPartNumber(lines, searchRegion):
                    sum = sum + int(number.group())
                    # print(f"Found part number {number.group()} Sum is now {sum}")
        print(f"Total of part numbers is {sum}")


def partTwo():
    with open("day3/day3input.txt") as file:
        lines = file.read().splitlines()
        numLines = len(lines)
        sum = 0
        for rowNum, line in enumerate(lines):
            asteriskMatches = [match for match in re.finditer(r"\*", line)]
            for asteriskMatch in asteriskMatches:
                asteriskIndex = asteriskMatch.span()[0]
                searchRegion = createSearchRegion(
                    rowNum, asteriskIndex, asteriskIndex, numLines, len(line)
                )
                sum = sum + calculatePartNumber(lines, searchRegion)
        print(f"Sum is now {sum}")


partTwo()
