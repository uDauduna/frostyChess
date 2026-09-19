# frostyChess Test Suite

This test suite targets the current AI-ready architecture, including:

- Core move legality and turn handling
- Captures and captured-piece bookkeeping
- Check, checkmate, and stalemate
- Castling and castling rights
- En passant
- Promotion
- Undo and state restoration
- FEN parsing/export and round trips
- UCI and SAN notation
- PGN import/export and FEN-start games
- Draw rules currently implemented by the engine
- Training API (`training.py`) without a UI
- Board-flip and casual/competitive UI control logic when Pygame is installed
- Basic perft validation

## Run

From the project root:

```bash
pytest -q
```

Install project dependencies first if needed:

```bash
pip install -r requirements.txt
```

## Validation performed

Against the uploaded current project, the suite produced:

```text
89 passed, 1 skipped
```

The skipped test module is the Pygame UI-control suite because the execution environment used for validation did not have `pygame` installed. On a normal development machine after `pip install -r requirements.txt`, those tests should run instead of being skipped.

## Important observations for the AI phase

### 1. Perft

The starting position passes:

- depth 1: 20
- depth 2: 400

Depth 3 was intentionally not included in the default suite because the current engine's clone/deepcopy-based legality checking becomes very slow. This is the biggest performance concern before large-scale self-play.

### 2. Make/unmake moves

The engine currently clones the complete game state when testing legal moves. That is acceptable for a GUI chess game, but it will become a major bottleneck for millions of AI/self-play positions.

A future engine optimization should replace this with a fast `make_move` / `unmake_move` search-state mechanism.

### 3. Draw rules

The current tests cover the draw logic that exists in the engine, including insufficient material, threefold repetition, and the 50-move counter. More complete FIDE draw-claim/automatic-draw semantics can be added later if competitive play needs them.

### 4. AI-facing state

The `training.py` API is tested to ensure that the chess state and legal actions can be accessed without importing or running the Pygame UI. This separation should be preserved as the AI is developed.
