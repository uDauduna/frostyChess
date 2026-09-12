"""Core chess game state and rules.

The UI is intentionally not coupled to this class.  This makes ChessGame suitable
for Pygame, a CLI, self-play, search algorithms, and ML data generation.
"""
import copy

from .board import Board
from .move import Move
from .rules import is_in_check, threefold_repetition
from .pieces import Queen, Rook, Bishop, Knight, Pawn, King
from .position import Position
from .fen import board_to_fen, load_fen
from .notation import san_for_move, uci_to_move, move_to_uci

PIECE_CLASSES = {
    "queen": Queen, "rook": Rook, "bishop": Bishop,
    "knight": Knight, "pawn": Pawn, "king": King,
}

class ChessGame:
    def __init__(self, fen=None):
        self.board = Board()
        self.turn = "white"
        self.move_history = []
        self.san_history = []
        self.position_history = []
        self.en_passant_target = None
        self.castling_rights = {
            "white_kingside": True, "white_queenside": True,
            "black_kingside": True, "black_queenside": True,
        }
        self.promotion_pending = None
        self.halfmove_clock = 0
        self.fullmove_number = 1
        self.pieces_captured_by_black = []
        self.pieces_captured_by_white = []
        self.piece_values = {"pawn": 1, "knight": 3, "bishop": 3, "rook": 5, "queen": 9, "king": 0}
        self._undo_stack = []
        if fen:
            load_fen(self, fen)
        else:
            self.record_position()
            self.initial_fen = self.to_fen()

    @classmethod
    def from_fen(cls, fen):
        return load_fen(cls(), fen)

    def to_fen(self):
        return board_to_fen(self)

    def clone(self):
        result = copy.deepcopy(self)
        result._undo_stack = []
        return result

    def is_square_attacked(self, square, by_color):
        for piece in self.board.pieces_of_color(by_color):
            if piece.piece_type == "pawn":
                if square in piece.attack_squares():
                    return True
            elif square in piece.pseudo_legal_moves(self.board):
                return True
        return False

    def opposite_color(self, color):
        return "black" if color == "white" else "white"

    def perform_castling(self, start, end):
        king = self.board.get_piece(start)
        row, king_col = start
        _, target_col = end
        rook_start = (row, 7) if target_col > king_col else (row, 0)
        rook_end = (row, 5) if target_col > king_col else (row, 3)
        rook = self.board.get_piece(rook_start)
        self.board.pieces[row][king_col] = None
        king.move_to(end)
        self.board.pieces[end[0]][end[1]] = king
        self.board.pieces[rook_start[0]][rook_start[1]] = None
        rook.move_to(rook_end)
        self.board.pieces[rook_end[0]][rook_end[1]] = rook
        return rook

    def can_castle(self, start, end):
        if not self.is_castling_move(start, end):
            return False
        king = self.board.get_piece(start)
        row, col = start
        target_col = end[1]
        kingside = target_col > col
        rook_col = 7 if kingside else 0
        empty_columns = [5, 6] if kingside else [1, 2, 3]
        king_path = [(row, 5), (row, 6)] if kingside else [(row, 3), (row, 2)]
        rook = self.board.get_piece((row, rook_col))
        if rook is None or rook.piece_type != "rook" or rook.color != king.color:
            return False
        if any(self.board.get_piece((row, c)) is not None for c in empty_columns):
            return False
        opponent = self.opposite_color(king.color)
        if self.is_square_attacked(start, opponent):
            return False
        return not any(self.is_square_attacked(square, opponent) for square in king_path)

    def is_castling_move(self, start, end):
        piece = self.board.get_piece(start)
        if piece is None or piece.piece_type != "king" or piece.color != self.turn:
            return False
        row, col = start
        if row != end[0] or abs(end[1] - col) != 2:
            return False
        side = "kingside" if end[1] > col else "queenside"
        return self.castling_rights[f"{piece.color}_{side}"]

    def is_en_passant_move(self, source, target):
        if self.en_passant_target != target:
            return False
        piece = self.board.get_piece(source)
        if piece is None or piece.piece_type != "pawn" or piece.color != self.turn:
            return False
        if abs(target[0] - source[0]) != 1 or abs(target[1] - source[1]) != 1:
            return False
        captured = self.board.get_piece((source[0], target[1]))
        return captured is not None and captured.piece_type == "pawn" and captured.color != piece.color

    def perform_en_passant(self, start, end):
        pawn = self.board.get_piece(start)
        captured_position = (start[0], end[1])
        captured_piece = self.board.get_piece(captured_position)
        if pawn is None or captured_piece is None:
            return None
        self.board.remove_piece(captured_position)
        self.board.remove_piece(start)
        pawn.move_to(end)
        self.board.set_piece(end, pawn)
        return captured_piece

    def update_en_passant_target(self, start, end, piece):
        self.en_passant_target = None
        if piece.piece_type == "pawn" and abs(end[0] - start[0]) == 2:
            self.en_passant_target = ((start[0] + end[0]) // 2, start[1])

    def update_castling_rights(self, piece, start, captured_piece, end):
        color = piece.color
        if piece.piece_type == "king":
            self.castling_rights[f"{color}_kingside"] = False
            self.castling_rights[f"{color}_queenside"] = False
        elif piece.piece_type == "rook":
            mapping = {
                ("white", (7, 0)): "white_queenside", ("white", (7, 7)): "white_kingside",
                ("black", (0, 0)): "black_queenside", ("black", (0, 7)): "black_kingside",
            }
            key = mapping.get((color, start))
            if key: self.castling_rights[key] = False
        if captured_piece and captured_piece.piece_type == "rook":
            mapping = {
                ("white", (7, 0)): "white_queenside", ("white", (7, 7)): "white_kingside",
                ("black", (0, 0)): "black_queenside", ("black", (0, 7)): "black_kingside",
            }
            key = mapping.get((captured_piece.color, end))
            if key: self.castling_rights[key] = False

    def get_position(self):
        return Position(
            board=self.board.get_position_state(),
            turn=self.turn,
            castling_rights=(
                self.castling_rights["white_kingside"], self.castling_rights["white_queenside"],
                self.castling_rights["black_kingside"], self.castling_rights["black_queenside"],
            ),
            en_passant_square=self.en_passant_target,
        )

    def record_position(self):
        self.position_history.append(self.get_position())

    def switch_turn(self):
        self.turn = self.opposite_color(self.turn)

    def pseudo_legal_moves(self, position):
        piece = self.board.get_piece(position)
        if piece is None or piece.color != self.turn:
            return []
        moves = piece.pseudo_legal_moves(self.board)
        if piece.piece_type == "pawn" and self.en_passant_target and self.is_en_passant_move(position, self.en_passant_target):
            if self.en_passant_target not in moves:
                moves.append(self.en_passant_target)
        if piece.piece_type == "king":
            for target in ((piece.row, piece.col + 2), (piece.row, piece.col - 2)):
                if 0 <= target[1] < 8 and self.can_castle(position, target):
                    moves.append(target)
        return moves

    def legal_moves(self, start):
        piece = self.board.get_piece(start)
        if piece is None or piece.color != self.turn:
            return []
        return [end for end in self.pseudo_legal_moves(start) if self.is_move_legal(start, end)]

    def legal_move_pairs(self, color=None):
        original = self.turn
        if color is not None: self.turn = color
        try:
            return [(piece.position, end) for piece in self.board.pieces_of_color(self.turn)
                    for end in self.legal_moves(piece.position)]
        finally:
            self.turn = original

    def is_move_legal(self, start, end):
        temp = self.clone()
        piece = temp.board.get_piece(start)
        if piece is None: return False
        if temp.is_en_passant_move(start, end):
            temp.perform_en_passant(start, end)
        elif temp.is_castling_move(start, end):
            if not temp.can_castle(start, end): return False
            temp.perform_castling(start, end)
        else:
            temp.board.move_piece(start, end)
        return not is_in_check(temp.board, self.turn)

    def _save_undo_state(self):
        snapshot = self.clone()
        snapshot._undo_stack = []
        self._undo_stack.append(snapshot)

    def make_move(self, start, end, promotion=None):
        piece = self.board.get_piece(start)
        if piece is None or piece.color != self.turn or end not in self.legal_moves(start):
            return False
        if piece.piece_type == "pawn" and self.is_promotion_rank_for_target(piece, end):
            if promotion and promotion.lower() in ("queen", "rook", "bishop", "knight", "q", "r", "b", "n"):
                self._save_undo_state()
                return self._make_move_internal(start, end, promotion)
            self._save_undo_state()
            self._make_move_internal(start, end, None, finalize=False)
            self.promotion_pending = self.board.get_piece(end)
            return True
        self._save_undo_state()
        return self._make_move_internal(start, end, promotion)

    def _make_move_internal(self, start, end, promotion=None, finalize=True):
        piece = self.board.get_piece(start)
        san = san_for_move(self, start, end, promotion)
        previous_ep = self.en_passant_target
        previous_castling = self.castling_rights.copy()
        previous_halfmove = self.halfmove_clock
        previous_fullmove = self.fullmove_number
        is_ep = self.is_en_passant_move(start, end)
        is_castle = self.is_castling_move(start, end)
        if is_ep:
            captured = self.perform_en_passant(start, end)
        elif is_castle:
            captured = None
            self.perform_castling(start, end)
        else:
            captured = self.board.move_piece(start, end)
        self.store_captured_pieces(captured)
        self.update_castling_rights(piece, start, captured, end)
        self.update_en_passant_target(start, end, piece)

        move = Move(start, end, piece, captured, promotion, is_castle, is_ep,
                    previous_ep, previous_castling, previous_halfmove, previous_fullmove)
        self.move_history.append(move)
        if promotion:
            self._replace_promoted_pawn(end, promotion)
        if not finalize:
            self.san_history.append(san)
            return True
        self.halfmove_clock = 0 if move.resets_fifty_move_counter else self.halfmove_clock + 1
        if self.turn == "black":
            self.fullmove_number += 1
        self.switch_turn()
        self.record_position()
        self.promotion_pending = None
        suffix = "#" if self.is_checkmate() else ("+" if self.is_in_check(self.turn) else "")
        self.san_history.append(san + suffix)
        return True

    def _replace_promoted_pawn(self, position, promotion):
        p = self.board.get_piece(position)
        if p is None: return
        name = {"q":"queen","r":"rook","b":"bishop","n":"knight"}.get(promotion.lower(), promotion.lower())
        self.board.set_piece(position, PIECE_CLASSES[name](p.color, position))
        self.move_history[-1].promotion = name
        self.promotion_pending = None

    def promote(self, piece_type):
        if self.promotion_pending is None: return False
        piece_type = {"q":"queen","r":"rook","b":"bishop","n":"knight"}.get(piece_type.lower(), piece_type.lower())
        if piece_type not in ("queen","rook","bishop","knight"): return False
        # Replace the pawn and finish the half-move/turn.
        position = self.promotion_pending.position
        self._replace_promoted_pawn(position, piece_type)
        self.halfmove_clock = 0
        if self.turn == "black": self.fullmove_number += 1
        self.switch_turn()
        self.record_position()
        self.promotion_pending = None
        if self.san_history:
            base_san = self.san_history[-1].split("=")[0].rstrip("+#")
            self.san_history[-1] = base_san + "=" + {"queen":"Q","rook":"R","bishop":"B","knight":"N"}[piece_type]
            if self.is_checkmate(): self.san_history[-1] += "#"
            elif self.is_in_check(self.turn): self.san_history[-1] += "+"
        return True

    def is_promotion_rank_for_target(self, pawn, target):
        return (pawn.color == "white" and target[0] == 0) or (pawn.color == "black" and target[0] == 7)

    def store_captured_pieces(self, piece):
        if piece is None: return
        target = self.pieces_captured_by_white if piece.color == "black" else self.pieces_captured_by_black
        target.append((piece.piece_type, self.piece_values[piece.piece_type]))
        target.sort(key=lambda x: -x[1])

    def undo(self):
        if not self._undo_stack: return False
        snapshot = self._undo_stack.pop()
        state_stack = self._undo_stack
        self.__dict__ = snapshot.__dict__
        self._undo_stack = state_stack
        return True

    def can_undo(self):
        return bool(self._undo_stack)

    def reset(self):
        self.__init__()

    def load_fen(self, fen):
        load_fen(self, fen)
        self._undo_stack = []
        return self

    def push_uci(self, text):
        start, end, promotion = uci_to_move(text)
        return self.make_move(start, end, promotion)

    def push_san(self, text):
        from .notation import san_to_move
        start, end, promotion = san_to_move(self, text)
        return self.make_move(start, end, promotion)

    def current_player_in_check(self):
        return self.is_in_check(self.turn)

    def is_in_check(self, color=None):
        return is_in_check(self.board, color or self.turn)

    def has_legal_moves(self, color=None):
        return bool(self.legal_move_pairs(color))

    def is_checkmate(self, color=None):
        color = color or self.turn
        return self.is_in_check(color) and not self.has_legal_moves(color)

    def is_stalemate(self, color=None):
        color = color or self.turn
        return not self.is_in_check(color) and not self.has_legal_moves(color)

    def is_threefold_repetition(self):
        return threefold_repetition(self.position_history)

    def is_insufficient_material(self):
        pieces = [p for p in self.board.pieces_of_color("white") + self.board.pieces_of_color("black") if p.piece_type != "king"]
        if not pieces: return True
        if any(p.piece_type in ("pawn", "rook", "queen") for p in pieces): return False
        bishops = [p for p in pieces if p.piece_type == "bishop"]
        knights = [p for p in pieces if p.piece_type == "knight"]
        if len(pieces) == 1: return True
        if len(pieces) == 2 and len(bishops) == 2:
            return (bishops[0].row + bishops[0].col) % 2 == (bishops[1].row + bishops[1].col) % 2
        return False

    def is_fifty_move_draw(self):
        return self.halfmove_clock >= 100

    def is_draw(self):
        return self.is_stalemate() or self.is_insufficient_material() or self.is_threefold_repetition() or self.is_fifty_move_draw()

    def game_in_progress(self):
        return not self.is_checkmate() and not self.is_draw()
