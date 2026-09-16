import pytest

from game import ChessGame
from game.notation import move_to_uci, san_for_move, san_to_move, uci_to_move


def test_uci_parser_and_promotion_suffix():
    assert uci_to_move("e2e4") == ((6, 4), (4, 4), None)
    assert uci_to_move("a7a8q") == ((1, 0), (0, 0), "q")


@pytest.mark.parametrize("text", ["e2e", "e9e4", "foo", "e2e4x", "a1a9"])
def test_invalid_uci_rejected(text):
    with pytest.raises(ValueError):
        uci_to_move(text)


def test_san_for_pawn_move_and_capture():
    game = ChessGame()
    start, end, _ = uci_to_move("e2e4")
    assert san_for_move(game, start, end) == "e4"
    assert game.push_uci("e2e4")
    assert game.push_uci("d7d5")
    start, end, _ = uci_to_move("e4d5")
    assert san_for_move(game, start, end) == "exd5"


def test_castling_san_and_zero_castling_input():
    game = ChessGame.from_fen("4k3/8/8/8/8/8/8/4K2R w K - 0 1")
    assert san_for_move(game, (7, 4), (7, 6)) == "O-O"
    start, end, promotion = san_to_move(game, "0-0")
    assert (start, end, promotion) == ((7, 4), (7, 6), None)


def test_san_parser_accepts_checkmate_suffix():
    game = ChessGame()
    for move in ("f2f3", "e7e5", "g2g4"):
        assert game.push_uci(move)
    start, end, promotion = san_to_move(game, "Qh4#")
    assert (start, end, promotion) == ((0, 3), (4, 7), None)


def test_san_disambiguation_for_two_knights():
    game = ChessGame.from_fen("4k3/8/8/8/8/8/2N1N3/4K3 w - - 0 1")
    assert san_for_move(game, (6, 2), (4, 3)) == "Ncd4"
    assert san_for_move(game, (6, 4), (4, 3)) == "Ned4"


def test_move_to_uci_with_promotion():
    game = ChessGame.from_fen("4k3/P7/8/8/8/8/8/4K3 w - - 0 1")
    assert game.push_uci("a7a8q")
    assert move_to_uci(game.move_history[-1]) == "a7a8q"
