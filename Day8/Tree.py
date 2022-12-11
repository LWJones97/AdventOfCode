class Tree:
    def __init__(self, height):
        self.height = height
        self.is_visible = False

    def update_visibility(self, max_height):
        if self.height > max_height:
            self.is_visible = True
            return self.height
        return max_height

    def get_visibility(self):
        return self.is_visible