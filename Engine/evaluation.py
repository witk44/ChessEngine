from main import engine_color
import chess

piece_values = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000
}
 

def evaluate_board(board):
    if board.is_checkmate():
        return -99999999999 if board.turn else 99999999999
    elif board.is_stalemate() or board.is_insufficient_material():
        return 0
    
    score = 0
    for piece in piece_values:
        score += len(board.pieces(piece,chess.WHITE))*piece_values[piece]
        score -= len(board.pieces(piece,chess.BLACK))*piece_values[piece]
    return score