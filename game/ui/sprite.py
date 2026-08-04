import pygame

class Piece(pygame.sprite.Sprite):
    def __init__(self, piece,color, position):
        pygame.sprite.Sprite.__init__(self)
        self.piece = piece
        self.color = color
        self.position = position #tuple
        self.path = self.get_image()

    def create_sprite(self):
        image = pygame.image.load(self.path).convert_alpha()
        width = image.get_rect().width
        height = image.get_rect().height
        final_sprite = pygame.transform.scale(image, (height*0.125,width*0.125))
        sprite_rect = final_sprite.get_rect()
        sprite_rect.center = (440, 80)
        return final_sprite, sprite_rect

    def get_image(self):
        """
        Get the path of the image
        """
        return



image = pygame.image.load('assets/b-bishop.png').convert_alpha()
width = image.get_rect().width
height = image.get_rect().height
print(width, height)
bishop = pygame.transform.scale(image, (width*0.125,width*0.125))
sprite_rect = bishop.get_rect()
sprite_rect.center = (440, 80)