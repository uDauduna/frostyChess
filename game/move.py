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