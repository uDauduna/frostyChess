from game import ChessGame, export_pgn, import_pgn


def test_fen_round_trip():
    game = ChessGame()
    assert game.to_fen() == "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    game.push_uci("e2e4")
    restored = ChessGame.from_fen(game.to_fen())
    assert restored.to_fen() == game.to_fen()


def test_undo_restores_position():
    game = ChessGame()
    initial = game.to_fen()
    game.push_uci("e2e4")
    assert game.can_undo()
    assert game.undo()
    assert game.to_fen() == initial


def test_pgn_round_trip():
    game = ChessGame()
    for move in ("e2e4", "e7e5", "g1f3", "b8c6"):
        assert game.push_uci(move)
    pgn = export_pgn(game, {"White": "Human", "Black": "AI"})
    restored = import_pgn(pgn)
    assert restored.to_fen() == game.to_fen()
    assert restored.san_history == ["e4", "e5", "Nf3", "Nc6"]
