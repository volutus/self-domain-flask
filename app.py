from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")


@app.route("/chess")
def chess():
    # TODO this should be wrapped in a class which will contain the hex / bytes logic, map, and piece color
    # the application should only expect a list of ChessPiece objects which would have all needed fields as public
    starting_state = '846ac6482222222200000000000000000000000000000000111111117359b537'
    pieces = list()
    piece_map = dict()
    piece_map['0'] = ('', 'w')
    piece_map['1'] = ('♙', 'w')
    piece_map['2'] = ('♟', 'b')
    piece_map['3'] = ('♘', 'w')
    piece_map['4'] = ('♞', 'b')
    piece_map['5'] = ('♗', 'w')
    piece_map['6'] = ('♝', 'b')
    piece_map['7'] = ('♖', 'w')
    piece_map['8'] = ('♜', 'b')
    piece_map['9'] = ('♕', 'w')
    piece_map['a'] = ('♛', 'b')
    piece_map['b'] = ('♔', 'w')
    piece_map['c'] = ('♚', 'b')
    piece_map['d'] = ('?', 'w')
    piece_map['e'] = ('?', 'w')
    piece_map['f'] = ('?', 'w')

    for e in starting_state:
        pieces.append(piece_map[e])

    content = dict()
    content['rows'] = [8, 7, 6, 5, 4, 3, 2, 1]
    content['squares'] = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    content['pieces'] = pieces
    return render_template("chessboard.html", **content)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
