from .piece import Piece
from ..rules import in_bounds


class Pawn(Piece):
    def __init__(self, color, position):
        super().__init__("pawn", color, position)
        self.direction = 1 if color == "black" else -1

    def pseudo_legal_moves(self, board):
        moves = []
        one_forward = (self.row + self.direction,self.col)
        if in_bounds(*one_forward) and board.is_empty(one_forward):
            moves.append(one_forward)
            if self.is_on_starting_rank():
                two_forward = (
                    self.row + 2 * self.direction,self.col)
                if (in_bounds(*two_forward)and board.is_empty(two_forward)):
                    moves.append(two_forward)

        for position in self.attack_squares():
            if not in_bounds(*position):
                continue
            target = board.get_piece(position)
            if target is not None and target.color != self.color:
                moves.append(position)
        return moves

    def attack_squares(self):
        return [(self.row + self.direction,self.col - 1),(self.row + self.direction,self.col + 1)]
    def is_on_starting_rank(self):
        if self.color == "white":
            return self.row == 6
        return self.row == 1