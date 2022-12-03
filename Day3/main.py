import sys
from RuckSackFileReader import RuckSackFileReader
import string


def intersect_strings(strings):
    character_sets = [set(string) for string in strings]
    return set.intersection(*character_sets).pop()


LETTER_SCORES = {string.ascii_letters[i]: (i + 1) for i in range(len(string.ascii_letters))}


def part1(file):
    priority_sum = 0

    while True:
        item = file.get_next_item()

        if item is None:
            break

        intersection = intersect_strings(item)
        priority_sum = priority_sum + LETTER_SCORES[intersection]

    print("The sum of priorities is " + str(priority_sum) + ".")


def part2(file):
    priority_sum = 0

    while True:
        item = file.get_n_items(3, False)

        if None in item:
            break

        intersection = intersect_strings(item)
        priority_sum = priority_sum + LETTER_SCORES[intersection]

    print("The sum of priorities is " + str(priority_sum) + ".")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise Exception("Expected usage: main.py <path to input file>")

    file_location = sys.argv[1]
    file = RuckSackFileReader(file_location)
    part1(file)
    file.reset()
    part2(file)
