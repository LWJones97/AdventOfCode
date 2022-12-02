class ScoreCalculator:
    def __init__(self):
        self.base_values = {"Rock": 1, "Paper": 2, "Scissors": 3}
        self.result_values = {"Win": 6, "Draw": 3, "Loss": 0}
        self.match_ups = {"Rock": {"Rock": "Draw", "Scissors": "Win", "Paper": "Loss"},
                          "Scissors": {"Rock": "Loss", "Scissors": "Draw", "Paper": "Win"},
                          "Paper": {"Rock": "Win", "Scissors": "Loss", "Paper": "Draw"}}
        self.result_choice = {key: {self.__flip_result(value2): key2 for key2, value2 in value.items()} for key, value in self.match_ups.items()}


    def get_score(self, opponent, mine):
        base_value = self.base_values[mine]
        result = self.match_ups[mine][opponent]
        result_value = self.result_values[result]
        return base_value + result_value

    def get_result_score(self, opponent, result):
        mine = self.result_choice[opponent][result]
        return self.get_score(opponent, mine)

    def __flip_result(self, result):
        flip_dict = {"Win": "Loss", "Draw": "Draw", "Loss": "Win"}
        return flip_dict[result]

