class Decrypter:
    def __init__(self, key):
        self.key = key

    def decrypt(self, value):
        return self.key[value]