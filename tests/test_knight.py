from game.board import Board


def test_white_knight_initial_moves():
    board = Board()

    knight = board.get_piece((7, 1))

    moves = knight.pseudo_legal_moves(board)

    assert (5, 0) in moves
    assert (5, 2) in moves