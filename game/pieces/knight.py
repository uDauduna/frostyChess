class Knight:
    def __init__(self, pos, color):
        self.x, self.y = pos
        self.color = color

    def eligible_moves(self, board):
        self.eligible = []
        if self.in_bounds(self.x - 1, self.y - 2):
            self.eligible.append((self.x - 1, self.y - 2))
        if self.in_bounds(self.x + 1, self.y - 2):
            self.eligible.append((self.x + 1, self.y -2))
        if self.in_bounds(self.x - 2, self.y - 1):
            self.eligible.append((self.x - 2, self.y - 1))
        if self.in_bounds(self.x + 2, self.y - 1):
            self.eligible.append((self.x + 2, self.y - 1))
        if self.in_bounds(self.x - 1, self.y + 2):
            self.eligible.append((self.x - 1, self.y + 2))
        if self.in_bounds(self.x - 2, self.y + 1):
            self.eligible.append((self.x - 2, self.y + 1))
        if self.in_bounds(self.x + 1, self.y + 2):
            self.eligible.append((self.x + 1, self.y + 2))
        if self.in_bounds(self.x + 2, self.y + 1):
            self.eligible.append((self.x + 2, self.y + 1))
        return self.eligible

    def in_bounds(self, x, y):
        if x >= 0 and x < 8:
            if y < 8 and y < 8:
                return True
        return False

    def is_move_legal(self, pos, board):
        self.eligible = self.eligible_moves(board)
        if pos in self.eligible:
            return True
        return False

    def update_position(self, new_pos):
        self.x, self.y = new_pos
        return