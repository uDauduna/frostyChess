"""Low-level chess rule helpers.

The functions in this module deliberately avoid creating temporary ChessGame
objects. Move legality is checked by temporarily changing the existing board
and restoring it immediately, which keeps long games responsive.
"""

from .constants import BOARD_SIZE


def in_bounds(row, col):
    """Return True when a board coordinate is on the 8x8 board."""
    return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE


def can_occupy(piece, board, position):
    """Return True when a piece may move onto the target square."""
    target = board.get_piece(position)
    return target is None or target.color != piece.color


def sliding_moves(piece, board, directions):
    """Generate unobstructed moves for bishops, rooks, and queens."""
    moves = []
    for dr, dc in directions:
        row = piece.row + dr
        col = piece.col + dc
        while in_bounds(row, col):
            target = board.get_piece((row, col))
            if target is None:
                moves.append((row, col))
            else:
                if target.color != piece.color:
                    moves.append((row, col))
                break
            row += dr
            col += dc
    return moves


def _piece_attacks_square(piece, board, target):
    """Check one piece directly without building its entire move list."""
    row, col = piece.position
    target_row, target_col = target
    row_delta = target_row - row
    col_delta = target_col - col

    if piece.piece_type == "pawn":
        direction = 1 if piece.color == "black" else -1
        return row_delta == direction and abs(col_delta) == 1

    if piece.piece_type == "knight":
        return (abs(row_delta), abs(col_delta)) in ((1, 2), (2, 1))

    if piece.piece_type == "king":
        return max(abs(row_delta), abs(col_delta)) == 1

    if piece.piece_type in ("bishop", "rook", "queen"):
        if piece.piece_type == "bishop" and abs(row_delta) != abs(col_delta):
            return False
        if piece.piece_type == "rook" and row_delta != 0 and col_delta != 0:
            return False
        if piece.piece_type == "queen" and not (
            row_delta == 0 or col_delta == 0 or abs(row_delta) == abs(col_delta)
        ):
            return False

        step_row = 0 if row_delta == 0 else (1 if row_delta > 0 else -1)
        step_col = 0 if col_delta == 0 else (1 if col_delta > 0 else -1)
        check_row = row + step_row
        check_col = col + step_col

        while (check_row, check_col) != target:
            if board.get_piece((check_row, check_col)) is not None:
                return False
            check_row += step_row
            check_col += step_col
        return True

    return False


def is_square_attacked(board, position, by_color):
    """Return True if *position* is attacked by *by_color*.

    This is the hot path used by legal move generation. It exits as soon as
    an attacking piece is found instead of constructing a complete attack list.
    """
    for row in board.pieces:
        for piece in row:
            if piece is not None and piece.color == by_color:
                if _piece_attacks_square(piece, board, position):
                    return True
    return False


def attacked_squares(board, color):
    """Return all squares attacked by a color.

    This remains useful for callers that need the complete attack map, while
    is_square_attacked() handles the much more common single-square query.
    """
    attacked = set()
    for row in board.pieces:
        for piece in row:
            if piece is None or piece.color != color:
                continue
            if piece.piece_type == "pawn":
                for square in piece.attack_squares():
                    if in_bounds(*square):
                        attacked.add(square)
            else:
                for square in piece.pseudo_legal_moves(board):
                    attacked.add(square)
    return attacked


def is_in_check(board, color):
    """Return True when the given side's king is currently attacked."""
    king = board.find_king(color)
    if king is None:
        return False
    opponent = "black" if color == "white" else "white"
    return is_square_attacked(board, king.position, opponent)


def threefold_repetition(position_counts):
    """Return True when the current position has occurred at least three times.

    New code passes a dictionary of position counts, making this O(1) instead
    of scanning the complete game history on every frame.
    """
    if isinstance(position_counts, dict):
        return bool(position_counts and max(position_counts.values()) >= 3)
    if not position_counts:
        return False
    return position_counts.count(position_counts[-1]) >= 3
