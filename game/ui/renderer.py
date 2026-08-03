# Example file showing a circle moving on screen
import pygame

#constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SQUARE_SIZE = 80
BOARD_SIZE = 640
# DARK_SQUARE = (92, 64, 51)
DARK_SQUARE = "black"
LIGHT_SQUARE = "grey"
BACKGROUND_COLOR = "navy"

# pygame setup


pygame.init()
screen = pygame.display.set_mode((1280, 720))
board = pygame.Surface((BOARD_SIZE + 4, BOARD_SIZE + 4))
clock = pygame.time.Clock()
running = True
dt = 0

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
    

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()