# app.py
# Flask Login SQLAlchemy Bootstrap

import os
import datetime
from datetime import date
from flask            import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_login      import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from flask_bcrypt     import Bcrypt
from forms import LoginForm, RegisterForm

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SECRET_KEY'] = "I like small town Idaho."
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, "database.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = "False"

db = SQLAlchemy ()
db.init_app(app)

bc = Bcrypt()
bc.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(1000))
    password = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    created = db.Column(
        db.DateTime(timezone=True), server_default=db.func.current_timestamp()
    )

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# Create Database with App Context
def create_db():
    with app.app_context():
        db.create_all()

@app.route('/')
def index():
        return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'GET':
        return render_template( 'login.html', form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            username = request.form.get('username')
            password = request.form.get('password') 
            user = Users.query.filter_by(username=username).first()
            if user:
                if bc.check_password_hash(user.password, password):
                    login_user(user)
                    flash("You have been logged in successfully.")
                    return redirect(url_for('index'))
                else:
                    flash("Incorrect password.")
                    return redirect(url_for('login'))
            else:
                flash("Username not found.")
                return redirect(url_for('login'))

        return render_template( 'login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'GET':
        return render_template( 'register.html', form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            username = request.form.get('username')
            password = request.form.get('password') 
            email    = request.form.get('email') 
            user = Users.query.filter_by(username=username).first()
            if user:
                flash("Username already taken.")
                return redirect(url_for('register'))
            else:         
                password = bc.generate_password_hash(password)
                user_obj = Users(username=username, password=password, email=email)
                db.session.add(user_obj)
                db.session.commit()
                flash("Account registration successful.")
                return redirect(url_for('login'))

        return render_template( 'register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == "__main__":
    create_db()
    app.run(debug=True, port=8080)

