class Pawn:
    def __init__(self, pos, color):
        self.color = color
        self.row, self.col = pos
        self.promotion = False
        self.eligible = []
        self.direction = 1 if self.color == "black" else -1


    def adjacent_capture_possible(self, board):
        """
        Add En passant
        """
        eligible = []
        if board.pieces[self.row + (1 * self.direction)][self.col - (1*self.direction)] != ".":
            if board.pieces[self.row + (1 * self.direction)][self.col - (1*self.direction)].color != self.color:
                eligible.append((self.row + (1 * self.direction), self.col - (1*self.direction)))
                
        if board.pieces[self.row + (1 * self.direction)][self.col + (1*self.direction)]!= ".":
            if board.pieces[self.row + (1 * self.direction)][self.col + (1*self.direction)].color != self.color:
                eligible.append((self.row + (1 * self.direction), self.col + (1*self.direction)))
        return eligible
    
    def eligible_moves(self, board):
        self.eligible = []
        if board.square_is_empty((self.row + (self.direction*1),self.col)):
            self.eligible.append((self.row + (self.direction*1), self.col))
        if (self.row == 1 and self.color == "black") or (self.row == 7 and self.color == "white"): # add forward moves, adjust for foreign objects later
            if board.square_is_empty((self.row + (self.direction*1),self.col)):
                self.eligible.append((self.row + (2 * self.direction), self.col))
        self.eligible = self.eligible + self.adjacent_capture_possible(board)
        return self.eligible

    def is_move_legal(self, pos, board):
        self.eligible = self.eligible_moves(board)
        if pos in self.eligible:
            return True
        return False

    def update_position(self, new_pos):
        self.row, self.col = new_pos
        return