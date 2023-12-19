import time
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class Part:
    x: int
    m: int
    a: int
    s: int


def main(filename: str, partTwo: bool):
    with open(filename) as file:
        lines = [line.rstrip() for line in file]
        blankIndex = lines.index("")
        sortLines = lines[:blankIndex]
        # print(f"Sortings: {sortLines}")
        partLines = lines[blankIndex + 1 :]

        workflows = defaultdict(list)
        for step in sortLines:
            name = step[0 : step.index("{")]
            workflows[name] = step[step.index("{") + 1 : -1].split(",")

        if partTwo:
            # need to solve with buckets, keeping track of what range gets to an "A" and discarding any that get to "R"
            buckets = [
                ["in", {"x": [0, 4001], "m": [0, 4001], "a": [0, 4001], "s": [0, 4001]}]
            ]

            accepted = []

            while len(buckets) > 0:
                bucket = buckets.pop()
                # print(f"Checking bucket {bucket}")
                if bucket[0] == "A":
                    accepted.append(bucket)
                    continue
                if bucket[0] == "R":
                    # these ranges do not work
                    continue
                workflow = workflows[bucket[0]]
                bounds = bucket[1]
                for rule in workflow:
                    if ":" in rule:
                        condition = rule.split(":")[0]
                        dest = rule.split(":")[1]
                        if ">" in condition:
                            attr = condition.split(">")[0]
                            val = int(condition.split(">")[1])
                            if bounds[attr][0] >= val:
                                # our entire boundary meets the condition
                                buckets.append([dest, bounds.copy()])
                                break
                            else:
                                # we're somewhere in the middle
                                newBounds = {
                                    # create a shallow copy of the bounds since we are going to reuse
                                    # the original bounds to check other conditions
                                    x: [z for z in y]
                                    for x, y in bounds.items()
                                }
                                newBounds[attr][0] = val
                                # new range from val -> upper
                                buckets.append([dest, newBounds])
                                # remove our range from the current bounds but continue going throught he rest of the workflow
                                bounds[attr][1] = min(bounds[attr][1], val + 1)
                        elif "<" in condition:
                            attr = condition.split("<")[0]
                            val = int(condition.split("<")[1])
                            if bounds[attr][1] <= val:
                                # our entire boundary meets the condition
                                buckets.append([dest, bounds.copy()])
                                break
                            else:
                                newBounds = {
                                    # create a shallow copy of the bounds since we are going to reuse
                                    # the original bounds to check other conditions
                                    x: [z for z in y]
                                    for x, y in bounds.items()
                                }
                                newBounds[attr][1] = val
                                buckets.append([dest, newBounds])
                                bounds[attr][0] = max(bounds[attr][0], val - 1)
                    else:
                        buckets.append([rule, {x: y for x, y in bounds.items()}])
                        break

            totalPermutations = 0
            # print(accepted)
            for x, bounds in accepted:
                permsForPart = 1
                for key, bound in bounds.items():
                    permsForPart *= bound[1] - bound[0] - 1
                totalPermutations += permsForPart
            print(f"Part Two: {totalPermutations}")

        else:
            # Part One
            parts = []
            for part in partLines:
                x, m, a, s = part[1:-1].split(",")
                x = int(x.split("=")[1])
                m = int(m.split("=")[1])
                a = int(a.split("=")[1])
                s = int(s.split("=")[1])
                parts.append(Part(x, m, a, s))

            acceptedParts = []
            for part in parts:
                nextStep = "in"
                while nextStep not in "AR":
                    workflow = workflows[nextStep]
                    for rule in workflow:
                        if ":" in rule:
                            condition = rule.split(":")[0]
                            dest = rule.split(":")[1]

                            if ">" in condition:
                                attr = condition.split(">")[0]
                                val = int(condition.split(">")[1])
                                if getattr(part, attr) > val:
                                    nextStep = dest
                                    break
                            elif "<" in condition:
                                attr = condition.split("<")[0]
                                val = int(condition.split("<")[1])
                                if getattr(part, attr) < val:
                                    nextStep = dest
                                    break
                        else:
                            # we've reached a default
                            nextStep = rule
                if nextStep == "A":
                    acceptedParts.append(part)
            # print(f"There are {len(acceptedParts)} accepted parts: {acceptedParts}")
            sum = 0
            for part in acceptedParts:
                sum += part.x + part.m + part.a + part.s

            print(f"Part One: {sum}")


if __name__ == "__main__":
    filename = "day19/input.txt"
    startTime = time.time()
    main(filename, False)
    print(f"Part One time: {time.time() - startTime:.3f} sec")
    startTime = time.time()
    main(filename, True)
    print(f"Part Two time: {time.time() - startTime:.3f} sec")
