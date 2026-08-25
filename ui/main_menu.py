import pygame

class MainMenu():

    def __init__(self):
        self.screen_manager = screen_manager
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.title_font = pygame.font.Font(None, 90)
        self.button_font = pygame.font.Font(None, 42)
        button_width = 300
        button_height = 65
        x = (self.width - button_width) // 2
        self.start_button = Button(
            (
                x,
                self.height // 2,
                button_width,
                button_height
            ),
            "START GAME",
            self.button_font,
            self.start_game
        )

        self.quit_button = Button(
            (
                x,
                self.height // 2 + 90,
                button_width,
                button_height
            ),
            "QUIT",
            self.button_font,
            self.quit_game
        )

    def start_game(self):
        self.screen_manager.show_game_setup()

    def quit_game(self):
        self.screen_manager.quit()

    def handle_event(self, event):
        self.start_button.handle_event(event)
        self.quit_button.handle_event(event)

    def update(self):
        pass

    def draw(self)
        self.screen.fill((25, 30, 38))
        title = self.title_font.render(
            "FROSTY CHESS",
            True,
            (240, 240, 240)
        )
        title_rect = title.get_rect(
            center=(self.width // 2, 170)
        )
        self.screen.blit(title, title_rect)
        self.start_button.draw(self.screen)
        self.quit_button.draw(self.screen)