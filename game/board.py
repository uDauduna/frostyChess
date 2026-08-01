from .pieces.pawn import Pawn
from .pieces.knight import Knight
from .pieces.bishop import Bishop
from .pieces.rook import Rook
from .pieces.king import King
from .pieces.queen import Queen


class Board:
    def __init__(self, clock=False):
        self.board_state = [["r", "n", "b", "q", "k", "b", "n", "r"],
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
        self.pieces = [[".", ".", ".", ".", ".", ".", ".", "."],
                      [".", ".", ".", ".", ".", ".", ".", "."],
                      [".", ".", ".", ".", ".", ".", ".", "."],
                      [".", ".", ".", ".", ".", ".", ".", "."],
                      [".", ".", ".", ".", ".", ".", ".", "."],
                      [".", ".", ".", ".", ".", ".", ".", "."],
                      [".", ".", ".", ".", ".", ".", ".", "."],
                      [".", ".", ".", ".", ".", ".", ".", "."],
                      ]
        self.initialize_Pieces()
        self.black_in_check = False
        self.white_in_check = False
        self.clock = clock

    def initialize_Pieces(self):
        for x in range(len(self.board_state)):
            for y in range(len(self.board_state)):
                piece_type = self.board_state[x][y]
                if piece_type != ".":
                    color = "black" if piece_type.islower() else "white"
                    if piece_type.lower() == "p":
                        self.pieces[x][y] = Pawn((x, y), color)
                    elif piece_type.lower() == "r":
                        self.pieces[x][y] = Rook((x, y), color)
                    elif piece_type.lower() == "n":
                        self.pieces[x][y] = Knight((x, y), color)
                    elif piece_type.lower() == "b":
                        self.pieces[x][y] = Bishop((x, y), color)
                    elif piece_type.lower() == "k":
                        self.pieces[x][y] = King((x, y), color)
                    elif piece_type.lower() == "q":
                        self.pieces[x][y] = Queen((x, y), color)
        return


    def get_board(self):
        """
        Return either the FEN or PGN 
        """
        return

    def square_is_empty(self, pos):
        if self.board_state[pos[0]][pos[1]] == ".":
            return True
        return False


    def timer(self):
        """
        To be implemented
        """
        return