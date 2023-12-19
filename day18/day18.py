import time
import numpy as np


def main(filename: str, partTwo: bool):
    with open(filename) as file:
        lines = [line.rstrip() for line in file]
        dirMap = {"R": (0, 1), "L": (0, -1), "U": (-1, 0), "D": (1, 0)}

        currCord = (0, 0)
        coords = [currCord]
        perimeter = 0
        for line in lines:
            dir, length, color = line.split(" ")

            if partTwo:
                dir, length = parseHexValue(color)

            length = int(length)
            perimeter += length
            dirMod = dirMap[dir]
            currCord = (
                currCord[0] + dirMod[0] * length,
                currCord[1] + dirMod[1] * length,
            )
            coords.append(currCord)

        xs, ys = zip(*coords)
        # numpy will default to int32, but our numbers are too big in part 2 so specify int64
        xs = np.array(xs, dtype="int64")
        ys = np.array(ys, dtype="int64")
        area = PolyArea(xs, ys)
        # Pick's Theorem: A = i + b/2 - 1
        # where A = area
        # i = # of internal points
        # b = perimeter
        # i = A + 1 - b/2
        internalPoints = area + 1 - perimeter / 2
        totalLavaVolume = internalPoints + perimeter
        if partTwo:
            print(f"Part Two: {totalLavaVolume}")
        else:
            print(f"Part One: {totalLavaVolume}")


def parseHexValue(hexValue: str):
    stripped = hexValue[hexValue.index("#") + 1 : -1]
    dir = int(stripped[-1])
    distance = int(stripped[0:-1], 16)

    if dir == 0:
        return ("R", distance)
    elif dir == 1:
        return ("D", distance)
    elif dir == 2:
        return ("L", distance)
    elif dir == 3:
        return ("U", distance)


# Shoelace formula copied from stackoverflow:
# https://stackoverflow.com/a/30408825
def PolyArea(x, y):
    return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))


if __name__ == "__main__":
    filename = "day18/input.txt"
    startTime = time.time()
    main(filename, False)
    print(f"Part One time: {time.time() - startTime:.3f} sec")
    startTime = time.time()
    main(filename, True)
    print(f"Part Two time: {time.time() - startTime:.3f} sec")
