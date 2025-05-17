# app.py
# Geeks for Geeks Flask Login and Register App

from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import re

app = Flask(__name__)
app.config["SECRET_KEY"] = "A walkin' I will go..."


def getDB():
    conn = sqlite3.connect("./data/database.db")
    return conn


@app.route("/")
@app.route("/login", methods=["GET", "POST"])
def login():
    msg = ""
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = getDB()
        curs = conn.cursor()
        curs.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, password),
        )
        user = curs.fetchone()
        if user:
            session["loggedin"] = True
            session["id"] = user[0]
            session["username"] = user[1]
            return render_template("index.html", msg="Logged in successfully!")
        else:
            msg = "Incorrect username or password!"
            return render_template("login.html", msg=msg)


@app.route("/register", methods=["GET", "POST"])
def register():
    msg = ""
    if request.method == "GET":
        return render_template("register.html", msg="Please create an account")
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        conn = getDB()
        curs = conn.cursor()
        curs.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = curs.fetchone()
        if user:
            msg = "Account already exists!"
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            msg = "Invalid email address!"
        elif not re.match(r"[A-Za-z0-9]+", username):
            msg = "Username must contain only letters and numbers!"
        elif not username or not password or not email:
            msg = "Please fill out the form!"
        else:
            curs.execute(
                "INSERT INTO users(username, password, email) VALUES(?, ?, ?)",
                (username, password, email),
            )
            conn.commit()
            conn.close()
            msg = "You have successfully registered!"
            return render_template("login.html", msg=msg)
        return render_template("register.html", msg=msg)


@app.route("/logout")
def logout():
    session.pop("loggedin", None)
    session.pop("id", None)
    session.pop("username", None)
    msg = "You have been logged out."
    return render_template("login.html", msg=msg)


if __name__ == "__main__":
    app.run(debug=True)
