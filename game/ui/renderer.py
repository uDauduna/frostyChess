# Example file showing a circle moving on screen
import pygame

#constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SQUARE_SIZE = 80
BOARD_SIZE = 640
DARK_SQUARE = (54, 69, 79)
# DARK_SQUARE = "grey"
LIGHT_SQUARE = "white"
BACKGROUND_COLOR = (44, 57, 66)

# pygame setup


pygame.init()
screen = pygame.display.set_mode((1280, 720))
board = pygame.Surface((BOARD_SIZE + 4, BOARD_SIZE + 4))
clock = pygame.time.Clock()
running = True
dt = 0

image = pygame.image.load('assets/b-bishop.png').convert_alpha()
width = image.get_rect().width
height = image.get_rect().height
print(width, height)
bishop = pygame.transform.scale(image, (height*0.125,width*0.125))
sprite_rect = bishop.get_rect()
sprite_rect.center = (440, 80)


def draw_board():
    for row in range(8):
        for col in range(8):
            if row%2 == 0:
                color = LIGHT_SQUARE if (row * 8 + col)%2 == 0 else DARK_SQUARE
            else:
                color = DARK_SQUARE if (row * 8 + col)%2 == 0 else LIGHT_SQUARE
            square = pygame.Rect(2+col* SQUARE_SIZE,2 + row* SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(board, color, square)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill(BACKGROUND_COLOR)
    board.fill("white")
    draw_board()
    screen.blit(board, (318, 38))
    screen.blit(bishop, sprite_rect)
    

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()