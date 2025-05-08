#chess engine utils
from core.constants import SQUARES, INDEX_TO_SQUARE

def square_name_to_index(name: str) -> int:
    """Convert algebraic notation (e.g., 'e4') to square index (0-63)."""
    return SQUARES[name]

def index_to_square_name(index: int) -> str:
    """Convert square index (0-63) to algebraic notation (e.g., 'e4')."""
    return INDEX_TO_SQUARE[index]

def index_to_bitboard(index: int) -> int:
    """Convert square index to bitboard with a 1 at that position."""
    return 1 << index

def bitboard_to_indices(bitboard: int) -> list[int]:
    """Get list of square indices (0–63) where bitboard has bits set."""
    return [i for i in range(64) if (bitboard >> i) & 1]

def bitboard_to_squares(bitboard: int) -> list[str]:
    """Get list of square names (like 'e4') where bitboard has bits set."""
    return [index_to_square_name(i) for i in bitboard_to_indices(bitboard)]

def print_bitboard(bb: int) -> None:
    """Pretty-print a bitboard for debugging."""
    print("Bitboard view:")
    for rank in reversed(range(8)):
        row = ''
        for file in range(8):
            index = rank * 8 + file
            row += '1 ' if (bb >> index) & 1 else '. '
        print(row)
    print()
