# core/bitboard.py

from Core.constants import PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING, WHITE, BLACK
from Core.utils import print_bitboard

class BitboardPosition:
    def __init__(self):
        # Each entry: piece_type (0–5) x color (0 or 1)
        self.pieces = {
            (PAWN, WHITE):   0x000000000000FF00,
            (KNIGHT, WHITE): 0x0000000000000042,
            (BISHOP, WHITE): 0x0000000000000024,
            (ROOK, WHITE):   0x0000000000000081,
            (QUEEN, WHITE):  0x0000000000000008,
            (KING, WHITE):   0x0000000000000010,
            (PAWN, BLACK):   0x00FF000000000000,
            (KNIGHT, BLACK): 0x4200000000000000,
            (BISHOP, BLACK): 0x2400000000000000,
            (ROOK, BLACK):   0x8100000000000000,
            (QUEEN, BLACK):  0x0800000000000000,
            (KING, BLACK):   0x1000000000000000,
        }

        self.side_to_move = WHITE
        self.castling_rights = {'K', 'Q', 'k', 'q'}
        self.en_passant = None
        self.halfmove_clock = 0
        self.fullmove_number = 1

        
    def toggle_side(self):
        self.side_to_move = WHITE if self.side_to_move == BLACK else BLACK

    def set_castling_rights(self, k, q, K, Q):
        self.castling_rights = (
            (1 if K else 0) |
            (1 << 1 if Q else 0) |
            (1 << 2 if k else 0) |
            (1 << 3 if q else 0)
        )

    def can_castle(self, color, side):
        if color == WHITE:
            return bool(self.castling_rights & (1 if side == "K" else 1 << 1))
        else:
            return bool(self.castling_rights & (1 << 2 if side == "k" else 1 << 3))

    def set_en_passant(self, square_index: int | None):
        self.en_passant_square = square_index

    def increment_halfmove(self):
        self.halfmove_clock += 1

    def reset_halfmove(self):
        self.halfmove_clock = 0

    def next_fullmove(self):
        if self.side_to_move == BLACK:
            self.fullmove_number += 1
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
