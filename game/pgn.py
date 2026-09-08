"""Portable PGN import/export built on the native chess engine."""

import re
from .notation import san_to_move

def export_pgn(game, headers=None):
    headers = dict(headers or {})
    headers.setdefault("Event", "frostyChess Game")
    headers.setdefault("Site", "?")
    headers.setdefault("Result", result(game))
    start_fen = getattr(game, "initial_fen", None)
    standard_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    if start_fen and start_fen != standard_fen:
        headers.setdefault("SetUp", "1")
        headers.setdefault("FEN", start_fen)

    header_text = "\n".join(f'[{k} "{str(v).replace(chr(34), chr(39))}"]' for k,v in headers.items())
    tokens = []
    start_fullmove = 1
    for i, san in enumerate(game.san_history):
        if i % 2 == 0:
            tokens.append(f"{start_fullmove + i//2}.")
        tokens.append(san)
    movetext = " ".join(tokens) + (" " if tokens else "") + headers.get("Result", "*")
    return header_text + "\n\n" + movetext + "\n"

def result(game):
    if game.is_checkmate():
        return "0-1" if game.turn == "white" else "1-0"
    if game.is_draw():
        return "1/2-1/2"
    return "*"

def import_pgn(text):
    from .chess_game import ChessGame
    headers = {}
    for key, value in re.findall(r'^\s*\[(\w+)\s+"(.*)"\]\s*$', text, re.MULTILINE):
        headers[key] = value

    movetext = re.sub(r'\{[^}]*\}', ' ', text, flags=re.S)
    movetext = re.sub(r';[^\n]*', ' ', movetext)
    movetext = re.sub(r'\([^)]*\)', ' ', movetext)
    movetext = re.sub(r'^\s*\[[^\]]*\]\s*', ' ', movetext, flags=re.M)
    tokens = re.findall(r'\S+', movetext)
    fen = headers.get("FEN") if headers.get("SetUp") == "1" else None
    game = ChessGame.from_fen(fen) if fen else ChessGame()
    for token in tokens:
        if re.fullmatch(r'\d+\.(\.\.)?', token) or re.fullmatch(r'\d+\.\.\.', token):
            continue
        if token in ("1-0", "0-1", "1/2-1/2", "*"):
            break
        game.push_san(token)
    game.pgn_headers = headers
    return game
