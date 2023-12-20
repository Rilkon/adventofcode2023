import math
import pathlib
import sys
from collections import defaultdict, deque


def parse(parsedata):
    modules = {}
    mymodules = {}

    module_types = {
        None: BroadcastModule,
        "%": FlipFlopModule,
        "&": ConjunctionModule
    }

    for line in parsedata.splitlines():
        name, next_modules = line.split(' -> ')
        next_modules = next_modules.split(', ')
        module_type = None if name == 'broadcaster' else name[0]
        name = name[1:] if module_type else name

        newmodule = module_types[module_type](name)
        modules[name] = (module_type, next_modules)
        mymodules[name] = newmodule

    predec = defaultdict(list)

    for modulename, (_, outputs) in modules.items():
        for entry in outputs:
            predec[entry].append(modulename)

    for modulename, module in mymodules.items():
        module.inputs.extend(mymodules[el] for el in predec[modulename])
        module.outputs.extend(mymodules[el] for el in modules[modulename][1] if el in mymodules)

    for name, pre in predec.items():
        if name not in mymodules:
            temp = CommunicationModule(name)
            temp.inputs.extend(pre)
            mymodules[name] = temp
            for el in pre:
                mymodules[el].outputs.append(temp)

    for module in mymodules.values():
        module.init_memory()

    return mymodules


class CommunicationModule():

    def __init__(self, name):
        self.inputs = []
        self.name = name
        self.outputs = []
        self.lowpulses = 0
        self.highpulses = 0

    def send_pulse(self, pulse, sender):
        if pulse:
            self.highpulses += 1
        else:
            self.lowpulses += 1

    def init_memory(self):
        return


class BroadcastModule(CommunicationModule):

    def __init__(self, name):
        super().__init__(name)

    def send_pulse(self, pulse, sender):
        super().send_pulse(pulse, sender)
        for entry in self.outputs:
            entry.send_pulse(pulse, self)


class FlipFlopModule(CommunicationModule):

    def __init__(self, name):
        super().__init__(name)
        self.state = False

    def send_pulse(self, pulse, sender):
        super().send_pulse(pulse, sender)

        if pulse:
            return
        else:
            self.state = not self.state
            for entry in self.outputs:
                entry.send_pulse(self.state, self)


class ConjunctionModule(CommunicationModule):

    def __init__(self, name):
        super().__init__(name)
        self.memory = {}

        for entry in self.inputs:
            self.memory[entry] = False

    def init_memory(self):
        for entry in self.inputs:
            self.memory[entry] = False

    def send_pulse(self, pulse, sender):
        super().send_pulse(pulse, sender)

        self.memory[sender] = pulse

        if all(p for p in self.memory.values()):
            for entry in self.outputs:
                entry.send_pulse(False, self)
        else:
            for entry in self.outputs:
                entry.send_pulse(True, self)


def part1(data):
    mymodules = data.copy()

    low_sum = 0
    high_sum = 0
    q = deque()
    for i in range(1000):
        q.append((None, mymodules["broadcaster"], False))

        # read part 1 wrong, so the whole OO send_pulse stuff is pretty much obsolete
        # and even the class model would not really have been necessary

        while q:
            sender, module, state = q.popleft()
            if state:
                high_sum += 1
            else:
                low_sum += 1
            if isinstance(module, ConjunctionModule):
                module.memory[sender] = state
                state = not all(module.memory.values())
            elif isinstance(module, FlipFlopModule):
                if state:
                    continue
                else:
                    state = not module.state
                    module.state = state

            for next_mod in module.outputs:
                q.append((module, next_mod, state))

    return high_sum * low_sum


def part2(data):
    mymodules = data.copy()

    cycles = []
    values_cycle = ["db", "qx", "gf", "vc"]
    # values_cycle = ["zl", "xf", "xn", "qn"]

    cycle_count = 0

    q = deque()
    for i in range(0, 1_000_000_000_000):
        q.append((None, mymodules["broadcaster"], False))


        while q:
            sender, module, state = q.popleft()

            if module.name in values_cycle:
                if all(module.memory.values()):
                    cycles.append((int(i)))

                    if len(cycles) == 4:
                        result = []
                        for cy in cycles:
                            result.append(cy + 1)

                        return math.lcm(*result), math.lcm(*cycles), math.prod(cycles)

            if isinstance(module, ConjunctionModule):
                module.memory[sender] = state
                state = not all(module.memory.values())
            elif isinstance(module, FlipFlopModule):
                if state:
                    continue
                else:
                    state = not module.state
                    module.state = state

            if module.name == "rx" and not state:
                return i

            for next_mod in module.outputs:
                q.append((module, next_mod, state))

    return i


def solve(puzzle_data):
    data = parse(puzzle_data)
    solution1 = part1(data)
    solution2 = part2(data)
    return solution1, solution2


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"{path}:")
        puzzle_input = pathlib.Path(path).read_text().strip()
        solutions = solve(puzzle_input)
        print("\n".join(str(solution) for solution in solutions))
