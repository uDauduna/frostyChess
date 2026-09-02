import pygame

from .base_screen import BaseScreen


class GameScreen(BaseScreen):

    def __init__(self, screen, screen_manager, color, difficulty):
        super().__init__(screen)
        self.screen_manager = screen_manager
        self.player_color = color
        self.difficulty = difficulty

        # Add existing ChessGame

        return

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.screen_manager.pause_game()

        # Add mouse handling
        return

    def update(self):
        pass
        return

    def draw(self):
        # Add renderer
        self.screen.fill((30, 35, 40))
        return