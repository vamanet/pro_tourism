from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from extension import db
from models import User

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session["user"] = user.username
            session["role"] = user.role
            return redirect(url_for("main.dashboard"))
        flash("Invalid username or password")

    return render_template("login.html")

@auth.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))

@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        confirm = request.form["confirm"]

        if len(username) < 3:
            flash("Username must be at least 3 characters")
        elif len(password) < 6:
            flash("Password must be at least 6 characters")
        elif password != confirm:
            flash("Passwords do not match")
        elif User.query.filter_by(username=username).first():
            flash("Username already taken")
        else:
            user = User(username=username, role="user")   # always "user"
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash("Account created. Please log in.")
            return redirect(url_for("auth.login"))

    return render_template("register.html")

# keep your login() and logout() below