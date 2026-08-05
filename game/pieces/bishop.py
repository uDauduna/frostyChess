from ..ui.sprite import Piece

class Bishop(Piece):
    def __init__(self, pos, color):
        super().__init__("bishop",color, pos)
        self.row, self.col = pos
        self.color = color
        self.eligible = []

    def eligible_moves(self, board):
        self.eligible = []
        row, col = self.row, self.col
        while True:
            row += 1
            col += 1
            if row >= 8 or col >= 8:
                break
            if board.square_is_empty((row, col)):
                self.eligible.append((row, col))
            else:
                if board.pieces[row][col].color != self.color:
                    self.eligible.append((row, col))
                break
        row, col = self.row, self.col
        while True:
            row -= 1
            col -= 1
            if row < 0 or col < 0:
                break
            if board.square_is_empty((row, col)):
                self.eligible.append((row, col))
            else:
                if board.pieces[row][col].color != self.color:
                    self.eligible.append((row, col))
                break
        row, col = self.row, self.col
        while True:
            row -= 1
            col += 1
            if row < 0 or col >= 8:
                break
            if board.square_is_empty((row, col)):
                self.eligible.append((row, col))
            else:
                if board.pieces[row][col].color != self.color:
                    self.eligible.append((row, col))
                break
        row, col = self.row, self.col
        while True:
            row += 1
            col -= 1
            if row >= 8 or col < 0:
                break
            if board.square_is_empty((row, col)):
                self.eligible.append((row, col))
            else:
                if board.pieces[row][col].color != self.color:
                    self.eligible.append((row, col))
                break

        return self.eligible

    def in_bounds(self, row, col):
        if row >= 0 and row < 8:
            if col >=0 and col < 8:
                return True
        return False

    def is_move_legal(self, pos, board):
        return pos in self.eligible_moves(board)

    def update_position(self, new_pos):
        self.row, self.col = new_pos
        self.update_board_position(new_pos)
        return
