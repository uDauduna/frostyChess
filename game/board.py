from moves import Piece
class Board:
    def __init__(self, clock=False):
        self.board = [["r", "n", "b", "q", "k", "b", "n", "r"],
                      ["p", "p", "p", "p", "p", "p", "p", "p"],
                      [".", ".", ".", ".", ".", ".", ".", "."],
                      [".", ".", ".", ".", ".", ".", ".", "."],
                      [".", ".", ".", ".", ".", ".", ".", "."],
                      [".", ".", ".", ".", ".", ".", ".", "."],
                      ["P", "P", "P", "P", "P", "P", "P", "P"],
                      ["R", "N", "B", "Q", "K", "B", "N", "R"],
                      ]

        self.ranks = {0:8,
                      1:7,
                      2:6,
                      3:5,
                      4:4,
                      5:3,
                      6:2,
                      7:1,
                      }
        
        self.files = {0:"a",
                      1:"b",
                      2:"c",
                      3:"d",
                      4:"e",
                      5:"f",
                      6:"g",
                      7:"h",
                      }
        self.pieces = self.board
        self.black_in_check = False
        self.white_in_check = False
        self.clock = clock

    def initialize_Pieces(self):
        for x in range(len(self.board)):
            for y in range(len(self.board)):
                piece_type = self.board[x][y]
                if piece_type != ".":
                    color = "black" if piece_type.isLower() else "white"
                    piece = Piece(piece_type, (x, y))
                    if color == "black":
                        self.black_pieces[piece.id] = piece
                        
                    else:
                        self.white_pieces[piece.id] = piece

                    self.pieces[x][y] = piece

        return


    def get_board(self):
        """
        Return either the FEN or PGN 
        """
        return

    def move_piece(self, old_pos, new_pos):
        piece_type = self.board[old_pos[0], old_pos[1]]
        piece = self.pieces[old_pos[0], old_pos[1]]
        if piece.legal_move(new_pos):
            self.board[old_pos[0]][old_pos[1]] = "."
            self.board[new_pos[0]][new_pos[1]] = piece_type
        else:
            """
            We can't raise an error
            """
            print("Illegal Move")

        return

    def square_is_empty(self, pos):
        if self.board[pos[0]][pos[1]] == ".":
            return True
        return False


    def timer(self):
        """
        To be implemented
        """
        return
    

board = Board()

print(board.board)