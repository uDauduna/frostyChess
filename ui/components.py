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
        # Determine colors based on state
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

        # Shadow
        if self.enabled:
            shadow_rect = self.rect.copy()
            shadow_rect.y += 4
            shadow_surface = pygame.Surface(shadow_rect.size, pygame.SRCALPHA)
            pygame.draw.rect(shadow_surface, (0, 0, 0, 70), shadow_surface.get_rect(), border_radius=10)
            screen.blit(shadow_surface, shadow_rect)
        # Main button
        pygame.draw.rect(screen, fill, self.rect, border_radius=10)
        # Border
        pygame.draw.rect(screen, border, self.rect, width=2 if self.selected or self.hovered else 1, border_radius=10)
        # Text
        text_surface = self.font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)