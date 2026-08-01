class Player:
    def __init__(self, color):
        self.color = color
        self.special_moves = {"castling"}
        self.check = False
        self.castle_legal = True
        self.timer = True