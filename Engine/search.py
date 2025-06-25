import chess
from ChessEngine.Engine import evaluation
transposition_table = {}

def score_move(board, move):
    if board.is_capture(move):
        return 10
    if board.gives_check(move):
        return 5
    return 0



def minimax(board: chess.Board,depth,alpha,beta,maximizing):
    
    board_key = (board.fen(), depth, maximizing)
    if transposition_table.get(board_key) != None :
        return transposition_table[board_key]

    if depth == 0 or board.is_game_over():
        return evaluation.evaluate_board(board), None

    best_move = None
    moves = sorted(board.legal_moves, key=lambda m: score_move(board, m), reverse=True)
    if maximizing:
        max_eval = -float('inf')
        for move in moves:
            board.push(move)
            eval,_ = minimax(board,depth-1,alpha,beta,False)
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
            eval,_ = minimax(board,depth-1,alpha,beta,True)
            board.pop()
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta,eval)
            if beta <= alpha:
                break
        transposition_table[board_key] = (min_eval, best_move)
        return min_eval,best_move