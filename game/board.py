from .constants import BOARD_SIZE
from .pieces import (Pawn, Knight, Bishop, Rook,Queen, King)


class Board:
    def __init__(self):
        self.pieces = [
            [None for _ in range(BOARD_SIZE)]
            for _ in range(BOARD_SIZE)
        ]
        self.initialize_pieces()

    def initialize_pieces(self):
        # Black pieces
        self.pieces[0] = [
            Rook("black", (0, 0)),
            Knight("black", (0, 1)),
            Bishop("black", (0, 2)),
            Queen("black", (0, 3)),
            King("black", (0, 4)),
            Bishop("black", (0, 5)),
            Knight("black", (0, 6)),
            Rook("black", (0, 7)),
        ]

        self.pieces[1] = [
            Pawn("black", (1, col))
            for col in range(BOARD_SIZE)
        ]

        # White pieces
        self.pieces[6] = [
            Pawn("white", (6, col))
            for col in range(BOARD_SIZE)
        ]

        self.pieces[7] = [
            Rook("white", (7, 0)),
            Knight("white", (7, 1)),
            Bishop("white", (7, 2)),
            Queen("white", (7, 3)),
            King("white", (7, 4)),
            Bishop("white", (7, 5)),
            Knight("white", (7, 6)),
            Rook("white", (7, 7)),
        ]

    def get_piece(self, position):
        row, col = position
        return self.pieces[row][col]

    def set_piece(self, position, piece):
        row, col = position
        self.pieces[row][col] = piece

    def remove_piece(self, position):
        row, col = position
        piece = self.pieces[row][col]
        self.pieces[row][col] = None
        return piece

    def is_empty(self, position):
        return self.get_piece(position) is None

    def move_piece(self, start, end):
        piece = self.remove_piece(start)
        if piece is None:
            return None
        captured_piece = self.remove_piece(end)
        piece.move_to(end)
        self.set_piece(end, piece)
        return captured_piece

    def pieces_of_color(self, color):
        result = []
        for row in self.pieces:
            for piece in row:
                if piece is not None and piece.color == color:
                    result.append(piece)
        return result

    def find_king(self, color):
        for row in self.pieces:
            for piece in row:
                if (piece is not None and piece.color == color and piece.piece_type == "king"):
                    return piece
        return None