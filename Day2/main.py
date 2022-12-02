import sys
import RockPaperScissorsFileReader
import Decrypter
import ScoreCalculator

OPPONENT_KEY = {"A": "Rock", "B": "Paper", "C": "Scissors"}
MY_KEY = {"X": "Rock", "Y": "Paper", "Z": "Scissors"}
RESULT_KEY = {"X": "Loss", "Y": "Draw", "Z": "Win"}

if __name__ == '__main__':
    if (len(sys.argv) != 2):
        raise Exception("Expected usage: main.py <path to input file>")

    file_location = sys.argv[1]
    file = RockPaperScissorsFileReader.RockPaperScissorsFileReader(file_location)

    my_decrypter = Decrypter.Decrypter(MY_KEY)
    opponent_decrypter = Decrypter.Decrypter(OPPONENT_KEY)
    result_decrypter = Decrypter.Decrypter(RESULT_KEY)

    score_calculator = ScoreCalculator.ScoreCalculator()

    score = 0
    result_score = 0

    while True:
        match = file.get_next_item()

        if match is None:
            break

        match["opponent"] = opponent_decrypter.decrypt(match["opponent"])

        result_match = match.copy()
        match["mine"] = my_decrypter.decrypt(match["mine"])
        result_match["mine"] = result_decrypter.decrypt(result_match["mine"])

        score = score + score_calculator.get_score(match["opponent"], match["mine"])
        result_score = result_score + score_calculator.get_result_score(result_match["opponent"], result_match["mine"])

    print("The final score is " + str(score) + ".")
    print("The final score, interpreting the second column as the result to achieve, is " + str(result_score) + ".")
