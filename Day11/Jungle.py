class JungleReader:
    def __init__(self, file_location):
        self.file = open(file_location, 'r')

    def read_jungle(self):
        divisors = self.read_divisors()
        jungle = Jungle(divisors)

        while True:
            monkey = self.read_monkey()
            if monkey is None:
                break
            jungle.add_monkey(monkey["test_divisor"], monkey["operation"], monkey["test"], monkey["starting_items"])

        return jungle

    def read_divisors(self):
        self.file.seek(0)
        divisors = []

        while True:
            line = self.file.readline()
            if line == '':
                break
            else:
                line = line.strip()

            if line.find("Test") == 0:
                divisors.append(self.read_test_divisor(line))

        self.file.seek(0)
        return divisors

    def read_monkey(self):
        line = self.file.readline()

        if line == '':
            return None

        starting_items = self.read_starting_items(self.file.readline().strip())
        operation = self.read_operation(self.file.readline().strip())
        test_divisor = self.read_test_divisor(self.file.readline().strip())
        test_true_monkey = self.read_test_outcome(self.file.readline().strip(), "true")
        test_false_monkey = self.read_test_outcome(self.file.readline().strip(), "false")
        self.file.readline()

        monkey_values = {"test_divisor": test_divisor, "operation": operation,
                         "test": {True: test_true_monkey, False: test_false_monkey},
                         "starting_items": starting_items}
        return monkey_values

    @staticmethod
    def read_starting_items(line):
        items = line.replace("Starting items: ", "")
        items = items.split(",")
        items = [int(item) for item in items]
        return items

    @staticmethod
    def read_operation(line):
        operation = line.replace("Operation: new = old ", "")
        if operation == "* old":
            return {"operator": "**", "value": 2}
        operation = operation.split(" ")
        operation[1] = int(operation[1])
        return {"operator": operation[0], "value": operation[1]}

    @staticmethod
    def read_test_divisor(line):
        test_divisor = int(line.replace("Test: divisible by ", ""))
        return test_divisor

    @staticmethod
    def read_test_outcome(line, outcome):
        outcome = int(line.replace("If " + outcome + ": throw to monkey ", ""))
        return outcome


class Jungle:
    def __init__(self, divisors):
        self.divisors = divisors
        self.monkeys = []

    def add_monkey(self, test_divisor, operation, test_result, starting_items):
        monkey = Monkey(test_divisor, operation, test_result)
        [monkey.add_worry_level(WorryLevel(item, self.divisors)) for item in starting_items]
        self.monkeys.append(monkey)

    def execute_round(self, remainder_method):
        for monkey in self.monkeys:
            while True:
                if remainder_method:
                    item = monkey.inspect_remainders()
                else:
                    item = monkey.inspect()
                if item is None:
                    break
                self.monkeys[item["throw_to"]].add_worry_level(item["worry_level"])

    def execute_rounds(self, n, remainder_method=False):
        for i in range(n):
            self.execute_round(remainder_method)

    def count_inspections(self):
        return [monkey.count_inspections() for monkey in self.monkeys]

    def __repr__(self):
        jungle_string = ""

        for i in range(len(self.monkeys)):
            jungle_string = jungle_string + "Monkey " + str(i) + ": " + str(self.monkeys[i]) + "\n"

        return jungle_string


class Monkey:
    def __init__(self, test_divisor, operation, test_result):
        self.test_divisor = test_divisor
        self.operation = operation
        self.test_result = test_result
        self.worry_levels = []
        self.inspections = 0

    def add_worry_level(self, worry_level):
        self.worry_levels.append(worry_level)

    def inspect(self):
        if len(self.worry_levels) == 0:
            return None

        self.inspections = self.inspections + 1
        self.worry_levels[0].apply_operation(self.operation)
        self.worry_levels[0].reduce_worry_level()
        throw_to = self.test_result[self.test_worry_level(self.worry_levels[0])]

        return {"worry_level": self.worry_levels.pop(0), "throw_to": throw_to}

    def inspect_remainders(self):
        if len(self.worry_levels) == 0:
            return None

        self.inspections = self.inspections + 1
        self.worry_levels[0].apply_operation_to_remainders(self.operation)
        throw_to = self.test_result[self.worry_levels[0].get_remainder(self.test_divisor) == 0]

        return {"worry_level": self.worry_levels.pop(0), "throw_to": throw_to}

    def test_worry_level(self, worry_level):
        return worry_level.value % self.test_divisor == 0

    def count_inspections(self):
        return self.inspections

    def __repr__(self):
        return str(self.worry_levels)


class WorryLevel:
    def __init__(self, value, divisors):
        self.value = value
        self.remainders = {divisor: None for divisor in divisors}
        self.set_remainders(value)

    def set_remainders(self, value):
        for divisor in self.remainders:
            self.remainders[divisor] = value % divisor

    def get_remainder(self, modulo):
        return self.remainders[modulo]

    def apply_operation(self, operation):
        if operation["operator"] == "*":
            self.value = self.value * operation["value"]

        if operation["operator"] == "+":
            self.value = self.value + operation["value"]

        if operation["operator"] == "**":
            self.value = self.value ** operation["value"]

    def apply_operation_to_remainders(self, operation):
        if operation["operator"] == "*":
            for divisor in self.remainders:
                self.remainders[divisor] = (self.remainders[divisor] * operation["value"]) % divisor

        if operation["operator"] == "+":
            for divisor in self.remainders:
                self.remainders[divisor] = (self.remainders[divisor] + operation["value"]) % divisor

        if operation["operator"] == "**":
            for divisor in self.remainders:
                self.remainders[divisor] = (self.remainders[divisor] ** operation["value"]) % divisor

    def reduce_worry_level(self):
        self.value = self.value // 3

    def __repr__(self):
        return str(self.value)
