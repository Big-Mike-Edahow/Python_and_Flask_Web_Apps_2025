# models.py

from db import db
from sqlalchemy import func


class Author(db.Model):
    author_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    books = db.relationship("Book", backref="author")
    created = db.Column(db.DateTime, server_default=func.now())

    def repr(self):
        return "<Author: {}>".format(self.books)


class Book(db.Model):
    book_id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("author.author_id"))
    title = db.Column(db.String)
    created = db.Column(db.DateTime, server_default=func.now())
