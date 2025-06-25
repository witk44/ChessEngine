import chess
from ChessEngine.Engine import evaluation
transposition_table = {}

def score_move(board, move):
    if board.is_capture(move):
        return 10
    if board.gives_check(move):
        return 5
    return 0


def Quiesce(alpha,beta,board,depth=3) -> int:
    static_score = evaluation.evaluate_board(board)
    best_score = static_score
    if(best_score >= beta):
        return best_score
    if best_score > alpha:
        alpha = best_score
    
    if depth == 0:
        return best_score
    
    for move in sorted(board.legal_moves, key = lambda m: score_move(board,m),reverse=True):
        if not board.is_capture(move) and not board.is_check():
            continue
        board.push(move)
        score = -(Quiesce(-beta,-alpha,board,depth-1))
        board.pop()
        if score >= beta:
            return beta
        if score > alpha:
            alpha = score
    return alpha


def minimax(board: chess.Board, depth, alpha, beta, maximizing,initial_maximizing):
    board_key = (board.fen(), depth, maximizing)
    if board_key in transposition_table:
        return transposition_table[board_key]

    if depth == 0 or board.is_game_over():
        score = Quiesce(alpha, beta, board) 
        transposition_table[board_key] = (score, None)
        return score, None

    best_move = None
    moves = sorted(board.legal_moves, key=lambda m: score_move(board, m), reverse=True)
    if maximizing:
        max_eval = -float('inf')
        for move in moves:
            board.push(move)
            eval,_ = minimax(board,depth-1,alpha,beta,False,initial_maximizing)
            board.pop()
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha,eval)
            if beta <= alpha:
                break
        transposition_table[board_key] = (max_eval, best_move)
        return max_eval,best_move
    else:
        min_eval = float('inf')
        for move in moves:
            board.push(move)
            eval,_ = minimax(board,depth-1,alpha,beta,True,initial_maximizing)
            board.pop()
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta,eval)
            if beta <= alpha:
                break
        transposition_table[board_key] = (min_eval, best_move)
        return min_eval,best_move