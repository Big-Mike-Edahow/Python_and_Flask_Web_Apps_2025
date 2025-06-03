# app.py
# Flask Admin Login SQLAlchemy

from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask_login import (
    LoginManager,
    UserMixin,
    login_required,
    login_user,
    logout_user,
    current_user,
)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_admin import Admin
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SECRET_KEY"] = "I like to make simple web apps as a hobby."

db = SQLAlchemy()
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    todos = db.relationship("Todo", back_populates="user")
    is_admin = db.Column(db.Boolean, default=False)
    created = db.Column(
        db.DateTime(timezone=True), server_default=db.func.current_timestamp()
    )

    def __str__(self):
        return self.username


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(50))
    content = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"), index=True)
    user = db.relationship("User", back_populates="todos")
    created = db.Column(
        db.DateTime(timezone=True), server_default=db.func.current_timestamp()
    )

    def __repr__(self):
        return f"<Todo {self.id}>"


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

class TodoView(ModelView):
    can_delete = True
    column_list = ["id", "author", "content", "created"]
    form_columns = ["author", "content"]

admin.add_view(UserView(User, db.session))
admin.add_view(TodoView(Todo, db.session))


def createDB():
    with app.app_context():
        db.create_all()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        todos = Todo.query.order_by(Todo.created).all()
        return render_template("index.html", todos=todos)
    elif request.method == "POST":
        if current_user.is_authenticated:
            author = current_user.username
        else:
            author = "anonymous"
        content = request.form["content"]
        new_todo = Todo(author=author, content=content)
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


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        # Check to see if user exists, and compare password to that in db.
        if not user or not check_password_hash(user.password, password):
            flash("Please check your login details and try again.")
            return redirect(url_for("login"))
        # if the above check passes, then we know the user has the right credentials
        login_user(user)
        flash("You have been logged in successfully.")
        return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        user = User.query.filter_by(username=username).first()
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


@app.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
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
@login_required
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


@app.route("/logout")
@login_required
def logout():
    logout_user()
    session.pop("_flashes", None)
    flash("You have been logged out.")
    return redirect(url_for("login"))


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    createDB()
    app.run(debug=True, port=8080)
