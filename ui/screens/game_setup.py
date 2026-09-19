import pygame

from .base_screen import BaseScreen
from ui.components import Button
from ui.theme import FrostyTheme


class GameSetup(BaseScreen):
    def __init__(self, screen, screen_manager):
        super().__init__(screen)
        self.screen_manager = screen_manager
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.title_font = pygame.font.Font(None, 72)
        self.section_font = pygame.font.Font(None, 28)
        self.font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)
        self.selected_color = "white"
        self.selected_difficulty = "medium"
        self.selected_mode = "casual"
        self.create_buttons()

    def create_buttons(self):
        cx = self.width // 2
        self.white_button = Button((cx - 250, 190, 220, 60), "WHITE", self.font, lambda: self.select_color("white"))
        self.black_button = Button((cx + 30, 190, 220, 60), "BLACK", self.font, lambda: self.select_color("black"))
        self.easy_button = Button((cx - 330, 315, 200, 60), "EASY", self.font, lambda: self.select_difficulty("easy"))
        self.medium_button = Button((cx - 100, 315, 200, 60), "MEDIUM", self.font, lambda: self.select_difficulty("medium"))
        self.hard_button = Button((cx + 130, 315, 200, 60), "HARD", self.font, lambda: self.select_difficulty("hard"))
        self.casual_button = Button((cx - 225, 440, 210, 60), "CASUAL", self.font, lambda: self.select_mode("casual"))
        self.competitive_button = Button((cx + 15, 440, 210, 60), "COMPETITIVE", self.font, lambda: self.select_mode("competitive"))
        self.start_button = Button((cx - 160, 550, 320, 65), "BEGIN GAME", self.font, self.start_game)
        self.back_button = Button((cx - 100, 635, 200, 45), "BACK", self.small_font, self.go_back)

        self.buttons = [
            self.white_button,
            self.black_button,
            self.easy_button,
            self.medium_button,
            self.hard_button,
            self.casual_button,
            self.competitive_button,
            self.start_button,
            self.back_button,
        ]
        self.update_selection_visuals()

    def select_color(self, value):
        self.selected_color = value
        self.update_selection_visuals()

    def select_difficulty(self, value):
        self.selected_difficulty = value
        self.update_selection_visuals()

    def select_mode(self, value):
        self.selected_mode = value
        self.update_selection_visuals()

    def update_selection_visuals(self):
        self.white_button.set_selected(self.selected_color == "white")
        self.black_button.set_selected(self.selected_color == "black")
        self.easy_button.set_selected(self.selected_difficulty == "easy")
        self.medium_button.set_selected(self.selected_difficulty == "medium")
        self.hard_button.set_selected(self.selected_difficulty == "hard")
        self.casual_button.set_selected(self.selected_mode == "casual")
        self.competitive_button.set_selected(self.selected_mode == "competitive")


    def start_game(self):
        self.screen_manager.start_game(self.selected_color, self.selected_difficulty, self.selected_mode)

    def go_back(self):
        self.screen_manager.show_main_menu()

    def handle_event(self, event):
        for button in self.buttons:
            button.handle_event(event)

    def update(self):
        pass

    def draw(self):
        self.screen.fill(FrostyTheme.BACKGROUND)
        FrostyTheme.draw_overlay(self.screen, alpha=30)
        title = self.title_font.render("NEW GAME", True, FrostyTheme.TEXT)
        title_rect = title.get_rect(center=(self.width // 2, 75))
        self.screen.blit(title, title_rect)
        line_width = 240
        line_x = (self.width - line_width) // 2
        pygame.draw.line(self.screen, FrostyTheme.GOLD, (line_x, 112), (line_x + line_width, 112), 2)
        self.draw_section_label("CHOOSE YOUR SIDE", 145)
        self.draw_selection_panel(pygame.Rect(self.width // 2 - 270, 175, 540, 95))
        self.draw_section_label("DIFFICULTY", 290)
        self.draw_section_label("MODE", 415)
        for button in self.buttons:
            button.draw(self.screen)
        info = f"{self.selected_color.upper()}  •  {self.selected_difficulty.upper()}  •  {self.selected_mode.upper()}"
        info_surface = self.small_font.render(info, True, FrostyTheme.TEXT_MUTED)
        info_rect = info_surface.get_rect(center=(self.width // 2, 525))
        self.screen.blit(info_surface, info_rect)

    def draw_section_label(self, text, y):
        surface = self.section_font.render(text, True, FrostyTheme.TEXT_MUTED)
        rect = surface.get_rect(center=(self.width // 2, y))
        self.screen.blit(surface, rect)

    def draw_selection_panel(self, rect):
        FrostyTheme.draw_shadow(self.screen, rect, offset=4, radius=12)
        FrostyTheme.draw_panel(self.screen, rect, fill=(27, 36, 45), border=(75, 88, 98), border_width=1, radius=12)