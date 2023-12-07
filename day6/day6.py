import re
import functools
from multiprocessing import Pool

def calculateWaysToWinRace(raceTime : int, recordDistance : int) -> int:
    with Pool(processes=8) as pool:
        partialIsRaceWin = functools.partial(isRaceAWin, raceTime=raceTime, distanceToBeat=recordDistance)
        results = pool.map(partialIsRaceWin, range(1, raceTime))

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

        print(f'Time {raceTime} -- Distance Record {recordDistance}')
        waysToWinThisRace = calculateWaysToWinRace(raceTime, recordDistance)
        print(f'{waysToWinThisRace} ways to win.')

if __name__ == "__main__":      
    partTwo()