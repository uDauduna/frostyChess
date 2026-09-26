"""This module contains the promotion ui used by frostyChess."""

import os
import pygame


class PromotionUI:
    def __init__(self):
        self.active = False
        self.color = None
        self.choice_rects = {}
        self.asset_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
        self.piece_images = self._load_piece_images()

    def _load_piece_images(self):
        images = {}
        for color in ("black", "white"):
            prefix = "b" if color == "black" else "w"
            for piece_type in ("queen", "rook", "bishop", "knight"):
                path = os.path.join(self.asset_dir, f"{prefix}-{piece_type}.png")
                image = pygame.image.load(path).convert_alpha()
                width = int(image.get_width() * 0.125)
                height = int(image.get_height() * 0.125)
                images[(color, piece_type)] = pygame.transform.smoothscale(image, (width, height))
        return images

    def open(self, pawn):
        self.active = True
        self.color = pawn.color

    def close(self):
        self.active = False
        self.color = None
        self.choice_rects = {}

    def draw(self, screen):
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        panel = pygame.Rect(screen.get_width() // 2 - 150, screen.get_height() // 2 - 150, 300, 300)
        pygame.draw.rect(screen, (45, 45, 45), panel, border_radius=12)
        pieces = [("q", "queen"), ("r", "rook"), ("b", "bishop"), ("n", "knight")]
        positions = [
            (panel.centerx - 60, panel.centery - 60),
            (panel.centerx + 60, panel.centery - 60),
            (panel.centerx - 60, panel.centery + 60),
            (panel.centerx + 60, panel.centery + 60),
        ]

        self.choice_rects = {}
        for (code, piece_type), position in zip(pieces, positions):
            image = self.piece_images[(self.color, piece_type)]
            rect = image.get_rect(center=position)
            self.choice_rects[code] = rect
            screen.blit(image, rect)

    def handle_click(self, event):
        if not self.active:
            return None
        for code, rect in self.choice_rects.items():
            if rect.collidepoint(event.pos):
                return code
        return None
