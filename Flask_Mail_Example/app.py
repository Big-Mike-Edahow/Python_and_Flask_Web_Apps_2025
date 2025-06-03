# app.py
# Flask Mail Example

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message

app = Flask(__name__)

app.config.from_pyfile('config.py')

mail = Mail(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        msg = Message(subject='New Contact Form Submission', sender='perigran_falcon@yahoo.com', recipients=['perigran_falcon@yahoo.com'])
        msg.body = f"Name: {name}\nEmail: {email}\nMessage: {message}"
        mail.send(msg)
        flash("Message sent successfully.", 'info')
        return redirect(url_for('index'))
    return render_template('index.html')    

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True, port=8080)
