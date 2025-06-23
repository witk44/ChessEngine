from main import engine_color
import chess
from pst import *
piece_values = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000
}
PST = {
    chess.PAWN: pawn_pst,
    chess.KNIGHT: knight_pst,
    chess.BISHOP: bishop_pst,
    chess.ROOK: rook_pst,
    chess.QUEEN: queen_pst,
    chess.KING: king_pst
}





 

def evaluate_board(board):
    if board.is_checkmate():
        return -99999999999 if board.turn else 99999999999
    elif board.is_stalemate() or board.is_insufficient_material():
        return 0
    
    score = 0
    for piece_type in piece_values:
        for square in board.pieces(piece_type, chess.WHITE):
            score += piece_values[piece_type]
            if piece_type in PST:
                score += PST[piece_type][square]

        for square in board.pieces(piece_type, chess.BLACK):
            score -= piece_values[piece_type]
            if piece_type in PST:
                mirrored_square = chess.square_mirror(square)
                score -= PST[piece_type][mirrored_square]
    return score