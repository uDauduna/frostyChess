from .piece import Piece
from ..rules import sliding_moves


class Bishop(Piece):
    def __init__(self, color, position):
        super().__init__("bishop", color, position)

    def pseudo_legal_moves(self, board):
        directions = [
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1),
        ]
        return sliding_moves(self, board, directions)