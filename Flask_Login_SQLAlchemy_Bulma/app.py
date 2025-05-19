# app.py
# Flask Login SQLAlchemy

from flask import Flask, render_template, redirect, request, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

app = Flask(__name__)

app.config['SECRET_KEY'] = "Rain rain go away."
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"

db = SQLAlchemy()
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(1000))
    password = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    created = db.Column(
        db.DateTime(timezone=True), server_default=db.func.current_timestamp()
    )

# Create Database with App Context
def create_db():
    with app.app_context():
        db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if request.form.get('remember'):
            remember = True
        else:
            remember = False
        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('login'))
        else:
            login_user(user, remember=remember)
            flash("You have been logged in successfully")
            return redirect(url_for('profile'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        user = User.query.filter_by(username=username).first()
        if user:
            flash("Account already exists.")
            return redirect(url_for('signup'))
        else:
            password = generate_password_hash(password)
            user_obj = User(username=username, password=password, email=email)
            db.session.add(user_obj)
            db.session.commit()
            flash("Account registration successful.")
            return redirect(url_for('login'))

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('index'))


if __name__ == "__main__":
    create_db()
    app.run(debug=True, port=8080)

