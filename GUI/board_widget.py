
# ui/board_view.py

import os
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QApplication
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Engine.bitboard import BitboardPosition
from Core.constants import PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING, WHITE, BLACK

ASSET_PATH = "assets/pieces"

PIECE_FILENAME = {
    (PAWN, WHITE): "wp.png", (KNIGHT, WHITE): "wn.png", (BISHOP, WHITE): "wb.png",
    (ROOK, WHITE): "wr.png", (QUEEN, WHITE): "wq.png", (KING, WHITE): "wk.png",
    (PAWN, BLACK): "bp.png", (KNIGHT, BLACK): "bn.png", (BISHOP, BLACK): "bb.png",
    (ROOK, BLACK): "br.png", (QUEEN, BLACK): "bq.png", (KING, BLACK): "bk.png",
}

class ChessBoard(QWidget):
    def __init__(self, position: BitboardPosition):
        super().__init__()
        self.setWindowTitle("ChessEngine")
        self.board_layout = QGridLayout()
        self.board_layout.setSpacing(0)
        self.setLayout(self.board_layout)
        self.draw_board(position)

    def draw_board(self, position: BitboardPosition):
        squares = [None] * 64
        for (ptype, color), bitboard in position.pieces.items():
            for i in range(64):
                if (bitboard >> i) & 1:
                    squares[i] = os.path.join(ASSET_PATH, PIECE_FILENAME[(ptype, color)])

        for rank in range(8):
            for file in range(8):
                index = (7 - rank) * 8 + file
                label = QLabel()
                label.setFixedSize(64, 64)
                color =  '#3B4252' if (rank + file) % 2 == 0 else '#2E3440'
                label.setStyleSheet(f'background-color: {color};')
                if squares[index]:
                    pixmap = QPixmap(squares[index]).scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    label.setPixmap(pixmap)
                self.board_layout.addWidget(label, rank, file)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    position = BitboardPosition()
    board = ChessBoard(position)
    board.show()
    sys.exit(app.exec_())
