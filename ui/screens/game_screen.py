"""This module contains the game screen used by frostyChess."""

import pygame

from .base_screen import BaseScreen
from ui.components import Button
from ui.renderer import Renderer
from ui.promotion_ui import PromotionUI
from game.chess_game import ChessGame
from game.pgn import export_pgn


class GameScreen(BaseScreen):
    def __init__(self, screen, screen_manager, color, difficulty, mode="casual"):
        super().__init__(screen)
        self.screen_manager = screen_manager
        self.player_color = color
        self.difficulty = difficulty
        self.mode = mode
        self.game = ChessGame()
        self.renderer = Renderer(screen, self.game, flipped=(color == "black"))
        self.promotion_ui = PromotionUI()
        self.selected_square = None
        self.selected_legal_moves = []
        self.last_result = None
        self.checked_state = None
        font = pygame.font.Font(None, 28)
        self.title_font = pygame.font.Font(None, 30)
        self.hint_font = pygame.font.Font(None, 22)
        self.flip_button = Button((970, 600, 120, 42), "FLIP", font, self.flip_board)
        self.undo_button = Button((1100, 600, 120, 42), "UNDO", font, self.undo)
        self.undo_button.enabled = mode == "casual"
        self.buttons = [self.flip_button, self.undo_button]

    def flip_board(self):
        self.renderer.set_flipped(not self.renderer.flipped)

    def undo(self):
        if self.mode != "casual" or not self.game.can_undo():
            return
        if self.game.undo():
            self.selected_square = None
            self.selected_legal_moves = []

    def mouse_to_board(self, position):
        x, y = position
        if not (self.renderer.board_x <= x < self.renderer.board_x + 640 and
                self.renderer.board_y <= y < self.renderer.board_y + 640):
            return None
        display_col = int((x - self.renderer.board_x) // 80)
        display_row = int((y - self.renderer.board_y) // 80)
        return self.renderer.model_square(display_row, display_col)

    def select_square(self, square):
        self.selected_square = square
        self.selected_legal_moves = self.game.legal_moves(square) if square is not None else []

    def handle_board_click(self, event):
        clicked = self.mouse_to_board(event.pos)
        if clicked is None:
            self.select_square(None)
            return

        if self.selected_square is None:
            piece = self.game.board.get_piece(clicked)
            if piece and piece.color == self.game.turn:
                self.select_square(clicked)
            return

        if clicked == self.selected_square:
            self.select_square(None)
            return

        start = self.selected_square
        piece = self.game.board.get_piece(start)
        if piece and clicked in self.selected_legal_moves and self.game.make_move(start, clicked):
            self.renderer.start_move_animation(self.game.move_history[-1].piece, start, clicked)
            self.select_square(None)
            if self.game.promotion_pending:
                self.promotion_ui.open(self.game.promotion_pending)
            return

        piece = self.game.board.get_piece(clicked)
        if piece and piece.color == self.game.turn:
            self.select_square(clicked)
        else:
            self.select_square(None)

    def handle_promotion(self, event):
        choice = self.promotion_ui.handle_click(event)
        if choice and self.game.promote(choice):
            self.promotion_ui.close()
            self.checked_move_count = len(self.game.move_history)

    def handle_event(self, event):
        for button in self.buttons:
            button.handle_event(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.screen_manager.pause_game()
            elif event.key == pygame.K_f:
                self.flip_board()
            elif event.key == pygame.K_u and self.mode == "casual":
                self.undo()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.promotion_ui.active:
                self.handle_promotion(event)
            else:
                self.handle_board_click(event)

    def update(self):
        """Check game-ending conditions only after a state change."""
        state = (self.game.state_version, self.game.promotion_pending is not None)
        if state == self.checked_state:
            return
        self.checked_state = state

        # A promotion is not a completed turn until the player chooses a piece.
        if self.game.promotion_pending is not None:
            return

        if not self.game.is_checkmate() and not self.game.is_draw():
            return

        if self.game.is_checkmate():
            result = "CHECKMATE — BLACK WINS" if self.game.turn == "white" else "CHECKMATE — WHITE WINS"
        elif self.game.is_stalemate():
            result = "DRAW — STALEMATE"
        elif self.game.is_threefold_repetition():
            result = "DRAW — THREEFOLD REPETITION"
        elif self.game.is_fifty_move_draw():
            result = "DRAW — 50-MOVE RULE"
        else:
            result = "DRAW — INSUFFICIENT MATERIAL"

        if self.last_result != result:
            self.last_result = result
            self.screen_manager.show_game_over(result)

    def draw(self):
        self.screen.fill((18, 25, 32))
        self.renderer.draw(
            self.game.pieces_captured_by_black,
            self.game.pieces_captured_by_white,
            self.selected_square,
            self.selected_legal_moves,
        )

        status_rect = pygame.Rect(270, 5, 500, 42)
        pygame.draw.rect(self.screen, (34, 43, 53), status_rect, border_radius=8)
        pygame.draw.rect(self.screen, (105, 118, 128), status_rect, width=1, border_radius=8)

        title = self.title_font.render(
            f"{self.mode.upper()}  •  {self.player_color.upper()}  •  {self.difficulty.upper()}",
            True,
            (235, 235, 235),
        )
        self.screen.blit(title, title.get_rect(center=status_rect.center))

        controls = ["[F] FLIP BOARD", "[U] UNDO", "[ESC] PAUSE"]
        x = 300
        for text in controls:
            surface = self.hint_font.render(text, True, (175, 190, 198))
            self.screen.blit(surface, (x, 690))
            x += surface.get_width() + 35

        for button in self.buttons:
            button.draw(self.screen)
        if self.promotion_ui.active:
            self.promotion_ui.draw(self.screen)
