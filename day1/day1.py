import re


def findFirstDigit(text: str):
    for c in text:
        if c.isdigit():
            return c


def fixString(text: str):
    text = text.replace("oneight", "18")
    text = text.replace("twone", "21")
    text = text.replace("eightwo", "82")
    text = text.replace("eighthree", "83")

    text = text.replace("zero", "0")
    text = text.replace("one", "1")
    text = text.replace("two", "2")
    text = text.replace("three", "3")
    text = text.replace("four", "4")
    text = text.replace("five", "5")
    text = text.replace("six", "6")
    text = text.replace("seven", "7")
    text = text.replace("eight", "8")
    text = text.replace("nine", "9")

    return text


def partOne():
    with open("day1/day1input.txt") as file:
        sum = 0
        for line in file:
            print(line)
            firstDigit = findFirstDigit(line)
            lastDigit = findFirstDigit(line[::-1])
            print(f"First digit: {firstDigit} last digit: {lastDigit}")

            calVal = int(firstDigit) * 10 + int(lastDigit)
            print(f"calVal is {calVal}")
            sum += calVal
            print(f"Sum is now {sum}")


def partTwo():
    with open("day1/day1input.txt") as file:
        sum = 0
        for line in file:
            print(line)
            cleanedLine = fixString(line)
            print(cleanedLine)
            firstDigit = findFirstDigit(cleanedLine)
            lastDigit = findFirstDigit(cleanedLine[::-1])
            print(f"First digit: {firstDigit} last digit: {lastDigit}")

            calVal = int(firstDigit) * 10 + int(lastDigit)
            print(f"calVal is {calVal}")
            sum += calVal
            print(f"Sum is now {sum}")


partTwo()
