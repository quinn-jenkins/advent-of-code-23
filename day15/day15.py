import time
from collections import defaultdict


def main(filename: str, partOne: bool):
    with open(filename) as file:
        input = file.readline().strip()
        commands = input.split(",")
        if partOne:
            totalHashVal = 0
            for command in commands:
                commandVal = hash(command)
                totalHashVal += commandVal
            print(f"Part One: {totalHashVal}")
        else:
            boxes = defaultdict(list)
            for command in commands:
                if "-" in command:
                    lensLabel, focalLength = command.split("-")
                    box = hash(lensLabel)
                    currentBoxContents = boxes[box]
                    indexOfLensToRemove = getIndexOfSameLens(
                        currentBoxContents, lensLabel
                    )
                    if indexOfLensToRemove != None:
                        currentBoxContents.pop(indexOfLensToRemove)
                        boxes[box] = currentBoxContents
                elif "=" in command:
                    lensLabel, focalLength = command.split("=")
                    box = hash(lensLabel)
                    lensId = (lensLabel, int(focalLength))
                    existingLensLocation = getIndexOfSameLens(boxes[box], lensLabel)
                    if existingLensLocation == None:
                        boxes[box].append(lensId)
                    else:
                        boxes[box][existingLensLocation] = lensId
                else:
                    raise Exception(f"Unknown command: {command}")
            totalFocusingPower = 0
            for box in boxes:
                focusingPower = 0
                for slot, lens in enumerate(boxes[box], 1):
                    focusingPower += slot * lens[1]
                totalFocusingPower += focusingPower * (box + 1)
            print(f"Part Two: {totalFocusingPower}")


def printBoxes(boxes):
    for box in boxes:
        if len(boxes[box]) > 0:
            print(f"Box: {box}")
            for lens in boxes[box]:
                print(f"\tLens: {lens}")


def getIndexOfSameLens(boxContents: list[str], lensLabel) -> int:
    for index, lens in enumerate(boxContents):
        if lens[0] == lensLabel:
            # we already have this lense, so replace it with our new one
            return index
    return None


def hash(command: str) -> int:
    currentVal = 0
    for ch in command:
        currentVal += ord(ch)
        currentVal *= 17
        currentVal = currentVal % 256
    return currentVal


if __name__ == "__main__":
    filename = "day15/input.txt"
    startTime = time.time()
    main(filename, True)
    print(f"Part One time: {time.time() - startTime:.3f} sec")
    startTime = time.time()
    main(filename, False)
    print(f"Part Two time: {time.time() - startTime:.3f} sec")
