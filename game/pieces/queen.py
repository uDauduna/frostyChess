from .piece import Piece
from ..rules import sliding_moves


class Queen(Piece):
    def __init__(self, color, position):
        super().__init__("queen", color, position)

    def pseudo_legal_moves(self, board):
        directions = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1),
        ]

        return sliding_moves(self, board, directions)