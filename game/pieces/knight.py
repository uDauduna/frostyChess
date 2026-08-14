from .piece import Piece
from ..rules import in_bounds, can_occupy


class Knight(Piece):
    def __init__(self, color, position):
        super().__init__("knight", color, position)

    def pseudo_legal_moves(self, board):
        moves = []

        offsets = [
            (-2, -1),
            (-2, 1),
            (-1, -2),
            (-1, 2),
            (1, -2),
            (1, 2),
            (2, -1),
            (2, 1),
        ]

        for dr, dc in offsets:
            row = self.row + dr
            col = self.col + dc

            if in_bounds(row, col):
                position = (row, col)

                if can_occupy(self, board, position):
                    moves.append(position)

        return moves