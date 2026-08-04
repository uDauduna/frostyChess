from ..ui.sprite import Piece

class Queen:
    def __init__(self, pos, color):
        super.__init__("queen", color, pos)
        self.color = color
        self.row, self.col = pos

    def move(self):
        return

    def eligible_moves(self, board):
        self.eligible = []
        row, col = self.row, self.col
        while row < 8 :
            row += 1
            if board.square_is_empty((row, col)):
                self.eligible.append((row, col))
            else:
                if board.pieces[row][col].color != self.color:
                    self.eligible.append((row, col))
                break
        row, col = self.row, self.col
        while row >= 0:
            row -= 1
            if board.square_is_empty((row, col)):
                self.eligible.append((row, col))
            else:
                if board.pieces[row][col].color != self.color:
                    self.eligible.append((row, col))
                break
        row, col = self.row, self.col
        while col < 8:
            col += 1 
            if board.square_is_empty((row, col)):
                self.eligible.append((row, col))
            else:
                if board.pieces[row][col].color != self.color:
                    self.eligible.append((row, col))
                break
        row, col = self.row, self.col
        while col >= 0:
            col -= 1 
            if board.square_is_empty((row, col)):
                self.eligible.append((row, col))
            else:
                if board.pieces[row][col].color != self.color:
                    self.eligible.append((row, col))
                break
        row, col = self.row, self.col
        while (row < 8 and col < 8):
            row += 1
            col += 1 
            if board.square_is_empty((row, col)):
                self.eligible.append((row, col))
            else:
                if board.pieces[row][col].color != self.color:
                    self.eligible.append((row, col))
                break
        row, col = self.row, self.col
        while (row >= 0 and col >= 0):
            row -= 1
            col -= 1 
            if board.square_is_empty((row, col)):
                self.eligible.append((row, col))
            else:
                if board.pieces[row][col].color != self.color:
                    self.eligible.append((row, col))
                break
        row, col = self.row, self.col
        while (row >= 0 and col < 8):
            row -= 1
            col += 1 
            if board.square_is_empty((row, col)):
                self.eligible.append((row, col))
            else:
                if board.pieces[row][col].color != self.color:
                    self.eligible.append((row, col))
                break
        row, col = self.row, self.col
        while (row < 8 and col >= 0):
            row += 1
            col -= 1 
            if board.square_is_empty((row, col)):
                self.eligible.append((row, col))
            else:
                if board.pieces[row][col].color != self.color:
                    self.eligible.append((row, col))
                break
        return self.eligible

    def is_move_legal(self, pos, board):
        self.eligible = self.eligible_moves(board)
        if pos in self.eligible:
            return True
        return False

    def update_position(self, new_pos):
        self.row, self.col = new_pos
        return
