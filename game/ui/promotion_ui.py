import pygame

from ..pieces.queen import Queen
from ..pieces.rook import Rook
from ..pieces.bishop import Bishop
from ..pieces.knight import Knight

class PromotionUI:
    def __init__(self):
        self.active = False
        self.color = None
        self.pawn = None
        self.queen_rect = None
        self.rook_rect = None
        self.bishop_rect = None
        self.knight_rect = None

    def open(self, pawn):
        self.active = True
        self.pawn = pawn
        self.color = pawn.color

    def close(self):
        self.active = False
        self.color = None
        self.pawn = None

    def draw(self, screen):
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        panel = pygame.Rect(
            screen.get_width() // 2 - 150,
            screen.get_height() // 2 - 150,
            300,
            300
        )
        pygame.draw.rect(
            screen,
            (45, 45, 45),
            panel,
            border_radius=12
        )

        queen = Queen((0, 0), self.color)
        rook = Rook((0, 0), self.color)
        bishop = Bishop((0, 0), self.color)
        knight = Knight((0, 0), self.color)
        queen.rect.center = (panel.centerx - 60, panel.centery - 60)
        rook.rect.center = (panel.centerx + 60, panel.centery - 60)
        bishop.rect.center = (panel.centerx - 60, panel.centery + 60)
        knight.rect.center = (panel.centerx + 60, panel.centery + 60)
        self.queen_rect = queen.rect
        self.rook_rect = rook.rect
        self.bishop_rect = bishop.rect
        self.knight_rect = knight.rect
        screen.blit(queen.image, queen.rect)
        screen.blit(rook.image, rook.rect)
        screen.blit(bishop.image, bishop.rect)
        screen.blit(knight.image, knight.rect)

    def handle_click(self, event):
        if not self.active:
            return None
        if self.queen_rect.collidepoint(event.pos):
            return "q"
        if self.rook_rect.collidepoint(event.pos):
            return "r"
        if self.bishop_rect.collidepoint(event.pos):
            return "b"
        if self.knight_rect.collidepoint(event.pos):
            return "n"
        return None