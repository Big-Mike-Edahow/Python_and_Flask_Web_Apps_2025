# app.py
# Flask SQLite Blog

from flask import Flask, render_template, redirect, request, url_for, flash, abort, session
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3

app = Flask(__name__)
app.config["SECRET_KEY"] = "This app turned out okay. ;)"


def getDB():
    conn = sqlite3.connect("./data/database.db")
    return conn


def getPost(id):
    conn = getDB()
    curs = conn.cursor()
    post = curs.execute("SELECT * FROM posts WHERE id = ?", (id,)).fetchone()
    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))
    else:
        return post


@app.route("/")
def index():
    conn = getDB()
    curs = conn.cursor()
    posts = curs.execute("SELECT * FROM posts ORDER BY created DESC").fetchall()
    return render_template("index.html", posts=posts)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = getDB()
        curs = conn.cursor()

        user = curs.execute(
            "SELECT * FROM users WHERE username = ? ", (username,)
        ).fetchone()

        if user is None or not check_password_hash(user[2], password):
            flash("Incorrect username or password.")
            return redirect(url_for("login"))
        else:
            session.clear()
            session["loggedin"] = True
            session["user_id"] = user[0]
            session["username"] = user[1]

            return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = getDB()
        curs = conn.cursor()

        if (
            curs.execute(
                "SELECT id FROM users WHERE username = ?", (username,)
            ).fetchone()
            is not None
        ):
            flash("Username already exists!")
            return redirect(url_for("register"))
        else:
            conn.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (
                    username,
                    generate_password_hash(password),
                ),
            )
            conn.commit()
            conn.close()
            flash("Account was created successfully.")
            return redirect(url_for("login"))


@app.route("/create", methods=["GET", "POST"])
def create():
    if "username" in session:
        if request.method == "GET":
            return render_template("create.html")
        elif request.method == "POST":
            author = request.form["author"]
            title = request.form["title"]
            content = request.form["content"]

            conn = getDB()
            curs = conn.cursor()
            curs.execute(
                "INSERT INTO posts (author, title, content) VALUES (?, ?, ?)",
                (author, title, content),
            )
            conn.commit()
            conn.close()
            return redirect(url_for("index"))
    else:
        flash("You are not logged in.")
        return redirect(url_for("login"))


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    if "username" in session:
        post = getPost(id)
        if request.method == "GET":
            return render_template("edit.html", post=post)
        elif request.method == "POST":
            author = request.form["author"]
            title = request.form["title"]
            content = request.form["content"]

            conn = getDB()
            curs = conn.cursor()
            curs.execute(
                "UPDATE posts SET author = ?, title = ?, content = ? WHERE id = ?",
                (author, title, content, id),
            )
            conn.commit()
            conn.close()
            return redirect(url_for("index"))
    else:
        flash("You are not logged in.")
        return redirect(url_for("login"))


@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    if "username" in session:
        post = getPost(id)
        conn = getDB()
        curs = conn.cursor()
        curs.execute("DELETE FROM posts WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        flash("Post was successfully deleted!")
        return redirect(url_for("index"))
    else:
        flash("You are not logged in.")
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    if "username" in session:
        session.clear()
        flash("You have been logged out successfully.")
        return redirect(url_for("index"))
    else:
        flash("You are not logged in.")
        return redirect(url_for("login"))


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True, port=8080)
