# app.py
# Flask Pillow Generative Art

from flask import Flask, render_template, redirect, url_for
from make_squares import create

app = Flask(__name__)

tmp_file_path = "./imgnew.png"

@app.route("/", methods=["GET"])
def index():
    graphic_image = create(tmp_file_path)
    return render_template("index.html", image=graphic_image)

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True, port=8080)

