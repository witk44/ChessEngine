import chess
from ChessEngine.Engine import evaluation
def minimax(board: chess.Board,depth,alpha,beta,maximizing):
    if depth == 0 or board.is_game_over():
        return evaluation.evaluate_board(board), None

    best_move = None
    if maximizing:
        max_eval = -float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval,_ = minimax(board,depth-1,alpha,beta,False)
            board.pop()
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha,eval)
            if beta <= alpha:
                break
        return max_eval,best_move
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval,_ = minimax(board,depth-1,alpha,beta,True)
            board.pop()
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta,eval)
            if beta <= alpha:
                break
        return min_eval,best_move