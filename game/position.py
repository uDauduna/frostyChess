from dataclasses import dataclass

@dataclass(frozen=True)
class Position:
    board: tuple
    turn: str
    castling_rights: tuple
    en_passant_square: tuple | None