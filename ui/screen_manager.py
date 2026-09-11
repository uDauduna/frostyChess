from enum import Enum

from ui.screens.main_menu import MainMenu
from ui.screens.game_setup import GameSetup
from ui.screens.game_screen import GameScreen
from ui.screens.pause_screen import PauseScreen
from ui.screens.game_over import GameOver


class Screen(Enum):
    MAIN_MENU = 1
    GAME_SETUP = 2
    PLAYING = 3
    PAUSED = 4
    GAME_OVER = 5


class ScreenManager:

    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.current_screen = Screen.MAIN_MENU
        self.main_menu = MainMenu(screen, self)
        self.game_setup = GameSetup(screen, self)
        self.pause_screen = PauseScreen(screen, self)
        self.game_over = GameOver(screen, self)
        self.active_screen = self.main_menu
        self.game_screen = None
        return

    def show_main_menu(self):
        self.current_screen = Screen.MAIN_MENU
        self.active_screen = self.main_menu
        return

    def show_game_setup(self):
        self.current_screen = Screen.GAME_SETUP
        self.active_screen = self.game_setup
        return

    def start_game(self, color, difficulty, mode="casual"):
        self.game_screen = GameScreen(self.screen, self, color, difficulty, mode)
        self.current_screen = Screen.PLAYING
        self.active_screen = self.game_screen
        return

    def pause_game(self):
        if self.game_screen is not None:
            self.current_screen = Screen.PAUSED
            self.active_screen = self.pause_screen
        return

    def resume_game(self):
        if self.game_screen is not None:
            self.current_screen = Screen.PLAYING
            self.active_screen = self.game_screen
        return

    def show_game_over(self, result):
        self.game_over.set_result(result)
        self.current_screen = Screen.GAME_OVER
        self.active_screen = self.game_over
        return

    def quit(self):
        self.running = False
        return

    def handle_event(self, event):
        self.active_screen.handle_event(event)
        return

    def update(self):
        self.active_screen.update()
        return

    def draw(self):
        self.active_screen.draw()
        return