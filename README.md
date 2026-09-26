# frostyChess

frostyChess is a Python chess engine with a Pygame UI and a UI-independent
game model intended to support future AI/self-play work.

## Run

```bash
python main.py
```

CLI (no Pygame window):

```bash
python cli.py
python cli.py --random-games 100
python cli.py --fen "8/8/8/8/8/8/4K3/4k2R w - - 0 1"
```

## Architecture

- `game/` — engine/model only; safe to import from training code.
- `game/fen.py` — FEN import/export.
- `game/notation.py` — SAN/UCI conversion.
- `game/pgn.py` — PGN import/export.
- `cli.py` — terminal play and lightweight random self-play.
- `training.py` — small engine-facing API for future RL/AI.
- `ui/` — Pygame presentation and interaction.

## Game modes

- **Casual:** undo is enabled.
- **Competitive:** undo is disabled by the UI. The engine still retains its
  history internally, so later features such as clocks, ratings/ELO, players,
  matchmaking, and server-side validation can be added without redesigning
  the board model.
- Selecting Black automatically starts with the board oriented from Black's
  side. The board can also be flipped at any time with the **FLIP** button or
  `F`.

## FEN / PGN

```python
from game import ChessGame, export_pgn, import_pgn

game = ChessGame()
game.push_uci("e2e4")
fen = game.to_fen()

pgn = export_pgn(game, {"White": "Human", "Black": "AI"})
replayed = import_pgn(pgn)
```

FEN includes piece placement, side to move, castling rights, en-passant target,
halfmove clock, and fullmove number.

## AI direction

The engine exposes deterministic state and legal actions without the UI.
`training.py` is deliberately small so a future model can choose an action,
apply it, collect `state_fen()`, and run self-play. For large-scale training,
a later optimization pass should replace the current deepcopy-based legality
simulation with a faster make/unmake representation.

## Controls

- Click a piece, then a destination.
- `F` — flip board.
- `U` — undo in Casual mode.
- `Esc` — pause.

## Performance notes

The engine is designed to stay responsive as games become longer.

- Legal move checks temporarily apply and undo moves on the existing board instead of deep-copying the complete game.
- Attack detection checks the requested square directly and stops at the first attacker.
- Threefold repetition uses a position-count dictionary instead of scanning the complete history.
- User undo snapshots store board references and compact metadata rather than copying every previous move and position.
- Piece sprites are synchronized only when the chess state changes, not every render frame.
- Board coordinate text is cached instead of being rendered every frame.
- Game-over checks run only after the game state changes.

The AI, advanced options, and load-game features can be added later without requiring the rendering loop to rebuild the chess state.

