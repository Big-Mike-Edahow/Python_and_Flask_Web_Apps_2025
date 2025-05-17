# app.py
# Flask SQLAlchemy Bootstrap Todo

import datetime
from datetime import date
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

# Creating Flask app instance
app = Flask(__name__)

app.config["SECRET_KEY"] = "Another weekend of fun."
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Creating SQLAlchemy instance
db = SQLAlchemy()
# Initialize the database with the app
db.init_app(app) 

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    created = db.Column(
        db.DateTime(timezone=True), server_default=db.func.current_timestamp()
    )

    def __repr__(self):
        return f'<Todo "{self.title}">'


def create_db():  # Create Database with App Context
    with app.app_context():
        db.create_all()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        todos = Todo.query.all()
        return render_template("index.html", todos=todos)
    elif request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        if title and content:
            new_todo = Todo(title=title, content=content)
            db.session.add(new_todo)
            db.session.commit()
            return redirect(url_for("index"))
        else:
            flash("Please provide title and content", "warning")
            return redirect(url_for("index"))

@app.route("/edit/<int:id>", methods = ["GET", "POST"])
def edit(id):
    todo = Todo.query.get_or_404(id)
    if request.method == 'GET':
        return render_template('edit.html', todo=todo)
    elif request.method == "POST":
        todo.title = request.form.get("title")
        todo.content = request.form.get("content")
        if not todo.title or not todo.content:
            flash("Please provide title and content", "warning")
            return redirect(url_for("edit"))
        else:
            db.session.commit()
            return redirect(url_for("index"))

@app.route("/delete/<int:id>")
def delete(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    create_db()
    app.run(debug=True)
