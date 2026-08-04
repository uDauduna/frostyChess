from ..ui.sprite import Piece 

class King(Piece):
    def __init__(self, pos, color):
        super().__init__("king", color, pos)
        self.row, self.y = pos
        self.color = color

    def update_position(self, new_pos):
        self.row, self.y = new_pos
        return