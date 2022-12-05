from Stack import Stacks
import re


class CraneFileReader:
    def __init__(self, file_location):
        self.file = open(file_location, 'r')
        self.instructions_offset = self.__find_instructions()
        self.stacks_height = self.__get_stacks_height()

    def reset(self):
        self.file.seek(0)

    def goto_instructions(self):
        self.file.seek(self.instructions_offset)

    def read_instructions(self):
        self.goto_instructions()

        instructions = []
        while True:
            line = self.file.readline()
            if line is '':
                return instructions
            instructions.append(self.__parse_instruction(line))

    def __parse_instruction(self, instruction):
        move = int(re.sub(r"move (.*) from (.*) to (.*)", r"\1", instruction))
        fro = int(re.sub(r"move (.*) from (.*) to (.*)", r"\2", instruction)) - 1
        to = int(re.sub(r"move (.*) from (.*) to (.*)", r"\3", instruction)) - 1
        return {"move": move, "from": fro, "to": to}

    def read_stacks(self):
        self.reset()
        line = self.file.readline()

        stack_count = int(len(line) / 4)
        self.reset()

        stacks = Stacks(stack_count)

        for crate in range(self.stacks_height):
            for stack in range(stack_count):
                self.file.readline(1)
                crate_label = self.file.readline(1)

                if crate_label is not " ":
                    stacks.add(stack, crate_label)

                self.file.readline(2)

        return stacks

    def __find_instructions(self):
        self.reset()
        offset = 0
        while True:
            line = self.file.readline()
            offset = offset + len(line)

            if line is '\n':
                break

        self.reset()
        return offset

    def __get_stacks_height(self):
        self.reset()
        height = 0
        while True:
            line = self.file.readline()

            if line is '\n':
                break
            else:
                height = height + 1

        return height - 1
