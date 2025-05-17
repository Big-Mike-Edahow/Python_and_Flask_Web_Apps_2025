# app.py
# Flask-Login User Model

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import (
    LoginManager,
    UserMixin,
    login_required,
    login_user,
    logout_user,
    current_user,
)

app = Flask(__name__)
app.config["SECRET_KEY"] = "Just keep hacking away at it."

# Initialize Flask-Login.
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# Create a User Class.
class User(UserMixin):
    def __init__(self, user_id, username, password):
        self.id = user_id
        self.username = username
        self.password = password

    def get_id(self):
        return str(self.id)


# Load users
users = {1: User(1, "mike", "pw123"), 2: User(2, "big_mike", "pw456")}


@login_manager.user_loader
def load_user(user_id):
    return users.get(int(user_id))

@app.route("/")
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("index.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = next(
            (user for user in users.values()
                if user.username == username and user.password == password),None,)
        if user:
            login_user(user)
            session["user_id"] = user.id
            session["user"] = user.username
            session.pop("_flashes", None)
            flash("You have been logged in successfully.")
            return redirect(url_for("profile"))
        else:
            session.pop("_flashes", None)
            flash("Invalid username or password")
            return redirect(url_for("login"))


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
