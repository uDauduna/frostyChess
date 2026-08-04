from ..ui.sprite import Piece

class Knight:
    def __init__(self, pos, color):
        super.__init__("knight", color, pos)
        self.row, self.col = pos
        self.color = color

    def eligible_moves(self, board):
        self.eligible = []
        if self.in_bounds(self.row - 1, self.col - 2):
            self.eligible.append((self.row - 1, self.col - 2))
        if self.in_bounds(self.row + 1, self.col - 2):
            self.eligible.append((self.row + 1, self.col -2))
        if self.in_bounds(self.row - 2, self.col - 1):
            self.eligible.append((self.row - 2, self.col - 1))
        if self.in_bounds(self.row + 2, self.col - 1):
            self.eligible.append((self.row + 2, self.col - 1))
        if self.in_bounds(self.row - 1, self.col + 2):
            self.eligible.append((self.row - 1, self.col + 2))
        if self.in_bounds(self.row - 2, self.col + 1):
            self.eligible.append((self.row - 2, self.col + 1))
        if self.in_bounds(self.row + 1, self.col + 2):
            self.eligible.append((self.row + 1, self.col + 2))
        if self.in_bounds(self.row + 2, self.col + 1):
            self.eligible.append((self.row + 2, self.col + 1))
        return self.eligible

    def in_bounds(self, row, col):
        if row >= 0 and row < 8:
            if col < 8 and col < 8:
                return True
        return False

    def is_move_legal(self, pos, board):
        self.eligible = self.eligible_moves(board)
        if pos in self.eligible:
            return True
        return False

    def update_position(self, new_pos):
        self.row, self.col = new_pos
        return