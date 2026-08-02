class Pawn:
    def __init__(self, pos, color):
        self.color = color
        self.x, self.y = pos
        self.promotion = False
        self.eligible = []
        self.direction = 1 if self.color == "black" else -1


    def adjacent_capture_possible(self, board):
        """
        Fix this function to check individual squares
        """
        eligible = []
        if board.pieces[self.x + (1 * self.direction)][self.y - (1*self.direction)] != ".":
            if board.pieces[self.x + (1 * self.direction)][self.y - (1*self.direction)].color != self.color:
                eligible.append((self.x + (1 * self.direction), self.y - (1*self.direction)))
                
        if board.pieces[self.x + (1 * self.direction)][self.y + (1*self.direction)]!= ".":
            if board.pieces[self.x + (1 * self.direction)][self.y + (1*self.direction)].color != self.color:
                eligible.append((self.x + (1 * self.direction), self.y + (1*self.direction)))
        return eligible
    
    def eligible_moves(self, board):
        self.eligible = []
        if board.square_is_empty((self.x + (self.direction*1),self.y)):
            self.eligible.append((self.x + (self.direction*1), self.y))
        if (self.x == 1 and self.color == "black") or (self.x == 7 and self.color == "white"): # add forward moves, adjust for foreign objects later
            if board.square_is_empty((self.x + (self.direction*1),self.y)):
                self.eligible.append((self.x + (2 * self.direction), self.y))
        self.eligible = self.eligible + self.adjacent_capture_possible(board)
        return self.eligible

    def is_move_legal(self, pos, board):
        self.eligible = self.eligible_moves(board)
        if pos in self.eligible:
            return True
        return False

    def update_position(self, new_pos):
        self.x, self.y = new_pos
        return