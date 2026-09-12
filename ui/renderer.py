import os
import pygame
from .sprite import PieceSprite
from .player_dashboard import PlayerPanel

class Renderer:
    BOARD_SIZE = 640
    SQUARE_SIZE = 80
    LIGHT_SQUARE = (235, 236, 208)
    DARK_SQUARE = (119, 149, 86)
    LAST_MOVE = (246, 246, 105)
    SELECTED = (90, 160, 220)
    MOVE_DOT = (45, 45, 45)
    CAPTURE_RING = (185, 65, 65)

    def __init__(self, screen, chess_game, board_x=320, board_y=40, flipped=False):
        self.screen = screen
        self.game = chess_game
        self.board_x = board_x
        self.board_y = board_y
        self.flipped = flipped
        self.board_surface = pygame.Surface((self.BOARD_SIZE, self.BOARD_SIZE), pygame.SRCALPHA)
        self.player_panel = PlayerPanel()
        self.sprites = {}
        self.animation = None
        self.last_drawn_move_count = 0

    def set_flipped(self, flipped):
        self.flipped = flipped

    def display_square(self, square):
        row, col = square
        if self.flipped:
            row, col = 7-row, 7-col
        return row, col

    def model_square(self, display_row, display_col):
        if self.flipped:
            return 7-display_row, 7-display_col
        return display_row, display_col

    def square_center(self, square):
        row, col = self.display_square(square)
        return (self.board_x + col*self.SQUARE_SIZE + 40,
                self.board_y + row*self.SQUARE_SIZE + 40)

    def sync_pieces(self):
        current = []
        for row in self.game.board.pieces:
            for piece in row:
                if piece is not None:
                    current.append(piece)
                    if piece not in self.sprites:
                        self.sprites[piece] = PieceSprite(piece)
        for piece in list(self.sprites):
            if piece not in current:
                del self.sprites[piece]

    def draw_board(self, selected=None, legal_moves=None):
        self.board_surface.fill((0,0,0,0))
        for dr in range(8):
            for dc in range(8):
                color = self.LIGHT_SQUARE if (dr+dc)%2 == 0 else self.DARK_SQUARE
                pygame.draw.rect(self.board_surface, color, (dc*80, dr*80, 80, 80))

        # Last move highlight
        if self.game.move_history:
            move = self.game.move_history[-1]
            for square in (move.start, move.end):
                dr, dc = self.display_square(square)
                pygame.draw.rect(self.board_surface, self.LAST_MOVE, (dc*80,dr*80,80,80), 0)

        if selected is not None:
            dr, dc = self.display_square(selected)
            pygame.draw.rect(self.board_surface, self.SELECTED, (dc*80,dr*80,80,80), 4)

        for move in legal_moves or []:
            dr, dc = self.display_square(move)
            target = self.game.board.get_piece(move)
            if target is None:
                pygame.draw.circle(self.board_surface, self.MOVE_DOT, (dc*80+40,dr*80+40), 9)
            else:
                pygame.draw.circle(self.board_surface, self.CAPTURE_RING, (dc*80+40,dr*80+40), 31, 5)

    def start_move_animation(self, piece, start, end, duration=0.16):
        self.animation = {"piece": piece, "start": start, "end": end, "elapsed": 0.0, "duration": duration}

    def _draw_coordinates(self):
        font = pygame.font.Font(None, 20)
        for dc in range(8):
            square = self.model_square(7, dc)
            file_label = "abcdefgh"[square[1]]
            self.screen.blit(font.render(file_label, True, (35,35,35)),
                             (self.board_x+dc*80+67, self.board_y+620))
        for dr in range(8):
            square = self.model_square(dr, 0)
            rank_label = str(8-square[0])
            self.screen.blit(font.render(rank_label, True, (35,35,35)),
                             (self.board_x+5, self.board_y+dr*80+5))

    def draw(self, pieces_captured_by_black, pieces_captured_by_white,
             selected_position=None, legal_moves=None, black_time=None,
             white_time=None, dt=0):
        self.draw_board(selected_position, legal_moves)
        self.screen.blit(self.board_surface, (self.board_x,self.board_y))
        self._draw_coordinates()
        self.sync_pieces()

        # if self.animation:
        #     a = self.animation
        #     a["elapsed"] += dt
        #     t = min(1.0, a["elapsed"]/a["duration"])
        #     t = t*t*(3-2*t)
        # else:
        #     a = None

        for piece, sprite in self.sprites.items():
            # if a and piece is a["piece"]:
            #     sr, sc = self.square_center(a["start"])
            #     er, ec = self.square_center(a["end"])
            #     x = sr + (er-sr)*t
            #     y = sc + (ec-sc)*t
            #     sprite.rect = sprite.image.get_rect(center=(x,y))
            # else:
            #     sprite.update_position(self.board_x,self.board_y,self.SQUARE_SIZE)
            sprite.update_position(self.board_x,self.board_y,self.SQUARE_SIZE)
            self.screen.blit(sprite.image, sprite.rect)

        # if a and a["elapsed"] >= a["duration"]:
        #     self.animation = None

        self.player_panel.draw(self.screen, pieces_captured_by_black,
                               pieces_captured_by_white, black_time,
                               white_time, self.game.turn, dt)
