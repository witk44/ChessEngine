import search
import chess
def get_best_move(board, depth=3):
    _, best_move = search.minimax(board, depth, -float('inf'), float('inf'), board.turn == chess.WHITE)
    return best_move
