from ChessEngine.Engine import search
import chess
def get_best_move(board, depth):
    _, best_move = search.minimax(board, depth, -float('inf'), float('inf'), board.turn == chess.WHITE)
    print(_)
    return best_move
