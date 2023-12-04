import re

def extractGameMoves(line: str):
    return re.split('; |, |\*|\n', line[line.index(":")+2:])

def validateMove(move: str):
    moveParts = move.split(" ")
    print(moveParts)
    color = moveParts[1]
    diceNumber = moveParts[0]
    if color == 'blue' and int(diceNumber) > 14:
        return False
    elif color == 'red' and int(diceNumber) > 12:
        return False
    elif color == 'green' and int(diceNumber) > 13:
        return False
    else:
        return True

def partOne():
    with open("day2/day2example.txt") as file:
        possibleGames = 0
        for line in file:
            print(line)
            gameMoves = extractGameMoves(line)
            print(gameMoves)
            for move in gameMoves:
                if validateMove(move):
                    possibleGames = possibleGames +1
                    print("Game is possible")
                else:
                    print("Game is not possible")



partOne()