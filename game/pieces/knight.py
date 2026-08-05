from ..ui.sprite import Piece

class Knight(Piece):
    def __init__(self, pos, color):
        super().__init__("knight", color, pos)
        self.row, self.col = pos
        self.color = color

    def safe_to_occupy(self, board, r, c):
        if board.square_is_empty((r, c)):
            return True
        else:
            if board.pieces[r][c].color != self.color:
                return True
        return False

    def eligible_moves(self, board):
        self.eligible = []
        if self.in_bounds(self.row - 1, self.col - 2):
            if self.safe_to_occupy(board, self.row - 1, self.col - 2):
                self.eligible.append((self.row - 1, self.col - 2))
        if self.in_bounds(self.row + 1, self.col - 2):
            if self.safe_to_occupy(board, self.row + 1, self.col - 2):
                self.eligible.append((self.row + 1, self.col -2))
        if self.in_bounds(self.row - 2, self.col - 1):
            if self.safe_to_occupy(board, self.row - 2, self.col - 1):
                self.eligible.append((self.row - 2, self.col - 1))
        if self.in_bounds(self.row + 2, self.col - 1):
            if self.safe_to_occupy(board,self.row + 2, self.col - 1 ):
                self.eligible.append((self.row + 2, self.col - 1))
        if self.in_bounds(self.row - 1, self.col + 2):
            if self.safe_to_occupy(board, self.row - 1, self.col + 2):
                self.eligible.append((self.row - 1, self.col + 2))
        if self.in_bounds(self.row - 2, self.col + 1):
            if self.safe_to_occupy(board,self.row - 2, self.col + 1 ):
                self.eligible.append((self.row - 2, self.col + 1))
        if self.in_bounds(self.row + 1, self.col + 2 ):
            if self.safe_to_occupy(board, self.row + 1, self.col + 2 ):
                self.eligible.append((self.row + 1, self.col + 2))
        if self.in_bounds(self.row + 2, self.col + 1):
            if self.safe_to_occupy(board, self.row + 2, self.col + 1):
                self.eligible.append((self.row + 2, self.col + 1))
        print(self.eligible)
        return self.eligible

    def in_bounds(self, row, col):
        if row >= 0 and row < 8:
            if col < 8 and col >= 0:
                return True
        return False

    def is_move_legal(self, pos, board):
        return pos in self.eligible_moves(board)

    def update_position(self, new_pos):
        self.row, self.col = new_pos
        self.update_board_position(new_pos)
        return