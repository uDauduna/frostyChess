from ..ui.sprite import Piece 

class King(Piece):
    def __init__(self, pos, color):
        super().__init__("king", color, pos)
        self.row, self.col = pos
        self.color = color

    def eligible_moves(self, board):

        """
        Update when you have check discovery etc
        """
        self.eligible = []
        row, col = self.row, self.col

        if board.square_is_empty((row - 1, col - 1)):
            self.eligible.append((row, col))
        else:
            if board.pieces[row][col].color != self.color:
                self.eligible.append((row, col))

        if board.square_is_empty((row - 1, col)):
            self.eligible.append((row, col))
        else:
            if board.pieces[row][col].color != self.color:
                self.eligible.append((row, col))

        if board.square_is_empty((row - 1, col + 1)):
            self.eligible.append((row, col))
        else:
            if board.pieces[row][col].color != self.color:
                self.eligible.append((row, col))

        if board.square_is_empty((row , col - 1)):
            self.eligible.append((row, col))
        else:
            if board.pieces[row][col].color != self.color:
                self.eligible.append((row, col))

        if board.square_is_empty((row, col + 1)):
            self.eligible.append((row, col))
        else:
            if board.pieces[row][col].color != self.color:
                self.eligible.append((row, col))

        if board.square_is_empty((row + 1, col - 1)):
            self.eligible.append((row, col))
        else:
            if board.pieces[row][col].color != self.color:
                self.eligible.append((row, col))

        if board.square_is_empty((row + 1, col)):
            self.eligible.append((row, col))
        else:
            if board.pieces[row][col].color != self.color:
                self.eligible.append((row, col))

        if board.square_is_empty((row + 1, col + 1)):
            self.eligible.append((row, col))
        else:
            if board.pieces[row][col].color != self.color:
                self.eligible.append((row, col))

        return
   
    def is_move_legal(self, pos, board):
        self.eligible = self.eligible_moves(board)
        if pos in self.eligible:
            return True
        return False

    def update_position(self, new_pos):
        self.row, self.y = new_pos
        self.update_board_position(new_pos)
        return

