class Pawn:
    def __init__(self, pos, color):
        self.color = color
        self.x, self.y = pos
        self.promotion = False
        self.eligible_moves = []
        self.direction = 1 if self.color == "black" else -1

    def move(self, new_pos, board):
        if self.new_pos in self.eligible_moves(board):
            board.change_state((self.x, self.y), new_pos)
            self.x, self.y = new_pos
        return

    def adjecent_capture_possible(self, board):
        if board.pieces[self.x + (1 * self.direction)][self.y + (1*self.direction)].color != self.color or board.pieces[self.x + (1 * self.direction)][self.y + (1*self.direction)].color != self.color:
            return True
        return False
    
    def eligible_moves(self, board):
        self.eligible_moves = []
        if (self.x == 1 and self.color == "black") or (self.x == 7 and self.color == "white"):
            self.eligible_moves.append((self.x + (self.direction*1), self.y))
            self.eligible_moves.append((self.x + (2 * self.direction), self.y))
        if self.adjecent_capture_possible(board):
            self.eligible_moves.append(self.x + (1 * self.direction), self.y + (1*self.direction))
            self.eligible_moves.append(self.x + (1 * self.direction), self.y + (1*self.direction))
        return self.eligible_moves