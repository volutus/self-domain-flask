from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")


@app.route("/chess")
def chess():
    return render_template("chessboard.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0')
