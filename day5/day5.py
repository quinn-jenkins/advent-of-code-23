import re

def getLowestSeedLocation(seeds, steps):
    lowestLocation = -1
    for seed in seeds:
        seedLocation = getSeedLocation(seed, steps)
        if lowestLocation == -1:
            lowestLocation = seedLocation
        elif seedLocation < lowestLocation:
            lowestLocation = seedLocation

    print(f'Lowest seed location is {lowestLocation}')

def getSeedLocation(seed, steps):
    # print(f'Processing seed {seed}')
    sourceVal = seed
    for step in steps:
        # print(f'Mapping: {steps[step]}')
        for map in steps[step]:
            if map[1] <= sourceVal and (map[1] + map[2]) > sourceVal:
                sourceVal = map[0] + sourceVal - map[1]
                break
        # print(f'Step {step} - {sourceVal}')
    # print(f'Seed {seed} location {sourceVal}')
    return sourceVal

def getSteps(lines, lineBreaks):
    steps = {}
    lastLineBreak = 0
    for sectionNumber, lineBreak in enumerate(lineBreaks):
        if lastLineBreak == 0:
            lastLineBreak = lineBreak + 2
        else:
            # our range is [lastLineBreak - lineBreak)
            for i in range(lastLineBreak, lineBreak):
                mapping = [int(s) for s in re.findall(r'\d+', lines[i])]
                if sectionNumber in steps:
                    steps[sectionNumber].append(mapping)
                else:
                    steps[sectionNumber] = [mapping]
            lastLineBreak = lineBreak + 2
            print(f'Section {sectionNumber}: {steps[sectionNumber]}')
    return steps

def getLineBreakLocations(lines):
    lineBreaks = []
    for i, line in enumerate(lines):
        if line == '':
            lineBreaks.append(i)

    lineBreaks.append(len(lines))
    return lineBreaks

def getPartTwoLowestSeedLocation(seedString : str, steps):
    lowestSeedLocation = -1
    numbers = [int(s) for s in re.findall(r'\d+', seedString)]
    print(f'Numbers: {numbers}')
    for i in range(0, len(numbers), 2):
        start = numbers[i]
        end = numbers[i] + numbers[i+1] - 1
        print(f'Processing seeds from {start} to {end}')
        for j in range(start, end):
            # print(f'Processing seed {j}')
            seedLocation = getSeedLocation(j, steps)
            if lowestSeedLocation == -1:
                lowestSeedLocation = seedLocation
            elif seedLocation < lowestSeedLocation:
                lowestSeedLocation = seedLocation
    return lowestSeedLocation


def partOne():
    with open("day5/day5input.txt") as file:
        lines = file.read().splitlines()

        lineBreaks = getLineBreakLocations(lines)
        print(lineBreaks)

        steps = getSteps(lines, lineBreaks)

        # get seeds
        seeds = [int(s) for s in re.findall(r'\d+', lines[0])]
        print(f'Seeds {seeds}')

        getLowestSeedLocation(seeds, steps)

def partTwo():
    with open("day5/day5input.txt") as file:
        lines = file.read().splitlines()

        lineBreaks = getLineBreakLocations(lines)
        print(lineBreaks)

        steps = getSteps(lines, lineBreaks)

        # get seeds
        lowestSeedLocation = getPartTwoLowestSeedLocation(lines[0], steps)
        print(f'Lowest seed location: {lowestSeedLocation}')

# partOne()
partTwo()