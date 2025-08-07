# app.py
# Flask WTForms Course List

from flask import Flask, render_template, redirect, url_for
from forms import CourseForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "Coding is a good way to kill time."


course_list = [
    {
        "title": "Python 101",
        "description": "Learn the basics of the Python programming language. Python is object oriented, human readable, and easy to learn.",
        "price": 34,
        "available": True,
        "level": "Beginner",
    }
]

@app.route("/")
def index():
    return render_template("index.html", course_list=course_list)

@app.route("/create", methods=("GET", "POST"))
def create():
    form = CourseForm()
    if form.validate_on_submit():
        course_list.append(
            {
                "title": form.title.data,
                "description": form.description.data,
                "price": form.price.data,
                "available": form.available.data,
                "level": form.level.data,
            }
        )
        return redirect(url_for("index"))
    return render_template("create.html", form=form)


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
