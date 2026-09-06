from dataclasses import dataclass

@dataclass
class Move:
    start: tuple
    end: tuple
    piece: object
    captured_piece: object = None
    promotion: str | None = None
    is_castling: bool = False
    is_en_passant: bool = False
    previous_en_passant_target: tuple | None = None
    previous_castling_rights: dict | None = None
    previous_halfmove_clock: int = 0
    previous_fullmove_number: int = 1

    @property
    def resets_fifty_move_counter(self):
        return self.piece.piece_type == "pawn" or self.captured_piece is not None
