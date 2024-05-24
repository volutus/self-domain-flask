from flask import Flask, render_template
from chess import chess

app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")


@app.route("/chess")
def chess_demo():
    # Fetch me from the database!
    starting_state = '846ac6482222222200000000000000000000000000000000111111117359b537'
    content = dict()
    content['pieces'] = chess.create_pieces(starting_state)
    return render_template("chessboard.html", **content)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
