class Day2 {
    static int maxRed = 12
    static int maxGreen = 13
    static int maxBlue = 14

    static void main(String[] args) {

        int total = 0
        List<String> lines = new File("day2/day2groovy/input.txt").readLines()
        for (line in lines) {
            String[] splits = line.split(": ")
            String gameId = splits[0]
            String[] diceTosses = splits[1].split("; ")
            boolean gamePossible = isGamePossible(diceTosses)
            if (gamePossible) {
                int gameNum = gameId.split(" ")[1] as int
                total += gameNum
            }
        }

        int totalPower = 0
        for (line in lines) {
            int highestBlue = 0
            int highestGreen = 0
            int highestRed = 0
            String[] diceTosses = line.split(": ")[1].split("; ")
            for (diceToss in diceTosses) {
                String[] rolls = diceToss.split(", ")
                for (roll in rolls) {
                    String[] parts = roll.split(" ")
                    int number = parts[0] as int
                    String color = parts[1]
                    if (color == "blue" && number > highestBlue) {
                        highestBlue = number
                    } else if (color == "red" && number > highestRed) {
                        highestRed = number
                    } else if (color == "green" && number > highestGreen) {
                        highestGreen = number
                    }
                }
            }
            int power = highestGreen * highestRed * highestBlue
            totalPower += power
        }

        println("Part One:" + total)
        println("Part Two:" + totalPower)
    }

    static boolean isGamePossible(String[] diceTosses) {
        for (int i = 0; i < diceTosses.length; i++) {
            String diceToss = diceTosses[i]
            String[] rollsInToss = diceToss.split(", ")
            if (!isDiceRollPossible(rollsInToss)) {
                return false
            }
        }
        return true
    }

    static boolean isDiceRollPossible(String[] diceRolls) {
        for (int i = 0; i < diceRolls.length; i++) {
            String[] splits = diceRolls[i].split(" ")
            int number = splits[0] as int
            String color = splits[1]
            if (color == "blue" && number > maxBlue) {
                return false
            } else if (color == "red" && number > maxRed) {
                return false
            } else if (color == "green" && number > maxGreen) {
                return false
            }
        }
        return true
    }
}