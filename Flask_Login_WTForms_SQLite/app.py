# app.py
# Flask-Login WTForms SQLite

from flask import Flask, render_template, redirect, request, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_required, current_user, login_user, logout_user
from forms import LoginForm
import sqlite3

app = Flask(__name__)
app.config["SECRET_KEY"] = "A mall walkin' I will go!"

login_manager = LoginManager(app)
login_manager.login_view = "login"


# Create a User Class.
class User(UserMixin):
    def __init__(self, user_id, username, password):
        self.id = user_id
        self.username = username
        self.password = password

    def get_id(self):
        return str(self.id)

@login_manager.user_loader
def load_user(user_id):
    conn = getDB()
    curs = conn.cursor()
    curs.execute("SELECT * from users where id = (?)", [user_id])
    user = curs.fetchone()
    if user is None:
        return None
    else:
        return User(int(user[0]), user[1], user[2])

def getDB():
    conn = sqlite3.connect("./data/database.db")
    return conn


@app.route("/")
@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        session.pop("_flashes", None)
        flash("You are already logged in.")
        return redirect(url_for("profile"))
    form = LoginForm()
    if request.method == "GET":
        return render_template("index.html", form=form)
    elif request.method == "POST":
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            conn = getDB()
            curs = conn.cursor()
            curs.execute("SELECT * FROM users where username = ?", (username,))
            user = curs.fetchone()
            if user is not None:
                user = list(user)
                user_obj = load_user(user[0])
            else:
                session.pop("_flashes", None)
                flash("Incorrect username or password.")
                return render_template("index.html", form=form)
            if username == user_obj.username and password == user_obj.password:
                login_user(user_obj, remember=form.remember_me.data)
                session.pop("_flashes", None)
                flash("You have been logged in successfully.")
                return redirect(url_for("profile"))
            else:
                session.pop("_flashes", None)
                flash("Incorrect username or password.")
                return render_template("index.html", form=form)
        return render_template("index.html", form=form)


@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html")


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
