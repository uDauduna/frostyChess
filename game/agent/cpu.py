"""
This is the game playing agent class. This agent will player against the human or against itself.
"""
# Maybe import from the game class as well as the uci module
class Agent:
    def __init__(self, color):
        self.color = color

    def get_board_state(self, text):
        """
        Get a snapshot of the current board state so the agent can make a move.
        """
        # start, end, promotion = uci_to_move(text)
        # return self.make_move(start, end, promotion)
        pass

    def make_move(self):
        pass
