
import chess
from ChessEngine.Engine.pst import *
piece_values = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000
}


game_phase = "opening"


 

def evaluate_board(board):
    pieces_left = len(board.pieces(piece_type, chess.BLACK))+len(board.pieces(piece_type, chess.WHITE))
    if pieces_left < 28:
        game_phase = "midgame"
    elif pieces_left < 6:
        game_phase = "endgame"
    PST = PST_DICT
    once = 1
    if board.is_checkmate():
        return -99999999999 if board.turn else 99999999999
    elif board.is_stalemate() or board.is_insufficient_material():
        return 0
    
    score = 0
    for piece_type in piece_values:
        for square in board.pieces(piece_type, chess.WHITE):
            score += piece_values[piece_type]
            if piece_type in PST:
                score += PST[piece_type][game_phase][square]*10

        for square in board.pieces(piece_type, chess.BLACK):
            score -= piece_values[piece_type]
            if piece_type in PST:
                mirrored_square = chess.square_mirror(square)
                
                score -= PST[piece_type][game_phase][mirrored_square]*10
    return score