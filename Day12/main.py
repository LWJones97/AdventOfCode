import sys
from HeightMap import MapReader
from BreadthFirstSearcher import BreadthFirstSearcher

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise Exception("Expected usage: main.py <path to input file>")

    file_location = sys.argv[1]

    map = MapReader(file_location).read_map()
    searcher = BreadthFirstSearcher(map)
    route_length = searcher.search()
    print("The length of the route to the summit is " + str(route_length))

    backward_map = MapReader(file_location, True).read_map()
    searcher = BreadthFirstSearcher(backward_map)
    route_length = searcher.search()
    print("The length of the most scenic route is " + str(route_length))
