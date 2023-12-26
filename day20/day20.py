import time
from collections import defaultdict
from math import lcm


def main(filename: str, partTwo: bool):
    with open(filename) as file:
        lines = [line.rstrip() for line in file]

    # module name (source) with a prefix that notes the type of module (% or &) -> connected modules
    mod_connections = {}
    # module name to the current state. 0 refers to either LOW pulse or OFF, 1 refers to HIGH pulse or ON
    mod_states = {}
    mod_types = {}

    module_before_rx = ""
    for line in lines:
        source = line.split(" -> ")[0]
        destinations = line.split(" -> ")[1].split(", ")
        if "%" in source:
            source = source[1:]
            mod_types[source] = "%"
        elif "&" in source:
            source = source[1:]
            mod_types[source] = "&"
        if "rx" in destinations:
            module_before_rx = source
        mod_connections[source] = destinations
        mod_states[source] = 0

    print(f"Module before RX is: {module_before_rx}")

    conjunction_inputs = defaultdict(dict)
    # for any module that is a Conjunction module (&) we need to find all of the modules that connect to it
    for module in mod_connections:
        if module in mod_types and "&" in mod_types[module]:
            for other_module in mod_connections:
                if module in mod_connections[other_module]:
                    conjunction_inputs[module][other_module] = 0

    if not partTwo:
        numButtonPushes = 1000
        totalPulses = []
        minNumberToRx = 0
        for i in range(numButtonPushes):
            pulses_sent = pushTheButton(
                mod_connections, mod_states, mod_types, conjunction_inputs
            )
            totalPulses.extend(pulses_sent)
            minNumberToRx += 1

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
    else:
        cycles = calculate_cycle_lengths(
            mod_connections, mod_states, mod_types, conjunction_inputs
        )
        p2 = lcm(*cycles.values())
        print(f"Part Two: {p2}")


# count the number of cycles before we send a low signal to each node, and then we'll calculate the LCM of those values
def calculate_cycle_lengths(mod_connections, mod_states, mod_types, conjunction_inputs):
    # big assumption is that there is one conjunction going into RX, and only conjunctions going into that module (LB)
    mod_before_rx = "lb"
    cycle_terminators = []
    for mod in mod_connections:
        if mod_before_rx in mod_connections[mod]:
            cycle_terminators.append(mod)
    cycles = {}
    cycle = 0
    while len(cycles) < len(cycle_terminators):
        cycle += 1
        if cycle % 100000 == 0:
            print(f"Cycle: {cycle}")

        signal_queue = [("button", 0, "broadcaster")]

        while signal_queue:
            sender, input_signal, receiver = signal_queue.pop(0)
            if input_signal == 0 and receiver == "rx":
                print(f"Sent low signal to receiver after {cycle} iterations.")
                exit(0)

            if (
                receiver in cycle_terminators
                and input_signal == 0
                and receiver not in cycles
            ):
                print(f"Reached {receiver} with a low signal after {cycle} cycles")
                cycles[receiver] = cycle

            destinations = []
            if receiver in mod_connections:
                destinations = mod_connections[receiver]
            moduleType = ""
            if receiver in mod_types:
                moduleType = mod_types[receiver]

            outputSignal = 0
            if "%" in moduleType:
                if input_signal == 0:
                    # flip flop modules change their state when they receive a LOW signal
                    old_state = mod_states[receiver]
                    mod_states[receiver] = (old_state + 1) % 2
                    if old_state == 0:
                        # going off -> on sends a HIGH signal (1)
                        outputSignal = 1
                else:
                    # flip flop modules ignore HIGH signals, so break and don't add anything to the queue
                    continue
            elif "&" in moduleType:
                # conjunction modules first update their memory
                mod_states[receiver] = input_signal
                conjunction_inputs[receiver][sender] = input_signal
                # if all inputs most recently sent a HIGH pulse, output a LOW pulse
                inputMods = conjunction_inputs[receiver]
                allHigh = True
                for inputMod in inputMods:
                    if conjunction_inputs[receiver][inputMod] == 0:
                        allHigh = False
                        break
                if allHigh:
                    outputSignal = 0
                # otherwise, send a HIGH pulse
                else:
                    outputSignal = 1

            for destinationMod in destinations:
                signal_queue.append((receiver, outputSignal, destinationMod))

    return cycles


def pushTheButton(mod_connections, mod_states, mod_types, conjunction_inputs):
    pulses_sent = []
    signal_queue = [("button", 0, "broadcaster")]
    while signal_queue:
        sender, input_signal, receiver = signal_queue.pop(0)
        if input_signal == 0 and receiver == "rx":
            return tuple(pulses_sent)
        destinations = []
        if receiver in mod_connections:
            destinations = mod_connections[receiver]
        moduleType = ""
        if receiver in mod_types:
            moduleType = mod_types[receiver]

        outputSignal = 0
        if "%" in moduleType:
            if input_signal == 0:
                # flip flop modules change their state when they receive a LOW signal
                old_state = mod_states[receiver]
                mod_states[receiver] = (old_state + 1) % 2
                if old_state == 0:
                    # going off -> on sends a HIGH signal (1)
                    outputSignal = 1
            else:
                # flip flop modules ignore HIGH signals, so break and don't add anything to the queue
                continue
        elif "&" in moduleType:
            # conjunction modules first update their memory
            mod_states[receiver] = input_signal
            conjunction_inputs[receiver][sender] = input_signal
            # if all inputs most recently sent a HIGH pulse, output a LOW pulse
            inputMods = conjunction_inputs[receiver]
            allHigh = True
            for inputMod in inputMods:
                if conjunction_inputs[receiver][inputMod] == 0:
                    allHigh = False
                    break
            if allHigh:
                outputSignal = 0
            # otherwise, send a HIGH pulse
            else:
                outputSignal = 1

        for destinationMod in destinations:
            signal_queue.append((receiver, outputSignal, destinationMod))
            pulses_sent.append((receiver, outputSignal, destinationMod))
    return tuple(pulses_sent)


if __name__ == "__main__":
    filename = "day20/input.txt"
    start_time = time.time()
    main(filename, False)
    print(f"Part One time: {time.time() - start_time:.3f} sec")
    start_time = time.time()
    main(filename, True)
    print(f"Part Two time: {time.time() - start_time:.3f} sec")
