from .constants import BOARD_SIZE


def in_bounds(row, col):
    return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE


def can_occupy(piece, board, position):
    target = board.get_piece(position)
    return target is None or target.color != piece.color

def sliding_moves(piece, board, directions):
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


def attacked_squares(board, color):
    """
    Return all squares attacked by pieces of the given color.

    This is intentionally separate from legal moves because
    pawn attacks and king movement have special considerations.
    """
    attacked = []
    for piece in board.pieces_of_color(color):
        if piece.piece_type == "pawn":
            for square in piece.attack_squares():
                if in_bounds(*square):
                    attacked.append(square)
        else:
            for square in piece.pseudo_legal_moves(board):
                attacked.append(square)
    return attacked


def is_square_attacked(board, position, by_color):
    return position in attacked_squares(board, by_color)


def is_in_check(board, color):
    king = board.find_king(color)
    if king is None:
        return False

    opponent = "black" if color == "white" else "white"

    return is_square_attacked(board, king.position,opponent)

def threefold_repetition(position_history):
    if not position_history:
        return False
    current_position = position_history[-1]
    return position_history.count(current_position) >= 3