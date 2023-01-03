def convert_to_disjoint_ranges(range_list):
    sorted_ranges = sorted(range_list)
    disjoint_ranges = []

    for r in sorted_ranges:
        if len(disjoint_ranges) == 0:
            disjoint_ranges.append(r)
        elif r.lower <= disjoint_ranges[-1].upper:
            disjoint_ranges[-1] = disjoint_ranges[-1].union(r)[0]
        else:
            disjoint_ranges.append(r)
    return disjoint_ranges


def get_empty_ranges(sensors, row):
    empty_ranges = []

    for sensor in sensors:
        empty_range = sensor.get_empty_range_in_row(row)
        if len(empty_range) > 0:
            empty_ranges.append(empty_range)
    return empty_ranges