class RockPaperScissorsFileReader:
    def __init__(self, file_location):
        self.file = open(file_location, 'r')

    def get_next_item(self):
        opponent = self.file.readline(1)
        self.file.readline(1)
        mine = self.file.readline(1)
        self.file.readline(1)

        if (opponent == ''):
            return None
        else:
            return {"opponent": opponent, "mine": mine}



