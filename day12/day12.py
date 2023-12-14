import functools
import time

def main(filename: str, partTwo : bool):
    with open(filename) as file:
        lines = file.read().splitlines()

        totalPermutations = 0
        for line in lines:
            if partTwo:
                line = expandLineForPartTwo(line)
            puzzle, groupsAsChars = line.split(" ")
            groups = tuple([int(i) for i in groupsAsChars.split(',')])
            possibleSolutions = getPermutations(puzzle, groups)
            totalPermutations += possibleSolutions

        if partTwo:
            print(f"Part Two: {totalPermutations}")
        else:
            print(f"Part One: {totalPermutations}")

def expandLineForPartTwo(line : str):
    puzzle, groups = line.split(" ")
    return puzzle +"?" + puzzle +"?" + puzzle +"?" + puzzle +"?" + puzzle + " " + groups +"," + groups +"," + groups +"," + groups +"," + groups 

@functools.cache
def getPermutations(puzzle: str, groups):
    if len(groups) == 0:
        if "#" not in puzzle:
            # make sure there aren't any more damaged springs in the puzzle because we're out of groups
            return 1
        else:
            # there are more damage springs, but not groups, so we return 0 because this isn't a valid permutation
            return 0

    if len(puzzle) == 0:
        # we're done!
        return 0
    
    currentChar = puzzle[0]
    currentGroup = groups[0]

    def isDot():
        return getPermutations(puzzle[1:], groups)

    def isPound():
        # if our current character is #, then the next len(currentGroup) characters must _also_ be # signs (or ?) for this to be valid
        groupChars = puzzle[:currentGroup].replace("?", "#")
        
        # if there is a . still in the current string, this is an invalid solution
        if groupChars != currentGroup * "#":
            return 0

        # if this is just the rest of the characters in the puzzle...
        if len(puzzle) == currentGroup:
            if len(groups) == 1:
                # this is a valid solution
                return 1
            else:
                # this is not a valid solution
                return 0
        
        # we're somewhere in the middle of the puzzle...
        # we need to make sure that the character after this group of characters is, or can be, a .
        if puzzle[currentGroup] in "?.":
            return getPermutations(puzzle[currentGroup+1:], groups[1:])
        
        # not possible
        return 0

    if currentChar == "#":
        permsInThisStep = isPound()
    elif currentChar == ".":
        # don't really need to do anything, we're just looking for the next #
        permsInThisStep = isDot()
    elif currentChar == "?":
        # can be either, so try both
        permsInThisStep = isDot() + isPound()
    
    # print(puzzle, groups, permsInThisStep)
    return permsInThisStep

if __name__ == "__main__":
    filename = "day12/input.txt"
    main(filename, False)
    startTime = time.time()
    main(filename, True)
    print(f"Total time to execute part two: {time.time() - startTime}")