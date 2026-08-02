class Knight:
    def __init__(self, pos, color):
        self.x, self.y = pos
        self.color = color

    def update_position(self, new_pos):
        self.x, self.y = new_pos
        return