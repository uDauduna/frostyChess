import pygame


class PromotionUI:
    def __init__(self):
        self.active = False
        self.color = None
        self.choice_rects = {}

    def open(self, pawn):
        self.active = True
        self.color = pawn.color

    def close(self):
        self.active = False
        self.color = None
        self.choice_rects = {}

    def get_image(self, piece_type):
        prefix = "b" if self.color == "black" else "w"
        path = (
            f"./assets/"
            f"{prefix}-{piece_type}.png"
        )
        image = pygame.image.load(path).convert_alpha()
        width = int(image.get_width() * 0.125)
        height = int(image.get_height() * 0.125)
        return pygame.transform.scale(image,(width, height),)

    def draw(self, screen):
        overlay = pygame.Surface(screen.get_size(),pygame.SRCALPHA,)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        panel = pygame.Rect(
            screen.get_width() // 2 - 150,
            screen.get_height() // 2 - 150,
            300,
            300,
        )

        pygame.draw.rect(
            screen,
            (45, 45, 45),
            panel,
            border_radius=12,
        )

        pieces = [
            ("q", "queen"),
            ("r", "rook"),
            ("b", "bishop"),
            ("n", "knight"),
        ]

        positions = [
            (panel.centerx - 60, panel.centery - 60),
            (panel.centerx + 60, panel.centery - 60),
            (panel.centerx - 60, panel.centery + 60),
            (panel.centerx + 60, panel.centery + 60),
        ]
        self.choice_rects = {}
        for (code, piece_type), position in zip(pieces,positions,):
            image = self.get_image(piece_type)
            rect = image.get_rect()
            rect.center = position
            self.choice_rects[code] = rect
            screen.blit(image, rect)

    def handle_click(self, event):
        if not self.active:
            return None
        for code, rect in self.choice_rects.items():
            if rect.collidepoint(event.pos):
                return code
        return None