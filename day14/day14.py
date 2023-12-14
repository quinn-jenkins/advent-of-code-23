import time
import functools

def main(filename: str, partTwo : bool):
    with open(filename) as file:
        lines = [line.rstrip() for line in file]
        # rotate one extra time first so that "Left" is "North" because for some reason that makes more sense in my head
        lines = rotateCCW(lines)
        
        if partTwo:
            numCycles = 1_000_000_000
            knownStates = {}

            for i in range(numCycles):
                lines = runOneCycle(tuple(lines))
                state = hash(lines)
                if state in knownStates:
                    # we found a repetition, so now we can extrapolate out and not run a lot of the remaining cycles
                    cycleStart = knownStates[state]
                    cycleSize = i - cycleStart
                    print(f"Found a repeated state after {i} cycles! Cycle is {cycleSize} long and starts at iteration {cycleStart}.")
                    break
                else:
                    knownStates[state] = i
            # find how far into a cycle we are after the last full cycle before the end
            numCyclesLeft = (numCycles - (cycleStart + 1)) % cycleSize
            print(f"Running {numCyclesLeft} times to get to the correct end state.")
            for i in range(numCyclesLeft):
                lines = runOneCycle(lines)
        else:
            lines = tilt(lines)
        
        #undo our extra rotation
        lines = rotateClockwise(lines)
        load = countLoad(lines)
        
        print(f"{'Part Two' if partTwo else 'Part One'} : {load}")

@functools.cache
def runOneCycle(lines):
    # rotate north
    lines = tilt(lines)
    lines = rotateClockwise(lines)
    
    # rotate west
    lines = tilt(lines)
    lines = rotateClockwise(lines)

    # rotate south
    lines = tilt(lines)
    lines = rotateClockwise(lines)

    # rotate east
    lines = tilt(lines)
    lines = rotateClockwise(lines)

    return lines

def rotateCCW(lines):
    return tuple(zip(*lines))[::-1]

def rotateClockwise(lines):
    return tuple(zip(*lines[::-1]))

def tilt(lines):
    tilted = []
    for line in lines:
        tilted.append(tiltLine(line))
    return tilted

@functools.cache
def tiltLine(line):
    blockedIndex = 0
    line = list(line)
    for i, ch in enumerate(line):
        if i > blockedIndex:
            if ch == "#":
                blockedIndex = i+1
            elif ch == "O":
                # move it to the blocked index, and open up its space
                line[blockedIndex] = "O"
                line[i] = "."
                blockedIndex += 1
        else:
            if ch in "O#":
                blockedIndex += 1
    return tuple(line)

def countLoad(lines) -> int:
    totalLoad = 0
    load = len(lines)
    for line in lines:
        totalLoad += load * line.count("O")
        load -= 1
    return totalLoad

if __name__ == "__main__":
    filename = "day14/input.txt"
    startTime = time.time()
    main(filename, False)
    print(f"Part One time: {time.time() - startTime:.3f} sec")
    startTime = time.time()
    main(filename, True)
    print(f"Part Two time: {time.time() - startTime:.3f} sec")