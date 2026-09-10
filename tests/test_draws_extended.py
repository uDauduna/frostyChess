from game import ChessGame


def test_king_vs_king_is_insufficient_material():
    game = ChessGame.from_fen("4k3/8/8/8/8/8/8/4K3 w - - 0 1")
    assert game.is_insufficient_material()


def test_king_and_bishop_vs_king_is_insufficient_material():
    game = ChessGame.from_fen("4k3/8/8/8/8/8/2B5/4K3 w - - 0 1")
    assert game.is_insufficient_material()


def test_king_and_knight_vs_king_is_insufficient_material():
    game = ChessGame.from_fen("4k3/8/8/8/8/8/2N5/4K3 w - - 0 1")
    assert game.is_insufficient_material()


def test_same_color_bishop_ending_is_insufficient_material():
    # Bishops on c1 and f4 are on the same square color.
    game = ChessGame.from_fen("4k3/8/8/8/5b2/8/8/2B1K3 w - - 0 1")
    assert game.is_insufficient_material()


def test_pawn_or_rook_prevents_insufficient_material():
    game = ChessGame.from_fen("4k3/8/8/8/8/8/4P3/4K3 w - - 0 1")
    assert not game.is_insufficient_material()


def test_fifty_move_draw_threshold():
    game = ChessGame.from_fen("4k3/8/8/8/8/8/7N/4K3 w - - 99 1")
    assert not game.is_fifty_move_draw()
    assert game.push_uci("h2f3")
    assert game.is_fifty_move_draw()


def test_threefold_repetition():
    game = ChessGame.from_fen("4k3/8/8/8/8/8/6N1/4K3 w - - 0 1")
    for move in ("g2f4", "e8d7", "f4g2", "d7e8") * 2:
        assert game.push_uci(move)
    assert game.is_threefold_repetition()
