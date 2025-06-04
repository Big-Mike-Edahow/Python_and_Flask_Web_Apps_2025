# app.py
# Flask Mail Contact Form

import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail
from init_db import db
from models import Messages

app = Flask(__name__)
app.config.from_pyfile('config.py')

mail = Mail(app)
db.init_app(app)

""" Creating Database with App Context"""
def createDB():
    with app.app_context():
        db.create_all()
 
# App route
@app.route("/", methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')

         # Adding entries to the DB and committing
        entry = Messages(name=name, email=email, subject=subject, message=message, date=datetime.datetime.now())
        db.session.add(entry)
        db.session.commit()

        # Sending email with Flask-Mail
        mail.send_message("Message from " + name + " at " + email,
                 sender = email,
                 recipients=['perigran_falcon@yahoo.com'],
                 body = subject + "\n\n" + message)
        flash("Message sent successfully.", 'info')
        return redirect(url_for('status'))
 
    return render_template("index.html")

@app.route("/status")
def status():
    message = db.session.query(Messages).order_by(Messages.id.desc()).first()
    return render_template("status.html", message=message)

@app.route('/about')
def about():
    return render_template('about.html')
 
if __name__=="__main__":
    createDB()
    app.run(debug=True, port=8080)
