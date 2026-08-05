from ..ui.sprite import Piece

class Pawn(Piece):
    def __init__(self, pos, color):
        super().__init__("pawn", color, pos)
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
        target_row = self.row + self.direction
        if 0 <= target_row < 8:
            if 0 <= self.col - 1 < 8:
                piece = board.pieces[target_row][self.col - 1]
                if piece != "." and piece.color != self.color:
                    eligible.append((target_row, self.col - 1))
            if 0 <= self.col + 1 < 8:
                piece = board.pieces[target_row][self.col + 1]
                if piece != "." and piece.color != self.color:
                    eligible.append((target_row, self.col + 1))
        return eligible
    
    def eligible_moves(self, board):
        self.eligible = []
        one_forward = (self.row + self.direction, self.col)
        # One-square move
        if (
            0 <= one_forward[0] < 8
            and board.square_is_empty(one_forward)
        ):
            self.eligible.append(one_forward)
            if ((self.color == "black" and self.row == 1) or (self.color == "white" and self.row == 6)):
                two_forward = (self.row + 2 * self.direction, self.col)
                if (
                    0 <= two_forward[0] < 8
                    and board.square_is_empty(two_forward)
                ):
                    self.eligible.append(two_forward)
        self.eligible.extend(self.adjacent_capture_possible(board))
        return self.eligible

    def is_move_legal(self, pos, board):
        return pos in self.eligible_moves(board)

    def update_position(self, new_pos):
        self.row, self.col = new_pos
        self.update_board_position(new_pos)