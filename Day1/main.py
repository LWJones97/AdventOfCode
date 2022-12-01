import sys
import CalorieFileReader

if __name__ == '__main__':
    if (len(sys.argv) != 2):
        raise Exception("Expected usage: main.py <path to input file>")

    file_location = sys.argv[1]
    file = CalorieFileReader.CalorieFileReader(file_location)

    aggregated_calories = {}

    while True:
        item = file.get_next_item()
        if item is None:
            break
        else:
            aggregated_calories[item["elf"]] = aggregated_calories.get(item["elf"], 0) + item["calories"]


    sorted_calories = sorted(aggregated_calories.values(), key=lambda value: -value)
    print("The maximum calories held by a single elf is " + str(sorted_calories[0]))
    print("The sum of the calories held by the top 3 elves is " + str(sum(sorted_calories[0:3])))

