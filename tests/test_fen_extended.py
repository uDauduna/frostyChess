import pytest

from game import ChessGame
from game.fen import parse_square, square_name


def test_starting_fen_is_exact():
    assert ChessGame().to_fen() == "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


def test_fen_round_trip_preserves_all_six_fields():
    fen = "r3k2r/8/8/3pP3/8/8/8/R3K2R b KQkq e6 17 42"
    game = ChessGame.from_fen(fen)
    assert game.to_fen() == fen
    assert game.turn == "black"
    assert game.en_passant_target == parse_square("e6")
    assert game.halfmove_clock == 17
    assert game.fullmove_number == 42


def test_fen_after_double_pawn_move_contains_ep_target():
    game = ChessGame()
    assert game.push_uci("e2e4")
    assert game.to_fen().split()[3] == "e3"


def test_fen_after_black_move_increments_fullmove_number():
    game = ChessGame()
    assert game.push_uci("e2e4")
    assert game.push_uci("e7e5")
    assert game.to_fen().split()[5] == "2"


@pytest.mark.parametrize("square", ["a1", "h8", "e4", "d6"])
def test_square_name_round_trip(square):
    assert square_name(parse_square(square)) == square


@pytest.mark.parametrize("name", ["", "a0", "a9", "i1", "aa", "a"])
def test_invalid_square_rejected(name):
    with pytest.raises(ValueError):
        parse_square(name)


@pytest.mark.parametrize(
    "fen",
    [
        "8/8/8/8/8/8/8/8 w - - 0",
        "8/8/8/8/8/8/8 w - - 0 1",
        "8/8/8/8/8/8/8/9 w - - 0 1",
        "8/8/8/8/8/8/8/x7 w - - 0 1",
        "8/8/8/8/8/8/8/8 x - - 0 1",
        "8/8/8/8/8/8/8/8 w - - -1 1",
        "8/8/8/8/8/8/8/8 w - - 0 0",
        "8/8/8/8/8/8/8/8 w - e9 0 1",
    ],
)
def test_invalid_fen_syntax_is_rejected(fen):
    with pytest.raises(ValueError):
        ChessGame.from_fen(fen)


def test_load_fen_clears_move_and_undo_history():
    game = ChessGame()
    assert game.push_uci("e2e4")
    assert game.can_undo()
    game.load_fen("4k3/8/8/8/8/8/8/4K3 w - - 0 1")
    assert game.move_history == []
    assert not game.can_undo()
    assert game.to_fen() == "4k3/8/8/8/8/8/8/4K3 w - - 0 1"
