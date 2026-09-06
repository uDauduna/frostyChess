"""Forsyth-Edwards Notation (FEN) support."""

FILES = "abcdefgh"
RANKS = "87654321"
PIECE_TO_FEN = {
    ("white", "pawn"): "P", ("white", "knight"): "N", ("white", "bishop"): "B",
    ("white", "rook"): "R", ("white", "queen"): "Q", ("white", "king"): "K",
    ("black", "pawn"): "p", ("black", "knight"): "n", ("black", "bishop"): "b",
    ("black", "rook"): "r", ("black", "queen"): "q", ("black", "king"): "k",
}
FEN_TO_PIECE = {v: k for k, v in PIECE_TO_FEN.items()}

def square_name(square):
    row, col = square
    return f"{FILES[col]}{8-row}"

def parse_square(name):
    if len(name) != 2 or name[0] not in FILES or name[1] not in "12345678":
        raise ValueError(f"Invalid square: {name}")
    return 8-int(name[1]), FILES.index(name[0])

def board_to_fen(game):
    rows = []
    for row in game.board.pieces:
        empty = 0
        text = ""
        for piece in row:
            if piece is None:
                empty += 1
            else:
                if empty:
                    text += str(empty); empty = 0
                text += PIECE_TO_FEN[(piece.color, piece.piece_type)]
        if empty:
            text += str(empty)
        rows.append(text)

    castling = ""
    for key, symbol in (
        ("white_kingside", "K"), ("white_queenside", "Q"),
        ("black_kingside", "k"), ("black_queenside", "q"),
    ):
        if game.castling_rights[key]:
            castling += symbol
    castling = castling or "-"
    ep = square_name(game.en_passant_target) if game.en_passant_target else "-"
    halfmove = game.halfmove_clock
    fullmove = game.fullmove_number
    return f"{'/'.join(rows)} {game.turn[0]} {castling} {ep} {halfmove} {fullmove}"

def load_fen(game, fen):
    parts = fen.strip().split()
    if len(parts) != 6:
        raise ValueError("FEN must contain 6 fields")
    placement, active, castling, ep, halfmove, fullmove = parts
    rows = placement.split("/")
    if len(rows) != 8:
        raise ValueError("FEN board must contain 8 ranks")
    # Build a fresh empty board, then populate it.
    from .board import Board
    from .pieces import Pawn, Knight, Bishop, Rook, Queen, King
    constructors = {
        "pawn": Pawn, "knight": Knight, "bishop": Bishop, "rook": Rook,
        "queen": Queen, "king": King,
    }
    board = Board()
    board.pieces = [[None for _ in range(8)] for _ in range(8)]
    for row_idx, row_text in enumerate(rows):
        col = 0
        for ch in row_text:
            if ch.isdigit():
                col += int(ch)
            elif ch in FEN_TO_PIECE:
                if col >= 8:
                    raise ValueError("Invalid FEN rank")
                color, piece_type = FEN_TO_PIECE[ch]
                board.pieces[row_idx][col] = constructors[piece_type](color, (row_idx, col))
                col += 1
            else:
                raise ValueError(f"Invalid FEN piece: {ch}")
        if col != 8:
            raise ValueError("Each FEN rank must describe 8 squares")

    if active not in ("w", "b"):
        raise ValueError("Invalid active color")
    try:
        halfmove_i, fullmove_i = int(halfmove), int(fullmove)
    except ValueError as exc:
        raise ValueError("Invalid FEN move counters") from exc
    if halfmove_i < 0 or fullmove_i < 1:
        raise ValueError("Invalid FEN move counters")

    game.board = board
    game.turn = "white" if active == "w" else "black"
    game.castling_rights = {
        "white_kingside": "K" in castling,
        "white_queenside": "Q" in castling,
        "black_kingside": "k" in castling,
        "black_queenside": "q" in castling,
    }
    game.en_passant_target = None if ep == "-" else parse_square(ep)
    game.halfmove_clock = halfmove_i
    game.fullmove_number = fullmove_i
    game.move_history = []
    game.position_history = []
    game.promotion_pending = None
    game.initial_fen = fen.strip()
    game.pieces_captured_by_black = []
    game.pieces_captured_by_white = []
    game.record_position()
    return game
