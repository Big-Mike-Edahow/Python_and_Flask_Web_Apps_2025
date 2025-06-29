# app.py
# Flask Markdown SQLite

import sqlite3
import markdown
from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.config["SECRET_KEY"] = "Feeling better this afternoon."


def getDB():
    conn = sqlite3.connect("./data/database.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def index():
    conn = getDB()
    curs = conn.cursor()
    db_notes = curs.execute("SELECT id, created, content FROM notes").fetchall()
    conn.close()

    notes = []
    for note in db_notes:
        note = dict(note)
        note["content"] = markdown.markdown(note["content"])
        notes.append(note)

    return render_template("index.html", notes=notes)


@app.route("/create/", methods=("GET", "POST"))
def create():
    conn = getDB()
    curs = conn.cursor()
    if request.method == "POST":
        content = request.form["content"]
        if not content:
            flash("Content is required!")
            return redirect(url_for("index"))
        curs.execute("INSERT INTO notes (content) VALUES (?)", (content,))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))

    return render_template("create.html")


if __name__ == "__main__":
    app.run(debug=True, port=8080)
