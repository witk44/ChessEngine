# core/bitboard.py

from Core.constants import PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING, WHITE, BLACK
from Core.utils import print_bitboard

class BitboardPosition:
    def __init__(self):
        # Each entry: piece_type (0–5) x color (0 or 1)
        self.pieces = {
            (PAWN, WHITE): 0,
            (KNIGHT, WHITE): 0,
            (BISHOP, WHITE): 0,
            (ROOK, WHITE): 0,
            (QUEEN, WHITE): 0,
            (KING, WHITE): 0,
            (PAWN, BLACK): 0,
            (KNIGHT, BLACK): 0,
            (BISHOP, BLACK): 0,
            (ROOK, BLACK): 0,
            (QUEEN, BLACK): 0,
            (KING, BLACK): 0,
        }

    def set_piece(self, piece_type: int, color: int, bitboard: int):
        """Set bitboard for a specific piece type and color."""
        self.pieces[(piece_type, color)] = bitboard

    def get_piece(self, piece_type: int, color: int) -> int:
        """Get bitboard for a specific piece type and color."""
        return self.pieces[(piece_type, color)]

    def occupancy(self, color: int) -> int:
        """Return combined bitboard of all pieces of a color."""
        return sum(self.pieces[(ptype, color)] for ptype in range(6))

    def all_occupancy(self) -> int:
        """Return combined bitboard of all pieces on the board."""
        return self.occupancy(WHITE) | self.occupancy(BLACK)

    def empty_squares(self) -> int:
        """Return bitboard of all empty squares."""
        return ~self.all_occupancy() & 0xFFFFFFFFFFFFFFFF  # 64-bit mask

    def print_board(self):
        """Print full board from piece bitboards."""
        print("Full Board:")
        board = ['.'] * 64
        symbols = {
            (PAWN, WHITE): 'P', (KNIGHT, WHITE): 'N', (BISHOP, WHITE): 'B',
            (ROOK, WHITE): 'R', (QUEEN, WHITE): 'Q', (KING, WHITE): 'K',
            (PAWN, BLACK): 'p', (KNIGHT, BLACK): 'n', (BISHOP, BLACK): 'b',
            (ROOK, BLACK): 'r', (QUEEN, BLACK): 'q', (KING, BLACK): 'k'
        }
        for (ptype, color), bb in self.pieces.items():
            for i in range(64):
                if (bb >> i) & 1:
                    board[i] = symbols[(ptype, color)]
        for rank in reversed(range(8)):
            print(' '.join(board[rank*8:(rank+1)*8]))
        print()
