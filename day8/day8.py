import math
import time
import functools
from multiprocessing import Pool


def parseInstructions(instructionsLine: str) -> []:
    instructions = []
    for char in instructionsLine:
        if char == "R":
            instructions.append(1)
        elif char == "L":
            instructions.append(0)
    return instructions


def parseNodeMap(nodeMapLines) -> {}:
    nodeMap = {}

    for line in nodeMapLines:
        mappingTo = []
        mappingFrom = line[0:3]
        mappingTo.append(line[7:10])
        mappingTo.append(line[12:15])
        nodeMap[mappingFrom] = mappingTo
    print(f"Node Map: {nodeMap}")

    return nodeMap


def getNumberOfStepsToEnd(startingNode: str, instructions: [], map: {}) -> int:
    print(f"Calculating steps to end for starting node {startingNode}")
    currentStep = startingNode
    instrNum = 0
    instructionsLength = len(instructions)
    totalNumSteps = 0
    while not currentStep.endswith("Z"):
        direction = instructions[instrNum]
        currentStep = map[currentStep][direction]
        totalNumSteps += 1
        instrNum += 1
        # if we reach the end of the instructions, start again at the beginning
        if instrNum >= instructionsLength:
            instrNum = 0
        # print(f'Step {totalNumSteps} goes to {currentStep} by going {"L" if direction == 0 else "R"}')
    print(
        f"Starting node {startingNode} takes {totalNumSteps} to reach a terminal node"
    )
    return totalNumSteps


def partOne(filename: str):
    with open(filename) as file:
        lines = file.read().splitlines()

        instructionsLine = lines[0]
        nodeMapLines = lines[2:]

        instructions = parseInstructions(instructionsLine)
        nodeMap = parseNodeMap(nodeMapLines)

        numberOfSteps = getNumberOfStepsToEnd("AAA", instructions, nodeMap)
        print(f"Total number of steps to find Z is {numberOfSteps}")


def getPossiblePartTwoStartingPoints(nodeMap: {}) -> []:
    startingPoints = []
    for key in nodeMap:
        if key.endswith("A"):
            startingPoints.append(key)
    return startingPoints


def partTwo(filename: str):
    with open(filename) as file:
        lines = file.read().splitlines()

        instructionsLine = lines[0]
        nodeMapLines = lines[2:]

        instructions = parseInstructions(instructionsLine)
        nodeMap = parseNodeMap(nodeMapLines)
        startingPoints = getPossiblePartTwoStartingPoints(nodeMap)
        print(f"Starting Points: {startingPoints}")
        numberOfStepsToEnd = []
        for startingPoint in startingPoints:
            numberOfStepsToEnd.append(
                getNumberOfStepsToEnd(startingPoint, instructions, nodeMap)
            )

        # find the number of steps to go from A->Z for each possible starting node, then find the LCM all of them
        print(f"Num steps to end for each starting point {numberOfStepsToEnd}")
        print(f"LCM: {math.lcm(*numberOfStepsToEnd)}")


def partTwoButWithThreads(filename: str, numThreads=8):
    with open(filename) as file:
        lines = file.read().splitlines()

        instructionsLine = lines[0]
        nodeMapLines = lines[2:]

        instructions = parseInstructions(instructionsLine)
        nodeMap = parseNodeMap(nodeMapLines)
        startingPoints = getPossiblePartTwoStartingPoints(nodeMap)
        print(f"Starting Points: {startingPoints}")

        startTime = time.time()
        with Pool(processes=numThreads) as pool:
            partialFuncStepsToEnd = functools.partial(
                getNumberOfStepsToEnd, instructions=instructions, map=nodeMap
            )
            numberOfStepsToEnd = pool.map(partialFuncStepsToEnd, startingPoints)
        print(f"Took {time.time() - startTime} seconds to calculate all steps to end")

        # find the number of steps to go from A->Z for each possible starting node, then find the LCM all of them
        print(f"Num steps to end for each starting point {numberOfStepsToEnd}")
        print(f"LCM: {math.lcm(*numberOfStepsToEnd)}")


if __name__ == "__main__":
    filename = "day8/ex1.txt"
    # partOne(filename)
    filename = "day8/ex2.txt"
    # partOne(filename)
    filename = "day8/expt2.txt"
    partTwo(filename)
    filename = "day8/input.txt"
    # partOne(filename)
    partTwo(filename)
    partTwoButWithThreads(filename)
