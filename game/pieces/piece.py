class Piece:
    def __init__(self, piece_type, color, position):
        self.piece_type = piece_type
        self.color = color
        self.row, self.col = position

    @property
    def position(self):
        return self.row, self.col

    def move_to(self, position):
        self.row, self.col = position

    def __repr__(self):
        return f"{self.color.capitalize()} {self.piece_type} at {self.position}"