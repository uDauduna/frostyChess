from game.board import Board

class Game:
    def __init__(self, timed = False):
        self.board = Board()

    def move_piece(self, old_pos, new_pos):
        piece_type = self.board.board_state[old_pos[0]][old_pos[1]]
        piece = self.board.pieces[old_pos[0]][old_pos[1]]
        if piece.is_move_legal(new_pos, self.board):
            self.board.board_state[old_pos[0]][old_pos[1]] = "."
            self.board.board_state[new_pos[0]][new_pos[1]] = piece_type
            self.board.pieces[old_pos[0]][old_pos[1]] = "."
            self.board.pieces[new_pos[0]][new_pos[1]] = piece
            piece.update_position(new_pos)
        else:
            """
            We can't raise an error
            """
            print("Illegal Move")

        return

    def play(self):
        for row in self.board.board_state:
            print(row)
        self.move_piece((1,1), (3,1))
        for row in self.board.board_state:
            print(row)
        return



game = Game()
game.play()

