from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")


@app.route("/chess")
def chess():
    content = dict()
    content['rows'] = [8, 7, 6, 5, 4, 3, 2, 1]
    content['squares'] = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    return render_template("chessboard.html", **content)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
