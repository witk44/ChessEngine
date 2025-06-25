from ChessEngine.Engine import search,evaluation
import chess
def get_best_move(board, depth):
    print(evaluation.evaluate_board(board))
    maximizing = board.turn == chess.WHITE
    _, best_move = search.minimax(board, depth, -float('inf'), float('inf'), maximizing,maximizing)
    return best_move
