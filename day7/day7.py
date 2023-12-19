def computeCardValues(hand: str):
    # hands are 5 cards
    cardValues = []
    for i in range(5):
        if hand[i].isdigit():
            cardValues.append(int(hand[i]))
        else:
            if hand[i] == "T":
                cardValues.append(10)
            elif hand[i] == "J":
                cardValues.append(11)
            elif hand[i] == "Q":
                cardValues.append(12)
            elif hand[i] == "K":
                cardValues.append(13)
            elif hand[i] == "A":
                cardValues.append(14)
    return cardValues


def computeCardValuesPartTwo(hand: str):
    # hands are 5 cards
    cardValues = []
    for i in range(5):
        if hand[i].isdigit():
            cardValues.append(int(hand[i]))
        else:
            if hand[i] == "T":
                cardValues.append(10)
            elif hand[i] == "J":
                cardValues.append(1)
            elif hand[i] == "Q":
                cardValues.append(12)
            elif hand[i] == "K":
                cardValues.append(13)
            elif hand[i] == "A":
                cardValues.append(14)
    return cardValues


def getMatches(hand):
    matches = {}
    for card in hand:
        matches[card] = sum(card == match for match in hand)

    return matches


def getMatchesPartTwo(hand):
    matches = {}
    for card in hand:
        matches[card] = sum(card == match for match in hand)

    # print(f'Hand {hand}')
    # print(f'Matches {matches}')
    # create a sorted list of Tuple<card, number of matches> for any card that occurs more than once EXCLUDING JOKERS
    sortedMatches = sorted(
        filter(lambda x: x[1] > 1 and x[0] != 1, matches.items()),
        key=lambda x: x[1],
        reverse=True,
    )
    # print(f'Sorted matches {sortedMatches}')
    if 1 in matches:
        # there is at least one joker in the hand
        numJokers = matches[1]
        if len(sortedMatches) > 0:
            # there are matches of non-joker cards, so add our number of jokers to whatever has the most matches
            # note that it doesn't really matter if there are ties (i.e. 2 pair without jokers), because it is a full house either way and it will be sorted later
            matches[sortedMatches[0][0]] += numJokers
            matches[1] = 0
        else:
            # there aren't any matches of non-jokers, so we should just add our jokers to the highest value card in the hand
            maxCardInHand = max(hand)
            # special check to make sure we don't have a hand of 5 jokers
            if maxCardInHand != 1:
                matches[max(hand)] += numJokers
                matches[1] = 0

    return matches


def partOne():
    with open("day7/input.txt") as file:
        lines = file.read().splitlines()

        fiveOfAKind = []
        fourOfAKind = []
        fullHouse = []
        threeOfAKind = []
        twoPair = []
        pair = []
        highCard = []

        handToBidAmount = {}
        handToCardValues = {}

        for handNum, line in enumerate(lines):
            cardValues = computeCardValues(line[:5])
            bidAmount = int(line[6:])
            handToBidAmount[handNum] = bidAmount
            handToCardValues[handNum] = cardValues
            # print(f'Hand {handNum} Card values: {cardValues} - bid {bidAmount}')
            matches = sorted(
                filter(lambda x: x[1] > 1, getMatches(cardValues).items()),
                key=lambda x: x[1],
                reverse=True,
            )
            if len(matches) == 0:
                # print("No matches -- high card")
                highCard.append(handNum)
            elif matches[0][1] == 5:
                # print("Five of a kind")
                fiveOfAKind.append(handNum)
            elif matches[0][1] == 4:
                # print("Four of a kind")
                fourOfAKind.append(handNum)
            elif matches[0][1] == 3 and len(matches) == 1:
                # print("Three of a kind")
                threeOfAKind.append(handNum)
            elif matches[0][1] == 3 and matches[1][1] == 2:
                # print("Full House")
                fullHouse.append(handNum)
            elif matches[0][1] == 2 and len(matches) == 1:
                # print("Pair")
                pair.append(handNum)
            elif matches[0][1] == 2 and matches[1][1] == 2:
                # print("Two Pair")
                twoPair.append(handNum)

        fiveOfAKind = sorted(fiveOfAKind, key=lambda hand: handToCardValues[hand])
        fourOfAKind = sorted(fourOfAKind, key=lambda hand: handToCardValues[hand])
        fullHouse = sorted(fullHouse, key=lambda hand: handToCardValues[hand])
        threeOfAKind = sorted(threeOfAKind, key=lambda hand: handToCardValues[hand])
        twoPair = sorted(twoPair, key=lambda hand: handToCardValues[hand])
        pair = sorted(pair, key=lambda hand: handToCardValues[hand])
        highCard = sorted(highCard, key=lambda hand: handToCardValues[hand])

        # print(f'Five of a kind {fiveOfAKind}')
        # print(f'Four of a kind {fourOfAKind}')
        # print(f'Full House {fullHouse}')
        # print(f'Three of a kind {threeOfAKind}')
        # print(f'Two Pair {twoPair}')
        # print(f'Pair {pair}')
        # print(f'High Card {highCard}')

        totalWinnings = 0
        # add high cards
        rank = 1
        for handNumber in highCard:
            totalWinnings += handToBidAmount[handNumber] * rank
            # print(f'Rank {rank} Hand Number {handNumber} Bid Amount {handToBidAmount[handNumber]} Winnings {handToBidAmount[handNumber] * rank}')
            rank += 1
        # add pairs
        for handNumber in pair:
            totalWinnings += handToBidAmount[handNumber] * rank
            # print(f'Rank {rank} Hand Number {handNumber} Bid Amount {handToBidAmount[handNumber]} Winnings {handToBidAmount[handNumber] * rank}')
            rank += 1
        # add two pairs
        for handNumber in twoPair:
            totalWinnings += handToBidAmount[handNumber] * rank
            # print(f'Rank {rank} Hand Number {handNumber} Bid Amount {handToBidAmount[handNumber]} Winnings {handToBidAmount[handNumber] * rank}')
            rank += 1
        # add three of a kind
        for handNumber in threeOfAKind:
            totalWinnings += handToBidAmount[handNumber] * rank
            # print(f'Rank {rank} Hand Number {handNumber} Bid Amount {handToBidAmount[handNumber]} Winnings {handToBidAmount[handNumber] * rank}')
            rank += 1
        # add full house
        for handNumber in fullHouse:
            totalWinnings += handToBidAmount[handNumber] * rank
            # print(f'Rank {rank} Hand Number {handNumber} Bid Amount {handToBidAmount[handNumber]} Winnings {handToBidAmount[handNumber] * rank}')
            rank += 1
        # add four of a kind
        for handNumber in fourOfAKind:
            totalWinnings += handToBidAmount[handNumber] * rank
            # print(f'Rank {rank} Hand Number {handNumber} Bid Amount {handToBidAmount[handNumber]} Winnings {handToBidAmount[handNumber] * rank}')
            rank += 1
        # add five of a kind
        for handNumber in fiveOfAKind:
            totalWinnings += handToBidAmount[handNumber] * rank
            # print(f'Rank {rank} Hand Number {handNumber} Bid Amount {handToBidAmount[handNumber]} Winnings {handToBidAmount[handNumber] * rank}')
            rank += 1

        print(f"Total Winnings {totalWinnings}")


def partTwo():
    with open("day7/input.txt") as file:
        lines = file.read().splitlines()

        fiveOfAKind = []
        fourOfAKind = []
        fullHouse = []
        threeOfAKind = []
        twoPair = []
        pair = []
        highCard = []

        handToBidAmount = {}
        handToCardValues = {}

        for handNum, line in enumerate(lines):
            cardValues = computeCardValuesPartTwo(line[:5])
            bidAmount = int(line[6:])
            handToBidAmount[handNum] = bidAmount
            handToCardValues[handNum] = cardValues
            # print(f'Hand {handNum} Card values: {cardValues} - bid {bidAmount}')
            matches = sorted(
                filter(lambda x: x[1] > 1, getMatchesPartTwo(cardValues).items()),
                key=lambda x: x[1],
                reverse=True,
            )
            if len(matches) == 0:
                # print("No matches -- high card")
                highCard.append(handNum)
            elif matches[0][1] == 5:
                # print("Five of a kind")
                fiveOfAKind.append(handNum)
            elif matches[0][1] == 4:
                # print("Four of a kind")
                fourOfAKind.append(handNum)
            elif matches[0][1] == 3 and len(matches) == 1:
                # print("Three of a kind")
                threeOfAKind.append(handNum)
            elif matches[0][1] == 3 and matches[1][1] == 2:
                # print("Full House")
                fullHouse.append(handNum)
            elif matches[0][1] == 2 and len(matches) == 1:
                # print("Pair")
                pair.append(handNum)
            elif matches[0][1] == 2 and matches[1][1] == 2:
                # print("Two Pair")
                twoPair.append(handNum)
            else:
                print("ERROR")

        fiveOfAKind = sorted(fiveOfAKind, key=lambda hand: handToCardValues[hand])
        fourOfAKind = sorted(fourOfAKind, key=lambda hand: handToCardValues[hand])
        fullHouse = sorted(fullHouse, key=lambda hand: handToCardValues[hand])
        threeOfAKind = sorted(threeOfAKind, key=lambda hand: handToCardValues[hand])
        twoPair = sorted(twoPair, key=lambda hand: handToCardValues[hand])
        pair = sorted(pair, key=lambda hand: handToCardValues[hand])
        highCard = sorted(highCard, key=lambda hand: handToCardValues[hand])

        # print(f'Five of a kind {fiveOfAKind}')
        # print(f'Four of a kind {fourOfAKind}')
        # print(f'Full House {fullHouse}')
        # print(f'Three of a kind {threeOfAKind}')
        # print(f'Two Pair {twoPair}')
        # print(f'Pair {pair}')
        # print(f'High Card {highCard}')

        totalWinnings = 0
        # add high cards
        rank = 1
        for handNumber in highCard:
            totalWinnings += handToBidAmount[handNumber] * rank
            # print(f'Rank {rank} Hand Number {handNumber} Bid Amount {handToBidAmount[handNumber]} Winnings {handToBidAmount[handNumber] * rank}')
            rank += 1
        # add pairs
        for handNumber in pair:
            totalWinnings += handToBidAmount[handNumber] * rank
            # print(f'Rank {rank} Hand Number {handNumber} Bid Amount {handToBidAmount[handNumber]} Winnings {handToBidAmount[handNumber] * rank}')
            rank += 1
        # add two pairs
        for handNumber in twoPair:
            totalWinnings += handToBidAmount[handNumber] * rank
            # print(f'Rank {rank} Hand Number {handNumber} Bid Amount {handToBidAmount[handNumber]} Winnings {handToBidAmount[handNumber] * rank}')
            rank += 1
        # add three of a kind
        for handNumber in threeOfAKind:
            totalWinnings += handToBidAmount[handNumber] * rank
            # print(f'Rank {rank} Hand Number {handNumber} Bid Amount {handToBidAmount[handNumber]} Winnings {handToBidAmount[handNumber] * rank}')
            rank += 1
        # add full house
        for handNumber in fullHouse:
            totalWinnings += handToBidAmount[handNumber] * rank
            # print(f'Rank {rank} Hand Number {handNumber} Bid Amount {handToBidAmount[handNumber]} Winnings {handToBidAmount[handNumber] * rank}')
            rank += 1
        # add four of a kind
        for handNumber in fourOfAKind:
            totalWinnings += handToBidAmount[handNumber] * rank
            # print(f'Rank {rank} Hand Number {handNumber} Bid Amount {handToBidAmount[handNumber]} Winnings {handToBidAmount[handNumber] * rank}')
            rank += 1
        # add five of a kind
        for handNumber in fiveOfAKind:
            totalWinnings += handToBidAmount[handNumber] * rank
            # print(f'Rank {rank} Hand Number {handNumber} Bid Amount {handToBidAmount[handNumber]} Winnings {handToBidAmount[handNumber] * rank}')
            rank += 1

        # for i in highCard:
        #     print(f'High Card: {handToCardValues[i]}')

        # for i in pair:
        #     print(f'Pair: {handToCardValues[i]}')

        # for i in twoPair:
        #     print(f'Two Pair: {handToCardValues[i]}')

        # for i in threeOfAKind:
        #     print(f'Three: {handToCardValues[i]}')

        # for i in fullHouse:
        #     print(f'Full House: {handToCardValues[i]}')

        # for i in fourOfAKind:
        #     print(f'Four: {handToCardValues[i]}')

        # for i in fiveOfAKind:
        #     print(f'Five: {handToCardValues[i]}')
        print(f"Total Winnings {totalWinnings}")


if __name__ == "__main__":
    partTwo()
