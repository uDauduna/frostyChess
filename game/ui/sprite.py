import pygame

class Piece(pygame.sprite.Sprite):
    def __init__(self, piece, color, position):
        super().__init__()
        self.piece = piece
        self.color = color
        self.center_x = 320 + (position[1] * 80) + 40
        self.center_y = 40 + (position[0] * 80) + 40
        self.path = self.get_image()
        self.image, self.rect = self.create_sprite()

    def create_sprite(self):
        image = pygame.image.load(self.path).convert_alpha()
        width = image.get_rect().width
        height = image.get_rect().height
        final_sprite = pygame.transform.scale(image, (height*0.125,width*0.125))
        sprite_rect = final_sprite.get_rect()
        sprite_rect.center = (self.center_x, self.center_y)
        return final_sprite, sprite_rect

    def get_image(self):
        pref = "b" if self.color == "black" else "w"
        path = f'game/assets/{pref}-{self.piece}.png'
        return path

    def update_board_position(self, pos):
        self.center_x = 320 + (pos[1] * 80) + 40
        self.center_y = 40 + (pos[0] * 80) + 40
        self.rect.center = (self.center_x, self.center_y)
        return