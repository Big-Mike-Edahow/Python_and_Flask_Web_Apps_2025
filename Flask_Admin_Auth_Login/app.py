# app.py
# Flask Admin Auth Login

from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask_login import (
    LoginManager,
    UserMixin,
    login_required,
    login_user,
    logout_user,
    current_user,
)
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from forms import LoginForm, RegistrationForm

app = Flask(__name__)

app.config["SECRET_KEY"] = "Keep studying the basics"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)

# Create user model.
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(64))
    email = db.Column(db.String(120))
    is_admin = db.Column(db.Boolean, default=False)
    created = db.Column(
        db.DateTime(timezone=True), server_default=db.func.current_timestamp()
    )

    # Required for administrative interface
    def __str__(self):
        return self.username

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin
    def inaccessible_callback(self, name, **kwargs):
        flash("You are not allowed to access the Admin Panel.")
        return redirect(url_for("login"))

app.config["FLASK_ADMIN_SWATCH"] = "cerulean"
admin = Admin(
    app, name="Flask-Admin! 👨‍💼", index_view=MyAdminIndexView(), template_mode="bootstrap4"
)

class UserView(ModelView):
    def _password_formatter(view, context, model, name):
        return model.password[:20]
    can_delete = True
    column_formatters = {"password": _password_formatter,}
    column_list = ["id", "username", "password", "email", "is_admin", "created"]
    form_columns = ["username", "password", "is_admin", "email"]

admin.add_view(UserView(User, db.session))

def createDB():
    with app.app_context():
        db.create_all()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in.")
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember_me = form.remember_me.data
        user = User.query.filter_by(username=username).first()
        if user is None or not check_password_hash(user.password, password):
            flash("Invalid username or password.")
            return redirect(url_for("login"))
        else:
            login_user(user, remember=remember_me)
            flash("You have been logged in successfully.")
            return redirect(url_for("index"))
    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        flash("You are already logged in.")
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        user = User.query.filter_by(username=username).first()
        if user:
            flash("Username already exists!")
            return redirect(url_for("register"))
        else:
            password = generate_password_hash(form.password.data)
            new_user = User(
                username=username, password=password, email=email
            )
            db.session.add(new_user)
            db.session.commit()
            flash("Congratulations, you are now a registered user!")
            return redirect(url_for("login"))
    return render_template("register.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("login"))

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    createDB()
    app.run(debug=True, port=8080)
