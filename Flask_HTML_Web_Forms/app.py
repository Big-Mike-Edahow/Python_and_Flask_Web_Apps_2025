# app.py
# Flask HTML Web Forms App

from flask import Flask, render_template, request, url_for, flash, redirect

app = Flask(__name__)

app.config["SECRET_KEY"] = "We'll get there someday."

messages = [
    {"title": "Message One", "content": "Message One Content"},
    {"title": "Message Two", "content": "Message Two Content"},
]


@app.route("/")
def index():
    return render_template("index.html", messages=messages)

@app.route("/create", methods=("GET", "POST"))
def create():
    if request.method == "GET":
        return render_template("create.html")
    elif request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        if not title or not content:
            flash("Both title and content are required!")
            return render_template("create.html")
        else:
            messages.append({"title": title, "content": content})
            return redirect(url_for("index"))

@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True, port=8080)
