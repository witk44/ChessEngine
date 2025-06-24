import tkinter as tk
import chess
from ChessEngine.Engine import engine
import time

TILE_SIZE = 80
WHITE_COLOR = "#EEEED2"
BLACK_COLOR = "#769656"
PIECE_UNICODE = {
    "P": "♙", "N": "♘", "B": "♗", "R": "♖", "Q": "♕", "K": "♔",
    "p": "♟", "n": "♞", "b": "♝", "r": "♜", "q": "♛", "k": "♚"
}

class ChessGUI:
    def __init__(self, root, engine_color):
        self.board = chess.Board()
        self.engine_color = engine_color
        self.root = root
        self.canvas = tk.Canvas(root, width=8*TILE_SIZE, height=8*TILE_SIZE)
        self.canvas.pack()
        self.selected_square = None
        self.flip = engine_color == chess.WHITE
        self.canvas.bind("<Button-1>", self.click)
        self.draw_board()

        if self.board.turn == self.engine_color:
            self.root.after(500, self.make_engine_move)

    def draw_board(self):
        self.canvas.delete("all")
        for rank in range(8):
            for file in range(8):
                display_rank = rank if not self.flip else 7 - rank
                display_file = file if not self.flip else 7 - file
                square_index = chess.square(display_file, 7 - display_rank)
                x1 = file * TILE_SIZE
                y1 = rank * TILE_SIZE
                x2 = x1 + TILE_SIZE
                y2 = y1 + TILE_SIZE
                color = WHITE_COLOR if (display_rank + display_file) % 2 == 0 else BLACK_COLOR
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

                piece = self.board.piece_at(square_index)
                if piece:
                    symbol = PIECE_UNICODE[piece.symbol()]
                    self.canvas.create_text(x1 + TILE_SIZE//2, y1 + TILE_SIZE//2,
                                            text=symbol, font=("Arial", 32))

    def click(self, event):
        if self.board.turn != self.engine_color:
            file = event.x // TILE_SIZE
            rank = (event.y // TILE_SIZE)
            if self.flip:
                file = 7-file
                rank = 7-rank
            square = chess.square(file, 7 - rank)

            if self.selected_square is None:
                if self.board.piece_at(square) and self.board.piece_at(square).color == self.board.turn:
                    self.selected_square = square
            else:
                move = chess.Move(self.selected_square, square)
                if self.board.piece_at(self.selected_square).piece_type == chess.PAWN:
                    rank_to = chess.square_rank(square)
                    if rank_to == 0 or rank_to == 7:
                        promo_piece = None
                        while promo_piece not in ['q', 'r', 'b', 'n']:
                            promo_piece = input("Promote to (q=queen, r=rook, b=bishop, n=knight): ").strip().lower()
                        promo_map = {'q': chess.QUEEN, 'r': chess.ROOK, 'b': chess.BISHOP, 'n': chess.KNIGHT}
                        move = chess.Move(self.selected_square, square, promotion=promo_map[promo_piece])

                if move in self.board.legal_moves:
                    self.board.push(move)
                    self.selected_square = None
                    self.draw_board()
                    if not self.board.is_game_over():
                        self.root.after(500, self.make_engine_move)
                else:
                    self.selected_square = None  # Reset on invalid move
                self.draw_board()

    def make_engine_move(self):
        if not self.board.is_game_over():
            start = time.time()
            move = engine.get_best_move(self.board, depth=5)
            print(f"Engine move: {move} ({time.time() - start:.2f}s)")
            self.board.push(move)
            self.draw_board()

def main():
    root = tk.Tk()
    root.title("Chess Engine GUI")

    choice = input("Play as white or black? (w/b): ").strip().lower()
    while choice not in ["w", "b"]:
        choice = input("Invalid input. Please enter 'w' or 'b': ").strip().lower()

    engine_color = chess.BLACK if choice == "w" else chess.WHITE

    gui = ChessGUI(root, engine_color)
    root.mainloop()

if __name__ == "__main__":
    main()
