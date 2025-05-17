# app.py
# Flask-Login SQLite

from flask import Flask, render_template, redirect, request, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
import sqlite3

app = Flask(__name__)
app.config["SECRET_KEY"] = "Start out small and simple. Build from there."

login_manager = LoginManager(app)
login_manager.login_view = "login"

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def get_id(self):
        return self.id

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

@app.route('/')
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("index.html")
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = getDB()
        curs = conn.cursor()
        curs.execute("SELECT * FROM users where username = ?", (username,))
        user = curs.fetchone()
        if user is not None:
            user = list(user)
            user_obj = load_user(user[0])
        else:
            flash("Login Unsuccessfull.")
            return render_template("index.html")
        if username == user_obj.username and password == user_obj.password:
            login_user(user_obj)
            session.pop("_flashes", None)
            flash("You have been logged in successfully.")
            return redirect(url_for("profile"))
        else:
            flash("Login Unsuccessfull.")
            return render_template("index.html")

@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user)
        
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out")
    return redirect(url_for("login"))

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True, port=8080)
