import sys
from Jungle import JungleReader

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise Exception("Expected usage: main.py <path to input file>")

    file_location = sys.argv[1]

    jungle_reader = JungleReader(file_location)
    jungle = jungle_reader.read_jungle()

    jungle.execute_rounds(20)
    inspections = jungle.count_inspections()
    inspections = sorted(inspections, reverse=True)
    print("The level of monkey business is " + str(inspections[0]*inspections[1]))

    jungle_reader = JungleReader(file_location)
    jungle = jungle_reader.read_jungle()
    jungle.execute_rounds(10000, True)
    inspections = jungle.count_inspections()
    inspections = sorted(inspections, reverse=True)
    print("The level of monkey business is " + str(inspections[0]*inspections[1]))



