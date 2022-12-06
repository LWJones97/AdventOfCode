class StreamReader:
    def __init__(self, file_location):
        self.file = open(file_location, 'r')

    def read_next(self):
        character = self.file.readline(1).strip()

        if character is '':
            return None
        else:
            return character

