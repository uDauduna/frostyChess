class Board:
    def __init__(self):
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
        

    def get_board(self):
        """
        Return either the FEN or PGN 
        """
        return

    def change_state(self, piece, old_pos, new_pos):

        """
        Change the state base on the move
        """
        if legal(new_pos):
            self.board[old_pos[0]][old_pos[1]] = "."
            self.board[new_pos[0]][new_pos[1]] = piece
        else:
            """
            We can't raise an error
            """
            print("Illegal Move")

        return

    

board = Board()

print(board.board)