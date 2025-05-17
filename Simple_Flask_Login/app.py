# app.py
# Simple Flask Login

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_required, current_user, login_user, logout_user

app = Flask(__name__)
app.secret_key = "Use the force, Luke!"

login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin):
    def __init__(self, email, password):
        self.id = email
        self.password = password


users = {"leafstorm": User("leafstorm", "secret")}


@login_manager.user_loader
def user_loader(id):
    return users.get(id)


@app.route("/")
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("index.html")
    elif request.method == "POST":
        user = users.get(request.form["email"])
        if user is None or user.password != request.form["password"]:
            session.pop("_flashes", None)
            flash("Improper login credentials.")
            return redirect(url_for("login"))
        else:
            login_user(user)
            session.pop("_flashes", None)
            flash("You have been logged in successfully.")
            return redirect(url_for("profile"))


@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    session.pop("_flashes", None)
    flash("You have been logged out.")
    return redirect(url_for("login"))


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True, port=8080)
