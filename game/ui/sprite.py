import pygame

class Piece(pygame.sprite.Sprite):
    def __init__(self, piece, color, position=None):
        super().__init__()
        self.piece = piece
        self.color = color
        self.position = position
        self.path = self.get_image()
        self.image, self.rect = self.create_sprite()

    def create_sprite(self):
        image = pygame.image.load(self.path).convert_alpha()
        width = image.get_rect().width
        height = image.get_rect().height
        final_sprite = pygame.transform.scale(image, (height*0.125,width*0.125))
        sprite_rect = final_sprite.get_rect()
        sprite_rect.center = (520, 80)
        return final_sprite, sprite_rect

    def get_image(self):
        pref = "b" if self.color == "black" else "w"
        path = f'assets/{pref}-{self.piece}.png'
        return path
