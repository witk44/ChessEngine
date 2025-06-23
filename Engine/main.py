import chess
import engine

engine_color = chess.BLACK

def main():
    # Initialize the chess board
    board = chess.Board()

    while not board.is_game_over():
        if board.turn == engine_color:
            pass
        else:
            player_move = input("enter your move: ")
            try:
                move = chess.Move.from_uci(player_move)
                if move in board.legal_moves:
                    board.push(move)
                    print("move made:", move)
                else:
                    print("Illegal move, try again.")
            except ValueError:
                print("Invalid input, please enter a valid UCI move.")


if __name__ == "__main__":
    main()