from game import ChessGame, export_pgn, import_pgn


def play(game, *moves):
    for move in moves:
        assert game.push_uci(move)


def test_pgn_contains_headers_and_correct_checkmate_result():
    game = ChessGame()
    play(game, "f2f3", "e7e5", "g2g4", "d8h4")
    pgn = export_pgn(game, {"White": "Alice", "Black": "Bob"})
    assert '[White "Alice"]' in pgn
    assert '[Black "Bob"]' in pgn
    assert '[Result "0-1"]' in pgn
    assert "Qh4# 0-1" in pgn


def test_pgn_import_ignores_comments_and_variations():
    pgn = '''[Event "Test"]
            [Result "*"]

            1. e4 {king pawn} e5 2. Nf3 (2. Bc4) Nc6 *
          '''
    game = import_pgn(pgn)
    assert game.san_history == ["e4", "e5", "Nf3", "Nc6"]


def test_pgn_set_up_fen_is_preserved():
    fen = "4k3/8/8/8/8/8/4P3/4K3 w - - 0 1"
    game = ChessGame.from_fen(fen)
    assert game.push_uci("e2e4")
    pgn = export_pgn(game)
    assert '[SetUp "1"]' in pgn
    assert f'[FEN "{fen}"]' in pgn
    restored = import_pgn(pgn)
    assert restored.to_fen() == game.to_fen()


def test_pgn_round_trip_with_castling():
    game = ChessGame.from_fen("r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1")
    play(game, "e1g1", "e8c8")
    restored = import_pgn(export_pgn(game))
    assert restored.to_fen() == game.to_fen()
