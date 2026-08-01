from game.board import Board

class Game:
    def __init__(self, timed = False):
        self.board = Board()

    def play(self):
        for row in self.board.board:
            print(row)
        return



game = Game()
game.play()
