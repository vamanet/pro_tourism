from functools import wraps
from flask import session, redirect, url_for, flash, abort

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user" not in session:
            flash("Please log in first")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return wrapper

def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user" not in session:
            flash("Please log in first")
            return redirect(url_for("auth.login"))
        if session.get("role") != "admin":
            abort(403)                      # "Forbidden"
        return f(*args, **kwargs)
    return wrapper