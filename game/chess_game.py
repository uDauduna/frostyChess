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
        self.pieces_captured_by_black = []
        self.pieces_captured_by_white = []
        self.piece_values = {
                            "pawn": 1,
                            "knight": 3,
                            "bishop": 3,
                            "rook": 5,
                            "queen": 9,
                            "king": 0
                        }

    def is_square_attacked(self, square, by_color):
        target_row, target_col = square
        for row in range(8):
            for col in range(8):
                piece = self.board.pieces[row][col]
                if piece is None:
                    continue
                if piece.color != by_color:
                    continue
                if piece.piece_type == "pawn":
                    direction = -1 if piece.color == "white" else 1
                    if target_row == row + direction and abs(target_col - col) == 1:
                        return True
                else:
                    if square in piece.pseudo_legal_moves(self.board):
                        return True
        return False

    def opposite_color(self, color):
        if color == "white":
            return "black"
        return "white"

    def perform_castling(self, start, end):
        king = self.board.get_piece(start)
        row, king_col = start
        _, target_col = end
        if target_col > king_col:
            rook_start = (row, 7)
            rook_end = (row, 5)
        else:
            rook_start = (row, 0)
            rook_end = (row, 3)
        rook = self.board.get_piece(rook_start)
        self.board.pieces[row][king_col] = None
        king.row = end[0]
        king.col = end[1]
        self.board.pieces[end[0]][end[1]] = king
        self.board.pieces[rook_start[0]][rook_start[1]] = None
        rook.row = rook_end[0]
        rook.col = rook_end[1]
        self.board.pieces[rook_end[0]][rook_end[1]] = rook
        return rook

    def can_castle(self, start, end):
        if not self.is_castling_move(start, end):
            return False
        king = self.board.get_piece(start)
        row, col = start
        _, target_col = end
        kingside = target_col > col
        if kingside:
            rook_col = 7
            empty_columns = [5, 6]
            king_path = [(row, 5), (row, 6)]
        else:
            rook_col = 0
            empty_columns = [1, 2, 3]
            king_path = [(row, 3), (row, 2)]
        rook = self.board.get_piece((row, rook_col))
        if rook is None:
            return False
        if rook.piece_type != "rook":
            return False
        if rook.color != king.color:
            return False
        for column in empty_columns:
            if self.board.get_piece((row, column)) is not None:
                return False
        if self.is_square_attacked(start, self.opposite_color(king.color)):
            return False
        for square in king_path:
            if self.is_square_attacked(square, self.opposite_color(king.color)):
                return False
        return True

    def is_castling_move(self, start, end):
        piece = self.board.get_piece(start)
        if piece is None:
            return False
        if piece.piece_type != "king":
            return False
        if piece.color != self.turn:
            return False
        row, col = start
        target_row, target_col = end
        if row != target_row:
            return False
        if abs(target_col - col) != 2:
            return False
        if target_col > col:
            return self.castling_rights[f"{piece.color}_kingside"]
        return self.castling_rights[f"{piece.color}_queenside"]

    def is_en_passant_move(self, source, target):
        if self.en_passant_target is None:
            return False
        if target != self.en_passant_target:
            return False
        piece = self.board.get_piece(source)
        if piece is None:
            return False
        if piece.piece_type != "pawn":
            return False
        if piece.color != self.turn:
            return False
        if abs(target[1] - source[1]) != 1:
            return False
        if abs(target[0] - source[0]) != 1:
            return False
        captured_position = (source[0], target[1])
        captured_piece = self.board.get_piece(captured_position)
        if captured_piece is None:
            return False
        if captured_piece.piece_type != "pawn":
            return False
        if captured_piece.color == piece.color:
            return False
        return True

    def perform_en_passant(self, start, end):
        pawn = self.board.get_piece(start)
        captured_position = (start[0], end[1])
        captured_piece = self.board.get_piece(captured_position)
        if pawn is None or captured_piece is None:
            return None
        self.board.pieces[captured_position[0]][captured_position[1]] = None
        self.board.pieces[start[0]][start[1]] = None
        pawn.row = end[0]
        pawn.col = end[1]
        self.board.pieces[end[0]][end[1]] = pawn
        return captured_piece

    def update_en_passant_target(self, start, end, piece):
        self.en_passant_target = None
        if piece.piece_type != "pawn":
            return
        if abs(end[0] - start[0]) == 2:
            middle_row = (start[0] + end[0]) // 2
            self.en_passant_target = (middle_row, start[1])
        return

    def update_castling_rights(self, piece, start, captured_piece, end):
        color = piece.color
        if piece.piece_type == "king":
            self.castling_rights[f"{color}_kingside"] = False
            self.castling_rights[f"{color}_queenside"] = False
        elif piece.piece_type == "rook":
            if color == "white":
                if start == (7, 0):
                    self.castling_rights["white_queenside"] = False
                elif start == (7, 7):
                    self.castling_rights["white_kingside"] = False
            else:
                if start == (0, 0):
                    self.castling_rights["black_queenside"] = False
                elif start == (0, 7):
                    self.castling_rights["black_kingside"] = False
        if captured_piece is not None and captured_piece.piece_type == "rook":
            if captured_piece.color == "white":
                if end == (7, 0):
                    self.castling_rights["white_queenside"] = False
                elif end == (7, 7):
                    self.castling_rights["white_kingside"] = False
            else:
                if end == (0, 0):
                    self.castling_rights["black_queenside"] = False
                elif end == (0, 7):
                    self.castling_rights["black_kingside"] = False

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
        moves = piece.pseudo_legal_moves(self.board)
        if piece.piece_type == "pawn":
            if self.en_passant_target is not None and self.is_en_passant_move(position, self.en_passant_target):
                moves.append(self.en_passant_target)
        if piece.piece_type == "king":
            row, col = position
            kingside_target = (row, col + 2)
            queenside_target = (row, col - 2)
            if self.can_castle(position, kingside_target):
                moves.append(kingside_target)
            if self.can_castle(position, queenside_target):
                moves.append(queenside_target)
        return moves

    def legal_moves(self, start):
        piece = self.board.get_piece(start)
        if piece is None:
            return []
        if piece.color != self.turn:
            return []
        pseudo_legal_moves = self.pseudo_legal_moves(start)
        legal_moves = []
        for end in pseudo_legal_moves:
            if self.is_move_legal(start, end):
                legal_moves.append(end)
        return legal_moves

    def is_move_legal(self, start, end):
        temp_game = copy.deepcopy(self)
        piece = temp_game.board.get_piece(start)
        if piece is None:
            return False
        if temp_game.is_en_passant_move(start, end):
            temp_game.perform_en_passant(start, end)
        elif temp_game.is_castling_move(start, end):
            if not temp_game.can_castle(start, end):
                return False
            temp_game.perform_castling(start, end)
        else:
            temp_game.board.move_piece(start, end)
        return not is_in_check(temp_game.board, self.turn)

    def make_move(self, start, end):
        piece = self.board.get_piece(start)
        if piece is None:
            return False
        if piece.color != self.turn:
            return False
        legal_moves = self.legal_moves(start)
        if end not in legal_moves:
            return False
        previous_en_passant_target = self.en_passant_target
        previous_castling_rights = self.castling_rights.copy()
        is_en_passant = self.is_en_passant_move(start, end)
        is_castling = self.is_castling_move(start, end)
        if is_en_passant:
            captured_piece = self.perform_en_passant(start, end)
        elif is_castling:
            captured_piece = None
            self.perform_castling(start, end)
        else:
            captured_piece = self.board.move_piece(start, end)
        self.store_captured_pieces(captured_piece)
        print(captured_piece,self.pieces_captured_by_black, self.pieces_captured_by_white)
            
        self.update_castling_rights(piece, start, captured_piece, end)
        self.update_en_passant_target(start, end, piece)
        move = Move(
            start=start,
            end=end,
            piece=piece,
            captured_piece=captured_piece,
            is_castling=is_castling,
            is_en_passant=is_en_passant,
            previous_en_passant_target=previous_en_passant_target,
            previous_castling_rights=previous_castling_rights
        )
        self.move_history.append(move)
        if piece.piece_type == "pawn" and self.is_promotion_rank(piece):
            self.promotion_pending = piece
            return True
        self.switch_turn()
        self.record_position()
        return True

    def store_captured_pieces(self, piece):
        if piece is None:
            return
        if piece.color == "black":
            self.pieces_captured_by_white.append((piece.piece_type, self.piece_values[piece.piece_type]))
            self.pieces_captured_by_white.sort(key = lambda x: -x[1])
        else:
            self.pieces_captured_by_black.append((piece.piece_type, self.piece_values[piece.piece_type]))
            self.pieces_captured_by_black.sort(key = lambda x: -x[1])
        return

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
        previous_turn = self.turn
        self.turn = color
        pieces = self.board.pieces_of_color(color)
        for piece in pieces:
            if self.legal_moves(piece.position):
                self.turn = previous_turn
                return True
        self.turn = previous_turn
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
        if len(self.board.pieces_of_color("black")) == 1 and len(self.board.pieces_of_color("white")) == 1:
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