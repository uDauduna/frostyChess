import pygame
from ui.screen_manager import ScreenManager

def main():
    pygame.init()
    screen = pygame.display.set_mode((1280,720))
    pygame.display.set_caption("frostyChess")
    clock=pygame.time.Clock()
    manager=ScreenManager(screen)
    while manager.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                manager.quit()
            else:
                manager.handle_event(event)
        manager.update()
        manager.draw()
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__=="__main__":
    main()
