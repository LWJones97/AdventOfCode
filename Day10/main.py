import sys
from CPU import CPUInstructor

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise Exception("Expected usage: main.py <path to input file>")

    file_location = sys.argv[1]

    poller = CPUInstructor(file_location)
    polled_cpus = poller.execute_instructions_with_polling(20, 40)

    signal_strength = 0

    for i in range(6):
        signal_strength = signal_strength + polled_cpus[i].clock.cycle * polled_cpus[i].X.value

    print("The sum of signal strengths is " + str(signal_strength) + ".")

    illustrator = CPUInstructor(file_location)
    illustrator.draw_crt(40)
