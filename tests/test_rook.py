from game.board import Board


def test_rook_blocked_at_start():
    board = Board()

    rook = board.get_piece((7, 0))

    moves = rook.pseudo_legal_moves(board)

    assert moves == []