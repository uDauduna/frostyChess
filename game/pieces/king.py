class King:
    def __init__(self, pos, color):
        self.row, self.y = pos
        self.color = color

    def update_position(self, new_pos):
        self.row, self.y = new_pos
        return