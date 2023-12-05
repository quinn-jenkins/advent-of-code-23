import re

def getNumberOfMatchingNumbers(line:str):
    winningNumbers = re.findall(r'\d+', line[line.index(':'):line.index("|")])
    numbersIHave = re.findall(r'\d+', line[line.index("|"):])
    score = 0
    for num in numbersIHave:
        if num in winningNumbers:
            score += 1
    return score

def partOne():
    totalPoints = 0
    with open("day4/day4input.txt") as file:
        lines = file.read().splitlines()
        for cardNumber, line in enumerate(lines):
            winningNumbers = re.findall(r'\d+', line[line.index(':'):line.index("|")])
            # print(f"Winning Numbers: {winningNumbers}")
            numbersIHave = re.findall(r'\d+', line[line.index("|"):])
            # print(f'Numbers I Have {numbersIHave}')
            score = 0
            for num in numbersIHave:
                if num in winningNumbers:
                    if score == 0:
                        score = 1
                    else:
                        score = score * 2
            totalPoints += score
            print(f'Card {cardNumber} score {score} - Total is now {totalPoints}')
        print(f'Total points {totalPoints}')

def partTwo():
    with open("day4/day4input.txt") as file:
        lines = file.read().splitlines()
        numCards = len(lines)
        cardToMatchNumberDict = {}
        numberOfEachCard = [1] * numCards
        for cardNumber, line in enumerate(lines):
            numMatches = getNumberOfMatchingNumbers(line)
            cardToMatchNumberDict[cardNumber] = numMatches

        result = 0
        for cardNum in range(numCards):
            matchesInCard = cardToMatchNumberDict[cardNum]
            for copyCard in range(cardNum + 1, cardNum + 1 + matchesInCard):
                numberOfEachCard[copyCard] += numberOfEachCard[cardNum]
            result += numberOfEachCard[cardNum]

        print(result)

partTwo()