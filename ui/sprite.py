import os
import pygame

class PieceSprite(pygame.sprite.Sprite):
    def __init__(self, piece, asset_dir=None):
        super().__init__()
        self.piece = piece
        self.asset_dir = asset_dir or os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
        self.image = self.load_image()
        self.rect = self.image.get_rect()

    def load_image(self):
        prefix = "b" if self.piece.color == "black" else "w"
        path = os.path.join(self.asset_dir, f"{prefix}-{self.piece.piece_type}.png")
        image = pygame.image.load(path).convert_alpha()
        scale = min(0.125, 74 / max(image.get_width(), image.get_height()))
        return pygame.transform.smoothscale(image, (int(image.get_width()*scale), int(image.get_height()*scale)))

    def board_rect(self, board_x, board_y, square_size, row, col):
        return self.image.get_rect(center=(
            board_x + col*square_size + square_size//2,
            board_y + row*square_size + square_size//2
        ))

    def update_position(self, board_x, board_y, square_size, row=None, col=None):
        row, col = self.piece.position if row is None else (row, col)
        self.rect = self.board_rect(board_x, board_y, square_size, row, col)
