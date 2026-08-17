from game.board import Board


def test_board_has_32_pieces():
    board = Board()

    pieces = [
        piece
        for row in board.pieces
        for piece in row
        if piece is not None
    ]

    assert len(pieces) == 32


def test_empty_squares_are_none():
    board = Board()

    assert board.get_piece((3, 3)) is None
    assert board.get_piece((4, 4)) is None


def test_initial_pieces():
    board = Board()

    assert board.get_piece((0, 0)).piece_type == "rook"
    assert board.get_piece((0, 0)).color == "black"

    assert board.get_piece((7, 4)).piece_type == "king"
    assert board.get_piece((7, 4)).color == "white"


def test_move_piece():
    board = Board()

    piece = board.get_piece((6, 4))

    board.move_piece((6, 4), (4, 4))

    assert board.get_piece((6, 4)) is None
    assert board.get_piece((4, 4)) is piece
    assert piece.position == (4, 4)