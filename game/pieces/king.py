from ..ui.sprite import Piece 

class King(Piece):
    def __init__(self, pos, color):
        super().__init__("king", color, pos)
        self.row, self.col = pos
        self.color = color

    def eligible_moves(self, board):

        """
        Update when you have check discovery etc
        """
        self.eligible = []
        row, col = self.row, self.col

        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]
        for dr, dc in directions:
            new_row = row + dr
            new_col = col + dc
            if not (0 <= new_row < 8 and 0 <= new_col < 8):
                continue

            if board.square_is_empty((new_row, new_col)):
                self.eligible.append((new_row, new_col))
            else:
                if board.pieces[new_row][new_col].color != self.color:
                    self.eligible.append((new_row, new_col))
        return self.eligible
   
    def is_move_legal(self, pos, board):
        return pos in self.eligible_moves(board)

    def update_position(self, new_pos):
        self.row, self.col = new_pos
        self.update_board_position(new_pos)
        return

