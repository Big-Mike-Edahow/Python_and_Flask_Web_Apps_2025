# app.py
# Flask SQLAlchemy Login App

from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SECRET_KEY"] = "The storm clouds are threatening..."
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy()
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)


# A User loader tells Flask-Login how to find a specific user
# by the ID that is stored in their session cookie.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(1000))
    password = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    created = db.Column(db.DateTime(), default = datetime.utcnow, index = True)


def create_db():
    with app.app_context():
        db.create_all()


@app.route('/')
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        remember = True if request.form.get("remember") else False

        user = User.query.filter_by(username=username).first()

        # Check to see if user exists, and compare password to that in db.
        if not user or not check_password_hash(user.password, password):
            flash("Please check your login details and try again.")
            return redirect(url_for("login"))

        # if the above check passes, then we know the user has the right credentials
        login_user(user, remember=remember)
        flash("You have been logged in successfully.")
        return redirect(url_for("profile"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")

        user = User.query.filter_by(email=email).first()

        # If user is found, redirect back to register page.
        if user:
            flash("Email address already exists")
            return redirect(url_for("register"))

        # Create new user with form data. Hash password.
        new_user = User(
            username=username,
            password=generate_password_hash(password),
            email=email,
        )

        # Add new user to the database and commit data.
        db.session.add(new_user)
        db.session.commit()
        flash("Your account has been registerd successfuly")
        return redirect(url_for("login"))

@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", username=current_user.username, created=current_user.created)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out successfully.")
    return redirect(url_for("index"))


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    create_db()
    app.run(debug=True, port=8080)
