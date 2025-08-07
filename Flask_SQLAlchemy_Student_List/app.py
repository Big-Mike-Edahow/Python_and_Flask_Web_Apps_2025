# app.py
# Flask SQLAlchemy Student List

import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config["SECRET_KEY"] = "I like to get my routine down."
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "database.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    age = db.Column(db.Integer)
    bio = db.Column(db.Text)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Student {self.firstname}>"


# Create Database with App Context
def create_db():
    with app.app_context():
        db.create_all()


@app.route("/")
def index():
    students = Student.query.all()
    return render_template("index.html", students=students)


@app.route("/view/<int:id>/")
def view(id):
    student = Student.query.get_or_404(id)
    return render_template("view.html", student=student)


@app.route("/create/", methods=("GET", "POST"))
def create():
    if request.method == "POST":
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        email = request.form["email"]
        age = int(request.form["age"])
        bio = request.form["bio"]
        student = Student(
            firstname=firstname, lastname=lastname, email=email, age=age, bio=bio
        )
        db.session.add(student)
        db.session.commit()

        return redirect(url_for("index"))

    return render_template("create.html")


@app.route("/edit/<int:id>", methods=("GET", "POST"))
def edit(id):
    student = Student.query.get_or_404(id)

    if request.method == "POST":
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        email = request.form["email"]
        age = int(request.form["age"])
        bio = request.form["bio"]

        student.firstname = firstname
        student.lastname = lastname
        student.email = email
        student.age = age
        student.bio = bio

        db.session.add(student)
        db.session.commit()

        return redirect(url_for("index"))

    return render_template("edit.html", student=student)


@app.post("/delete/<int:id>/")
def delete(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    create_db()
    app.run(debug=True, port=8080)

