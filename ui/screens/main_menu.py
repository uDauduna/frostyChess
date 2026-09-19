import pygame
from .base_screen import BaseScreen
from ui.components import Button
from ui.theme import FrostyTheme
import os

class MainMenu(BaseScreen):
    def __init__(self, screen, screen_manager):
        super().__init__(screen)
        self.screen_manager = screen_manager
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.title_font = pygame.font.Font(None, 86)
        self.subtitle_font = pygame.font.Font(None, 26)
        self.font = pygame.font.Font(None, 34)
        self.asset_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
        path = os.path.join(self.asset_dir, "theme.png")
        self.background_raw = pygame.image.load(path).convert()
        self.background = pygame.transform.scale(self.background_raw, (self.width, self.height))
        self.create_buttons()

    def create_buttons(self):
        cx = self.width // 2
        self.start_button = Button((cx - 150, 350, 300, 65), "NEW GAME", self.font, self.start_game)
        self.continue_button = Button((cx - 150, 430, 300, 60), "CONTINUE", self.font, self.continue_game)
        self.options_button = Button((cx - 150, 505, 300, 60), "OPTIONS", self.font, self.show_options)
        self.quit_button = Button((cx - 150, 580, 300, 60), "QUIT", self.font, self.quit_game)

        self.buttons = [
            self.start_button,
            self.continue_button,
            self.options_button,
            self.quit_button,
        ]

    def start_game(self):
        self.screen_manager.show_game_setup()

    def continue_game(self):
        # Placeholder for future saved-game functionality
        pass

    def show_options(self):
        # Placeholder for future options screen
        pass

    def quit_game(self):
        pygame.event.post(pygame.event.Event(pygame.QUIT))

    def handle_event(self, event):
        for button in self.buttons:
            button.handle_event(event)

    def update(self):
        pass


    def draw(self):
        self.draw_background()

        # Dark overlay makes UI readable
        FrostyTheme.draw_overlay(self.screen, alpha=80)
        title = self.title_font.render("FROSTY CHESS", True, FrostyTheme.TEXT)
        title_rect = title.get_rect(center=(self.width // 2, 175))
        self.screen.blit(title, title_rect)

        subtitle = self.subtitle_font.render("A CHESS GAME FORGED IN WINTER", True, FrostyTheme.TEXT_MUTED)
        subtitle_rect = subtitle.get_rect(center=(self.width // 2, 225))
        self.screen.blit(subtitle, subtitle_rect)
        line_width = 260
        line_x = (self.width - line_width) // 2
        pygame.draw.line(self.screen, FrostyTheme.GOLD, (line_x, 255), (line_x + line_width, 255), 2)
        for button in self.buttons:
            button.draw(self.screen)
        footer = self.subtitle_font.render("THE KINGDOM WAITS", True, FrostyTheme.TEXT_MUTED)
        footer_rect = footer.get_rect(center=(self.width // 2, self.height - 45))
        self.screen.blit(footer, footer_rect)

    def draw_background(self):
        self.screen.blit(self.background)


    def show_main_menu(self):
        self.current_screen = self.main_menu


    def show_game_setup(self):
        self.current_screen = self.game_setup

