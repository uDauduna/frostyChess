"""
Come back to this.

Not yet done
"""

class Piece:
    def __init__(self, piece, position):
        self.piece = piece
        self.position = position #tuple
        self.promotion_elgible = False
        self.active = True

    def move(self):
        return

    def legal(self, move):
        if move == "castle":
            if self.castle_legal:
                #castle
                castle = "castle"

    def in_bounds(self,pos):
        x, y = pos
        if x >= 0 and x < 8:
            if y < 8 and y < 8:
                return True
        return False

    def knight_move(self,old_pos, new_pos):
        legal = False
        legal_moves = []

        x, y = old_pos
        if self.in_bounds(x - 1, y - 2):
            legal_moves.append((x, y))
            if new_pos == (x - 1, y - 2):
                legal = True
        if self.in_bounds(x + 1, y - 2):
            legal_moves.append((x, y))
            if new_pos == (x + 1, y - 2):
                legal = True
        if self.in_bounds(x - 2, y - 1):
            legal_moves.append((x, y))
            if new_pos == (x - 2, y - 1):
                legal = True
        if self.in_bounds(x + 2, y - 1):
            legal_moves.append((x, y))
            if new_pos == (x + 2, y - 1):
                legal = True
        if self.in_bounds(x - 1, y + 2):
            legal_moves.append((x, y))
            if new_pos == (x - 1, y + 2):
                legal = True
        if self.in_bounds(x - 2, y + 1):
            legal_moves.append((x, y))
            if new_pos == (x - 2, y + 1):
                legal = True
        if self.in_bounds(x + 1, y + 2):
            legal_moves.append((x, y))
            if new_pos == (x + 1, y + 2):
                legal = True
        if self.in_bounds(x + 2, y + 1):
            legal_moves.append((x, y))
            if new_pos == (x + 2, y + 1):
                legal = True
        if legal:
            if not_in_check:
                play_move(new_pos)
                

    def diagonal_move(self,old_pos, new_pos):
        legal_positions = []
        x, y = old_pos
        legal = False
        while (x < 8 and y < 8):
            x += 1
            y += 1 
            if empty_square((x, y)):
                legal_positions.append((x, y))
            else:
                if legal_obstacle((x, y)):
                    legal_positions.append((x, y))
            if (x, y) == new_pos:
                legal = True

        while (x >= 0 and y >= 0):
            x -= 1
            y -= 1 
            if empty_square((x, y)):
                legal_positions.append((x, y))
            else:
                if legal_obstacle((x, y)):
                    legal_positions.append((x, y))

            if (x, y) == new_pos:
                legal = True
        while (x >= 0 and y < 8):
            x -= 1
            y += 1 
            if empty_square((x, y)):
                legal_positions.append((x, y))
            else:
                if legal_obstacle((x, y)):
                    legal_positions.append((x, y))
            if (x, y) == new_pos:
                legal = True
        while (x < 8 and y >= 0):
            x += 1
            y -= 1 
            if empty_square((x, y)):
                legal_positions.append((x, y))
            else:
                if legal_obstacle((x, y)):
                    legal_positions.append((x, y))
            if (x, y) == new_pos:
                legal = True

        if legal:
            if not in_check:
                play_move(new_pos)

        return legal_positions

    
    def horizontal_vertical_move(self, old_pos, new_pos):
        legal_positions = []
        x, y = old_pos
        legal = False
        while x < 8 :
            x += 1
            if empty_square((x, y)):
                legal_positions.append((x, y))
            else:
                if legal_obstacle((x, y)):
                    legal_positions.append((x, y))
            if (x, y) == new_pos:
                legal = True

        while x >= 0:
            x -= 1
            if empty_square((x, y)):
                legal_positions.append((x, y))
            else:
                if legal_obstacle((x, y)):
                    legal_positions.append((x, y))

            if (x, y) == new_pos:
                legal = True
        while y < 8:
            y += 1 
            if empty_square((x, y)):
                legal_positions.append((x, y))
            else:
                if legal_obstacle((x, y)):
                    legal_positions.append((x, y))
            if (x, y) == new_pos:
                legal = True
        while y >= 0:
            x += 1
            y -= 1 
            if empty_square((x, y)):
                legal_positions.append((x, y))
            else:
                if legal_obstacle((x, y)):
                    legal_positions.append((x, y))
            if (x, y) == new_pos:
                legal = True

        if legal:
            if not_in_check:
                play_move(new_pos)

        return legal_positions

