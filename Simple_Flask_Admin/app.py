# app.py
# Simple Flask Admin

from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SECRET_KEY"] = "I like to make simple web apps as a hobby."

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created = db.Column(
        db.DateTime(timezone=True), server_default=db.func.current_timestamp()
    )

    def __repr__(self):
        return f"<User {self.username}>"


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    created = db.Column(
        db.DateTime(timezone=True), server_default=db.func.current_timestamp()
    )

    def __repr__(self):
        return f"<Todo {self.content}>"
    
app.config["FLASK_ADMIN_SWATCH"] = "cerulean"
admin = Admin(app, name="Flask-Admin! 👨‍💼", template_mode="bootstrap4")
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Todo, db.session))


def createDB():
    with app.app_context():
        db.create_all()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        todos = Todo.query.order_by(Todo.created).all()
        return render_template("index.html", todos=todos)
    elif request.method == "POST":
        content = request.form["content"]
        new_todo = Todo(content=content)
        try:
            db.session.add(new_todo)
            db.session.commit()
            session.pop("_flashes", None)
            flash("Todo added successfully.")
            return redirect(url_for("index"))
        except:
            session.pop("_flashes", None)
            flash("There was a problem adding your todo.")
            return redirect(url_for("index"))


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    todo = Todo.query.get_or_404(id)
    if request.method == "GET":
        return render_template("edit.html", todo=todo)
    elif request.method == "POST":
        todo.content = request.form["content"]
        try:
            db.session.commit()
            session.pop("_flashes", None)
            flash("Todo updated successfully.")
            return redirect(url_for("index"))
        except:
            session.pop("_flashes", None)
            flash("There was a problem updating your todo.")
            return redirect(url_for("index"))


@app.route("/delete/<int:id>")
def delete(id):
    todo = Todo.query.get_or_404(id)
    try:
        db.session.delete(todo)
        db.session.commit()
        session.pop("_flashes", None)
        flash("Todo deleted successfully.")
        return redirect(url_for("index"))
    except:
        session.pop("_flashes", None)
        flash("There was a problem deleting the todo.")
        return redirect(url_for("index"))


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    createDB()
    app.run(debug=True, port=8080)
