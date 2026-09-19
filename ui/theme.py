import pygame


class FrostyTheme:
    # Background
    BACKGROUND = (18, 25, 32)
    BACKGROUND_DARK = (10, 16, 22)
    # UI panels
    PANEL = (34, 43, 53)
    PANEL_HOVER = (49, 63, 75)
    PANEL_SELECTED = (75, 61, 38)
    # Borders
    BORDER = (105, 118, 128)
    BORDER_HOVER = (155, 180, 190)
    BORDER_SELECTED = (202, 166, 91)
    # Text
    TEXT = (240, 240, 235)
    TEXT_MUTED = (180, 190, 198)
    TEXT_DARK = (35, 38, 40)
    # Accent
    GOLD = (202, 166, 91)
    GOLD_BRIGHT = (225, 191, 115)
    # Ice
    ICE = (175, 215, 225)
    ICE_BRIGHT = (215, 238, 242)
    # Disabled
    DISABLED = (48, 53, 58)
    DISABLED_TEXT = (125, 130, 135)

    @staticmethod
    def draw_panel(screen, rect, fill=None, border=None, border_width=1, radius=12):
        rect = pygame.Rect(rect)
        if fill is None:
            fill = FrostyTheme.PANEL
        if border is None:
            border = FrostyTheme.BORDER
        pygame.draw.rect(screen, fill, rect, border_radius=radius)
        if border_width > 0:
            pygame.draw.rect(screen, border, rect, width=border_width, border_radius=radius)

    @staticmethod
    def draw_shadow(screen, rect, offset=5, radius=12):
        shadow_rect = pygame.Rect(rect)
        shadow_rect.x += offset
        shadow_rect.y += offset

        shadow = pygame.Surface((shadow_rect.width, shadow_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(shadow, (0, 0, 0, 90), shadow.get_rect(), border_radius=radius)
        screen.blit(shadow, shadow_rect)

    @staticmethod
    def draw_overlay(screen, alpha=100):
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((5, 12, 18, alpha))
        screen.blit(overlay, (0, 0))

    