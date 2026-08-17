from game.board import Board


def test_queen_blocked_at_start():
    board = Board()

    queen = board.get_piece((7, 3))

    moves = queen.pseudo_legal_moves(board)

    assert moves == []