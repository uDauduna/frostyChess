import pygame

from .base_screen import BaseScreen
from ui.components import Button


class MainMenu(BaseScreen):

    def __init__(self, screen, screen_manager):
        super().__init__(screen)
        self.screen_manager = screen_manager
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.title_font = pygame.font.Font(None, 90)
        self.button_font = pygame.font.Font(None, 42)
        button_width = 300
        button_height = 65
        x = (self.width - button_width) // 2
        self.start_button = Button((x, self.height // 2, button_width, button_height), "START GAME", self.button_font, self.start_game)
        self.quit_button = Button((x, self.height // 2 + 90, button_width, button_height), "QUIT", self.button_font, self.quit_game)
        return

    def start_game(self):
        self.screen_manager.show_game_setup()
        return

    def quit_game(self):
        self.screen_manager.quit()
        return

    def handle_event(self, event):
        self.start_button.handle_event(event)
        self.quit_button.handle_event(event)
        return

    def update(self):
        pass
        return

    def draw(self):
        self.screen.fill((25, 30, 38))
        title = self.title_font.render("FROSTY CHESS", True, (240, 240, 240))
        title_rect = title.get_rect(center=(self.width // 2, 170))
        self.screen.blit(title, title_rect)
        self.start_button.draw(self.screen)
        self.quit_button.draw(self.screen)
        return