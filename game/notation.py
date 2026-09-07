"""Chess notation helpers (SAN/UCI)."""

import re
from .fen import square_name, parse_square

PIECE_LETTER = {"pawn": "", "knight": "N", "bishop": "B", "rook": "R", "queen": "Q", "king": "K"}

def uci_to_move(text):
    text = text.strip().lower()
    if not re.fullmatch(r"[a-h][1-8][a-h][1-8][qrbn]?", text):
        raise ValueError(f"Invalid UCI move: {text}")
    return parse_square(text[:2]), parse_square(text[2:4]), (text[4] if len(text) == 5 else None)

def move_to_uci(move):
    result = square_name(move.start) + square_name(move.end)
    if move.promotion:
        result += move.promotion[0].lower()
    return result

def san_for_move(game, start, end, promotion=None):
    piece = game.board.get_piece(start)
    if piece is None:
        raise ValueError("No piece on start square")
    legal = game.legal_moves(start)
    if end not in legal:
        raise ValueError("Illegal move")
    if piece.piece_type == "king" and abs(end[1] - start[1]) == 2:
        return "O-O" if end[1] > start[1] else "O-O-O"
    capture = game.is_en_passant_move(start, end) or game.board.get_piece(end) is not None
    prefix = PIECE_LETTER[piece.piece_type]
    if piece.piece_type == "pawn":
        text = (square_name(start)[0] + "x") if capture else ""
        text += square_name(end)
    else:
        # SAN disambiguation: among legal moves by same piece type/color.
        competitors = []
        for other in game.board.pieces_of_color(piece.color):
            if other is piece or other.piece_type != piece.piece_type:
                continue
            if end in game.legal_moves(other.position):
                competitors.append(other)
        dis = ""
        if competitors:
            same_file = any(p.col == piece.col for p in competitors)
            same_rank = any(p.row == piece.row for p in competitors)
            if not same_file:
                dis = square_name(start)[0]
            elif not same_rank:
                dis = square_name(start)[1]
            else:
                dis = square_name(start)
        text = prefix + dis + ("x" if capture else "") + square_name(end)

    if promotion:
        text += "=" + PIECE_LETTER.get(promotion, promotion.upper())
    return text

def san_to_move(game, token):
    token = token.strip()
    token = re.sub(r"[+#?!]+$", "", token)
    if token in ("O-O", "0-0"):
        for piece in game.board.pieces_of_color(game.turn):
            if piece.piece_type == "king":
                target = (piece.row, piece.col + 2)
                if target in game.legal_moves(piece.position):
                    return piece.position, target, None
        raise ValueError("Illegal castling")
    if token in ("O-O-O", "0-0-0"):
        for piece in game.board.pieces_of_color(game.turn):
            if piece.piece_type == "king":
                target = (piece.row, piece.col - 2)
                if target in game.legal_moves(piece.position):
                    return piece.position, target, None
        raise ValueError("Illegal castling")

    m = re.fullmatch(r"([KQRBN])?([a-h1-8]{0,2})(x?)([a-h][1-8])(?:=([QRBN]))?", token)
    if not m:
        # Also accept UCI in PGN-like input.
        return (*uci_to_move(token),)

    letter, dis, capture_marker, destination, promotion = m.groups()
    piece_type = {v:k for k,v in PIECE_LETTER.items() if v}.get(letter, "pawn")
    target = parse_square(destination)
    candidates = []
    for piece in game.board.pieces_of_color(game.turn):
        if piece.piece_type != piece_type:
            continue
        if dis:
            sq = square_name(piece.position)
            if not (dis in sq):
                continue
            if len(dis) == 2 and sq != dis:
                continue
        if target in game.legal_moves(piece.position):
            actual_capture = game.is_en_passant_move(piece.position, target) or game.board.get_piece(target) is not None
            if capture_marker and not actual_capture:
                continue
            if not capture_marker and actual_capture and piece_type == "pawn":
                continue
            candidates.append(piece)
    if len(candidates) != 1:
        raise ValueError(f"Could not uniquely resolve SAN move: {token}")
    return candidates[0].position, target, (promotion.lower() if promotion else None)
