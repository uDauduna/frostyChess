"""Small engine-facing API for ML/self-play experiments.

No UI or Pygame import is required here.
"""
from game.chess_game import ChessGame

def new_game(fen=None):
    return ChessGame.from_fen(fen) if fen else ChessGame()

def legal_actions(game):
    """Return legal moves as (start, end) board-coordinate tuples."""
    return game.legal_move_pairs()

def apply_uci(game, action):
    """Apply a UCI action such as e2e4 or e7e8q."""
    return game.push_uci(action)

def state_fen(game):
    """FEN is a compact, reproducible state representation for datasets."""
    return game.to_fen()

def clone(game):
    return game.clone()
