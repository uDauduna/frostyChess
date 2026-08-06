from .pieces.pawn import Pawn
from .pieces.knight import Knight
from .pieces.bishop import Bishop
from .pieces.rook import Rook
from .pieces.king import King
from .pieces.queen import Queen
import pygame


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
        self.piece_group = pygame.sprite.Group()
        self.initialize_Pieces()
        self.black_in_check = False
        self.white_in_check = False
        self.clock = clock
        self.promotion = False


    def initialize_Pieces(self):
        for row in range(len(self.board_state)):
            for col in range(len(self.board_state)):
                piece_type = self.board_state[row][col]
                if piece_type != ".":
                    color = "black" if piece_type.islower() else "white"
                    if piece_type.lower() == "p":
                        piece = Pawn((row, col), color)
                    elif piece_type.lower() == "r":
                        piece = Rook((row, col), color)
                    elif piece_type.lower() == "n":
                        piece = Knight((row, col), color)
                    elif piece_type.lower() == "b":
                        piece = Bishop((row, col), color)
                    elif piece_type.lower() == "k":
                        piece = King((row, col), color)
                    elif piece_type.lower() == "q":
                        piece = Queen((row, col), color)
                    self.pieces[row][col] = piece
                    self.piece_group.add(piece)
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

    def promote_piece(self, pawn, promoted_piece):
        pieces = {
            "q": Queen,
            "r": Rook,
            "b": Bishop,
            "n": Knight,
        }
        new_piece = pieces[promoted_piece.lower()]((pawn.row, pawn.col),pawn.color)
        pawn.kill()
        self.pieces[pawn.row][pawn.col] = new_piece
        self.board_state[pawn.row][pawn.col] = promoted_piece
        self.piece_group.add(new_piece)

    def timer(self):
        """
        To be implemented
        """
        return