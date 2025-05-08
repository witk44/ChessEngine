from Engine.bitboard import BitboardPosition
from Core.constants import PAWN, WHITE
from Core.utils import square_name_to_index, index_to_bitboard

pos = BitboardPosition()
e4 = square_name_to_index("e2")
pos.set_piece(PAWN, WHITE, index_to_bitboard(e4))
pos.print_board()
