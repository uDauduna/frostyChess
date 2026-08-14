import pygame


class PieceSprite(pygame.sprite.Sprite):
    BOARD_X = 320
    BOARD_Y = 40
    SQUARE_SIZE = 80

    def __init__(self, piece):
        super().__init__()
        self.piece = piece
        self.image = self.load_image()
        self.rect = self.image.get_rect()
        self.update_position()

    def load_image(self):
        prefix = "b" if self.piece.color == "black" else "w"
        path = (
            f"./assets/"
            f"{prefix}-{self.piece.piece_type}.png"
        )
        image = pygame.image.load(path).convert_alpha()
        width = int(image.get_width() * 0.125)
        height = int(image.get_height() * 0.125)
        return pygame.transform.scale(image, (width, height))

    def update_position(self):
        row, col = self.piece.position
        center_x = (self.BOARD_X + col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2)
        center_y = (self.BOARD_Y + row * self.SQUARE_SIZE + self.SQUARE_SIZE // 2)
        self.rect.center = (center_x, center_y)