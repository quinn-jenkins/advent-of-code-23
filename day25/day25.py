import time
from collections import defaultdict

def main(filename: str, partTwo: bool):
    with open(filename) as file:
        lines = [line.rstrip() for line in file]

    wires = defaultdict(list)
    for line in lines:
        source, connections = line.split(": ")
        connections = connections.split(" ")
        wires[source] = connections
    
    print(wires)



if __name__ == "__main__":
    filename = "day25/example.txt"
    startTime = time.time()
    main(filename, False)
    print(f"Part One time: {time.time() - startTime:.3f} sec")
    # startTime = time.time()
    # main(filename, True)
    # print(f"Part Two time: {time.time() - startTime:.3f} sec")
