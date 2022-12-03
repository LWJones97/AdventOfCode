class RuckSackFileReader:
    def __init__(self, file_location):
        self.file = open(file_location, 'r')

    def reset(self):
        self.file.seek(0)

    def get_next_item(self, split_compartments=True):
        line = self.file.readline().strip()

        if line == '':
            return None

        if split_compartments:
            compartments = self.__split_compartments(line)
            return compartments
        else:
            return line

    def get_n_items(self, n, split_compartments=True):
        items = [self.get_next_item(split_compartments) for i in range(n)]
        return items

    def __split_compartments(self, line):
        n = len(line)
        compartment_n = int(n / 2)

        compartment1 = line[0:compartment_n]
        compartment2 = line[(compartment_n):]

        return compartment1, compartment2
