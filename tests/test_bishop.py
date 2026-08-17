from game.board import Board


def test_bishop_blocked_at_start():
    board = Board()

    bishop = board.get_piece((7, 2))

    moves = bishop.pseudo_legal_moves(board)

    assert moves == []