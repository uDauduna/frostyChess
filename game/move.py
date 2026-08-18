from dataclasses import dataclass

@dataclass
class Move:
    start: tuple
    end: tuple
    piece: object
    captured_piece: object = None
    promotion: str = None
    is_castling: bool = False
    is_en_passant: bool = False

    @property
    def resets_fifty_move_counter(self) ->bool:
        return (self.piece.piece_type == "pawn" or self.captured_piece is not None)