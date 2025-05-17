# app.py
# Flask WTForms Login App

import datetime
from datetime import date
from flask import Flask, render_template, redirect, request, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config["SECRET_KEY"] = "Studying at the library."
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.init_app(app)

# Registers the function with Flask-Login to load users from the database.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    created = db.Column(
        db.DateTime(timezone=True), server_default=db.func.current_timestamp()
    )

# Create Database with App Context
def create_db():
    with app.app_context():
        db.create_all()

@app.route("/")
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "GET":
        return render_template("login.html", form=form)
    elif request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("Login successful!", "success")
                return redirect(url_for("dashboard"))
            else:
                flash("Invalid username or password", "danger")
                return render_template("login.html", form=form)
        return render_template("login.html", form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if request.method == "GET":
        return render_template("register.html", form=form)
    elif request.method == "POST":
        if form.validate_on_submit():
            username=form.username.data
            user = User.query.filter_by(username=username).first()

            # If user is found, redirect back to register page.
            if user:
                session.pop('_flashes', None)
                flash("Username already exists")
                return redirect(url_for("register"))
            else:
                hashed_password = generate_password_hash(form.password.data)
                new_user = User(username=form.username.data, password=hashed_password)
                db.session.add(new_user)
                db.session.commit()
                flash("Registration successful! Please log in.", "success")
                return redirect(url_for("login"))

        return render_template("register.html", form=form)
    
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", username=current_user.username, created=current_user.created)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))

@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    create_db()
    app.run(debug=True, port=8080)

