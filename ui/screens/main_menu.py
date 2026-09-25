"""This module contains the main menu used by frostyChess."""

import os
import random
from pathlib import Path

import pygame

from .base_screen import BaseScreen
from ui.theme import FrostyTheme


class MenuItem:
    def __init__(self, rect, text, font, callback=None, enabled=True):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.callback = callback
        self.enabled = enabled
        self.hovered = False

    def handle_event(self, event):
        if not self.enabled:
            return
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos):
            if self.callback:
                self.callback()

    def draw(self, screen):
        color = FrostyTheme.ICE_BRIGHT if self.hovered else FrostyTheme.TEXT
        if not self.enabled:
            color = FrostyTheme.DISABLED_TEXT

        text = self.font.render(self.text, True, color)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

        if self.hovered and self.enabled:
            left = self.font.render("❮", True, color)
            right = self.font.render("❯", True, color)
            screen.blit(left, left.get_rect(midright=(text_rect.left - 20, text_rect.centery)))
            screen.blit(right, right.get_rect(midleft=(text_rect.right + 20, text_rect.centery)))


class MainMenu(BaseScreen):
    def __init__(self, screen, screen_manager):
        super().__init__(screen)
        self.screen_manager = screen_manager
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.title_font = pygame.font.SysFont("serif", 78)
        self.menu_font = pygame.font.SysFont("serif", 30)
        self.small_font = pygame.font.SysFont("serif", 21)
        self.snow_font = pygame.font.SysFont("serif", 25)
        self.asset_dir = Path(__file__).resolve().parents[2] / "assets"
        self.background = self.load_background()
        self.snow = self.create_snow()
        self.menu_items = self.create_menu_items()

    def load_background(self):
        path = os.path.join(self.asset_dir, "theme.jpg")
        image = pygame.image.load(path).convert()
        scale = max(self.width / image.get_width(), self.height / image.get_height())
        size = (int(image.get_width() * scale), int(image.get_height() * scale))
        image = pygame.transform.smoothscale(image, size)
        rect = image.get_rect(center=(self.width // 2, self.height // 2))
        background = pygame.Surface((self.width, self.height))
        background.blit(image, rect)
        return background

    def create_snow(self):
        rng = random.Random(12)
        snow = []
        for _ in range(55):
            snow.append([rng.randrange(self.width), rng.randrange(self.height), rng.choice((1, 1, 2)), rng.uniform(10, 28)])
        return snow

    def create_menu_items(self):
        center_x = int(self.width * 0.63)
        start_y = 335
        spacing = 52
        labels = [
            ("START GAME", self.start_game, True),
            ("OPTIONS", self.show_options, True),
            ("ACHIEVEMENTS", self.show_achievements, True),
            ("EXTRAS", self.show_extras, True),
            ("QUIT GAME", self.quit_game, True),
        ]
        items = []
        for index, (text, callback, enabled) in enumerate(labels):
            rect = (center_x - 190, start_y + index * spacing - 24, 380, 48)
            items.append(MenuItem(rect, text, self.menu_font, callback, enabled))
        return items

    def start_game(self):
        self.screen_manager.show_game_setup()

    def show_options(self):
        pass

    def show_achievements(self):
        pass

    def show_extras(self):
        pass

    def quit_game(self):
        self.screen_manager.quit()

    def handle_event(self, event):
        for item in self.menu_items:
            item.handle_event(event)

    def update(self):
        for flake in self.snow:
            flake[1] += flake[3] / 60
            flake[0] += 0.15
            if flake[1] > self.height + 5:
                flake[0] = random.randrange(self.width)
                flake[1] = -5
            if flake[0] > self.width + 5:
                flake[0] = -5

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        FrostyTheme.draw_overlay(self.screen, alpha=125)
        self.draw_snow()

        title = self.title_font.render("FROSTY CHESS", True, FrostyTheme.TEXT)
        title_rect = title.get_rect(center=(int(self.width * 0.63), 145))
        self.screen.blit(title, title_rect)

        snow_title = self.snow_font.render("❄        ❄        ❄", True, FrostyTheme.ICE_BRIGHT)
        snow_rect = snow_title.get_rect(center=(int(self.width * 0.63), 205))
        self.screen.blit(snow_title, snow_rect)

        subtitle = self.small_font.render("A WINTER CHESS TALE", True, FrostyTheme.TEXT_MUTED)
        self.screen.blit(subtitle, subtitle.get_rect(center=(int(self.width * 0.63), 245)))

        line_width = 220
        line_x = int(self.width * 0.63) - line_width // 2
        pygame.draw.line(self.screen, FrostyTheme.ICE, (line_x, 270), (line_x + line_width, 270), 1)

        for item in self.menu_items:
            item.draw(self.screen)

        footer = self.small_font.render("THE KINGDOM WAITS", True, FrostyTheme.TEXT_MUTED)
        footer_rect = footer.get_rect(center=(int(self.width * 0.63), self.height - 38))
        self.screen.blit(footer, footer_rect)

    def draw_snow(self):
        for x, y, radius, _ in self.snow:
            pygame.draw.circle(self.screen, (235, 242, 245), (int(x), int(y)), radius)
