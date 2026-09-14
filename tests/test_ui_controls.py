import pytest
pygame = pytest.importorskip("pygame")

from game import ChessGame
from ui.renderer import Renderer
from ui.screens.game_screen import GameScreen
from ui.screens.game_setup import GameSetup


class DummyManager:
    def __init__(self):
        self.started = None
        self.paused = False
        self.main_menu = False

    def start_game(self, color, difficulty, mode):
        self.started = (color, difficulty, mode)

    def pause_game(self):
        self.paused = True

    def show_main_menu(self):
        self.main_menu = True


def make_screen():
    pygame.init()
    return pygame.Surface((1300, 760))


def test_renderer_flip_mapping_is_reversible():
    screen = make_screen()
    game = ChessGame()
    renderer = Renderer(screen, game, flipped=False)
    assert renderer.display_square((7, 0)) == (7, 0)
    assert renderer.model_square(7, 0) == (7, 0)
    renderer.set_flipped(True)
    assert renderer.display_square((7, 0)) == (0, 7)
    assert renderer.model_square(0, 7) == (7, 0)
    pygame.quit()


def test_renderer_square_center_changes_when_flipped():
    screen = make_screen()
    game = ChessGame()
    renderer = Renderer(screen, game, board_x=100, board_y=20, flipped=False)
    normal = renderer.square_center((7, 0))
    renderer.set_flipped(True)
    flipped = renderer.square_center((7, 0))
    assert normal != flipped
    pygame.quit()


def test_game_screen_black_starts_flipped_and_can_flip_back():
    screen = make_screen()
    manager = DummyManager()
    game_screen = GameScreen(screen, manager, "black", "medium", "casual")
    assert game_screen.renderer.flipped is True
    game_screen.flip_board()
    assert game_screen.renderer.flipped is False
    pygame.quit()


def test_competitive_mode_disables_undo():
    screen = make_screen()
    manager = DummyManager()
    game_screen = GameScreen(screen, manager, "white", "medium", "competitive")
    assert game_screen.undo_button.enabled is False
    assert game_screen.game.can_undo() is False
    pygame.quit()


def test_casual_mode_enables_undo_and_undoes():
    screen = make_screen()
    manager = DummyManager()
    game_screen = GameScreen(screen, manager, "white", "medium", "casual")
    assert game_screen.undo_button.enabled is True
    assert game_screen.game.push_uci("e2e4")
    game_screen.undo()
    assert game_screen.game.to_fen() == "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    pygame.quit()


def test_game_setup_selection_and_start_callback():
    screen = make_screen()
    manager = DummyManager()
    setup = GameSetup(screen, manager)
    setup.select_color("black")
    setup.select_difficulty("hard")
    setup.select_mode("competitive")
    setup.start_game()
    assert manager.started == ("black", "hard", "competitive")
    pygame.quit()
