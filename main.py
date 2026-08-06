from game.board import Board
import pygame
from game.ui.sprite import Piece
from game.board import Board
import random
import time
from game.ui.promotion_ui import PromotionUI

class Game:
    def __init__(self, timed = False):
        self.SCREEN_WIDTH = 1280
        self.SCREEN_HEIGHT = 720
        self.SQUARE_SIZE = 80
        self.BOARD_SIZE = 640
        self.BOARD_X = 320
        self.BOARD_Y = 40
        self.DARK_SQUARE = (181, 136, 99)
        self.LIGHT_SQUARE = (240, 217, 181) 
        self.BACKGROUND_COLOR = (44, 57, 66)
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("frostyChess")
        self.board = Board()
        self.board_surface = pygame.Surface((self.BOARD_SIZE + 4, self.BOARD_SIZE + 4))
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0
        self.selected_square = None
        self.source_square = None
        self.target_square = None
        self.legal_squares = None 
        self.clicked_piece = None
        self.turn = "white"
        self.selected_piece = None
        self.game_over = False
        self.in_check = False
        self.winner = None
        self.en_passant_square = None
        self.promotion_ui = PromotionUI()

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
                # print(self.board.pieces)
                # print(self.board.piece_group)
                if not self.board.square_is_empty(new_pos):
                    self.capture(new_pos)
                self.board.board_state[old_pos[0]][old_pos[1]] = "."
                self.board.pieces[old_pos[0]][old_pos[1]] = "."
                if piece_type.lower() == "p" and (new_pos[0] == 0  or new_pos[0] == 7):
                    piece.update_position(new_pos)
                    self.board.board_state[new_pos[0]][new_pos[1]] = piece_type
                    self.board.pieces[new_pos[0]][new_pos[1]] = piece
                    self.promotion_ui.open(piece)
                    return
                piece.update_position(new_pos)               
                self.board.board_state[new_pos[0]][new_pos[1]] = piece_type
                self.board.pieces[new_pos[0]][new_pos[1]] = piece

                # print(self.board.pieces)
                # print(self.board.piece_group)
            else:
                """
                We can't raise an error
                """
                

        return

    def capture(self, pos):
        piece = self.board.pieces[pos[0]][pos[1]]
        if piece != ".":
            piece.kill()
        self.board.board_state[pos[0]][pos[1]] = "."
        self.board.pieces[pos[0]][pos[1]] = "."
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

    def mouse_click(self, event):
        """Convert a mouse click into a board square."""
        mouse_x, mouse_y = event.pos
        if (
            self.BOARD_X <= mouse_x < self.BOARD_X + self.BOARD_SIZE
            and self.BOARD_Y <= mouse_y < self.BOARD_Y + self.BOARD_SIZE
        ):
            col = (mouse_x - self.BOARD_X) // self.SQUARE_SIZE
            row = (mouse_y - self.BOARD_Y) // self.SQUARE_SIZE
            self.clicked_square = (row, col)
            print(f"Clicked square: {self.clicked_square}")
        else:
            print("Clicked outside board")
        return None

    def handle_click(self):
        """Simple two-click move logic."""
        # Clicked outside the board
        if self.clicked_square is None:
            self.selected_square = None
            return

        # First click
        if self.selected_square is None:
            if self.board.board_state[self.clicked_square[0]][self.clicked_square[1]] == ".":
                self.selected_square = None
            else:
                self.selected_square = self.clicked_square
            print(f"Selected: {self.selected_square}")
            return

        # Clicked the same square again
        if self.clicked_square == self.selected_square:
            print("Selection cleared")
            self.selected_square = None
            return

        # Second click
        self.source_square = self.selected_square
        self.target_square = self.clicked_square

        self.move_piece(self.source_square, self.target_square)


        print(f"Move: {self.source_square} -> {self.target_square}")

        # move_piece(source_square, target_square)

        self.selected_square = None

    def draw_selected_square(self):
        if self.selected_square is not None:
            row, col = self.selected_square
            pygame.draw.rect(
                self.board_surface,
                (50, 205, 50),
                (
                    2 + col * self.SQUARE_SIZE,
                    2 + row * self.SQUARE_SIZE,
                    self.SQUARE_SIZE,
                    self.SQUARE_SIZE,
                ),
                width=4,
            )

    def draw_legal_moves(self):
        if self.selected_square:
            self.clicked_piece = self.board.pieces[self.selected_square[0]][self.selected_square[1]]
            self.legal_squares = self.clicked_piece.eligible_moves(self.board)
            radius = 10
            for row, col in self.legal_squares:
                center_x = col * 80 + 40 + 2
                center_y = row * 80 + 40 + 2
                pygame.draw.circle(
                    self.board_surface,
                    (50, 200, 50),
                    (center_x, center_y),
                    radius
                )

    def render_game(self):
        while self.running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if self.promotion_ui.active:
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                choice = self.promotion_ui.handle_click(event)
                                if choice is not None:
                                    self.board.promote_piece( self.promotion_ui.pawn,choice)
                                    self.promotion_ui.close()
                            continue
                elif event.type == pygame.MOUSEBUTTONDOWN:

                    if event.button == 1:
                        self.mouse_click(event)
                        self.handle_click()

            # fill the screen with a color to wipe away anything from last frame
            self.screen.fill(self.BACKGROUND_COLOR)
            self.board_surface.fill("white")
            if self.promotion_ui.active:
                self.promotion_ui.draw(self.screen)
            else:
                self.draw_board()
                self.board.piece_group.draw(self.screen)
                self.draw_selected_square()
                self.draw_legal_moves()
                self.screen.blit(self.board_surface, (318, 38))
                self.board.piece_group.draw(self.screen)

            pygame.display.flip()
            # limits FPS to 60
            # dt is delta time in seconds since last frame, used for framerate-
            # independent physics.
            dt = self.clock.tick(60) / 1000
        pygame.quit()


game = Game()
game.render_game()


# SELECTED_COLOR = (50, 205, 50)      # Lime green
# LEGAL_MOVE_COLOR = (30, 144, 255)   # Dodger blue
# CAPTURE_COLOR = (220, 20, 60)       # Crimson
# LAST_MOVE_COLOR = (255, 215, 0)     # Gold