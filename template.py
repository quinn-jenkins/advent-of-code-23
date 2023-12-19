import time


def main(filename: str, partTwo: bool):
    with open(filename) as file:
        lines = [line.rstrip() for line in file]


if __name__ == "__main__":
    filename = "day19/example.txt"
    startTime = time.time()
    main(filename, False)
    print(f"Part One time: {time.time() - startTime:.3f} sec")
    # startTime = time.time()
    # main(filename, True)
    # print(f"Part Two time: {time.time() - startTime:.3f} sec")
