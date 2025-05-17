# app.py
# Flask SQLAlchemy Semantic UI Todo

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

# Creating Flask app instance
app = Flask(__name__)

app.config["SECRET_KEY"] = "Walking in the morning and afternoon."
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Creating SQLAlchemy instance
db = SQLAlchemy()
# Initialize the database with the app
db.init_app(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)
    created = db.Column(
        db.DateTime(timezone=True), server_default=db.func.current_timestamp()
    )

    def __repr__(self):
        return f'<Todo "{self.title}">'

# Create Database with App Context
def create_db():
    with app.app_context():
        db.create_all()

@app.route("/")
def index():
    todos = Todo.query.all()
    return render_template("index.html", todos=todos)

@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/update/<int:id>")
def update(id):
    todo = Todo.query.get(id)
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<int:id>")
def delete(id):
    todo = Todo.query.get(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    create_db()
    app.run(debug=True, port=8080)

