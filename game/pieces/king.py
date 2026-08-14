from .piece import Piece
from ..rules import in_bounds, can_occupy


class King(Piece):
    def __init__(self, color, position):
        super().__init__("king", color, position)

    def pseudo_legal_moves(self, board):
        moves = []
        directions = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        ]
        for dr, dc in directions:
            row = self.row + dr
            col = self.col + dc
            if in_bounds(row, col):
                position = (row, col)
                if can_occupy(self, board, position):
                    moves.append(position)
        return moves