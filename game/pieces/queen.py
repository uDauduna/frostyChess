from ..ui.sprite import Piece

class Queen(Piece):
    def __init__(self, pos, color):
        super().__init__("queen", color, pos)
        self.color = color
        self.row, self.col = pos

    def move(self):
        return

    def eligible_moves(self, board):
        self.eligible = []
        row, col = self.row, self.col
        while True:
            row += 1
            if row >= 8:
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
            if row < 0:
                break
            if board.square_is_empty((row, col)):
                self.eligible.append((row, col))
            else:
                if board.pieces[row][col].color != self.color:
                    self.eligible.append((row, col))
                break
        row, col = self.row, self.col
        while True:
            col += 1
            if col >= 8:
                break
            if board.square_is_empty((row, col)):
                self.eligible.append((row, col))
            else:
                if board.pieces[row][col].color != self.color:
                    self.eligible.append((row, col))
                break
        row, col = self.row, self.col
        while True:
            col -= 1
            if col < 0:
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

    def is_move_legal(self, pos, board):
        return pos in self.eligible_moves(board)

    def update_position(self, new_pos):
        self.row, self.col = new_pos
        self.update_board_position(new_pos)
        return
