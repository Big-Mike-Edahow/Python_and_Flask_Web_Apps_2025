# app.py
# Flask SQLAlchemy Many to Many Booklist

from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

app = Flask(__name__)

app.config["SECRET_KEY"] = "AI to the rescue!"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy()
db.init_app(app)

# Define the association table
association_table = db.Table(
    "association",
    db.Column("book_id", db.Integer, db.ForeignKey("book.id"), primary_key=True),
    db.Column("author_id", db.Integer, db.ForeignKey("author.id"), primary_key=True),
)

# Define the Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    authors = db.relationship(
        "Author", secondary=association_table, back_populates="books"
    )
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())

# Define the Author model
class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    books = db.relationship(
        "Book", secondary=association_table, back_populates="authors"
    )


# Create Database with App Context.
def createDB():
    with app.app_context():
        db.create_all()


@app.route("/")
def index():
    books = Book.query.all()
    return render_template("index.html", books=books)


@app.route("/create", methods=("GET", "POST"))
def create():
    # Create authors and books
    author1 = Author(name="James Patterson")
    author2 = Author(name="David Ellis")
    author3 = Author(name="David Eddings")
    author4 = Author(name="Leigh Eddings")
    book1 = Book(title="3 Days to Live")
    book2 = Book(title="The Red Book")
    book3 = Book(title="High Hunt")
    book4 = Book(title="Belgarath the Sorcerer")

    # Add books to authors and authors to books
    author1.books.append(book1)
    author1.books.append(book2)
    author3.books.append(book3)
    author3.books.append(book4)
    book2.authors.append(author2)
    book4.authors.append(author4)

    # Add to the session and commit
    db.session.add_all([author1, author2, author3, author4, book1, book2, book3, book4])
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    createDB()
    app.run(debug=True, port=8080)
