from abc import ABC, abstractmethod


class BaseScreen(ABC):
    def __init__(self, screen):
        self.screen = screen

    @abstractmethod
    def handle_event(self, event):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self):
        pass