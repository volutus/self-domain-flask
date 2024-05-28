"""
   This dictionary maps a hex value to a type of chess piece. 0 is a blank tile and D/E/F are unused
   Mapping:
   0: Blank
   1: White Pawn
   2: Black Pawn
   3: White Knight
   4: Black Knight
   5: White Bishop
   6: Black Bishop
   7: White Rook
   8: Black Rook
   9: White Queen
   A: Black Queen
   B: White King
   C: Black King
   D: N/A
   E: N/A
   F: N/A
"""

# Initialize convenience maps
if __name__ != '__main__':
    piece_map = dict()
    piece_map['0'] = None
    piece_map['1'] = '♙'
    piece_map['2'] = '♟'
    piece_map['3'] = '♘'
    piece_map['4'] = '♞'
    piece_map['5'] = '♗'
    piece_map['6'] = '♝'
    piece_map['7'] = '♖'
    piece_map['8'] = '♜'
    piece_map['9'] = '♕'
    piece_map['a'] = '♛'
    piece_map['b'] = '♔'
    piece_map['c'] = '♚'
    piece_map['d'] = None
    piece_map['e'] = None
    piece_map['f'] = None

    square_map = dict()
    _i = 0
    for row in [8, 7, 6, 5, 4, 3, 2, 1]:
        for column in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']:
            square_map[_i] = column + str(row)
            _i += 1


def create_pieces(hex_string):
    pieces = list()
    index = 0
    for e in hex_string:
        pieces.append(ChessPiece(e, index))
        index += 1
    return pieces


class ChessPiece:
    def __init__(self, hex_value, index):
        self.hex_value = hex_value
        self.index = index
        self.square = None
        self.token = None
        self.color = ''
        self.create()

    def create(self):
        self.token = piece_map[self.hex_value]
        self.square = square_map[self.index]
        if self.hex_value in ['1', '3', '5', '7', '9', 'b']:
            self.color = 'white'
        elif self.hex_value in ['2', '4', '6', '8', 'a', 'c']:
            self.color = 'black'


