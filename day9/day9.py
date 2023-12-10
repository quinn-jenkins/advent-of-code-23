import numpy as np

def isAllZeroes(sequence : []) -> bool:
    for val in sequence:
        if val != 0:
            return False
    return True

def getNextValueInSequence(sequence : []) -> int:
    nextSequence = np.diff(sequence)
    
    if isAllZeroes(nextSequence):
        return 0
    
    return nextSequence[-1] + getNextValueInSequence(nextSequence)

def getPreviousValueInSequence(sequence : []) -> int:
    nextSequence = np.diff(sequence)

    if isAllZeroes(nextSequence):
        return 0
    
    return nextSequence[0] - getPreviousValueInSequence(nextSequence)

def partOne(filename: str):
    with open(filename) as file:
        lines = file.read().splitlines()

        totalOfExtrapolatedValues = 0
        for line in lines:
            sequence = [int(s) for s in line.split(' ')]
            nextValue = sequence[-1] + getNextValueInSequence(sequence)
            totalOfExtrapolatedValues += nextValue
        print(f'Part 1 : {totalOfExtrapolatedValues}')

def partTwo(filename: str):
    with open(filename) as file:
        lines = file.read().splitlines()

        totalOfExtrapolatedValues = 0
        for line in lines:
            sequence = [int(s) for s in line.split(' ')]
            nextValue = sequence[0] - getPreviousValueInSequence(sequence)
            totalOfExtrapolatedValues += nextValue
        print(f'Part 2 : {totalOfExtrapolatedValues}')
            

if __name__ == "__main__":
    filename = "day9/example.txt"
    # partOne(filename)
    # partTwo(filename)
    filename = "day9/input.txt"
    partOne(filename)
    partTwo(filename)