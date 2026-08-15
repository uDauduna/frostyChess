import pygame

from .sprite import PieceSprite

class Renderer:
    BOARD_X = 320
    BOARD_Y = 40
    BOARD_SIZE = 640
    SQUARE_SIZE = 80
    DARK_SQUARE = (181, 136, 99)
    LIGHT_SQUARE = (240, 217, 181)
    def __init__(self, screen, chess_game):
        self.screen = screen
        self.game = chess_game
        self.board_surface = pygame.Surface(
            (self.BOARD_SIZE, self.BOARD_SIZE)
        )
        self.sprites = {}

    def sync_pieces(self):
        current_pieces = []
        for row in self.game.board.pieces:
            for piece in row:
                if piece is not None:
                    current_pieces.append(piece)
                    if piece not in self.sprites:
                        self.sprites[piece] = PieceSprite(piece)
                    self.sprites[piece].update_position()
        # Remove sprites for captured pieces
        for piece in list(self.sprites):
            if piece not in current_pieces:
                del self.sprites[piece]

    def draw_board(self):
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 0:
                    color = self.LIGHT_SQUARE
                else:
                    color = self.DARK_SQUARE
                square = pygame.Rect(
                    col * self.SQUARE_SIZE,
                    row * self.SQUARE_SIZE,
                    self.SQUARE_SIZE,
                    self.SQUARE_SIZE,
                )
                pygame.draw.rect(
                    self.board_surface,
                    color,
                    square,
                )

    def draw_selected_square(self, position):
        if position is None:
            return
        row, col = position
        pygame.draw.rect(
            self.board_surface,
            (0, 0, 255),
            (
                col * self.SQUARE_SIZE,
                row * self.SQUARE_SIZE,
                self.SQUARE_SIZE,
                self.SQUARE_SIZE,
            ),
            width=40,
        )

    def draw_legal_moves(self, moves):
        for row, col in moves:
            pygame.draw.rect(
            self.board_surface,
            (50, 205, 50),
            (
                col * self.SQUARE_SIZE,
                row * self.SQUARE_SIZE,
                self.SQUARE_SIZE,
                self.SQUARE_SIZE,
            ),
            width=40,
        )

    def draw(self, selected_position=None, legal_moves=None):
        self.board_surface.fill("white")
        self.draw_board()
        if selected_position is not None:
            self.draw_selected_square(selected_position)
        if legal_moves:
            self.draw_legal_moves(legal_moves)
        self.sync_pieces()
        self.screen.blit(
            self.board_surface,
            (self.BOARD_X, self.BOARD_Y),
        )
        for sprite in self.sprites.values():
            self.screen.blit(sprite.image, sprite.rect)