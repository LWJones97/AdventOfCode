class Stack:
    def __init__(self):
        self.crates = []

    def add_to_bottom(self, crate):
        self.crates.insert(0, crate)

    def view_top_crate(self):
        return self.crates[-1]

    def get_top_crates(self, n=1):
        crates = []
        for i in range(n):
            crates.insert(0, self.crates.pop())
        return crates

    def add_to_top(self, crates):
        for crate in crates:
            self.crates.append(crate)

    def __str__(self):
        return str(self.crates)


class Stacks:
    def __init__(self, count):
        self.stacks = [Stack() for i in range(count)]
        self.count = count

    def add(self, stack, crate):
        self.stacks[stack].add_to_bottom(crate)

    def move_one_by_one(self, from_stack, to_stack, times):
        for i in range(times):
            crate = self.stacks[from_stack].get_top_crates()
            self.stacks[to_stack].add_to_top(crate)

    def move_together(self, from_stack, to_stack, times):
        crate = self.stacks[from_stack].get_top_crates(times)
        self.stacks[to_stack].add_to_top(crate)

    def __str__(self):
        string = ""
        for i in range(self.count):
            string = string + str(self.stacks[i]) + '\n'

        return string

    def view_top_crates(self):

        top_crates = ""
        for i in range(self.count):
            top_crates = top_crates + self.stacks[i].view_top_crate()
        return top_crates
