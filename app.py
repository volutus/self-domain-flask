from flask import Flask, render_template
from chess import chess
from noodles import noodles

app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")


@app.route("/ping")
def ping():
    return "200"


@app.route("/chess")
def chess_route():
    # Fetch me from the database!
    starting_state = '846ac6482222222200000000000000000000000000000000111111117359b537'
    content = dict()
    content['pieces'] = chess.create_pieces(starting_state)
    return render_template("chess.html", **content)

@app.route("/noodles")
def noodles_route():
    reviews = noodles.fetch_reviews()
    content = dict()
    content['reviews'] = reviews
    return render_template("noodles.html", **content)

@app.route("/nms/login")
def nms_login():
    return render_template("nms/login.html")

if __name__ == "__main__":
    # This is only used for local runs, so you can set debug true with no problem
    # In prod, it's being run by gunicorn. See the docker repo for the details on that.
    app.run(host='0.0.0.0', debug=True)
