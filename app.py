from flask import Flask, render_template, request
from flask_session import Session
from pysrc import chess, noodles, nms, sauces
from pysrc.decorators import nms_login_required

app = Flask(__name__)

# Session Config
app.config["SESSION_PERMANENT"] = False       # Sessions expire when the browser is closed
app.config["SESSION_TYPE"] = "filesystem"     # Store session data in files
Session(app)

def to_values(object):
	return list(vars(object).values())
app.jinja_env.globals.update(to_values=to_values)

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


@app.route("/sauces")
def sauces_route():
    return render_template("sauces.html", **sauces.fetch_all())

@app.route("/nms/login", methods=["GET"])
def nms_login_get():
    return nms.render_login()

@app.route("/nms/login_action", methods=["POST"])
def nms_login_post():
    return nms.login_post(request.form)

@app.route("/nms/dashboard")
@nms_login_required
def nms_dashboard():
    return nms.render_dashboard()

@app.route("/nms/edit-noodle-makers", methods=["GET"])
@nms_login_required
def nms_edit_noodle_makers():
    return nms.render_noodle_makers()

@app.route("/nms/edit-noodle-maker", methods=["GET"])
@nms_login_required
def nms_edit_noodle_maker():
    id = request.args.get('id')
    return nms.render_noodle_maker_editor(id)

@app.route("/nms/update/noodle-maker", methods=["POST"])
@nms_login_required
def nms_update_noodle_maker():
    print(f"Handling POST to noodle maker update endpoint: {request.form}")
    return nms.edit_noodle_maker(request.form)

@app.route("/nms/edit-noodle-reviews", methods=["GET"])
@nms_login_required
def nms_edit_noodle_reviews():
    return nms.render_reviews()

@app.route("/nms/edit-noodle-review", methods=["GET"])
@nms_login_required
def nms_edit_noodle_review():
    id = request.args.get('id')
    return nms.render_review(id)

@app.route("/nms/update/noodle-review", methods=["POST"])
@nms_login_required
def nms_update_noodle_review():
    print(f"Handling POST to noodle maker update endpoint: {request.form}")
    return nms.edit_review(request.form)

if __name__ == "__main__":
    # This is only used for local runs, so you can set debug true with no problem
    # In prod, it's being run by gunicorn. See the docker repo for the details on that.
    app.run(host='0.0.0.0', debug=True)
