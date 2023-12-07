import re
import functools
import time
from multiprocessing import Pool
import math

def calculateWaysToWinRace(raceTime : int, recordDistance : int, numThreads=8) -> int:
    print(f'Time {raceTime} -- Distance Record {recordDistance}')
    startTime = time.time()
    with Pool(processes=numThreads) as pool:
        partialIsRaceWin = functools.partial(isRaceAWin, raceTime=raceTime, distanceToBeat=recordDistance)
        results = pool.map(partialIsRaceWin, range(1, raceTime))

    endTime = time.time()
    print(f'Took {endTime - startTime} with {numThreads} threads')
    return(sum(results))

def isRaceAWin(holdTime, raceTime, distanceToBeat):
    distanceTravelled = holdTime * (raceTime - holdTime)
    return distanceTravelled > distanceToBeat

def partOne():
    with open("day6/input.txt") as file:
        lines = file.read().splitlines()

        raceTimes = [int(s) for s in re.findall(r'\d+', lines[0])]
        recordDistances = [int(s) for s in re.findall(r'\d+', lines[1])]

        numRaces = len(raceTimes)
        waysToWinEachRace = []
        for race in range(numRaces):
            raceTime = raceTimes[race]
            recordDistance = recordDistances[race]
            print(f'Race {race} -- Time {raceTime} -- Distance Record {recordDistance}')
            waysToWinThisRace = calculateWaysToWinRace(raceTime, recordDistance)
            waysToWinEachRace.append(waysToWinThisRace)

        print(waysToWinEachRace)
        errorMargin = None
        for waysToWinRace in waysToWinEachRace:
            if errorMargin == None:
                errorMargin = waysToWinRace
            else:
                errorMargin = errorMargin * waysToWinRace

        print(errorMargin)

def partTwo():
    with open("day6/input.txt") as file:
        lines = file.read().splitlines()
        
        raceTime = int(re.search(r'\d+', lines[0].replace(" ", "")).group())
        recordDistance = int(re.search(r'\d+', lines[1].replace(" ", "")).group())

        waysToWinThisRace = calculateWaysToWinRace(raceTime, recordDistance, 16)
        print(f'{waysToWinThisRace} ways to win.')

def partTwoEasyWay():
    with open("day6/input.txt") as file:
        lines = file.read().splitlines()
        
        raceTime = int(re.search(r'\d+', lines[0].replace(" ", "")).group())
        recordDistance = int(re.search(r'\d+', lines[1].replace(" ", "")).group())

        sqrtPart = math.sqrt(raceTime**2 - 4 * recordDistance) / 2

        firstRoot = math.floor(raceTime + sqrtPart)
        secondRoot = math.floor(raceTime - sqrtPart)

        print(f'Roots are {firstRoot} , {secondRoot}')
        print(f'There are {abs(firstRoot - secondRoot)} ways to win')

if __name__ == "__main__":
    partTwoEasyWay()
    partTwo()