import time

TEST_AREA_MIN = 200000000000000
TEST_AREA_MAX = 400000000000000

def main(filename: str, partTwo: bool):
    with open(filename) as file:
        lines = [line.rstrip() for line in file]
    
    hailstones = []
    for line in lines:
        line = line.replace(" @", ",")
        x1, y1, z1, vx, vy, vz = map(int, line.split(", "))
        hailstones.append((x1, y1, z1, vx, vy, vz))

    intersectionPairs = []
    for i, hail1 in enumerate(hailstones):
        for hail2 in hailstones[i+1:]:
            x1,y1,z1,vx1,vy1,vz1 = hail1
            x2,y2,z2,vx2,vy2,vz2 = hail2

            if vy1*vx2 == vy2*vx1: 
                continue

            t1 = (vy2*(x1-x2) - vx2*(y1-y2)) / (vy1*vx2 - vx1*vy2)
            t2 = (vy1*(x2-x1) - vx1*(y2-y1)) / (vy2*vx1 - vx2*vy1)

            if (t1 > 0 and TEST_AREA_MIN < x1+t1*vx1 < TEST_AREA_MAX
                and t2 > 0 and TEST_AREA_MIN < y1+t1*vy1 < TEST_AREA_MAX):
                intersectionPairs.append((hail1, hail2))
    if not partTwo:
        print(f"Part One: {len(intersectionPairs)}")
    


if __name__ == "__main__":
    filename = "day24/input.txt"
    startTime = time.time()
    main(filename, False)
    print(f"Part One time: {time.time() - startTime:.3f} sec")
    # startTime = time.time()
    # main(filename, True)
    # print(f"Part Two time: {time.time() - startTime:.3f} sec")
