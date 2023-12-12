def partOne(filename: str):
    with open(filename) as file:
        lines = file.read().splitlines()

        totalMutations = 0
        for line in lines:
            possibleSolutions = getMutationsForPuzzle(line)
            totalMutations += possibleSolutions

        print(f"Part One: {totalMutations}")

def getMutationsForPuzzle(line : str) -> int:
    splitIndex = line.index(" ")
    puzzle = line[:splitIndex]
    hints = line[splitIndex+1:]
    currentHint = 0

    print(f'Puzzle: {puzzle}\n Hints: {hints}')
    totalPermutations = 0
    for i, char in enumerate(puzzle):
        if char == "?":
            nextBlock = findNextPossibleBlock(puzzle[i:], hints[currentHint])
            totalPermutations += getNumPermutationsInBlock(nextBlock, hints[currentHint])
            currentHint += 1
    
    return totalPermutations

def findNextPossibleBlock(puzzle : str, size : int) -> str:
    geysersFound = 0
    for i, char in enumerate(puzzle[1:]):
        if char in "#":
            geysersFound += 1
            if geysersFound == size:
                return puzzle[:i]


def getNumPermutationsInBlock(block : str, size : int) -> int:
    return 0

if __name__ == "__main__":
    filename = "day12/example.txt"
    partOne(filename)