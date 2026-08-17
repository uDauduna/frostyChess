from game.board import Board


def test_white_pawn_initial_moves():
    board = Board()

    pawn = board.get_piece((6, 4))

    moves = pawn.pseudo_legal_moves(board)

    assert (5, 4) in moves
    assert (4, 4) in moves


def test_black_pawn_initial_moves():
    board = Board()

    pawn = board.get_piece((1, 4))

    moves = pawn.pseudo_legal_moves(board)

    assert (2, 4) in moves
    assert (3, 4) in moves