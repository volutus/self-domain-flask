from functools import wraps
from flask import session
from pysrc.nms import redirect_to_login

def nms_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print("Testing NMS Login status")
        user = session.get('nms_user', None)
        if user is None:
            print("Redirecting unauthenticated user back to login screen.")
            return redirect_to_login()
        return f(*args, **kwargs)
    return decorated_function