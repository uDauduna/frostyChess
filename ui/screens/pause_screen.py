import pygame

from .base_screen import BaseScreen
from ui.components import Button


class PauseScreen(BaseScreen):

    def __init__(self, screen, screen_manager):
        super().__init__(screen)
        self.screen_manager = screen_manager
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.title_font = pygame.font.Font(None, 70)
        self.font = pygame.font.Font(None, 36)
        center_x = self.width // 2
        self.resume_button = Button((center_x - 150, 270, 300, 60), "RESUME", self.font, self.resume)
        self.new_game_button = Button((center_x - 150, 350, 300, 60), "NEW GAME", self.font, self.new_game)
        self.menu_button = Button((center_x - 150, 430, 300, 60), "MAIN MENU", self.font, self.main_menu)
        self.buttons = [self.resume_button, self.new_game_button, self.menu_button]
        return

    def resume(self):
        self.screen_manager.resume_game()
        return

    def new_game(self):
        self.screen_manager.show_game_setup()
        return

    def main_menu(self):
        self.screen_manager.show_main_menu()
        return

    def handle_event(self, event):
        for button in self.buttons:
            button.handle_event(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.resume()
        return

    def update(self):
        pass
        return

    def draw(self):
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        self.screen.blit(overlay, (0, 0))
        panel = pygame.Rect(self.width // 2 - 200, 140, 400, 430)
        pygame.draw.rect(self.screen, (35, 40, 50), panel, border_radius=12)
        title = self.title_font.render("PAUSED", True, (240, 240, 240))
        self.screen.blit(title, title.get_rect(center=(self.width // 2, 210)))
        for button in self.buttons:
            button.draw(self.screen)
        return