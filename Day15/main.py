import sys
from ManhattanCoordinate import SensorFileReader
import Helpers

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise Exception("Expected usage: main.py <path to input file>")

    file_location = sys.argv[1]

    sensors = SensorFileReader(file_location).read_sensors()
    beacons = [(sensor.closest_beacon.x, sensor.closest_beacon.y) for sensor in sensors]
    beacons = set(beacons)
    row_to_check = 2000000

    confirmed_empty = 0
    empty_ranges = Helpers.get_empty_ranges(sensors, row_to_check)
    ranges = Helpers.convert_to_disjoint_ranges(empty_ranges)

    for r in ranges:
        confirmed_empty = confirmed_empty + len(r)

    print("The number of confirmed empty squares in row " + str(row_to_check) + " is " + str(confirmed_empty))

    dimension_to_search = 4000000
    point_found = None

    for sensor in sensors:
        perimeter_points = sensor.get_perimeter(dimension_to_search)
        for point in perimeter_points:
            in_range = False
            for comparison_sensor in sensors:
                distance = comparison_sensor.position.distance_to(point)
                if distance <= comparison_sensor.range:
                    in_range = True
                    break
            if not in_range:
                point_found = point
                break
        if not in_range:
            break

    print("The location of the beacon is " + str(point_found) + ".")
