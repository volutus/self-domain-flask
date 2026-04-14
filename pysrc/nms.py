from flask import redirect, url_for, session, render_template
from pysrc.nms_objects import DashboardLink, NoodleMaker, NoodleReview, SelectOption
from pysrc import db

def redirect_to_login():
    return redirect(url_for("nms_login_get"))


def redirect_to_dashboard():
    return redirect(url_for("nms_dashboard"))


def render_login():
    if session.get('nms_user', None) is not None:
        return redirect_to_dashboard()
    
    content = dict()
    content["title"] = "NMS Login"
    content["error"] = session.pop("login_error", None)
    return render_template("nms/login.html", **content)


def login_post(form):
    auth = login(form["username"], form["password"])
    if auth:
        return redirect_to_dashboard()
    else:
        session["login_error"] = "The username/password provided was not found."
        return redirect_to_login()


def render_dashboard():
    content = dict()
    content["title"] = "NMS Dashboard"
    content["dashboard_links"] = DashboardLink.fetch_all()
    return render_template("nms/dashboard.html", **content)

def render_noodle_makers():
    content = table_view_data("Edit Noodle Makers", '/nms/edit-noodle-maker', NoodleMaker.fetch_all())
    return render_template("nms/editors/table-view.html", **content)

def render_noodle_maker_editor(id):
    maker = None    
    if id is not None:
        maker = NoodleMaker.fetch_id(id)
    
    content = dict()
    title = "Add New Noodle Maker" if maker is None else f"Edit Noodle Maker with ID #{maker.id}"
    content["title"] = title
    content["maker"] = maker
    return render_template("nms/editors/edit-maker.html", **content)

def edit_noodle_maker(form):
    if form is None or form['mode'] is None:
        session['notice'] = 'No form fields present. No update performed'
        return redirect("/nms/edit-noodle-makers")
    
    try:
        maker = NoodleMaker(form)
        response = maker.edit(form['mode'])
        session['notice'] = response
    except Exception as e:
        session['notice'] = f'No update performed. Uncaught exception: {e}'
    
    return redirect("/nms/edit-noodle-makers")

def render_reviews():
    content = table_view_data("Edit Noodle Reviews", '/nms/edit-noodle-review', NoodleReview.fetch_all())
    return render_template("nms/editors/table-view.html", **content)

def render_review(id):
    review = None    
    if id is not None:
        review = NoodleReview.fetch_id(id)
        
    content = dict()
    makers = NoodleMaker.fetch_all()
    content["maker_options"] = NoodleMaker.to_select_options(makers)
    
    container_types = list()
    container_types.append(SelectOption("Cup", "Cup"))
    container_types.append(SelectOption("Bowl", "Bowl"))
    container_types.append(SelectOption("Yakisoba", "Yakisoba"))
    content["container_types"] = container_types
    
    title = "Add New Review" if review is None else f"Edit Review with ID #{review.id}"
    content["title"] = title
    content["review"] = review
    return render_template("nms/editors/edit-review.html", **content)


def edit_review(form):
    if form is None or form['mode'] is None:
        session['notice'] = 'No form fields present. No update performed'
        return redirect("/nms/edit-noodle-reviews")
    
    try:
        obj = NoodleReview(form)
        response = obj.edit(form['mode'])
        session['notice'] = response
    except Exception as e:
        session['notice'] = f'No update performed. Uncaught exception: {e}'
    
    return redirect("/nms/edit-noodle-reviews")

def table_view_data(title, link, records):
    content = dict()
    content["title"] = title
    content['link'] = link
    content["records"] = records
    content["notice"] = session.pop("notice", None)
    
    fields = list()
    if len(records) > 0:
        record = records[0]
        fields = list(vars(record).keys())
    content["fields"] = fields
    return content
    
def login(username, password):
    sql = "SELECT (hashed_password = crypt(%s, hashed_password)) from nms_user where username = %s"
    with db.fetch_connection() as conn:
        cur = conn.cursor()
        params = (password, username)
        cur.execute(sql, params)

        record = cur.fetchone()
        auth = False
        if record is not None and len(record) > 0:
            auth = record[0]

        if auth:
            print(f"Good authentication for {username}. Setting session value and returning true")
            session["nms_user"] = username
        else:
            # Do not print the username here. This is the most likely spot in the entire application
            # for a user to transpose their username and password.
            # If you log usernames here, you WILL (100%) log passwords by accident.
            print("Bad authentication result. Returning with error.")
        return auth
