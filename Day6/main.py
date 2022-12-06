import sys
from StreamReader import StreamReader
from DuplicateTracker import DuplicateTracker

def find_first_nondupe_string(n, file_location):
    stream = StreamReader(file_location)
    tracker = DuplicateTracker(n)
    offset = 1

    while True:
        character = stream.read_next()
        tracker.update(character)

        if (not tracker.any_duplicates()) and tracker.is_window_full():
            break
        else:
            offset = offset + 1

    return offset


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise Exception("Expected usage: main.py <path to input file>")

    file_location = sys.argv[1]

    packet_offset = find_first_nondupe_string(4, file_location)
    message_offset = find_first_nondupe_string(14, file_location)

    print("The start of packet is at position " + str(packet_offset) + ".")
    print("The start of message is at position " + str(message_offset) + ".")
