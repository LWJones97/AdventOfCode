import sys
from RangeFileReader import RangeFileReader


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise Exception("Expected usage: main.py <path to input file>")

    file_location = sys.argv[1]
    file = RangeFileReader(file_location)
    fully_contained_count = 0
    overlap_count = 0

    while True:
        ranges = file.get_next_item()
        if ranges is None:
            break

        fully_contained = int(ranges[0].contains(ranges[1]) or ranges[1].contains(ranges[0]))
        fully_contained_count = fully_contained_count + fully_contained
        overlap_count = overlap_count + int(ranges[0].overlaps(ranges[1]))

    print(str(fully_contained_count) + " of the ranges fully intersect.")
    print(str(overlap_count) + " of the ranges overlap.")
