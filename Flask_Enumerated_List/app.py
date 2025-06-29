# app.py
# Flask Enumerated List

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# list of student names
student_name = ["Spongebob", "Jimmy Neutron", "Alice"]

@app.route("/")
def index():
    student_index = list(enumerate(student_name))
    return render_template("index.html", students=student_index)


@app.route("/add", methods=["POST"])
def add():
    name = request.form.get("name")
    if name:
        student_name.append(name)
    return redirect(url_for("index"))


@app.route("/edit", methods=["GET", "POST"])
def edit():
    index = int(request.args.get("index"))
    if request.method == "GET":
        current_name = student_name[index]
        return render_template("edit.html", current_name=current_name)
    elif request.method == "POST":
        new_name = request.form.get("new_name")
        student_name[index] = new_name
        return redirect(url_for("index"))


@app.route("/delete")
def delete():
    index = int(request.args.get("index"))
    student_name.pop(index)
    return redirect(url_for("index"))


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True, port=8080)
