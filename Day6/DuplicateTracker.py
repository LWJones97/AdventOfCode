import string

class DuplicateTracker:
    def __init__(self, n):
        self.character_window = CharacterWindow(n)
        self.character_count = {letter: 0 for letter in string.ascii_lowercase}
        self.duplicates = set()
        self.update_count = 0
        self.n = n

    def update(self, character):
        removed = self.character_window.push(character)
        self.update_character_count(character, removed)
        self.update_duplicates(character, removed)
        self.update_count = self.update_count + 1

    def update_character_count(self, added, removed):
        self.character_count[added] = self.character_count[added] + 1
        if removed is not None:
            self.character_count[removed] = self.character_count[removed] - 1

    def update_duplicates(self, added, removed):
        if self.character_count[added] > 1:
            self.duplicates.add(added)
        if removed is not None:
            if self.character_count[removed] <= 1:
                self.duplicates.discard(removed)

    def any_duplicates(self):
        return len(self.duplicates) > 0

    def is_window_full(self):
        return self.update_count >= self.n


class CharacterWindow:
    def __init__(self, n):
        self.window = []
        self.n = n

    def push(self, character):
        removed = None
        if len(self.window) >= self.n:
            removed = self.window.pop()
        self.window.insert(0, character)
        return removed

