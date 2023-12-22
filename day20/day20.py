import time
from collections import defaultdict
import functools


def main(filename: str, partTwo: bool):
    with open(filename) as file:
        lines = [line.rstrip() for line in file]

    # module name (source) with a prefix that notes the type of module (% or &) -> connected modules
    modConnections = {}
    # module name to the current state. 0 refers to either LOW pulse or OFF, 1 refers to HIGH pulse or ON
    modStates = {}
    modTypes = {}

    for line in lines:
        source = line.split(" -> ")[0]
        destinations = line.split(" -> ")[1].split(", ")
        if "%" in source:
            source = source[1:]
            modTypes[source] = "%"
        elif "&" in source:
            source = source[1:]
            modTypes[source] = "&"
        print(f"Source: {source} Destination: {destinations}")
        modConnections[source] = destinations
        modStates[source] = 0
        print(f"Source signal: {modStates[source]}")

    conjuctionInputs = defaultdict(dict)
    # for any module that is a Conjunction module (&) we need to find all of the modules that connect to it
    for module in modConnections:
        if module in modTypes and "&" in modTypes[module]:
            print(f"{module} is a conjunction")
            for otherModule in modConnections:
                if module in modConnections[otherModule]:
                    print(
                        f"{otherModule} with connections {modConnections[otherModule]} is connected to {module}"
                    )
                    conjuctionInputs[module][otherModule] = 0
    print(conjuctionInputs)

    numButtonPushes = 1000
    totalPulses = []
    minNumberToRx = 0
    reachedRx = False
    for i in range(numButtonPushes):
        pulsesSent, reachedRx = pushTheButton(
            modConnections, modStates, modTypes, conjuctionInputs
        )
        totalPulses.extend(pulsesSent)
        minNumberToRx += 1

    print(f"Minimum number to RX: {minNumberToRx}")

    numHigh = 0
    numLow = numButtonPushes  # each button push adds a low signal
    for pulse in totalPulses:
        if pulse[1] == 0:
            numLow += 1
        else:
            numHigh += 1

    print(
        f"There were {numLow} low pulses and {numHigh} high pulses. Total {numLow * numHigh}"
    )


def pushTheButton(modConnections, modStates, modTypes, conjuctionInputs):
    pulsesSent = []
    signalQueue = [("button", 0, "broadcaster")]
    while signalQueue:
        sender, inputSignal, receiver = signalQueue.pop(0)
        # print(f" -- Processing signal {sender} --{inputSignal}-> {receiver}")
        if inputSignal == 0 and receiver == "rx":
            return tuple(pulsesSent), True
        destinations = []
        if receiver in modConnections:
            destinations = modConnections[receiver]
        moduleType = ""
        if receiver in modTypes:
            moduleType = modTypes[receiver]

        outputSignal = 0
        if "%" in moduleType:
            if inputSignal == 0:
                # flip flop modules change their state when they receive a LOW signal
                oldState = modStates[receiver]
                modStates[receiver] = (oldState + 1) % 2
                # print(
                #     f"Flip Flop {receiver} switching from {oldState} to {modStates[receiver]}"
                # )
                if oldState == 0:
                    # going off -> on sends a HIGH signal (1)
                    outputSignal = 1
            else:
                # flip flop modules ignore HIGH signals, so break and don't add anything to the queue
                # print(f"Flip Flop Module {receiver} ignoring HIGH signal")
                continue
        elif "&" in moduleType:
            # conjunction modules first update their memory
            modStates[receiver] = inputSignal
            conjuctionInputs[receiver][sender] = inputSignal
            # if all inputs most recently sent a HIGH pulse, output a LOW pulse
            inputMods = conjuctionInputs[receiver]
            allHigh = True
            for inputMod in inputMods:
                if conjuctionInputs[receiver][inputMod] == 0:
                    allHigh = False
                    # print(
                    #     f"One or more inputs did not send a HIGH pulse -- sending HIGH"
                    # )
                    break
            if allHigh:
                # print(f"All inputs to {receiver} are HIGH -- sending LOW")
                outputSignal = 0
            # otherwise, send a HIGH pulse
            else:
                outputSignal = 1

        for destinationMod in destinations:
            # print(f"{receiver} --{outputSignal}--> {destinationMod}")
            signalQueue.append((receiver, outputSignal, destinationMod))
            pulsesSent.append((receiver, outputSignal, destinationMod))
    return tuple(pulsesSent), False


if __name__ == "__main__":
    filename = "day20/input.txt"
    startTime = time.time()
    main(filename, False)
    print(f"Part One time: {time.time() - startTime:.3f} sec")
    # startTime = time.time()
    # main(filename, True)
    # print(f"Part Two time: {time.time() - startTime:.3f} sec")
