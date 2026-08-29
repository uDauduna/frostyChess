import pygame

class Button:
    def __init__(self, rect, text, font, callback=None):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.callback = callback
        self.normal_color = (70, 80, 95)
        self.hover_color = (95, 110, 130)
        self.text_color = (240, 240, 240)
        self.hovered = False
        return

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    if self.callback:
                        self.callback()
        return

    def draw(self, screen):
        color = self.hover_color if self.hovered else self.normal_color
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        return