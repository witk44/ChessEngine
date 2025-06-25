from ChessEngine.Engine import search
import chess
def get_best_move(board, depth):
    maximizing = board.turn == chess.WHITE
    print(maximizing)
    _, best_move = search.minimax(board, depth, -float('inf'), float('inf'), maximizing)
    print(_)
    return best_move
