import pygame

from .base_screen import BaseScreen
from ui.components import Button


class GameSetup(BaseScreen):

    def __init__(self, screen, screen_manager):
        super().__init__(screen)
        self.screen_manager = screen_manager
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.title_font = pygame.font.Font(None, 70)
        self.font = pygame.font.Font(None, 36)
        self.selected_color = "white"
        self.selected_difficulty = "medium"
        self.create_buttons()
        return

    def create_buttons(self):
        center_x = self.width // 2
        self.white_button = Button((center_x - 260, 230, 220, 60), "WHITE", self.font, lambda: self.select_color("white"))
        self.black_button = Button((center_x + 40, 230, 220, 60), "BLACK", self.font, lambda: self.select_color("black"))
        self.easy_button = Button((center_x - 330, 380, 200, 60), "EASY", self.font, lambda: self.select_difficulty("easy"))
        self.medium_button = Button((center_x - 100, 380, 200, 60), "MEDIUM", self.font, lambda: self.select_difficulty("medium"))
        self.hard_button = Button((center_x + 130, 380, 200, 60), "HARD", self.font, lambda: self.select_difficulty("hard"))
        self.start_button = Button((center_x - 150, 520, 300, 65), "START GAME", self.font, self.start_game)
        self.back_button = Button((center_x - 100, 610, 200, 55), "BACK", self.font, self.go_back)
        self.buttons = [
            self.white_button,
            self.black_button,
            self.easy_button,
            self.medium_button,
            self.hard_button,
            self.start_button,
            self.back_button
        ]
        return

    def select_color(self, color):
        self.selected_color = color
        return

    def select_difficulty(self, difficulty):
        self.selected_difficulty = difficulty
        return

    def start_game(self):
        self.screen_manager.start_game(self.selected_color, self.selected_difficulty)
        return

    def go_back(self):
        self.screen_manager.show_main_menu()
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
        title = self.title_font.render("NEW GAME", True, (240, 240, 240))
        title_rect = title.get_rect(center=(self.width // 2, 100))
        self.screen.blit(title, title_rect)
        color_text = self.font.render("CHOOSE YOUR COLOR", True, (220, 220, 220))
        self.screen.blit(color_text, color_text.get_rect(center=(self.width // 2, 190)))
        difficulty_text = self.font.render("DIFFICULTY", True, (220, 220, 220))
        self.screen.blit(difficulty_text, difficulty_text.get_rect(center=(self.width // 2, 340)))
        for button in self.buttons:
            button.draw(self.screen)
        return