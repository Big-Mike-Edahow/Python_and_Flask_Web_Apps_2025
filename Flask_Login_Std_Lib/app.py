# app.py
# Flask Login Standard Library

from flask import Flask, request, session, redirect, url_for, render_template, flash

app = Flask(__name__)
app.config["SECRET_KEY"] = "Camping along the Wasatch Front for the weekend."

# Dictionary of users
users = {"mike": "foobar", "admin": "foobar"}


@app.route("/")
@app.route("/login", methods=["GET", "POST"])
def login():
    if "username" in session:
        flash("You are already logged in.")
        return redirect(url_for("profile"))
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username in users and users[username] == password:
            session["username"] = username
            flash("You have been logged in successfully.")
            return redirect(url_for("profile"))
        else:
            flash("Incorrect username or password")
            return redirect(url_for("login"))


@app.route("/profile")
def profile():
    if "username" in session:
        return render_template("profile.html")
    else:
        flash("You must be logged in first.")
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for("login"))


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True, port=8080)
