from game.board import Board
import pygame
from game.ui.sprite import Piece
from game.board import Board
import random
import time

class Game:
    def __init__(self, timed = False):
        self.SCREEN_WIDTH = 1280
        self.SCREEN_HEIGHT = 720
        self.SQUARE_SIZE = 80
        self.BOARD_SIZE = 640
        self.DARK_SQUARE = (54, 69, 79)
        self.LIGHT_SQUARE = "white"
        self.BACKGROUND_COLOR = (44, 57, 66)
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("frostyChess")
        self.board = Board()
        self.board_surface = pygame.Surface((self.BOARD_SIZE + 4, self.BOARD_SIZE + 4))
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0

    def draw_board(self):
        for row in range(8):
            for col in range(8):
                if row%2 == 0:
                    color = self.LIGHT_SQUARE if (row * 8 + col)%2 == 0 else self.DARK_SQUARE
                else:
                    color = self.DARK_SQUARE if (row * 8 + col)%2 == 0 else self.LIGHT_SQUARE
                square = pygame.Rect(2+col* self.SQUARE_SIZE,2 + row* self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE)
                pygame.draw.rect(self.board_surface, color, square)
        return

    def move_piece(self, old_pos, new_pos):
        if self.board.board_state[old_pos[0]][old_pos[1]] != ".":
            piece_type = self.board.board_state[old_pos[0]][old_pos[1]]
            piece = self.board.pieces[old_pos[0]][old_pos[1]]
            if piece.is_move_legal(new_pos, self.board):
                print(self.board.pieces)
                print(self.board.piece_group)
                self.board.board_state[old_pos[0]][old_pos[1]] = "."
                self.board.pieces[old_pos[0]][old_pos[1]] = "."
                if piece_type.lower() == "p" and (new_pos[0] == 0  or new_pos[0] == 7):
                    piece_type, piece = self.board.promote_piece(new_pos)
                piece.update_position(new_pos)
                self.board.board_state[new_pos[0]][new_pos[1]] = piece_type
                self.board.pieces[new_pos[0]][new_pos[1]] = piece

                print(self.board.pieces)
                print(self.board.piece_group)
            else:
                """
                We can't raise an error
                """
                

        return

    def play(self):
        for row in self.board.board_state:
            print(row)
        print("===============================================")
        self.move_piece((6,1), (7,1))
        for row in self.board.board_state:
            print(row)
        print("===============================================")
        self.move_piece((0,1), (2,2))
        for row in self.board.board_state:
            print(row)
        print("===============================================")
        self.move_piece((0,1), (1,3))
        for row in self.board.board_state:
            print(row)
        return

    def render_game(self):
        while self.running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # fill the screen with a color to wipe away anything from last frame
            self.screen.fill(self.BACKGROUND_COLOR)
            self.board_surface.fill("white")
            self.draw_board()
            self.screen.blit(self.board_surface, (318, 38))
            self.board.piece_group.draw(self.screen)
            self.move_piece((0,1), (2,2))
            # flip() the display to put your work on screen
            pygame.display.flip()

            # limits FPS to 60
            # dt is delta time in seconds since last frame, used for framerate-
            # independent physics.
            dt = self.clock.tick(60) / 1000
        pygame.quit()


game = Game()
game.render_game()
