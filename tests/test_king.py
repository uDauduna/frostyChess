from game.board import Board


def test_king_blocked_at_start():
    board = Board()

    king = board.get_piece((7, 4))

    moves = king.pseudo_legal_moves(board)

    assert moves == []