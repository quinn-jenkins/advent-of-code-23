import re

maxBlue = 14
maxRed = 12
maxGreen = 13


def extractGameId(line: str):
    return re.findall(r"\d+", line[0 : line.index(":")])[0]


def extractGameMoves(line: str):
    return re.split("; |, |\*|\n", line[line.index(":") + 2 :])


def validateMove(move: str):
    moveParts = move.split(" ")
    # print(moveParts)
    color = moveParts[1]
    diceNumber = moveParts[0]
    if color == "blue" and int(diceNumber) > maxBlue:
        print(f"Too many blue dice {diceNumber} > {maxBlue}")
        return False
    elif color == "red" and int(diceNumber) > maxRed:
        print(f"Too many red dice {diceNumber} > {maxRed}")
        return False
    elif color == "green" and int(diceNumber) > maxGreen:
        print(f"Too many green dice {diceNumber} > {maxGreen}")
        return False
    else:
        return True


def updateMaxColorDice(move: str, colors: dict):
    moveParts = move.split(" ")
    # print(moveParts)
    color = moveParts[1]
    diceNumber = int(moveParts[0])
    if (not color in colors) or (diceNumber > int(colors[color])):
        print(f"Max for {color} is now {diceNumber}")
        colors[color] = diceNumber


def calculateGameScore(colors: dict):
    total = 1
    for value in colors.values():
        total = total * int(value)
    return total


def partOne():
    with open("day2/day2input.txt") as file:
        totalPossibleGameScore = 0
        for line in file:
            print(line)
            line = line.strip()
            gameId = int(extractGameId(line))
            # print(gameId)
            gameMoves = extractGameMoves(line)
            # print(gameMoves)
            allPossible = True
            for move in gameMoves:
                if not validateMove(move):
                    print("Game is not possible")
                    allPossible = False
                    break

            if allPossible:
                totalPossibleGameScore = totalPossibleGameScore + gameId
                print(
                    f"Game is possible!\nTotal Possible Game Count is {totalPossibleGameScore}"
                )


def partTwo():
    with open("day2/day2input.txt") as file:
        totalPossibleGameScore = 0
        for line in file:
            print(line)
            line = line.strip()
            gameId = int(extractGameId(line))
            # print(gameId)
            gameMoves = extractGameMoves(line)
            # print(gameMoves)
            colorsDict = {}
            for move in gameMoves:
                print(f"Move: {move}")
                updateMaxColorDice(move, colorsDict)
            gameScore = calculateGameScore(colorsDict)
            totalPossibleGameScore = totalPossibleGameScore + gameScore
            print(f"Game score for this game is {gameScore}")
            print(f"Total Possible Game Count is {totalPossibleGameScore}")


# partOne()
partTwo()
