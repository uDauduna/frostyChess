from .board import Board
from .move import Move
from .rules import is_in_check
from .pieces import (Queen, Rook, Bishop, Knight)


class ChessGame:
    def __init__(self):
        self.board = Board()
        self.turn = "white"
        self.move_history = []
        self.en_passant_target = None
        self.castling_rights = {
            "white_kingside": True,
            "white_queenside": True,
            "black_kingside": True,
            "black_queenside": True,
        }
        self.promotion_pending = None

    def switch_turn(self):
        if self.turn == "white":
            self.turn = "black"
        else:
            self.turn = "white"

    def pseudo_legal_moves(self, position):
        piece = self.board.get_piece(position)
        if piece is None:
            return []
        if piece.color != self.turn:
            return []
        return piece.pseudo_legal_moves(self.board)

    def make_move(self, start, end):
        piece = self.board.get_piece(start)
        if piece is None:
            return False
        if piece.color != self.turn:
            return False
        moves = piece.pseudo_legal_moves(self.board)
        if end not in moves:
            return False
        captured_piece = self.board.move_piece(start, end)
        move = Move(start=start,end=end,piece=piece,captured_piece=captured_piece)
        self.move_history.append(move)
        if piece.piece_type == "pawn":
            if self.is_promotion_rank(piece):
                self.promotion_pending = piece
                return True
        self.switch_turn()
        return True

    def promote(self, piece_type):
        if self.promotion_pending is None:
            return False
        pawn = self.promotion_pending
        position = pawn.position
        pieces = {
            "q": Queen,
            "r": Rook,
            "b": Bishop,
            "n": Knight,
        }
        piece_class = pieces.get(piece_type.lower())
        if piece_class is None:
            return False
        new_piece = piece_class(pawn.color, position)
        self.board.set_piece(position, new_piece)
        self.move_history[-1].promotion = piece_type.lower()
        self.promotion_pending = None
        self.switch_turn()
        return True

    def is_promotion_rank(self, pawn):
        if pawn.color == "white":
            return pawn.row == 0
        return pawn.row == 7

    def is_in_check(self, color=None):
        if color is None:
            color = self.turn
        return is_in_check(self.board, color)

    def current_player_in_check(self):
        return self.is_in_check(self.turn)