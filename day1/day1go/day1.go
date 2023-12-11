package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
	"unicode"
)

func findFirstDigit(line string) string {
	for _, char := range line {
		if unicode.IsDigit(char) {
			return string(char)
		}
	}
	return ""
}

func findLastDigit(line string) string {
	for i := len(line) - 1; i >= 0; i-- {
		if unicode.IsDigit(rune(line[i])) {
			return string(line[i])
		}
	}
	return ""
}

func ReverseString(s string) string {
	r := []rune(s)
	for i, j := 0, len(r)-1; i < len(r)/2; i, j = i+1, j-1 {
		r[i], r[j] = r[j], r[i]
	}
	return string(r)
}

func ReplaceTextWithNumbers(s string) string {
	s = strings.ReplaceAll(s, "oneight", "18")
	s = strings.ReplaceAll(s, "twone", "21")
	s = strings.ReplaceAll(s, "eightwo", "82")
	s = strings.ReplaceAll(s, "eighthree", "83")

	s = strings.ReplaceAll(s, "zero", "0")
	s = strings.ReplaceAll(s, "one", "1")
	s = strings.ReplaceAll(s, "two", "2")
	s = strings.ReplaceAll(s, "three", "3")
	s = strings.ReplaceAll(s, "four", "4")
	s = strings.ReplaceAll(s, "five", "5")
	s = strings.ReplaceAll(s, "six", "6")
	s = strings.ReplaceAll(s, "seven", "7")
	s = strings.ReplaceAll(s, "eight", "8")
	s = strings.ReplaceAll(s, "nine", "9")

	return s
}

func main() {
	file, _ := os.Open("input.txt")
	defer file.Close()

	var lines []string
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}

	total := 0
	for _, line := range lines {
		firstDigit, _ := strconv.Atoi(findFirstDigit(line))
		lastDigit, _ := strconv.Atoi(findLastDigit(line))
		val := firstDigit*10 + lastDigit
		total += val
	}

	fmt.Println("Part One: ", total)

	// start part 2
	total = 0
	for _, line := range lines {
		fixedString := ReplaceTextWithNumbers(line)
		firstDigit, _ := strconv.Atoi(findFirstDigit(fixedString))
		lastDigit, _ := strconv.Atoi(findLastDigit(fixedString))
		val := firstDigit*10 + lastDigit
		total += val
	}

	fmt.Println("Part Two: ", total)
}
