from .piece import Piece
from ..rules import sliding_moves


class Rook(Piece):
    def __init__(self, color, position):
        super().__init__("rook", color, position)

    def pseudo_legal_moves(self, board):
        directions = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
        ]

        return sliding_moves(self, board, directions)