import pytest

from game import ChessGame
from game.rules import is_in_check

START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


def play(game, *moves):
    for move in moves:
        assert game.push_uci(move), f"failed to play {move}"


def test_initial_position_has_20_legal_moves():
    assert len(ChessGame().legal_move_pairs()) == 20


def test_wrong_side_cannot_move_and_failed_move_does_not_mutate_state():
    game = ChessGame()
    before = game.to_fen()
    assert not game.push_uci("e7e5")
    assert game.turn == "white"
    assert game.to_fen() == before


def test_capture_updates_board_and_captured_material():
    # White pawn on d2 captures black pawn on e3.
    game = ChessGame.from_fen("4k3/8/8/8/8/4p3/3P4/4K3 w - - 0 1")
    assert game.push_uci("d2e3")
    assert game.board.get_piece((5, 4)).color == "white"
    assert game.pieces_captured_by_white == [("pawn", 1)]
    assert game.pieces_captured_by_black == []


def test_en_passant_and_target_lifecycle():
    game = ChessGame()
    play(game, "e2e4")
    assert game.en_passant_target == (5, 4)
    play(game, "a7a6", "e4e5", "d7d5")
    assert game.en_passant_target == (2, 3)
    assert (2, 3) in game.legal_moves((3, 4))
    assert game.push_uci("e5d6")
    assert game.board.get_piece((3, 3)) is None
    assert game.board.get_piece((2, 3)).color == "white"
    assert game.pieces_captured_by_white == [("pawn", 1)]


def test_en_passant_expires_after_one_non_en_passant_reply():
    game = ChessGame()
    play(game, "e2e4", "a7a6", "e4e5", "d7d5", "g1f3")
    assert (2, 3) not in game.legal_moves((3, 4))


def test_kingside_castling_moves_king_and_rook():
    game = ChessGame.from_fen("r3k2r/8/8/8/8/8/8/4K2R w Kk - 0 1")
    assert game.push_uci("e1g1")
    assert game.board.get_piece((7, 6)).piece_type == "king"
    assert game.board.get_piece((7, 5)).piece_type == "rook"
    assert game.turn == "black"
    assert not game.castling_rights["white_kingside"]


def test_queenside_castling_moves_king_and_rook():
    game = ChessGame.from_fen("r3k2r/8/8/8/8/8/8/R3K3 w Qkq - 0 1")
    assert game.push_uci("e1c1")
    assert game.board.get_piece((7, 2)).piece_type == "king"
    assert game.board.get_piece((7, 3)).piece_type == "rook"
    assert not game.castling_rights["white_queenside"]


def test_castling_through_attacked_square_is_rejected():
    # Black rook on f8 attacks f1, so White may not castle through f1.
    game = ChessGame.from_fen("r3kr1r/8/8/8/8/8/8/4K2R w K - 0 1")
    assert not game.push_uci("e1g1")


def test_castling_without_right_is_rejected():
    game = ChessGame.from_fen("4k2r/8/8/8/8/8/8/4K2R w - - 0 1")
    assert not game.push_uci("e1g1")


def test_moving_rook_removes_only_that_castling_right():
    game = ChessGame.from_fen("r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1")
    assert game.push_uci("h1h2")
    assert not game.castling_rights["white_kingside"]
    assert game.castling_rights["white_queenside"]


def test_capturing_rook_removes_opponents_castling_right():
    game = ChessGame.from_fen("4k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1")
    assert game.push_uci("h1h8")
    assert not game.castling_rights["black_kingside"]


def test_move_into_check_is_rejected():
    game = ChessGame.from_fen("4r1k1/8/8/8/8/8/4K3/8 w - - 0 1")
    assert not game.push_uci("e2e3")
    assert game.turn == "white"


def test_check_detection():
    game = ChessGame.from_fen("4k3/8/8/8/8/8/4R3/4K3 b - - 0 1")
    assert game.current_player_in_check()
    assert is_in_check(game.board, "black")


def test_fools_mate_is_checkmate_and_game_ends():
    game = ChessGame()
    play(game, "f2f3", "e7e5", "g2g4", "d8h4")
    assert game.is_checkmate()
    assert game.turn == "white"
    assert game.san_history[-1] == "Qh4#"
    assert not game.game_in_progress()


def test_stalemate_is_not_check():
    game = ChessGame.from_fen("7k/5Q2/6K1/8/8/8/8/8 b - - 0 1")
    assert game.is_stalemate()
    assert not game.is_in_check("black")
    assert not game.game_in_progress()


def test_halfmove_clock_resets_on_pawn_move():
    game = ChessGame.from_fen("4k3/8/8/8/8/8/4P3/4K3 w - - 42 10")
    assert game.push_uci("e2e4")
    assert game.halfmove_clock == 0


def test_halfmove_clock_increments_on_quiet_piece_move():
    game = ChessGame.from_fen("4k3/8/8/8/8/8/7N/4K3 w - - 42 10")
    assert game.push_uci("h2f3")
    assert game.halfmove_clock == 43
    assert game.fullmove_number == 10


def test_fullmove_number_increments_after_black_move():
    game = ChessGame.from_fen("4k3/8/8/8/8/8/7N/4K3 b - - 0 10")
    assert game.push_uci("e8d7")
    assert game.fullmove_number == 11
    assert game.turn == "white"


def test_undo_multiple_moves_restores_exact_previous_states():
    game = ChessGame()
    states = [game.to_fen()]
    for move in ("e2e4", "e7e5", "g1f3"):
        assert game.push_uci(move)
        states.append(game.to_fen())
    for expected in reversed(states[:-1]):
        assert game.undo()
        assert game.to_fen() == expected
    assert not game.can_undo()
    assert not game.undo()


def test_undo_restores_en_passant_and_turn():
    game = ChessGame()
    initial = game.to_fen()
    assert game.push_uci("e2e4")
    assert game.en_passant_target == (5, 4)
    assert game.undo()
    assert game.to_fen() == initial
    assert game.turn == "white"
    assert game.en_passant_target is None


def test_undo_restores_capture_bookkeeping():
    game = ChessGame.from_fen("4k3/8/8/8/8/4p3/3P4/4K3 w - - 0 1")
    assert game.push_uci("d2e3")
    assert game.pieces_captured_by_white == [("pawn", 1)]
    assert game.undo()
    assert game.pieces_captured_by_white == []


def test_promotion_pending_then_all_four_promotions():
    for promotion in ("queen", "rook", "bishop", "knight"):
        game = ChessGame.from_fen("4k3/P7/8/8/8/8/8/4K3 w - - 0 1")
        assert game.push_uci("a7a8")
        assert game.promotion_pending is not None
        assert game.turn == "white"
        assert game.promote(promotion)
        assert game.board.get_piece((0, 0)).piece_type == promotion
        assert game.turn == "black"
        assert game.san_history[-1].startswith("a8=")


def test_uci_promotion_can_be_applied_directly():
    game = ChessGame.from_fen("4k3/P7/8/8/8/8/8/4K3 w - - 0 1")
    assert game.push_uci("a7a8q")
    assert game.board.get_piece((0, 0)).piece_type == "queen"
    assert game.turn == "black"


def test_clone_is_independent():
    game = ChessGame()
    clone = game.clone()
    assert clone.to_fen() == game.to_fen()
    assert clone.push_uci("e2e4")
    assert game.to_fen() == START_FEN


def test_legal_move_pairs_color_override_preserves_turn():
    game = ChessGame()
    black_moves = game.legal_move_pairs("black")
    assert len(black_moves) == 20
    assert game.turn == "white"


def test_reset_clears_game_history():
    game = ChessGame()
    play(game, "e2e4", "e7e5")
    game.reset()
    assert game.to_fen() == START_FEN
    assert game.move_history == []
    assert game.san_history == []
    assert not game.can_undo()
