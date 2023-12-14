def main(filename: str, partTwo : bool):
    with open(filename) as file:
        puzzleSections = []
        lines = file.read().splitlines()
        lastLineBreak = 0
        for index, line in enumerate(lines):
            if line == "":
                puzzleSections.append(lines[lastLineBreak:index])
                lastLineBreak = index + 1
        puzzleSections.append(lines[lastLineBreak:])

        total = 0
        for puzzle in puzzleSections:
            # print('\n'.join(' '.join(str(x) for x in row) for row in puzzle))
            if (partTwo):
                horMir = findHorizontalMirrorPt2(puzzle)
            else:
                horMir = findHorizontalMirror(puzzle)
            if horMir != None:
                # print(f"Found horizontal mirror between index {horMir} and {horMir + 1} - Adding {horMir}")
                total += 100 * (horMir)
            else:
                rotatedPuzzle = list(zip(*puzzle[::-1]))
                # print('\n'.join(' '.join(str(x) for x in row) for row in rotatedPuzzle))
                if (partTwo):
                    vertMir = findHorizontalMirrorPt2(rotatedPuzzle)
                else:
                    vertMir = findHorizontalMirror(rotatedPuzzle)
                if vertMir != None:
                    # print(f"Found vertical mirror between index {vertMir} and {vertMir + 1} - Adding {vertMir}")
                    total += vertMir
                else:
                    print("No mirror found!")
        print(f"{'Part Two' if partTwo else 'Part One'} : {total}")

def findHorizontalMirrorPt2(puzzle):
    lastRowNum = 0
    for rowNum, row in enumerate(puzzle[1:], 1):
        diff = countRowDifferences(row, puzzle[lastRowNum])
        if diff <= 1:
            lastRowNum = rowNum - 1
            curRowNum = rowNum
            allMatch = True
            smudgesFound = 0
            while curRowNum < len(puzzle) and lastRowNum >= 0:
                smudgesFound += countRowDifferences(puzzle[curRowNum], puzzle[lastRowNum])
                if smudgesFound > 1:
                    allMatch = False
                    break
                curRowNum += 1
                lastRowNum -= 1
            if allMatch and smudgesFound == 1:
                return rowNum
        lastRowNum = rowNum

def countRowDifferences(row1, row2) -> int:
    count = 0
    for i, ch in enumerate(row1):
        if ch != row2[i]:
            count += 1
    return count

def findHorizontalMirror(puzzle):
    lastRow = []
    lastRowNum = -1
    for rowNum, row in enumerate(puzzle):
        if row == lastRow:
            lastRowNum = rowNum - 1
            curRowNum = rowNum
            allMatch = True
            while curRowNum < len(puzzle) and lastRowNum >= 0:
                if puzzle[curRowNum] != puzzle[lastRowNum]:
                    allMatch = False
                    break
                curRowNum += 1
                lastRowNum -= 1
            if allMatch:
                return rowNum
        lastRow = row

if __name__ == "__main__":
    filename = "day13/input.txt"
    
    main(filename, False)
    main(filename, True)
