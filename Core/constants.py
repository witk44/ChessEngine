# Constants for a chess game
PAWN = 1
KNIGHT = 2
BISHOP = 3
ROOK = 4
QUEEN = 5
KING = 6

PIECE_TYPES = {
    'P': PAWN,
    'N': KNIGHT,
    'B': BISHOP,
    'R': ROOK,
    'Q': QUEEN,
    'K': KING
}

PIECE_SYMBOLS = {
    PAWN: 'P',
    KNIGHT: 'N',
    BISHOP: 'B',
    ROOK: 'R',
    QUEEN: 'Q',
    KING: 'K'
}


WHITE = 1
BLACK = -1

COLOR_NAMES = {
    WHITE: 'white',
    BLACK: 'black'
}

FILES = 'abcdefgh'
RANKS = '12345678'
SQUARE_NAMES = [f + r for r in RANKS for f in FILES]
SQUARES = {name: i for i, name in enumerate(SQUARE_NAMES)}
INDEX_TO_SQUARE = {i: name for name, i in SQUARES.items()}

NORTH = 8
SOUTH = -8
EAST = 1
WEST = -1
NORTH_EAST = NORTH + EAST
NORTH_WEST = NORTH + WEST
SOUTH_EAST = SOUTH + EAST
SOUTH_WEST = SOUTH + WEST

