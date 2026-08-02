"""
Come back to this.

Not yet done

If any legal move threatens the king directly, call, check then call legal move for the king,
also create a path for the pieces so that when the king is in check you can find out which moves can block the path
"""

class Piece:
    def __init__(self, piece, position):
        self.piece = piece
        self.position = position #tuple
        self.promotion_elgible = False
        self.active = True

    def in_bounds(self,pos):
        row, col = pos
        if row >= 0 and row < 8:
            if col < 8 and col < 8:
                return True
        return False

    def diagonal_move(self,old_pos, new_pos):
        legal_positions = []
        row, col = old_pos
        legal = False
        while (row < 8 and col < 8):
            row += 1
            col += 1 
            if empty_square((row, col)):
                legal_positions.append((row, col))
            else:
                if legal_obstacle((row, col)):
                    legal_positions.append((row, col))
                    break
            if (row, col) == new_pos:
                legal = True

        while (row >= 0 and col >= 0):
            row -= 1
            col -= 1 
            if empty_square((row, col)):
                legal_positions.append((row, col))
            else:
                if legal_obstacle((row, col)):
                    legal_positions.append((row, col))
                    break

            if (row, col) == new_pos:
                legal = True
        while (row >= 0 and col < 8):
            row -= 1
            col += 1 
            if empty_square((row, col)):
                legal_positions.append((row, col))
            else:
                if legal_obstacle((row, col)):
                    legal_positions.append((row, col))
                    break
            if (row, col) == new_pos:
                legal = True
        while (row < 8 and col >= 0):
            row += 1
            col -= 1 
            if empty_square((row, col)):
                legal_positions.append((row, col))
            else:
                if legal_obstacle((row, col)):
                    legal_positions.append((row, col))
                    break
            if (row, col) == new_pos:
                legal = True
            self.move(new_pos)
        return legal_positions

    
    def horizontal_vertical_move(self, old_pos, new_pos):
        legal_positions = []
        row, col = old_pos
        legal = False
        while row < 8 :
            row += 1
            if empty_square((row, col)):
                legal_positions.append((row, col))
            else:
                if legal_obstacle((row, col)):
                    legal_positions.append((row, col))
                    break
            if (row, col) == new_pos:
                legal = True

        while row >= 0:
            row -= 1
            if empty_square((row, col)):
                legal_positions.append((row, col))
            else:
                if legal_obstacle((row, col)):
                    legal_positions.append((row, col))
                    break

            if (row, col) == new_pos:
                legal = True
        while col < 8:
            col += 1 
            if empty_square((row, col)):
                legal_positions.append((row, col))
            else:
                if legal_obstacle((row, col)):
                    legal_positions.append((row, col))
                    break
            if (row, col) == new_pos:
                legal = True
        while col >= 0:
            row += 1
            col -= 1 
            if empty_square((row, col)):
                legal_positions.append((row, col))
            else:
                if legal_obstacle((row, col)):
                    legal_positions.append((row, col))
                    break
            if (row, col) == new_pos:
                legal = True

        if legal:
            if not_in_check:
                play_move(new_pos)

        return legal_positions

