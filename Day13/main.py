import sys
from NestedList import NestedList

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise Exception("Expected usage: main.py <path to input file>")

    file_location = sys.argv[1]
    file = open(file_location, 'r')

    # Part 1
    correct_order_indices = []
    current_pair = 1

    while True:
        line1 = file.readline().strip()
        line2 = file.readline().strip()

        list1 = NestedList(line1)
        list2 = NestedList(line2)

        if list1 < list2:
            correct_order_indices.append(current_pair)
        current_pair = current_pair + 1

        line3 = file.readline()
        if line3 == '':
            break

    print("The number of packets in the right order is " + str(sum(correct_order_indices)) + ".")

    # Part 2
    file.seek(0)
    all_lists = [NestedList("[[2]]"), NestedList("[[6]]")]

    while True:
        line = file.readline()
        if line == '':
            break
        if line == '\n':
            continue
        all_lists.append(NestedList(line))

    # All the effort in part 1 means that we get sorting for free :)
    all_lists = sorted(all_lists)

    divider_locations = []

    for i in range(len(all_lists)):
        if all_lists[i] in (NestedList("[[2]]"), NestedList("[[6]]")):
            divider_locations.append(i + 1)

    print("The product of the divider locations is " + str(divider_locations[0]*divider_locations[1]) + ".")
