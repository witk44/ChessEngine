
import chess
from ChessEngine.Engine.pst import *
piece_values = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 2
}


game_phase = "opening"

def last_move(board: chess.Board, color: chess.Color ) -> chess.Move | None:
    
    for move in reversed(board.move_stack):
        if board.color_at(move.from_square) == color:
            return move
    return chess.Move(from_square=chess.A1, to_square=chess.A2) 
 

def evaluate_board(board):
    move_count = len(board.move_stack)
    pieces_left = sum(len(board.pieces(pt, chess.WHITE)) + len(board.pieces(pt, chess.BLACK)) for pt in piece_values)

    if pieces_left < 6:
        phase = "endgame"
    elif pieces_left < 29 or move_count > 20:
        phase = "midgame"
    else:
        phase = "opening"
    PST = PST_DICT
    
    if board.is_checkmate():
        return -99999999999 if board.turn else 99999999999
    elif board.is_stalemate() or board.is_insufficient_material():
        return 0
    
    material_score = 0
    positional_score = 0
    center = [chess.D4, chess.E4, chess.D5, chess.E5]
    dev_squares = [chess.C3, chess.F3, chess.C6, chess.F6]

    if board.is_castling(last_move(board,chess.BLACK)):
                positional_score -= 250
    elif board.is_castling(last_move(board,chess.WHITE)):
                positional_score += 250
    for piece_type in piece_values:
        for square in board.pieces(piece_type, chess.WHITE):
            material_score += piece_values[piece_type]
            positional_score += 100 if square in center else 0
            positional_score += 50 if square in dev_squares else 0
            if piece_type in PST:
                
                positional_score += PST[piece_type][phase][square]*5

        for square in board.pieces(piece_type, chess.BLACK):
            material_score -= piece_values[piece_type]
            
            mirrored_square = chess.square_mirror(square)
            positional_score -= 100 if mirrored_square in [chess.D4, chess.E4, chess.D5, chess.E5] else 0
            positional_score -= 50 if mirrored_square in [chess.C3, chess.F3, chess.C6, chess.F6] else 0
            if piece_type in PST:
                
                positional_score -= PST[piece_type][phase][mirrored_square]*5
    
    total_score = material_score + .1 * positional_score
    return total_score if board.turn == chess.WHITE else -total_score
