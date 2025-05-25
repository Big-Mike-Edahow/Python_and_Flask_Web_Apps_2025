# app.py
# Flask SQLAlchemy One to Many Blog

from datetime import datetime, timezone
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

app = Flask(__name__)

app.config["SECRET_KEY"] = "Just about got a simple back-end down."
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy()
db.init_app(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100))
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    comments = db.relationship('Comment', backref='post', lazy='dynamic')
    created = db.Column(
        db.DateTime(timezone=True), server_default=db.func.current_timestamp()
    )

    # Give object a string representation to recognize it for debugging.
    def __repr__(self):
        return f'<Post "{self.title}">'


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100))
    content = db.Column(db.Text)
    post_id = db.Column(db.Integer(), db.ForeignKey('post.id'))
    created = db.Column(
        db.DateTime(timezone=True), server_default=db.func.current_timestamp()
    )

    # Show the first 20 characters give the object a short string representation.
    def __repr__(self):
        return f'<Comment "{self.content[:20]}...">'


# Create Database with App Context.
def createDB():
    with app.app_context():
        db.create_all()


# Handle file not found errors.
@app.errorhandler(404)
def not_found_error(error):
    return render_template("404.html"), 404


@app.route("/")
def index():
    posts = Post.query.all()
    return render_template("index.html", posts=posts)


@app.route("/view/<int:post_id>", methods=('GET', 'POST'))
def view(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == 'GET':
        return render_template("view.html", post=post)
    elif request.method == 'POST':
        author = request.form['author']
        content=request.form['content']
        comment = Comment(author=author, content=content, post=post)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('view', post_id=post.id))

@app.route('/create', methods = ['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('create.html')
    if request.method == 'POST':
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')
        post = Post(author=author, title=title, content=content)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index'))

@app.route('/edit/<int:post_id>', methods = ['GET', 'POST'])
def edit(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == 'GET':
        return render_template('edit.html', post=post)
    elif request.method == 'POST' :
        post.title = request.form.get('title')
        post.content = request.form.get('content')
        db.session.commit()
        return redirect(url_for("index"))

@app.route('/comments')
def comments():
    comments = Comment.query.all()
    return render_template('comments.html', comments=comments)

@app.route("/delete/<int:post_id>")
def delete(post_id):
    post = Post.query.get(post_id)
    comment = Comment.query.get_or_404(post_id)
    db.session.delete(comment)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("index"))

@app.post('/delete_comment/<int:comment_id>')
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    post_id = comment.post.id
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('view', post_id=post_id))

@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    createDB()
    app.run(debug=True, port=8080)

