import copy


class CPUInstructor:
    def __init__(self, file_location):
        self.instructions = open(file_location, 'r')
        self.cpu = CPU()
        self.execution_times = {"addx": 2, "noop": 1}

    def execute_instructions_with_polling(self, initial_poll, poll_interval):
        polled_cpus = []
        instruction_completed = True
        while True:
            if instruction_completed:
                instruction = self.next_instruction()
                if instruction is None:
                    break
                self.cpu.start_instruction(instruction, self.execution_times[instruction[0]])
            polled_cpus = self.poll_cpus(polled_cpus, initial_poll, poll_interval)
            instruction_completed = self.cpu.next_cycle()
        return polled_cpus

    def poll_cpus(self, polled_cpus, initial_poll, poll_interval):
        cycles_past_initial = self.cpu.clock.cycle - initial_poll
        if cycles_past_initial >= 0 and (cycles_past_initial == 0 or cycles_past_initial % poll_interval == 0):
            polled_cpus.append(copy.deepcopy(self.cpu))
        return polled_cpus

    def draw_crt(self, width):
        instruction_completed = True
        while True:
            if instruction_completed:
                instruction = self.next_instruction()
                if instruction is None:
                    break
                self.cpu.start_instruction(instruction, self.execution_times[instruction[0]])
            self.draw_pixel(width)
            instruction_completed = self.cpu.next_cycle()

    def draw_pixel(self, width):
        if ((self.cpu.clock.cycle - 1) % width) == 0:
            print()
        if self.is_visible():
            print('▮', end='')
        else:
            print('▯', end='')

    def is_visible(self):
        sprite_centre = self.cpu.X.value
        sprite_pixels = (sprite_centre - 1, sprite_centre, sprite_centre + 1)
        column = (self.cpu.clock.cycle - 1) % 40
        return column in sprite_pixels

    def next_instruction(self):
        instruction = self.instructions.readline().strip()
        if instruction == '':
            return None
        else:
            return self.parse_instruction(instruction)

    @staticmethod
    def parse_instruction(instruction):
        instruction = instruction.split(" ")
        if len(instruction) == 2:
            instruction[1] = int(instruction[1])
        return instruction


class CPU:
    def __init__(self):
        self.X = Register()
        self.clock = ClockCircuit()
        self.instruction = None
        self.instruction_time = None

    def start_instruction(self, instruction, time):
        self.instruction = instruction
        self.instruction_time = time

    def next_cycle(self):
        self.clock.increment()
        self.instruction_time = self.instruction_time - 1
        completed = False

        if self.instruction_time == 0:
            self.execute_instruction(self.instruction)
            completed = True
        return completed

    def execute_instruction(self, instruction):
        if instruction[0] == "addx":
            self.X.addx(instruction[1])


class ClockCircuit:
    def __init__(self):
        self.cycle = 1

    def increment(self):
        self.cycle = self.cycle + 1


class Register:
    def __init__(self):
        self.value = 1

    def addx(self, V):
        self.value = self.value + V
