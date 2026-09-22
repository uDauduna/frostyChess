import pygame
from ui.theme import FrostyTheme


class Button:
    def __init__(self, rect, text, font, callback=None, selected=False, enabled=True):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.callback = callback
        self.hovered = False
        self.selected = selected
        self.enabled = enabled
        self.clicked = False
        self.normal_color = FrostyTheme.PANEL
        self.hover_color = FrostyTheme.PANEL_HOVER
        self.selected_color = FrostyTheme.PANEL_SELECTED
        self.normal_border = FrostyTheme.BORDER
        self.hover_border = FrostyTheme.BORDER_HOVER
        self.selected_border = FrostyTheme.BORDER_SELECTED
        self.text_color = FrostyTheme.TEXT
        self.shadow = self._create_shadow()
        self._text_cache = {}

    def _create_shadow(self):
        surface = pygame.Surface((self.rect.width, self.rect.height + 4), pygame.SRCALPHA)
        pygame.draw.rect(surface, (0, 0, 0, 70),
                         (0, 4, self.rect.width, self.rect.height), border_radius=10)
        return surface

    def set_selected(self, selected):
        self.selected = selected

    def set_enabled(self, enabled):
        self.enabled = enabled

    def handle_event(self, event):
        if not self.enabled:
            return
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos):
            self.clicked = True
            if self.callback:
                self.callback()

    def draw(self, screen):
        if not self.enabled:
            fill = FrostyTheme.DISABLED
            border = FrostyTheme.DISABLED
            text_color = FrostyTheme.DISABLED_TEXT
        elif self.selected:
            fill = self.selected_color
            border = self.selected_border
            text_color = FrostyTheme.TEXT
        elif self.hovered:
            fill = self.hover_color
            border = self.hover_border
            text_color = FrostyTheme.ICE_BRIGHT
        else:
            fill = self.normal_color
            border = self.normal_border
            text_color = self.text_color

        if self.enabled:
            screen.blit(self.shadow, self.rect.move(0, 0))

        pygame.draw.rect(screen, fill, self.rect, border_radius=10)
        border_width = 2 if self.selected or self.hovered else 1
        pygame.draw.rect(screen, border, self.rect, width=border_width, border_radius=10)

        cache_key = (self.text, text_color)
        text_surface = self._text_cache.get(cache_key)
        if text_surface is None:
            text_surface = self.font.render(self.text, True, text_color)
            self._text_cache[cache_key] = text_surface
        screen.blit(text_surface, text_surface.get_rect(center=self.rect.center))
