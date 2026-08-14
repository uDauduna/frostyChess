import pygame
from game.chess_game import ChessGame
from ui.renderer import Renderer
from ui.promotion_ui import PromotionUI


class Game:
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    BOARD_X = 320
    BOARD_Y = 40
    BOARD_SIZE = 640
    SQUARE_SIZE = 80
    BACKGROUND_COLOR = (44, 57, 66)

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("frostyChess")
        self.clock = pygame.time.Clock()
        self.running = True
        self.chess_game = ChessGame()
        self.renderer = Renderer(self.screen,self.chess_game)
        self.promotion_ui = PromotionUI()
        self.selected_square = None

    def mouse_to_board(self, position):
        mouse_x, mouse_y = position
        if not (self.BOARD_X <= mouse_x < self.BOARD_X + self.BOARD_SIZE):
            return None
        if not (self.BOARD_Y <= mouse_y < self.BOARD_Y + self.BOARD_SIZE):
            return None
        col = (mouse_x - self.BOARD_X) // self.SQUARE_SIZE
        row = (mouse_y - self.BOARD_Y) // self.SQUARE_SIZE
        return row, col

    def handle_board_click(self, event):
        clicked_square = self.mouse_to_board(event.pos)
        if clicked_square is None:
            self.selected_square = None
            return

        # First click
        if self.selected_square is None:
            piece = self.chess_game.board.get_piece(clicked_square)
            if piece is not None:
                if piece.color == self.chess_game.turn:
                    self.selected_square = clicked_square
            return

        # Clicked selected square again
        if clicked_square == self.selected_square:
            self.selected_square = None
            return

        # Second click
        start = self.selected_square
        end = clicked_square

        moved = self.chess_game.make_move(start,end,)

        if moved:
            if self.chess_game.promotion_pending:
                self.promotion_ui.open(self.chess_game.promotion_pending)
            self.selected_square = None
        else:
            # If clicking another friendly piece,
            # select that piece instead.
            piece = self.chess_game.board.get_piece(clicked_square)
            if (piece is not None and piece.color == self.chess_game.turn):
                self.selected_square = clicked_square
            else:
                self.selected_square = None

    def handle_promotion_click(self, event):
        choice = self.promotion_ui.handle_click(event)
        if choice is None:
            return
        if self.chess_game.promote(choice):
            self.promotion_ui.close()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button != 1:
                    continue
                if self.promotion_ui.active:
                    self.handle_promotion_click(event)
                else:
                    self.handle_board_click(event)

    def render(self):
        legal_moves = []
        if self.selected_square is not None:
            legal_moves = (
                self.chess_game.pseudo_legal_moves(self.selected_square))
        self.screen.fill(self.BACKGROUND_COLOR)
        if self.promotion_ui.active:
            self.renderer.draw()
            self.promotion_ui.draw(self.screen)
        else:
            self.renderer.draw(selected_position=self.selected_square,legal_moves=legal_moves)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.render()
            self.clock.tick(60)
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()