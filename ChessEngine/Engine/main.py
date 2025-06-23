import chess
import engine
import time
engine_color = chess.WHITE

def main():
    board = chess.Board()
    
    while True:
        player_color_input = input("Play as white or black? (w/b): ").strip().lower()
        if player_color_input in ["w", "b"]:
            break
        print("Invalid input. Type 'w' for white or 'b' for black.")

    engine_color = chess.BLACK if player_color_input == "w" else chess.WHITE
    while not board.is_game_over():
        if board.turn == engine_color:
            start = time.time()
            move = engine.get_best_move(board, 4)
            print(f"Engine move: {move} (calculated in {time.time() - start:.2f}s)")

        else:
            player_move = input("enter your move: ")
            try:
                move = chess.Move.from_uci(player_move)
                
            except ValueError:
                print("Invalid input, please enter a valid UCI move.")
        if move in board.legal_moves:
            board.push(move)
            print("move made:", move)
        else:
            print("Illegal move, try again.")

if __name__ == "__main__":
    main()