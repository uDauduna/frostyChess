from .board import Board
from .move import Move
from .rules import is_in_check, threefold_repetition
from .pieces import (Queen, Rook, Bishop, Knight)
import copy
from .position import Position

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
        self.position_history = []
        self.record_position()

    def get_position(self):
        castling_rights = (
        self.castling_rights["white_kingside"],
        self.castling_rights["white_queenside"],
        self.castling_rights["black_kingside"],
        self.castling_rights["black_queenside"],
    )
        return Position(
            board=self.board.get_position_state(),
            turn=self.turn,
            castling_rights=castling_rights,
            en_passant_square=self.en_passant_target,
        )

    def record_position(self):
        position = self.get_position()
        self.position_history.append(position)
        return
        
    def switch_turn(self):
        if self.turn == "white":
            self.turn = "black"
        else:
            self.turn = "white"
        return

    def pseudo_legal_moves(self, position):
        piece = self.board.get_piece(position)
        if piece is None:
            return []
        if piece.color != self.turn:
            return []
        return piece.pseudo_legal_moves(self.board)

    def legal_moves(self, start):
        piece = self.board.get_piece(start)
        if piece is None:
            return []
        if piece.color != self.turn:
            return []
        pseudo_legal_moves = piece.pseudo_legal_moves(self.board)
        legal_moves = []
        for end in pseudo_legal_moves:
            if self.is_move_legal(start, end):
                legal_moves.append(end)
        return legal_moves

    def is_move_legal(self, start, end):
        temp_board = copy.deepcopy(self.board)
        temp_board.move_piece(start, end)
        if is_in_check(temp_board, self.turn):
            return False
        return True

    def make_move(self, start, end):
        piece = self.board.get_piece(start)
        if piece is None:
            return False
        if piece.color != self.turn:
            return False
        moves = self.legal_moves(start)
        if end not in moves:
            return False
        captured_piece = self.board.move_piece(start, end)
        move = Move(start=start,end=end,piece=piece,captured_piece=captured_piece)
        self.move_history.append(move)
        if piece.piece_type == "pawn" and self.is_promotion_rank(piece):
            self.promotion_pending = piece
            return True
        self.switch_turn()
        self.record_position()
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

    def has_legal_moves(self, color=None):
        if color is None:
            color = self.turn
        pieces = self.board.pieces_of_color(color)
        for piece in pieces:
            if self.legal_moves(piece.position):
                return True
        return False

    def is_checkmate(self, color=None):
        if color is None:
            color = self.turn
        if not self.is_in_check(color):
            return False
        return not self.has_legal_moves(color)

    def is_stalemate(self, color=None):
        if color is None:
            color = self.turn
        if self.is_in_check(color):
            return False
        return not self.has_legal_moves(color)

    def is_threefold_repetition(self):
        return threefold_repetition(self.position_history)


    def is_insufficient_material(self):
        if (len(self.board.pieces_of_color("black")) == 1 and len(self.board.pieces_of_color("white")) == 1):
            return True
        return False

    def is_fifty_move_draw(self):
        if len(self.move_history) < 100:
            return False
        return not any(move.resets_fifty_move_counter for move in self.move_history[-100:])

    def is_draw(self):
        return (self.is_stalemate() or self.is_insufficient_material() or self.is_threefold_repetition() or self.is_fifty_move_draw())

    def game_in_progress(self):
        if self.is_checkmate():
            return False
        if self.is_draw():
            return False
        return True