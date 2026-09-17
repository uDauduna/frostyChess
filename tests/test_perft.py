from game import ChessGame


def perft(game, depth):
    if depth == 0:
        return 1
    total = 0
    for start, end in game.legal_move_pairs():
        child = game.clone()
        piece = child.board.get_piece(start)
        promotion = None
        if piece.piece_type == "pawn" and end[0] in (0, 7):
            promotion = "queen"
        assert child.make_move(start, end, promotion)
        if child.promotion_pending:
            assert child.promote("queen")
        total += perft(child, depth - 1)
    return total


def test_start_position_perft_depth_1():
    assert perft(ChessGame(), 1) == 20


def test_start_position_perft_depth_2():
    assert perft(ChessGame(), 2) == 400
