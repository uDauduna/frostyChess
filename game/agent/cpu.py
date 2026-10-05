"""
This is the game playing agent class. This agent will player against the human or against itself.
"""

import random


# Maybe import from the game class as well as the uci module
class Agent:
    def __init__(self, color):
        """
        Initialize agent with the opposite color
        """
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

    def choose_random_move(self, game):

        """
        Choose from a set of all legal moves
        """
        moves=game.legal_move_pairs()
        if not moves:
            return
        start,end=random.choice(moves)
        promotion="queen" if game.board.get_piece(start).piece_type=="pawn" and end[0] in (0,7) else None
        game.make_move(start,end,promotion)
        if game.promotion_pending: game.promote("queen")
        return
