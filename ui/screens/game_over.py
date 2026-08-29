import pygame

from .base_screen import BaseScreen
from ui.components import Button


class GameOver(BaseScreen):

    def __init__(self, screen, screen_manager):
        super().__init__(screen)
        self.screen_manager = screen_manager
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.title_font = pygame.font.Font(None, 75)
        self.result_font = pygame.font.Font(None, 50)
        self.button_font = pygame.font.Font(None, 34)
        self.result = "GAME OVER"
        center_x = self.width // 2
        self.new_game_button = Button((center_x - 150, 400, 300, 60), "PLAY NEW GAME", self.button_font, self.new_game)
        self.menu_button = Button((center_x - 150, 480, 300, 60), "MAIN MENU", self.button_font, self.main_menu)
        self.quit_button = Button((center_x - 150, 560, 300, 60), "QUIT", self.button_font, self.quit)
        self.buttons = [self.new_game_button, self.menu_button, self.quit_button]
        return

    def set_result(self, result):
        self.result = result
        return

    def new_game(self):
        self.screen_manager.show_game_setup()
        return

    def main_menu(self):
        self.screen_manager.show_main_menu()
        return

    def quit(self):
        self.screen_manager.quit()
        return

    def handle_event(self, event):
        for button in self.buttons:
            button.handle_event(event)
        return

    def update(self):
        pass
        return

    def draw(self):
        self.screen.fill((25, 30, 38))
        title = self.title_font.render("GAME OVER", True, (240, 240, 240))
        self.screen.blit(title, title.get_rect(center=(self.width // 2, 130)))
        result = self.result_font.render(self.result, True, (240, 240, 240))
        self.screen.blit(result, result.get_rect(center=(self.width // 2, 230)))
        for button in self.buttons:
            button.draw(self.screen)
        return